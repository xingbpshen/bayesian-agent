"""
An external program to calculate Expected Calibration Error (ECE) for a given model.
"""
import json
from collections import defaultdict, OrderedDict
from tqdm import tqdm
import openai
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import re
from scipy.stats import pearsonr, spearmanr
import numpy as np
import math

# gpt_config = json.load(open("../run_toydata_aokvqa/gpt_config.json", "r"))
# openai.api_key = gpt_config["api_key"]


def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        buffer = ""
        for line in file:
            buffer += line.strip()
            try:
                # Try to parse the buffered text as JSON
                json_object = json.loads(buffer)
                data.append(json_object)
                buffer = ""  # Clear the buffer after successfully reading an object
            except json.JSONDecodeError:
                # If JSON is incomplete, continue buffering
                continue
    return data


def calculate_ece(data, model, num_bins=10, uniform_bins=False):
    # materials for calculating correlations in bcot
    tuples_z1_conf = []
    tuples_z2_conf = []
    if uniform_bins:
        bin_size = 1.0 / num_bins
        bin_boundaries = [i * bin_size for i in range(num_bins + 1)]
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        # Initialize bins
        bins = defaultdict(lambda: {'confidence_sum': 0, 'accuracy_sum': 0, 'total': 0})
    else:
        bin_boundaries = [i / num_bins for i in range(num_bins + 1)]
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        # Initialize bins
        bins = defaultdict(lambda: {'confidence_sum': 0, 'accuracy_sum': 0, 'total': 0})
    for item in data:
        # Extract information
        if model in ["bcot-ticoh-s", "bcot-ticoh-l"]:
            probs = item['bcot_option_prob_dict']
            sampled_solution = item['bcot_sampled_solution']
            correct_option_index = item['example']['answer']  # Index of the correct answer
            correct_option = chr(correct_option_index + 65)  # Convert index to letter (assuming 'A' is 0)
            # Find the predicted probability and correctness
            predicted_prob = probs[str(ord(sampled_solution) - 65)]
            correctness = 1 if sampled_solution == correct_option else 0
        elif model in ['io', 'cot', 'chameleon', 'chameleon-hybrid']:
            predicted_prob = item['option_prob']  # change to 'option_prob_s0' for calculating ECE for chameleon-verb with results file from chameleon-hybrid
            correctness = 1 if item['true_false'] else 0
        else:
            raise ValueError(f"Model {model} is not supported")
        # Find the right bin for the predicted probability
        for lower, upper in zip(bin_lowers, bin_uppers):
            if lower <= predicted_prob < upper or (upper == 1 and predicted_prob == 1):
                bins[lower]['confidence_sum'] += predicted_prob
                bins[lower]['accuracy_sum'] += correctness
                bins[lower]['total'] += 1
                break

    # Calculate ECE and prepare bin_values for all bins, even if they have no data
    ece = 0
    bin_values = []
    if uniform_bins:
        for lower, upper in zip(bin_lowers, bin_uppers):
            bin_info = bins[lower]
            if bin_info['total'] > 0:
                avg_confidence = bin_info['confidence_sum'] / bin_info['total']
                avg_accuracy = bin_info['accuracy_sum'] / bin_info['total']
                ece += (abs(avg_accuracy - avg_confidence) * bin_info['total'])
            else:
                avg_confidence = 0
                avg_accuracy = 0
            bin_values.append({
                'bin_lower_bound': lower,
                'bin_upper_bound': upper,
                'avg_confidence': avg_confidence,
                'avg_accuracy': avg_accuracy,
                'total': bin_info['total']
            })
    else:
        for lower, bin_info in bins.items():
            if bin_info['total'] > 0:
                avg_confidence = bin_info['confidence_sum'] / bin_info['total']
                avg_accuracy = bin_info['accuracy_sum'] / bin_info['total']
                ece += (abs(avg_accuracy - avg_confidence) * bin_info['total'])
                bin_values.append({
                    'bin_lower_bound': lower,
                    'avg_confidence': avg_confidence,
                    'avg_accuracy': avg_accuracy,
                    'total': bin_info['total']
                })
    total_count = sum(bin_info['total'] for bin_info in bins.values())
    ece /= total_count

    return ece, bin_values


