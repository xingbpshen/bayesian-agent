# Verbalized Probabilistic Graphical Modeling with Large Language Models

This repository contains the official implementation of the paper:

> __Verbalized Probabilistic Graphical Modeling with Large Language Models__  
> [Hengguan Huang](https://scholar.google.com/citations?hl=en&user=GQm1eZEAAAAJ), [Xing Shen](https://xingbpshen.github.io), Songtao Wang, [Dianbo Liu](https://scholar.google.com/citations?user=kGSzBpMAAAAJ&hl=en), [Hao Wang](https://scholar.google.com/citations?user=NrOA9QoAAAAJ&hl=en)  
> _arXiv Preprint, June 2024_  
> __[Paper](https://arxiv.org/abs/2406.05516)&nbsp;/ [BibTeX]()__

## Setup
1. Install the required packages:
```bash
pip install -r requirements.txt
```
2. Provide the OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY=your_openai_api_key
```

## Run ScienceQA
1. Run vPGM on ScienceQA dataset:
```bash
cd run_scienceqa
bash bash_run.sh
```
2. After running the above command, you can find the results in the `results/scienceqa_3568/` folder. Please note down the path of the results folder.
3. In the `run_scienceqa/dirichlet_hyperparam_test.py` file, change the `path` variable to the path of the test cache file (e.g., `path = "../results/scienceqa_3568/exp1_test_cache.json"`)
4. Run BayesVPGM on ScienceQA dataset:
```bash
cd run_scienceqa
python dirichlet_hyperparam_test.py
```

## Acknowledgement
This repository contains code adapted from repository [chameleon-llm](https://github.com/lupantech/chameleon-llm). We thank to the above repository's authors for their great work.

## Citation

If you find this repository useful in your research, please cite our paper:

```
@article{huang2024verbalized,
  title={Verbalized Probabilistic Graphical Modeling with Large Language Models},
  author={Huang, Hengguan and Shen, Xing and Wang, Songtao and Liu, Dianbo and Wang, Hao},
  journal={arXiv preprint arXiv:2406.05516},
  year={2024}
}
```