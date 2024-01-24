import json
from collections import defaultdict


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
        if model == 'bcot-ticoh-s':
            probs = item['bcot_option_prob_dict']
            sampled_solution = item['bcot_sampled_solution']
            correct_option_index = item['example']['answer']  # Index of the correct answer
            correct_option = chr(correct_option_index + 65)  # Convert index to letter (assuming 'A' is 0)
            # Find the predicted probability and correctness
            predicted_prob = probs[str(ord(sampled_solution) - 65)]
            correctness = 1 if sampled_solution == correct_option else 0
        elif model in ['cot', 'chameleon']:
            predicted_prob = item['option_prob']
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


if __name__ == '__main__':
    # parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True, choices=['cot', 'chameleon', 'bcot-ticoh-s'])
    parser.add_argument('--file_path', type=str, required=True)
    parser.add_argument('--num_bins', type=int, default=10)
    parser.add_argument('--uniform_bins', action='store_true')
    args = parser.parse_args()
    # Load data
    data = load_data(args.file_path)
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
