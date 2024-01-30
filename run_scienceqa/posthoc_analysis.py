import re

file1 = '../results/scienceqa/exp6_test_cache.json'
file2 = '../results/scienceqa/exp7_test_cache.json'
# Initialize counters
m = 0
c = 0

# Open the file and read it as a single string
with open(file1, 'r') as file:
    file_content = file.read()

# Use regular expressions to find all instances of "answer_generator:input" and "true_false"
answer_inputs = re.findall(r'"answer_generator:input":\s*"([^"]*)"', file_content)
true_falses = re.findall(r'"true_false":\s*(true|false)', file_content)

# Ensure we have the same number of each (sanity check)
if len(answer_inputs) != len(true_falses):
    print("Mismatched number of answer_generator:inputs and true_false entries.")
else:
    # Iterate over the matched results
    for answer_input, true_false in zip(answer_inputs, true_falses):
        if "from random selection" not in answer_input.lower():
            m += 1
            if true_false.lower() == "true":
                c += 1

# Calculate the ratio
ratio = c / m if m != 0 else 0

# Print the results
print(f"Total samples (m): {m}")
print(f"Samples with true_false=true (c): {c}")
print(f"Ratio (c/m): {ratio}\n")


import re

def extract_data_from_file(filename):
    # Open the file and read it as a single string
    with open(filename, 'r') as file:
        file_content = file.read()

    # Use regular expressions to find all instances of "answer_generator:input", "true_false", and "pid"
    answer_inputs = re.findall(r'"answer_generator:input":\s*"([^"]*)"', file_content)
    true_falses = re.findall(r'"true_false":\s*(true|false)', file_content)
    pids = re.findall(r'"pid":\s*"([^"]*)"', file_content)

    return answer_inputs, true_falses, pids

# Extract data from FILE1
answer_inputs_file1, true_falses_file1, pids_file1 = extract_data_from_file(file1)

# Initialize list for pids where the condition fails
pids_rand_guess = [pid for answer_input, pid in zip(answer_inputs_file1, pids_file1) if "from random selection" in answer_input.lower()]

# Extract data from FILE2
answer_inputs_file2, true_falses_file2, pids_file2 = extract_data_from_file(file2)

# Initialize counters
x = 0
y = 0

# Iterate over the extracted data from FILE2
for pid, true_false in zip(pids_file2, true_falses_file2):
    # Check if pid is in pids_rand_guess
    if pid in pids_rand_guess:
        x += 1  # Increment x for each selected sample
        # Check if 'true_false' is true for this sample
        if true_false.lower() == "true":
            y += 1

# Calculate the ratio
ratio = y / x if x != 0 else 0

# Print the results
print(f"Total selected samples (x): {x}")
print(f"Samples with true_false=true (y): {y}")
print(f"Ratio (y/x): {ratio}\n")

print(f"Total ensemble samples: {m + x}")
print(f"Samples with true_false=true: {c + y}")
print(f"Acc.: {(c + y) / (m + x)}\n")


def extract_relevant_pids(filename):
    # Extract "answer_generator:input" and "pid" values from the given file
    answer_inputs, _, pids = extract_data_from_file(filename)

    # Get pids for data samples where "answer_generator:input" does not contain "from random selection"
    pids_nrand = [pid for answer_input, pid in zip(answer_inputs, pids) if
                  "from random selection" not in answer_input.lower()]

    return pids_nrand


def count_true_false(file_pids_nrand, filename):
    # Extract "pid" and "true_false" values from the given file
    _, true_falses, pids = extract_data_from_file(filename)

    # Initialize count
    count = sum(
        1 for true_false, pid in zip(true_falses, pids) if pid in file_pids_nrand and true_false.lower() == "true")

    return count


# Extract relevant pids from FILE1 and FILE2
file1_pids_nrand = extract_relevant_pids(file1)
file2_pids_nrand = extract_relevant_pids(file2)

# Find intersection of the two lists
intersect_pids_nrand = list(set(file1_pids_nrand) & set(file2_pids_nrand))

# Count and calculate ratio for FILE1
count_file1 = count_true_false(intersect_pids_nrand, file1)
ratio_file1 = count_file1 / len(intersect_pids_nrand) if intersect_pids_nrand else 0

# Count and calculate ratio for FILE2
count_file2 = count_true_false(intersect_pids_nrand, file2)
ratio_file2 = count_file2 / len(intersect_pids_nrand) if intersect_pids_nrand else 0

import json
#
# # Save intersect_pids_nrand to a new file
# with open('intersect_pids_nrand.json', 'w') as file:
#     json.dump(intersect_pids_nrand, file)
# print("Saved intersect_pids_nrand to 'intersect_pids_nrand.json'")

print(f"Total interested samples: {len(intersect_pids_nrand)}")
# Print results for FILE1
print(f"FILE1: Count of 'true_false'=true: {count_file1}")
print(f"FILE1: Ratio: {ratio_file1}")

# Print results for FILE2
print(f"FILE2: Count of 'true_false'=true: {count_file2}")
print(f"FILE2: Ratio: {ratio_file2}\n")


def extract_and_filter_data(filename, pids_to_keep):
    filtered_data_texts = []
    current_sample = []
    brace_count = 0

    with open(filename, 'r') as file:
        for line in file:
            # Count braces to determine the start and end of a data sample
            brace_count += line.count('{')
            brace_count -= line.count('}')

            # If we are inside a data sample, add the line to current_sample
            if brace_count > 0:
                current_sample.append(line)
            elif brace_count == 0 and current_sample:
                # We reached the end of a data sample
                current_sample.append(line)
                sample_text = ''.join(current_sample)

                # Check if the sample's pid is in the list
                pid_search = re.search(r'"pid":\s*"([^"]*)"', sample_text)
                if pid_search:
                    pid = pid_search.group(1)
                    if pid in pids_to_keep:
                        filtered_data_texts.append(sample_text)

                # Reset for the next sample
                current_sample = []

    return filtered_data_texts


def save_data_to_file(data_texts, output_filename):
    # Combine all data texts into one string separated by newlines
    combined_data_text = '\n\n'.join(data_texts)  # Separate samples by two newlines for clarity

    # Save the combined data text to the output file
    with open(output_filename, 'w') as file:
        file.write(combined_data_text)

    print(f"Filtered data saved to '{output_filename}'")

# Assuming intersect_pids_nrand is already defined and contains the pids

# Extract and filter data from FILE1 and save to NEW_FILE1.txt
filtered_data_texts_file1 = extract_and_filter_data(file1, intersect_pids_nrand)
save_data_to_file(filtered_data_texts_file1, 'NEW_FILE1.txt')

# Extract and filter data from FILE2 and save to NEW_FILE2.txt
filtered_data_texts_file2 = extract_and_filter_data(file2, intersect_pids_nrand)
save_data_to_file(filtered_data_texts_file2, 'NEW_FILE2.txt')
