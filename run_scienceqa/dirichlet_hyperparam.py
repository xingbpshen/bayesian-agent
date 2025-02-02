import numpy as np
from ece import load_data
import json
import torch
import torch.nn as nn
from ece import calculate_ece_2

# data = load_data("../results/scienceqa_3568/bcot-ticoh-s_sciqafull_nrand_inter.json")
#
# num_k_dist = {}
# for dp in data:
#     if len(dp["bcot_option_prob_dict"]) not in num_k_dist:
#         num_k_dist[len(dp["bcot_option_prob_dict"])] = 1
#     else:
#         num_k_dist[len(dp["bcot_option_prob_dict"])] += 1
# print(num_k_dist)
#
# n = 1007
# n_pick_2 = int(n * (num_k_dist[2] / len(data)))
# n_pick_3 = int(n * (num_k_dist[3] / len(data)))
# n_pick_4 = int(n * (num_k_dist[4] / len(data)))
# n_pick_5 = int(n * (num_k_dist[5] / len(data)))
# pick_2, pick_3, pick_4, pick_5 = [],[],[],[]
# for dp in data:
#     if len(dp["bcot_option_prob_dict"]) == 2 and len(pick_2) < n_pick_2:
#         pick_2.append(dp)
#     if len(dp["bcot_option_prob_dict"]) == 3 and len(pick_3) < n_pick_3:
#         pick_3.append(dp)
#     if len(dp["bcot_option_prob_dict"]) == 4 and len(pick_4) < n_pick_4:
#         pick_4.append(dp)
#     if len(dp["bcot_option_prob_dict"]) == 5 and len(pick_5) < n_pick_5:
#         pick_5.append(dp)
# print(len(pick_2), len(pick_3), len(pick_4), len(pick_5))
# # Merge pick_2, pick_3, pick_4, pick_5
# pick_all = pick_2 + pick_3 + pick_4 + pick_5
# # Save pick_all to a json file ../results/scienceqa_3568/vpgm_dirich_val_{}.json with indent=4
# with open(f"../results/scienceqa_3568/vpgm_dirich_val_{len(pick_all)}.json", "w") as f:
#     json.dump(pick_all, f, indent=4)
# not_pick_all = [dp for dp in data if dp not in pick_all]
# # Check not_pick_all is proper to be a json file
# print(len(not_pick_all))
# # Save not_pick_all to a json file ../results/scienceqa_3568/vpgm_dirich_test_{}.json with indent=4
# with open(f"../results/scienceqa_3568/vpgm_dirich_test_{len(not_pick_all)}.json", "w") as f:
#     json.dump(not_pick_all, f, indent=4)


path = "../results/scienceqa_3568/vpgm_dirich_val_1005.json"
max_num_category = 5
with open(path, "r") as f:
    data = json.load(f)

# Create tensor dataset
pis = []
tags = []
gt_answers = []
selected_answers = []
nks = torch.zeros(max_num_category)
for dp in data:
    bcot_option_prob_dict = dp["bcot_option_prob_dict"]
    # Convert values of bcot_option_prob_dict to a list
    _bcot_option_prob_dict = list(bcot_option_prob_dict.values())
    # If the length of _bcot_option_prob_dict is less than max_num_category,
    # append 0 to _bcot_option_prob_dict until the length is max_num_category
    while len(_bcot_option_prob_dict) < max_num_category:
        _bcot_option_prob_dict.append(0)
    # Append _bcot_option_prob_dict to pis
    pis.append(_bcot_option_prob_dict)
    # Append the value of dp["example"]["answer"] to gt_answers
    gt_answers.append(dp["example"]["answer"])
    # Find the key of the maximum value in the bcot_option_prob_dict
    _selected_answers = int(max(bcot_option_prob_dict, key=bcot_option_prob_dict.get))
    nks[_selected_answers] += 1
    selected_answers.append(_selected_answers)
    # Append the length of the bcot_option_prob_dict to tags
    tags.append(len(bcot_option_prob_dict))
# Convert to tensors and numpy arrays
pis_tensor = torch.tensor(pis, dtype=torch.float32)
gt_answers_tensor = torch.tensor(gt_answers, dtype=torch.long)
tags_tensor = torch.tensor(tags, dtype=torch.long)
pis_np = np.array(pis)
gt_answers_np = np.array(gt_answers)
selected_answers_np = np.array(selected_answers)


