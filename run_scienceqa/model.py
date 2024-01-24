import os
import re
import sys
import json
import openai

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities import *
from demos import prompt_policy, prompt_kr, prompt_sg, prompt_qg

# OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

# OpenAI
bing_api_key = os.getenv("BING_API_KEY")
print(bing_api_key)

class solver:

    def __init__(self, args):
        # arguments
        for key, value in vars(args).items():
            setattr(self, key, value)
        # for chameleon
        if self.model in ["cot", "chameleon", "bcot-ticoh-s"]:
            self.use_caption = False # disabled by default, could be enabled by the policy

        # external arguments
        self.api_key = openai.api_key
        self.examples, self.pids = self.load_data()

    def load_data(self):
        # load test data
        pid_splits = json.load(open(os.path.join(self.data_root, "pid_splits.json")))
        _examples = json.load(open(os.path.join(self.data_root, "problems.json")))

        examples = {pid: _examples[pid] for pid in pid_splits[self.test_split]}
        pids = list(examples.keys())

        # update metadata
        for pid, example in examples.items():
            image = example["image"]
            split = example["split"]
            if image:
                example["image_file"] = os.path.join(self.data_root, "images", split, pid, image)
            else:
                example["image_file"] = ""

        # limit the number of test examples
        if self.test_number > 0:
            if self.test_number < len(pids):
                pids = pids[:self.test_number]
                examples = {key: value for key, value in examples.items() if key in pids}

        # load caption data
        if os.path.exists(self.caption_file):
            captions = json.load(open(self.caption_file))["captions"]
            for pid in examples:
                examples[pid]['caption'] = captions[pid] if pid in captions else ""

        # load ocr data
        if os.path.exists(self.ocr_file):
            ocrs = json.load(open(self.ocr_file))["texts"]
            for pid in examples:
                examples[pid]['ocr'] = ocrs[pid] if pid in ocrs else []
        

        return examples, pids


    def get_question_text(self):
        if "question_text" in self.cache:
            return self.cache["question_text"] 
        
        # context
        text_context = self.cache["example"]["hint"]
        image_context = self.cache["example"]["caption"] if self.use_caption else ""
        context = " ".join([text_context, image_context]).strip()

        # option
        choices = self.cache["example"]["choices"]
        inds = ["A", "B", "C", "D", "E"]
        choice_list = [f"({inds[i]}) {choices[i]}" for i in range(len(choices))]
        option = " ".join(choice_list)

        # question text
        question = self.cache["example"]["question"]
        if context != "":
            question_text = f"{question}\n\nContext: {context}\n\nOptions: {option}"
        else:
            question_text = f"{question}\n\nOptions: {option}"

        self.cache["question_text"] = question_text
        return question_text

    def get_metadata(self):
        if "metadata" in self.cache:
            return self.cache["metadata"] 
        
        # extract metadata
        metadata = {}
        example = self.cache["example"]
        metadata["has_image"] = True if example["image"] else False
        metadata["grade"] = int(example["grade"].replace("grade", ""))
        metadata["subject"] = example["subject"]
        metadata["topic"] = example["topic"]
        metadata["category"] = example["category"]
        metadata["skill"] = example["skill"]

        self.cache["metadata"] = metadata
        return metadata

    def build_prompt_for_policy(self):
        # get the example
        question_text = self.get_question_text()
        metadata = self.get_metadata()

        # build the prompt
        demo_prompt = prompt_policy.prompt.strip() # demo prompt
        test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\nModules: " # test prompt
        full_prompt = demo_prompt + "\n\n" + test_prompt # full prompt

        return test_prompt, full_prompt

    def predict_modules(self):
        # get the module input
        test_prompt, full_prompt = self.build_prompt_for_policy()
        messages=[
            {"role": "user", "content": full_prompt},
        ]

        # execute the module
        modules = get_chat_response(messages, self.api_key, self.policy_engine, self.policy_temperature, self.policy_max_tokens)
        modules = self.update_modules(modules)

        # update the cache
        self.cache["modules:input"] = test_prompt
        self.cache["modules:output"] = modules
        return modules

    def update_modules(self, _modules):
        # default modules
        default_modules = ["solution_generator", "answer_generator"]
        
        try:
            modules = eval(_modules.lower().strip())
            assert modules[-2:] == default_modules
        except:
            modules = default_modules

        return modules
    
    def image_captioner(self):
        # get the module input
        image_file = self.cache["example"]["image_file"]
        response = self.cache["response"] if "response" in self.cache else ""

        # excute the module 
        if "caption" in self.cache["example"]:
            caption = self.cache["example"]["caption"]
        else:
            if not os.path.exists(image_file):
                caption = ""
            else:
                # TODO: run the image captioner model on the fly
                caption = "" 

        # update the response cache
        if caption != "":
            response += f"\n\nImage caption: {caption}"
            response = response.strip()

        # update the cache
        self.cache["response"] = response
        self.cache["image_captioner:input"] = image_file
        self.cache["image_captioner:output"] = caption
        return image_file, caption
    
    def text_detector(self):
        # get the module input
        image_file = self.cache["example"]["image_file"]
        response = self.cache["response"] if "response" in self.cache else ""

        # excute the module 
        texts = []
        if "ocr" in self.cache["example"]:
            try:
                ocr = eval(self.cache["example"]["ocr"])
                if len(ocr) > 0:
                    texts = [(t[0], t[1]) for t in ocr] # (coordinates, text)
            except:
                pass
        else:
            if not os.path.exists(image_file):
                texts = []
            else:
                # TODO: run the image captioner model on the fly
                texts = []

        # update the response cache
        if len(texts) > 0:
            response += f"\n\nDetected text in the image: {texts}"
            response = response.strip()

        # update the cache
        self.cache["response"] = response
        self.cache["text_detector:input"] = image_file
        self.cache["text_detector:output"] = texts
        return image_file, texts
    
    def knowledge_retrieval(self):
        # get the example
        question_text = self.get_question_text()
        metadata = self.get_metadata()
        response = self.cache["response"] if "response" in self.cache else ""

        # build the prompt
        demo_prompt = prompt_kr.prompt.strip() # demo prompt
        if response != "":
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\n{response}\n\nKnowledge:\n"
        else:
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\nKnowledge:\n" # test prompt
        full_prompt = demo_prompt + "\n\n" + test_prompt # full prompt

        messages=[
            {"role": "user", "content": full_prompt},
        ]

        # execute the module
        knowledge = get_chat_response(messages, self.api_key, self.kr_engine, self.kr_temperature, self.kr_max_tokens)

        # update the response cache
        if knowledge != "" and knowledge != None:
            response += f"\n\nKnowledge:\n{knowledge}"
            response = response.strip()

        # update the cache
        self.cache["response"] = response
        self.cache["knowledge_retrieval:input"] = test_prompt
        self.cache["knowledge_retrieval:output"] = knowledge
        return test_prompt, knowledge

    def query_generator(self):
        # get the example
        question_text = self.get_question_text()
        metadata = self.get_metadata()
        response = self.cache["response"] if "response" in self.cache else ""

        # demo prompt
        demo_prompt = prompt_qg.prompt.strip() 
        # test prompt
        if response != "":
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\n{response}\n\nSearch Query: "
        else:
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\nSearch Query: "
        # full prompt
        full_prompt = demo_prompt + "\n\n" + test_prompt
        messages=[
            {"role": "user", "content": full_prompt},
        ]

        # execute the module
        query = get_chat_response(messages, self.api_key, self.qg_engine, self.qg_temperature, self.qg_max_tokens)
        if query == "" or query == None:
            query = None

        # update the cache
        self.cache["query"] = query
        self.cache["query_generator:input"] = test_prompt
        self.cache["query_generator:output"] = query
        return test_prompt, query

    def bing_search(self):
        # get the module input
        endpoint = self.endpoint
        count = self.search_count
        query = self.cache["query"] if "query" in self.cache else None
        response = self.cache["response"] if "response" in self.cache else ""

        # excute the module (call the Bing Search API and get the responses)
        if query != None and query != "":
            result = call_bing_search(endpoint, bing_api_key, query, count)
        else:
            result = None
        responses = parse_bing_result(result)

        if len(responses) > 0 and responses[0] != "":
            response += f"\n\nBing search response: {responses}"
            response = response.strip()

        # update the cache
        self.cache["response"] = response
        self.cache["bing_search:input"] = query
        self.cache["bing_search:output"] = responses
        return query, responses

    def build_prompt_for_sg_chameleon(self):
        # get the input
        question_text = self.get_question_text()
        metadata = self.get_metadata()
        response = self.cache["response"] if "response" in self.cache else ""

        # build the prompt
        demo_prompt = prompt_sg.prompt_chameleon.strip() # WARNING: this is the prompt for chameleon
        if response != "":
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\n{response}\n\nSolution: "
        else:
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\nSolution: "
        full_prompt = demo_prompt + "\n\n" + test_prompt # full prompt
        return test_prompt, full_prompt

    def build_prompt_for_sg_bcot_ticoh_s(self):
        # get the input
        question_text = self.get_question_text()
        metadata = self.get_metadata()
        response = self.cache["response"] if "response" in self.cache else ""

        # build the prompt
        demo_prompt = prompt_sg.prompt_bcot_ticoh_s.strip() # WARNING: this is the prompt for BCoT-TiCoh-S
        if response != "":
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\n{response}\n\nSolution: "
        else:
            test_prompt = f"Question: {question_text}\n\nMetadata: {metadata}\n\nSolution: "
        full_prompt = demo_prompt + "\n\n" + test_prompt # full prompt
        return test_prompt, full_prompt

    def build_prompt_for_sg_cot(self):
        question = self.cache["example"]["question"]
        choices = self.cache["example"]["choices"]
        hint = self.cache["example"]["hint"]
        caption = self.cache["example"]["caption"]

        # demo prompt
        demo_prompt = prompt_sg.prompt_cot.strip() # WARNING: this is the prompt for COT
    
        # option
        inds = ["A", "B", "C", "D", "E"]
        choice_list = [f"({inds[i]}) {choices[i]}" for i in range(len(choices))]
        option = " ".join(choice_list)

        # context
        context = hint.strip() 
        if self.use_caption and caption != "":
            context += f" Image: {caption}"
    
        #  test prompt
        if context != "":
            test_prompt = f"Question: {question}\n\nContext: {context}\n\nOptions: {option}\n\nSolution: "
        else:
            test_prompt = f"Question: {question}\n\nOptions: {option}\n\nSolution: "

        full_prompt = demo_prompt + "\n\n" + test_prompt
        return test_prompt, full_prompt

    def build_prompt_for_sg_io(self):
        question = self.cache["example"]["question"]
        choices = self.cache["example"]["choices"]
        hint = self.cache["example"]["hint"]
        caption = self.cache["example"]["caption"]

        # demo prompt
        demo_prompt = prompt_sg.prompt_io.strip()  # WARNING: this is the prompt for COT

        # option
        inds = ["A", "B", "C", "D", "E"]
        choice_list = [f"({inds[i]}) {choices[i]}" for i in range(len(choices))]
        option = " ".join(choice_list)

        # context
        context = hint.strip()
        if self.use_caption and caption != "":
            context += f" Image: {caption}"

        #  test prompt
        if context != "":
            test_prompt = f"Question: {question}\n\nContext: {context}\n\nOptions: {option}\n\nSolution: "
        else:
            test_prompt = f"Question: {question}\n\nOptions: {option}\n\nSolution: "

        full_prompt = demo_prompt + "\n\n" + test_prompt
        return test_prompt, full_prompt

    def solution_generator(self):
        # get the module input
        if self.model == "chameleon":
            test_prompt, full_prompt = self.build_prompt_for_sg_chameleon()
        elif self.model == "bcot-ticoh-s":
            test_prompt, full_prompt = self.build_prompt_for_sg_bcot_ticoh_s()
        elif self.model == "cot":
            test_prompt, full_prompt = self.build_prompt_for_sg_cot()
        elif self.model == "io":
            test_prompt, full_prompt = self.build_prompt_for_sg_io()
        else:
            raise Exception("ERROR: solution_generator(self), invalid model name " + self.model)

        messages=[
            {"role": "user", "content": full_prompt},
        ]

        # excute the module
        patience = self.sg_patience

        if self.model == "bcot-ticoh-s":
            num_sampling = 3
            # in the form of {0: 0.500, 1: 0.500, ...}
            option_prob_dict = None
            for idx_sampling in range(num_sampling):
                # this will only print the 3rd sampling result,
                # however, it will record all probabilities across all samplings in the backend
                success = False
                count = 0
                while count < patience and not success:
                    if self.sg_temperature < 0.1 and count > 0:
                        _temperature = min(self.sg_temperature + 0.1, 1.0)
                    else:
                        _temperature = self.sg_temperature
                    solution = get_chat_response(messages, self.api_key, self.sg_engine, _temperature, self.sg_max_tokens)
                    # parse the solution to obtain probabilities
                    try:
                        # in the form of {0: 0.500, 1: 0.500, ...}, safe when empty dict,
                        # however, not safe when probs not sum to 1, we will normalize it later
                        option_prob_dict_curr = extract_option_prob_from_solution(solution, len(self.cache["example"]["choices"]))
                    except Exception as e:
                        print("Failed to obtain the option probabilities from the solution. Retrying...")
                        count += 1
                        continue
                    pattern = re.compile(r"[Tt]he answer is ([A-Z])")  # "The answer is XXXXX.",
                    res = pattern.findall(solution)
                    if len(res) > 0:
                        # normalize the probabilities (round to maximum 3 decimal places) if not sum to 1
                        option_prob_dict_curr = normalize_dict(option_prob_dict_curr)
                        # process the probability dictionary, summing
                        if option_prob_dict is None:
                            # for the first successful sampling
                            option_prob_dict = option_prob_dict_curr
                        else:
                            # add current probabilities to the existing dictionary, key by key
                            for key in option_prob_dict:
                                option_prob_dict[key] += option_prob_dict_curr[key]
                        # change flag when all good, proceed to the next sampling
                        success = True
                    count += 1
                if count >= patience:
                    print(solution)
                    raise Exception("ERROR: out-of-patience")
            # after the sampling is done, we need to divide the sum by the number of samplings
            # (round to maximum 3 decimal places)
            option_prob_dict = {_key: round(_value / num_sampling, 3) for _key, _value in option_prob_dict.items()}
            # for higher safety, normalize the probabilities (round to maximum 3 decimal places) if not sum to 1
            option_prob_dict = normalize_dict(option_prob_dict)
            self.cache["bcot_option_prob_dict"] = option_prob_dict
            # assign the self.cache["bcot_sampled_solution"] to the highest probability option
            # for example, if option_prob_dict = {0: 0.500, 1: 0.500}, then the highest probability option is 0
            # then you should assign self.cache["bcot_sampled_solution"] = "The answer is A."

            # # TODO: this selects the first highest option given the set of highest options
            # # Find the key with the highest probability
            # highest_prob_key = max(option_prob_dict, key=option_prob_dict.get)
            # # Map the key to an option letter (A, B, C, ...)
            # # The ASCII code of 'A' is 65, so we add the key to 65 to get the corresponding letter
            # option_letter = chr(65 + highest_prob_key)

            # TODO: this selects a random option among the set of highest options
            # Find the highest probability value
            _max_prob = max(option_prob_dict.values())
            # Filter options that have the highest probability
            _max_prob_options = [_option for _option, _prob in option_prob_dict.items() if _prob == _max_prob]
            # Randomly select one option if there's more than one
            _selected_option = random.choice(_max_prob_options)
            # Map the selected option to A, B, C, D, etc.
            # Assuming options are 0-indexed, we add 65 (ASCII value of 'A') to get the letter representation
            option_letter = chr(_selected_option + 65)

            # Assign the result to the cache
            self.cache["bcot_sampled_solution"] = f"{option_letter}"
        else:
            _prob = None
            success = False
            count = 0
            while count < patience and not success:
                if self.sg_temperature < 0.1 and count > 0:
                    _temperature = min(self.sg_temperature + 0.1, 1.0)
                else:
                    _temperature = self.sg_temperature
                solution = get_chat_response(messages, self.api_key, self.sg_engine, _temperature, self.sg_max_tokens)
                # parse the solution to obtain probabilities
                try:
                    # TODO: implement this
                    # find the "Probability: value" section in the solution, then get the numerical value and save it
                    _pattern = re.compile(r"[Pp]robability: ([0-9.]+)")
                    _res = _pattern.findall(solution)
                    if len(_res) > 0:
                        _prob = _res[0]
                        _prob = float(_prob)
                    else:
                        raise Exception("ERROR: failed to obtain the option probabilities from the solution, "
                                        "no probability found")
                except Exception as e:
                    if count >= patience:
                        raise Exception("ERROR: failed to obtain the option probabilities from the solution, "
                                        "out-of-patience")
                    print(solution)
                    print("Failed to obtain the option probabilities from the solution. Retrying...")
                    count += 1
                    continue
                pattern = re.compile(r"[Tt]he answer is ([A-Z])")  # "The answer is XXXXX.",
                res = pattern.findall(solution)
                if len(res) > 0:
                    success = True
                count += 1
            if count >= patience:
                print(solution)
                raise Exception("ERROR: out-of-patience")
            self.cache["option_prob"] = _prob

        # update the cache
        self.cache["solution"] = solution
        self.cache["solution_generator:input"] = test_prompt
        self.cache["solution_generator:output"] = solution

        return test_prompt, solution
    
    def answer_generator(self):
        # get the module input
        output = self.cache["solution"]
        options = self.cache["example"]["choices"]
        inds = ["A", "B", "C", "D", "E"]

        # excute the module
        if self.model in ["io", "cot", "chameleon"]:
            success = False
            if output:
                pattern = re.compile(r"[Tt]he answer is ([A-Z])") # "The answer is A.",
                res = pattern.findall(output)
                if len(res) > 0:
                    ans = res[0] # "A"
                    if ans in inds[:len(options)]:
                        success = True
                        prediction = options[inds.index(ans)]
            if not success:
                prediction = normalize_prediction_scienceqa(output, options)
        elif self.model in ["bcot-ticoh-s"]:
            ans = self.cache["bcot_sampled_solution"]
            prediction = options[inds.index(ans)]
        else:
            raise Exception("ERROR: answer_generator(self), invalid model name " + self.model)

        # update the cache
        # in BCoT, self.cache["prediction"] and self.cache["answer_generator:output"] are the same
        # however, in BCoT, self.cache["answer_generator:input"] may be different from
        # self.cache["solution_generator:output"] and self.cache["prediction"] because
        # self.cache["answer_generator:input"] only records the last sampling result,
        # hence we ignore self.cache["answer_generator:input"] in BCoT
        self.cache["prediction"] = prediction
        self.cache["answer_generator:input"] = output
        self.cache["answer_generator:output"] = prediction
        return output, prediction


