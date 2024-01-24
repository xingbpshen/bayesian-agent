# import openai
#
# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )
#
# print(completion['choices'][0]['message']['content'].strip())


# import json
# import re
#
# # Step 1: Read the content of ocr.json
# with open('../data/scienceqa/ocrs.json', 'r') as file:
#     content = file.read()
#
# # Step 2: Remove all occurrences of the pattern [a, b]
# # Note: This pattern looks for square brackets containing two integers separated by a comma and optional spaces
# edited_content = re.sub(r'\[\s*\d+\s*,\s*\d+\s*\]', '', content)
#
# # Step 3: Save the edited content to ocr_wo_pos.json
# with open('../data/scienceqa/ocr_wo_pos.json', 'w') as file:
#     file.write(edited_content)
#
# print("The file 'ocr_wo_pos.json' has been created with the specified changes.")


# import re
#
# # Step 1: Read the content of ocr_wo_pos.json
# with open('../data/scienceqa/ocr_wo_pos.json', 'r') as file:
#     content = file.read()
#
# # Step 2: Remove all occurrences of the pattern [, , , ],
# edited_content = re.sub(r'\[\s*,\s*,\s*,\s*\],?', '', content)
#
# # Step 3: Save the edited content back to ocr_wo_pos.json or a new file if you prefer
# with open('../data/scienceqa/ocr_wo_pos.json', 'w') as file:
#     file.write(edited_content)
#
# print("The file 'ocr_wo_pos.json' has been updated with the specified changes.")


# import re
#
# # Step 1: Read the content of ocr_wo_pos.json
# with open('../data/scienceqa/ocr_wo_pos.json', 'r') as file:
#     content = file.read()
#
# # Step 2: Remove all floating-point numbers with exactly 17 decimal places
# # edited_content = re.sub(r'\b\d+\.\d{15}\b', '', content)
# edited_content = re.sub(r'%', '', content)
#
# # Step 3: Save the edited content back to ocr_wo_pos.json
# with open('../data/scienceqa/ocr_wo_pos.json', 'w') as file:
#     file.write(edited_content)
#
# print("The file 'ocr_wo_pos.json' has been updated with the specified changes.")

text = """
Understanding Knowledge and Context (Variable Z1)
Analysis:
- Main Topic: Identifying a figure of speech used in a given text.
- Specific Knowledge Required: Knowledge of different figures of speech and their definitions.
- Retrieved Knowledge: The text describes a salesperson trying to convince Franklin to buy a jacket by emphasizing that it is made of "genuine imitation leather."
- Bing Search Response: No additional information is provided.
Given the clear information in the text about the contradictory phrase "genuine imitation leather," the probability of Z1 capturing the essential knowledge and context accurately is high.
Probability:
P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response)=0.900

Analyzing Textual and Visual Information (Variable Z2)
Analysis:
- No image or detected text is provided for this question.
- Only the given text needs to be analyzed.
- The phrase "genuine imitation leather" combines contradictory terms, suggesting the use of an oxymoron.
Given that only the given text needs to be analyzed and the clear presence of a contradictory phrase, the probability of Z2 accurately reflecting the meaning difference and assigning appropriate weightage is high.
Probability:
P(Z2 | Z1,Detected Text, Image Caption)=0.900

Make a Decision with Confidence (Variable Z3)
Analysis:
- Option A (hyperbole): Not supported. The given text does not contain an exaggerated statement or claim.
- Option B (oxymoron): Strongly supported. The phrase "genuine imitation leather" combines contradictory terms, fitting the definition of an oxymoron.
Given the analysis and the clear presence of an oxymoron in the given text, the confidence in each option being correct is as follows:
Probabilities:
P(Z3_{Option A} | Z2)=0.100
P(Z3_{Option B} | Z2)=0.900

Conclusion:
The answer is B with a numerical probability of 0.900.
"""

# lines = text.split('\n')  # Split the text into individual lines
# probabilities_start = None
# probabilities_end = None
#
# # Find the line numbers for "Probabilities:" and "Conclusion:"
# for i, line in enumerate(lines):
#     if "Probabilities:" in line:
#         probabilities_start = i + 1  # Start capturing from the next line
#     if "Conclusion:" in line:
#         probabilities_end = i  # Stop capturing at this line
#         break  # No need to continue searching
#
# # Extract the lines between "Probabilities:" and "Conclusion:"
# if probabilities_start is not None and probabilities_end is not None:
#     probability_lines = lines[probabilities_start:probabilities_end]
#     probabilities_info = "\n".join(probability_lines)
# else:
#     probabilities_info = "No probabilities information found"
#
# print(probabilities_info)

def normalize_dict(_dict):
    # normalize the probabilities (with maximum 3 decimal places) if not sum to 1
    # if the case of all 0s, assign 1/len(_dict) to each key
    _sum = sum(_dict.values())
    if _sum != 1.0:
        if _sum == 0.0:
            _dict = {_key: round(1.0 / len(_dict), 3) for _key in _dict.keys()}
        else:
            _dict = {_key: round(_value / _sum, 3) for _key, _value in _dict.items()}
    return _dict

print(normalize_dict({0: 0, 1: 0, 2: 0}))