def calculate_ece_2(confidences, pred_labels, true_labels, n_bins=10):
    # Example usage
    # confidences = np.random.rand(100)
    # pred_labels = np.random.randint(0, 2, 100)
    # true_labels = np.random.randint(0, 2, 100)

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

        accuracy_in_bin = 0
        avg_confidence_in_bin = 0
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(pred_labels[in_bin] == true_labels[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += prop_in_bin * np.abs(avg_confidence_in_bin - accuracy_in_bin)

        # Print the average confidence and accuracy in this bin
        print(f"Bin {bin_lower:.2f}-{bin_upper:.2f}: ")
        print(f"\tAverage Confidence: {avg_confidence_in_bin:.4f}")
        print(f"\tAverage Accuracy: {accuracy_in_bin:.4f}")
        print(f"\tTotal in Bin: {np.sum(in_bin)}\n")

    return ece


def calculate_correlation(data, model):
    # materials for calculating correlations in bcot
    tuples_z1_conf = []
    tuples_z2_conf = []
    tuples_z1_embed = []
    tuples_z2_embed = []
    embed_dim = 256
    option_prob_dicts = []
    for item in tqdm(data):
        # Extract information
        if model in ["bcot-ticoh-s", "bcot-ticoh-l"]:
            probs = item['bcot_option_prob_dict']
            option_prob_dicts.append(probs)
            sampled_solution = item['bcot_sampled_solution']
            correct_option_index = item['example']['answer']  # Index of the correct answer
            correct_option = chr(correct_option_index + 65)  # Convert index to letter (assuming 'A' is 0)
            # Find the predicted probability and correctness
            predicted_prob = probs[str(ord(sampled_solution) - 65)]
            # materials for calculating correlations Z1
            # Regular expression pattern to match "P(Z1 |...)=X\n" and capture X
            pattern_z1 = r"P\(Z1\s*\|\s*.*?\)\s*=\s*(\d+\.\d+|\d+)"
            # Find all matches in the text
            _matches = re.findall(pattern_z1, item['answer_generator:input'])
            if len(_matches) > 0:
                # Convert the first match to float and append to the list
                tuples_z1_conf.append((float(_matches[0]), predicted_prob))
            # materials for calculating correlations Z2
            # Regular expression pattern to match "P(Z2 |...)=X\n" and capture X
            pattern_z2 = r"P\(Z2\s*\|\s*.*?\)\s*=\s*(\d+\.\d+|\d+)"
            # Find all matches in the text
            _matches = re.findall(pattern_z2, item['answer_generator:input'])
            if len(_matches) > 0:
                # Convert the first match to float and append to the list
                tuples_z2_conf.append((float(_matches[0]), predicted_prob))

            def extract_get_embed(txt, regex_pattern):
                _match = re.search(regex_pattern, txt, re.DOTALL)
                if _match:
                    _response = openai.Embedding.create(
                        input=_match.group(1),
                        model="text-embedding-3-small",
                        dimensions=embed_dim
                    )
                    return _response.data[0].embedding
                else:
                    return None

            pattern_ans_embed = r"Make a Decision with Confidence \(Variable Z3\)(.*?)Conclusion:"
            embed_ans = extract_get_embed(item['answer_generator:input'], pattern_ans_embed)
            pattern_z1_embed = r"Understanding Knowledge and Context \(Variable Z1\)(.*?)Analyzing Textual and Visual Information \(Variable Z2\)"
            embed_z1 = extract_get_embed(item['answer_generator:input'], pattern_z1_embed)
            pattern_z2_embed = r"Analyzing Textual and Visual Information \(Variable Z2\)(.*?)Make a Decision with Confidence \(Variable Z3\)"
            embed_z2 = extract_get_embed(item['answer_generator:input'], pattern_z2_embed)
            if embed_ans is not None and embed_z1 is not None:
                tuples_z1_embed.append((embed_z1, embed_ans))
            if embed_ans is not None and embed_z2 is not None:
                tuples_z2_embed.append((embed_z2, embed_ans))

        else:
            raise ValueError(f"Model {model} is not supported")

    def calculate_cosine_similarity(embed1, embed2):
        return sum([e1 * e2 for e1, e2 in zip(embed1, embed2)]) / (
                    sum([e1 ** 2 for e1 in embed1]) * sum([e2 ** 2 for e2 in embed2])) ** 0.5

    cossim_z1_ans = []
    cossim_z2_ans = []
    for embed_z1, embed_ans in tuples_z1_embed:
        cossim_z1_ans.append(calculate_cosine_similarity(embed_z1, embed_ans))
    for embed_z2, embed_ans in tuples_z2_embed:
        cossim_z2_ans.append(calculate_cosine_similarity(embed_z2, embed_ans))
    print(f"Average cosine similarity between Z1 and answer: {sum(cossim_z1_ans) / len(cossim_z1_ans)}")
    print(f"Average cosine similarity between Z2 and answer: {sum(cossim_z2_ans) / len(cossim_z2_ans)}")

    def calculate_pearson_spearman(tuples_z_conf):
        # Step 1: Sort the list of tuples by v values
        # tuples_z_conf = sorted(tuples_z_conf, key=lambda x: (x[0], x[1]))
        # Step 2: Extract v and s values into separate lists
        _v_values = [v for v, _ in tuples_z_conf]
        _s_values = [s for _, s in tuples_z_conf]
        # Step 3: Compute Pearson and Spearman correlation
        pearson_corr, _ = pearsonr(_v_values, _s_values)
        spearman_corr, _ = spearmanr(_v_values, _s_values)

        return pearson_corr, spearman_corr

    # normalized_entropies = []
    # for option_prob_dict in option_prob_dicts:
    #     probabilities = list(option_prob_dict.values())
    #     n = len(probabilities)  # number of options
    #     entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)  # calculate entropy
    #     max_entropy = math.log2(n)  # maximum possible entropy
    #     normalized_entropy = entropy / max_entropy
    #     normalized_entropies.append(normalized_entropy)
    # conj_normalized_entropies = [1 - ne for ne in normalized_entropies]
    # v_values = [v for v, _ in tuples_z1_conf]
    # # combine z1 and normalized entropies as tuples
    # tuples_z1_nentropy = list(zip(v_values, conj_normalized_entropies))
    # v_values = [v for v, _ in tuples_z2_conf]
    # tuples_z2_nentropy = list(zip(v_values, conj_normalized_entropies))

    if len(tuples_z1_conf) > 0:
        corr_z1 = calculate_pearson_spearman(tuples_z1_conf)
    else:
        corr_z1 = (999, 999)
    if len(tuples_z2_conf) > 0:
        corr_z2 = calculate_pearson_spearman(tuples_z2_conf)
    else:
        corr_z2 = (999, 999)

    return corr_z1, corr_z2


def calculate_auroc_pr(data, model):
    predictions = []
    for item in data:
        # Extract information
        if model in ["bcot-ticoh-s", "bcot-ticoh-l"]:
            probs = item['bcot_option_prob_dict']
            sampled_solution = item['bcot_sampled_solution']
            correct_option_index = item['example']['answer']  # Index of the correct answer
            correct_option = chr(correct_option_index + 65)  # Convert index to letter (assuming 'A' is 0)
            # Find the predicted probability and correctness
            predicted_prob = probs[str(ord(sampled_solution) - 65)]
            correctness = 1 if sampled_solution == correct_option else 0
        elif model in ['io', 'cot', 'chameleon', 'chameleon-hybrid']:
            predicted_prob = item['option_prob']
            correctness = 1 if item['true_false'] else 0
        else:
            raise ValueError(f"Model {model} is not supported")
        # Append predictions
        predictions.append({'probability': predicted_prob, 'correct': correctness})

    # Extract true labels and predicted probabilities from the predictions
    true_labels = [pred['correct'] for pred in predictions]
    pred_probs = [pred['probability'] for pred in predictions]
    # Calculate accuracy, sum all correct predictions and divide by the total number of predictions
    accuracy = sum(true_labels) / len(true_labels)
    print(f"Accuracy: {accuracy}")
    # Calculate AUROC
    auroc = roc_auc_score(true_labels, pred_probs)
    # Calculate AUPRC for Positive class (PR-P)
    precision, recall, _ = precision_recall_curve(true_labels, pred_probs)
    auprc_positive = auc(recall, precision)
    # Calculate AUPRC for Negative class (PR-N)
    # Invert labels and probabilities for PR-N calculation
    inverted_labels = [1 - label for label in true_labels]
    inverted_probs = [1 - prob for prob in pred_probs]
    precision_neg, recall_neg, _ = precision_recall_curve(inverted_labels, inverted_probs)
    auprc_negative = auc(recall_neg, precision_neg)

    return auroc, auprc_positive, auprc_negative


def update_json_file(file_path, new_ece, new_ece_bins):
    # Read the existing data from the file
    with open(file_path, 'r') as file:
        data = json.load(file, object_pairs_hook=OrderedDict)
    # Create a new OrderedDict
    new_data = OrderedDict()
    for key, value in data.items():
        new_data[key] = value
        # Insert 'ece' and 'ece_bins' after 'count'
        if key == 'count':
            new_data['ece'] = new_ece
            new_data['ece_bins'] = new_ece_bins
    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(new_data, file, indent=2)


if __name__ == '__main__':
    # parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True, choices=['io', 'cot', 'chameleon', 'bcot-ticoh-s', 'chameleon-hybrid', "bcot-ticoh-l"])
    parser.add_argument('--file_path', type=str, required=True)
    parser.add_argument('--num_bins', type=int, default=10)
    parser.add_argument('--uniform_bins', type=bool, default=True, required=False)
    args = parser.parse_args()
    # Load data
    __data = load_data(args.file_path)



    # load json file '../results/scienceqa_3568/vpgm_dirich_test_2563.json'
    _data = json.load(open('../results/scienceqa_3568/vpgm_test_2563.json', "r"))
    # Extract the set of pids from B
    b_pids = {item["pid"] for item in _data}
    # Filter A to include only items whose pid is in B's pids
    data = [item for item in __data if item["pid"] in b_pids]



    # Calculate ECE and bin values
    ece, bin_values = calculate_ece(data, args.model, args.num_bins, args.uniform_bins)
    print(f"The ECE of {args.model} is: {ece}")
    # Sort bin values based on bin_lower_bound
    bin_values = sorted(bin_values, key=lambda x: x['bin_lower_bound'])
    # Print bin values in sorted order
    for bin_value in bin_values:
        print(f"Bin {bin_value['bin_lower_bound']} - {bin_value['bin_lower_bound'] + 1 / len(bin_values)}:")
        print(f"\tAverage Confidence: {bin_value['avg_confidence']}")
        print(f"\tAverage Accuracy: {bin_value['avg_accuracy']}")
        print(f"\tTotal in Bin: {bin_value['total']}\n")

    # Calculate the metrics
    auroc, auprc_positive, auprc_negative = calculate_auroc_pr(data, args.model)
    # Print the results
    print(f"AUROC: {auroc}")
    print(f"AUPRC-Positive (PR-P): {auprc_positive}")
    print(f"AUPRC-Negative (PR-N): {auprc_negative}")

    # Calculate correlations
    if args.model in ["bcot-ticoh-s"]:
        corr_z1, corr_z2 = calculate_correlation(data, args.model)
        # Assuming corr_z1 and corr_z2 are tuples like (pearson_corr, spearman_corr)
        print(f"Correlation Z1 (pearson, spearman): ({corr_z1[0]:.4f}, {corr_z1[1]:.4f})")
        print(f"Correlation Z2 (pearson, spearman): ({corr_z2[0]:.4f}, {corr_z2[1]:.4f})")
