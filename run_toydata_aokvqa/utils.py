import json


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



# Example dictionary load from file path
with open("../data/toydata_aokvqa/aokvqa_val_108_subset_3.json", "r") as file:
    data = json.load(file)


# Generate the prompt
prompt = format_question_prompt(data[2])
print(prompt)
