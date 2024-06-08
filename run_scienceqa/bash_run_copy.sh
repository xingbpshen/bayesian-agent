#!/bin/bash

# Settings
test_trial=scienceqa-100
sg_temperature=0.2  # set 0.2 for chameleon-hybrid, bcot-ticoh-s, bcot-ticoh-l, set 0 otherwise
sg_num_samplings=1  # for chameleon-hybrid, bcot-ticoh-s, bcot-ticoh-l
model=bcot-ticoh-l  # choose from cot, chameleon, chameleon-hybrid, bcot-ticoh-s, bcot-ticoh-l
label=exp15

# Command to execute
CMD="python run.py
      --policy_engine gpt-3.5-turbo
      --kr_engine gpt-3.5-turbo
      --qg_engine gpt-3.5-turbo
      --sg_engine gpt-3.5-turbo
      --test_split test
      --test_number -1
      --test_trial $test_trial
      --model $model
      --sg_temperature $sg_temperature
      --sg_num_samplings $sg_num_samplings
      --label $label
    "

# Run the command in a loop until it exits successfully
while true; do
    $CMD

    # Check the exit status of the last command
    if [ $? -eq 0 ]; then
        echo "The command terminated normally."
        break
    else
        echo "The command terminated with an exception. Retrying..."
    fi
done

echo "Script completed."

python ece.py --model $model --file_path ../results/scienceqa/${label}_test_cache.json --num_bins 10 --uniform_bins
