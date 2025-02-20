import json
import random


def manipulate_data(data_path, mismatch_ratio=0.0, mismatch_key="caption"):
    # load the dictionary from the json file
    with open(data_path, "r") as file:
        data = json.load(file)

    # Determine the number of entries to manipulate
    num_entries = int(len(data) * mismatch_ratio)

    # randomly shuffle the data
    random.shuffle(data)

    # Perform the caption swap operation on the first num_entries entries
    if num_entries > 1:
        values = [data[i][mismatch_key] for i in range(num_entries)]
        new_values = values[-1:] + values[:-1]

        for i in range(num_entries):
            data[i][mismatch_key] = new_values[i]

    # Save the manipulated data to a JSON file
    output_filename = "aokvqa_val_108_subset_105_{}_mismatch_{}.json".format(mismatch_key, mismatch_ratio)
    with open(output_filename, 'w') as f:
        json.dump(data, f, indent=4)


manipulate_data("./aokvqa_val_108_subset_105.json", mismatch_ratio=0.3, mismatch_key="rationales")
