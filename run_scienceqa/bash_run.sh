#!/bin/bash

# Command to execute
CMD="python run.py
      --policy_engine gpt-3.5-turbo
      --kr_engine gpt-3.5-turbo
      --qg_engine gpt-3.5-turbo
      --sg_engine gpt-3.5-turbo
      --test_split test
      --test_number -1
      --num_test_trial 100
      --model bcot-ticoh-s
      --sg_temperature 0.2
      --label exp2
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