# Create model
class pi_k_model(nn.Module):
    def __init__(self):
        super(pi_k_model, self).__init__()
        self.lamb = nn.Parameter(torch.ones(1) * 0.001) # This is \tau in the paper
        self.nks = nks.clone().detach().requires_grad_(True)

    def forward(self, pis, tags):
        # Expand temperature to match the size of logits
        temperature = self.lamb.unsqueeze(1).expand(pis.size(0), pis.size(1))
        alpha_k = pis / temperature

        # Function to manipulate nks according to the tag
        def f(tag, nks):
            # Create a mask that zeroes out elements after the 'tag' index
            mask = torch.arange(nks.size(0)) < tag
            return nks * mask

        # Create _nks with shape (b, c)
        _b = pis.shape[0]  # Batch size
        _c = pis.shape[1]  # Number of categories (same as nks.shape)
        _nks = torch.zeros((_b, _c), dtype=torch.float32)

        # Apply function f for each row
        for i in range(_b):
            _nks[i] = f(tags[i], self.nks)

        alpha_k_prime = _nks + alpha_k
        # Sum over the second dimension (sum of each row)
        sum_alpha = alpha_k_prime.sum(dim=1, keepdim=True)
        return alpha_k_prime / sum_alpha


class MDCA(torch.nn.Module):
    def __init__(self):
        super(MDCA, self).__init__()

    def forward(self, output, target):
        output = torch.softmax(output, dim=1)
        # [batch, classes]
        loss = torch.tensor(0.0)
        batch, classes = output.shape
        for c in range(classes):
            avg_count = (target == c).float().mean()
            avg_conf = torch.mean(output[:, c])
            loss += torch.abs(avg_conf - avg_count)
        denom = classes
        loss /= denom
        return loss


class FocalLoss(nn.Module):
    def __init__(self, gamma=0, **kwargs):
        super(FocalLoss, self).__init__()

        self.gamma = gamma
        # logging.info("using gamma={}".format(gamma))

    def forward(self, input, target):
        target = target.view(-1, 1)

        logpt = torch.nn.functional.log_softmax(input, dim=1)
        logpt = logpt.gather(1, target)
        logpt = logpt.view(-1)
        pt = logpt.exp()

        loss = -1 * (1 - pt) ** self.gamma * logpt

        return loss.mean()


class ClassficationAndMDCA(nn.Module):
    def __init__(self, loss="FL+MDCA", alpha=0.1, beta=1.0, gamma=1.0, **kwargs):
        super(ClassficationAndMDCA, self).__init__()

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        if "NLL" in loss:
            self.classification_loss = nn.CrossEntropyLoss()
        elif "FL" in loss:
            self.classification_loss = FocalLoss(gamma=self.gamma)
        self.MDCA = MDCA()

    def forward(self, logits, targets):
        loss_cls = self.classification_loss(logits, targets)
        loss_cal = self.MDCA(logits, targets)
        return loss_cls + self.beta * loss_cal


model = pi_k_model()
optimizer = torch.optim.LBFGS(model.parameters(), lr=0.00000001, max_iter=1000)
criterion = ClassficationAndMDCA()
# Train
model.train()
# Training
def closure():
    optimizer.zero_grad()
    pis_map_mean = model(pis_tensor, tags)
    loss = criterion(pis_map_mean, gt_answers_tensor)
    loss.backward()
    return loss
print(f"Lambda before optimization: {model.lamb.item()}")
optimizer.step(closure)
print(f"Lambda after optimization: {model.lamb.item()}")

# Calculate accuracy and ECE with pis_np, gt_answers_np, selected_answers_np before optimization
correct = np.sum(selected_answers_np == gt_answers_np)
accuracy = correct / len(gt_answers_np)
# The confidence is the value of the selected answer in pis_np
confidence = pis_np[np.arange(len(gt_answers_np)), selected_answers_np]
ece = calculate_ece_2(confidence, selected_answers_np, gt_answers_np)
print(f"Accuracy before optimization: {accuracy}")
print(f"ECE before optimization: {ece}")
# Calculate accuracy and ECE after optimization
pis_map_mean = model(pis_tensor, tags)
selected_answers_after_optimization = torch.argmax(pis_map_mean, dim=1).numpy()
correct = np.sum(selected_answers_after_optimization == gt_answers_np)
accuracy = correct / len(gt_answers_np)
ece = calculate_ece_2(np.max(pis_map_mean.detach().numpy(), axis=1), selected_answers_after_optimization, gt_answers_np)
print(f"Accuracy after optimization: {accuracy}")
print(f"ECE after optimization: {ece}")
