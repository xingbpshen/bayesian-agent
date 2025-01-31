import json
import openai
import time
import prompt
import re
import numpy as np


def format_question_prompt(data_dict):
    # Extract data from dictionary
    question = data_dict["question"]
    choices = data_dict["choices"]
    caption = data_dict["caption"]
    rationales = data_dict["rationales"]

    # Format the choices
    choices_str = " ".join(f"({chr(65 + i)}) {choice}" for i, choice in enumerate(choices))

    # Format the rationales
    rationales_str = " ".join(rationales)

    # Create the prompt
    question_prompt = f"""
    Question: {question}
    Options: {choices_str}
    Image caption: {caption}
    Retrieved knowledge: {rationales_str}
    Solution:
    """

    return question_prompt


def parse_response_content(response_content, thought_model):
    parsed_dict = {}
    if thought_model == "vpgm":
        # Extract Z1 probability
        z1_prob = float(re.search(r"P\(Z1 \| .*?\) = ([0-9.]+)", response_content).group(1))

        # Extract Z2 probability
        z2_prob = float(re.search(r"P\(Z2 \| Z1, .*?\) = ([0-9.]+)", response_content).group(1))

        # Extract choice probabilities
        choice_probs = re.findall(r"P\(Y = .*? \| Z1, Z2\) = ([0-9.]+)", response_content)
        choice_probs = [float(prob) for prob in choice_probs]

        # check if there are 4 choices
        if len(choice_probs) != 4:
            raise Exception("Invalid number of choices, there must be 4 choices.")

        # Determine the answer index (the index of the highest probability)
        answer_idx = choice_probs.index(max(choice_probs))

        # Create the parsed dictionary
        parsed_dict = {
            "Z1": z1_prob,
            "Z2": z2_prob,
            "Y": choice_probs,
            "answer_idx": answer_idx
        }
    elif thought_model == "chameleon-sr-ac":
        # Extract the answer letter (case insensitive)
        answer_pattern = r"The answer is ([A-Da-d]) with a numerical probability"
        answer_match = re.search(answer_pattern, response_content)
        if answer_match:
            answer = answer_match.group(1).upper()  # Convert to upper case for consistency
            answer_idx = ord(answer) - ord('A')
        else:
            raise Exception("Failed to extract the answer letter.")

        # Extract the probability
        prob_pattern = r"numerical probability of ([0-9.]+)"
        prob_match = re.search(prob_pattern, response_content)
        if prob_match:
            choice_prob = float(prob_match.group(1).strip('.'))  # Removing any trailing period
        else:
            raise Exception("Failed to extract the probability.")

        # Create the parsed dictionary
        parsed_dict = {
            "answer_idx_prob": choice_prob,
            "answer_idx": answer_idx
        }

    return parsed_dict

def get_gpt_response(gpt_config, message, thought_model, sleep_time=0.5):
    try:
        response = openai.ChatCompletion.create(model=gpt_config["model"],
                                                messages=message,
                                                api_key=gpt_config["api_key"],
                                                temperature=gpt_config["temperature"],
                                                max_tokens=gpt_config["max_tokens"],
                                                n=gpt_config["n"])
        if gpt_config["n"] == 1:
            response_content = response["choices"][0]["message"]["content"]
            return response_content, parse_response_content(response_content, thought_model)
        else:
            raise Exception("Invalid number of completions, n must be 1.")
    except Exception as e:
        if sleep_time > 0:
            time.sleep(sleep_time)


def compose_message(system_message, user_message):
    return [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]


def predict(gpt_config, data_point, thought_model):
    if thought_model == "vpgm":
        system_message = prompt.prompt_vpgm
    elif thought_model == "chameleon-sr-ac":
        system_message = prompt.prompt_chameleon_vc
    else:
        raise Exception("Invalid thought model, must be either 'vpgm' or 'chameleon'.")
    # Generate the prompt
    user_message = format_question_prompt(data_point)
    response, parsed_response = get_gpt_response(
        gpt_config, compose_message(system_message, user_message), thought_model)
    return response, parsed_response


def run_with_retry(func, max_attempts=5, *args, **kwargs):
    attempts = 0
    while attempts < max_attempts:
        try:
            result = func(*args, **kwargs)
            return result  # Exit if successful
        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts} failed with exception: {e}")
            if attempts == max_attempts:
                # Ask the user if they want to retry
                retry = input("Exceed maximum auto-retry budget. Do you still want to retry? (y/n): ")
                if retry.lower() == "y":
                    attempts = 0  # Reset the attempts counter
                else:
                    raise  # Re-raise the exception if the max number of attempts is reached
    return None # Return None if all attempts fail


def calculate_ece(confidences, pred_labels, true_labels, n_bins=10):
    # Example usage
    # confidences = np.random.rand(100)
    # pred_labels = np.random.randint(0, 2, 100)
    # true_labels = np.random.randint(0, 2, 100)

    # # Convert to np arrays if not already
    # probs = np.array(probs)
    # true_labels = np.array(true_labels)
    # # Calculate confidence scores and predicted labels
    # confidences = np.max(probs, axis=1)
    # pred_labels = np.argmax(probs, axis=1)
    confidences = np.array(confidences)
    pred_labels = np.array(pred_labels)
    true_labels = np.array(true_labels)

    # Initialize bins
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0

    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        # Select samples that fall into this bin
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)  # Proportion of samples in this bin

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(pred_labels[in_bin] == true_labels[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += prop_in_bin * np.abs(avg_confidence_in_bin - accuracy_in_bin)

    return ece


def dump_json(data, file_path):

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()  # Convert NumPy array to list
            else:
                return super(NumpyEncoder, self).default(obj)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, cls=NumpyEncoder)
