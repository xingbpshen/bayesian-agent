#!/bin/bash

# Setting
num_test_trial=100
sg_temperature=0
model=chameleon
label=exp3

# Command to execute
CMD="python run.py
      --policy_engine gpt-3.5-turbo
      --kr_engine gpt-3.5-turbo
      --qg_engine gpt-3.5-turbo
      --sg_engine gpt-3.5-turbo
      --test_split test
      --test_number -1
      --num_test_trial $num_test_trial
      --model $model
      --sg_temperature $sg_temperature
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

python ece.py --model $model --file_path ../results/scienceqa/${label}_test_cache.json --uniform_bins