def extract_option_prob_from_solution(text, num_options):
    """
    Return text as:
    P(Z3_{Option A} | Z2)=0.100\nP(Z3_{Option B} | Z2)=0.900\n
    Then parse the text into a dictionary: {opt idx: probability, ...}
    :param text: solution
    :return: dictionary
    """
    lines = text.split('\n')  # Split the text into individual lines
    probabilities_start = None
    probabilities_end = None

    # Find the line numbers for "Probabilities:" and "Conclusion:"
    for i, line in enumerate(lines):
        if "Probabilities:" in line:
            probabilities_start = i + 1  # Start capturing from the next line
        if "Conclusion:" in line:
            probabilities_end = i  # Stop capturing at this line
            break  # No need to continue searching

    # Extract the lines between "Probabilities:" and "Conclusion:"
    if probabilities_start is not None and probabilities_end is not None:
        probability_lines = lines[probabilities_start:probabilities_end]
        probabilities_info = "\n".join(probability_lines)
    else:
        raise Exception("ERROR: extract_option_prob_from_solution(text), None starting / ending")

    def parse_text_to_dict(_text):
        # Split the text into lines
        _lines = _text.strip().split('\n')
        # Create a dictionary with the extracted values
        _created_dict = {_i: float(_line.split('=')[1]) for _i, _line in enumerate(_lines)}

        return _created_dict

    probabilities_info = parse_text_to_dict(probabilities_info)
    # check if probabilities_info is empty
    if len(probabilities_info) == 0:
        raise Exception("ERROR: extract_option_prob_from_solution(text), empty dict")
    # check number of options
    elif len(probabilities_info) != num_options:
        raise Exception("ERROR: extract_option_prob_from_solution(text), options mismatch")

    return probabilities_info


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
