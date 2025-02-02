import json
import torch
import numpy as np
from ece import calculate_ece_2
from torch import nn


path = "../results/scienceqa_3568/vpgm_test_2563.json"
min_num_category = 2
max_num_category = 5
with open(path, "r") as f:
    data = json.load(f)
results_save = data.copy()

# Create tensor dataset from min_num_category to max_num_category
pis = {k: [] for k in range(min_num_category, max_num_category + 1)}
gt_answers = {k: [] for k in range(min_num_category, max_num_category + 1)}
selected_answers = {k: [] for k in range(min_num_category, max_num_category + 1)}
nks = torch.zeros(max_num_category)
for dp in data:
    bcot_option_prob_dict = dp["bcot_option_prob_dict"]
    # Convert values of bcot_option_prob_dict to a list
    _bcot_option_prob_dict = list(bcot_option_prob_dict.values())
    # Append _bcot_option_prob_dict to pis
    pis[len(_bcot_option_prob_dict)].append(_bcot_option_prob_dict)
    # Append the value of dp["example"]["answer"] to gt_answers
    gt_answers[len(_bcot_option_prob_dict)].append(dp["example"]["answer"])
    # Find the key of the maximum value in the bcot_option_prob_dict
    _selected_answers = int(max(bcot_option_prob_dict, key=bcot_option_prob_dict.get))
    nks[_selected_answers] += 1
    selected_answers[len(_bcot_option_prob_dict)].append(_selected_answers)
# Convert to tensors and numpy arrays
pis_tensor = {k: torch.tensor(v, dtype=torch.float32) for k, v in pis.items()}
pis_np = {k: np.array(v) for k, v in pis.items()}
gt_answers_tensor = {k: torch.tensor(v, dtype=torch.long) for k, v in gt_answers.items()}
gt_answers_np = {k: np.array(v) for k, v in gt_answers.items()}
selected_answers_np = {k: np.array(v) for k, v in selected_answers.items()}

# Calculate accuracy and ECE with pis_np, gt_answers_np, selected_answers_np before optimization
# Concate all gt_answers_np, selected_answers_np
_gt_answers_np = np.concatenate([gt_answers_np[k] for k in range(min_num_category, max_num_category + 1)])
_selected_answers_np = np.concatenate([selected_answers_np[k] for k in range(min_num_category, max_num_category + 1)])
correct = np.sum(_selected_answers_np == _gt_answers_np)
accuracy = correct / len(_gt_answers_np)
# The confidence is the value of the selected answer in pis_np
_confidence = np.concatenate([pis_np[k][np.arange(len(gt_answers_np[k])), selected_answers_np[k]]
                              for k in range(min_num_category, max_num_category + 1)])
ece = calculate_ece_2(_confidence, _selected_answers_np, _gt_answers_np)
print(f"Accuracy before dirichlet: {accuracy}")
print(f"ECE before dirichlet: {ece}\n")

class pi_k_model(nn.Module):
    def __init__(self, init_lamb):
        super(pi_k_model, self).__init__()
        self.lamb = nn.Parameter(torch.ones(1) * init_lamb) # This is \tau in the paper
        self.nks = nks.clone().detach().requires_grad_(True)

    def forward(self, pis):
        # Expand temperature to match the size of logits
        temperature = self.lamb.unsqueeze(1).expand(pis.size(0), pis.size(1))
        alpha_k = pis / temperature

        b, c2 = pis.shape
        # Step 1: Slice nks to get the first c2 elements
        sliced_nks = self.nks[:c2]  # Shape (c2,)
        # Step 2: Repeat the sliced_nks along the batch dimension to get shape (b, c2)
        _nks = sliced_nks.unsqueeze(0).expand(b, c2)

        alpha_k_prime = _nks + alpha_k
        # Sum over the second dimension (sum of each row)
        sum_alpha = alpha_k_prime.sum(dim=1, keepdim=True)
        return alpha_k_prime / sum_alpha


## Use group div
# models = {2: pi_k_model(init_lamb=9.989992395276204e-05),
#           3: pi_k_model(init_lamb=8.106351015157998e-05),
#           4: pi_k_model(init_lamb=-0.0001605218421900645),
#           5: pi_k_model(init_lamb=0.0008139978745020926)}
# Use shared
models = {k: pi_k_model(init_lamb=2.0513503841357306e-05) for k in range(min_num_category, max_num_category + 1)}
# Set to eval mode
for k in models:
    models[k].eval()

# Calculate accuracy and ECE after optimization
selected_answers_after_optimization = {k: torch.argmax(models[k](pis_tensor[k]), dim=1).numpy()
                                      for k in range(min_num_category, max_num_category + 1)}
_selected_answers_after_optimization_np = np.concatenate([selected_answers_after_optimization[k]
                                                            for k in range(min_num_category, max_num_category + 1)])
correct = np.sum(_selected_answers_after_optimization_np == _gt_answers_np)
accuracy = correct / len(_gt_answers_np)
_confidence_after_optimization = np.concatenate([np.max(models[k](pis_tensor[k]).detach().numpy(), axis=1)
                                                 for k in range(min_num_category, max_num_category + 1)])
ece = calculate_ece_2(_confidence_after_optimization, _selected_answers_after_optimization_np, _gt_answers_np)
print(f"Accuracy after dirichlet: {accuracy}")
print(f"ECE after dirichlet: {ece}\n")
