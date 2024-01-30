# Input-output (IO)
prompt_io = """
Given the question (and the context), directly select the answer from the options ["A", "B", "C", "D", "E"] without explicit reasoning. You must conclude the answer in the format of "the answer is [ANSWER]", where [ANSWER] is one from the options ["A", "B", "C", "D", "E"]. For example, "the answer is A", "the answer is B", "the answer is C", "the answer is D", or "the answer is E". If the answer is not in the options, select one random letter option from ["A", "B", "C", "D", "E"]. Then you need to provide a numerical probability with 3 decimal places for the answer, which is a number between 0.000 and 1.000, where 0.000 means the answer is impossible and 1.000 means the answer is certain.


For example:
Question: Select the one substance that is not a mineral.

Context: Select the better answer.

Options: (A) turtle shell is not a pure substance. It is made by a living thing (B) Celestine is a pure substance. It is a solid. (C) Hematite is not made by living things. It is a solid.

Solution:
The answer is A.
Probability: 0.980


For another example:
Question: Which property do these two objects have in common?

Context: Select the better answer. Image: A pair of scissors next to a pair of scissors.

Options: (A) hard (B) bendable

Solution:
The answer is B.
Probability: 0.950
"""


# cot
prompt_cot = """
Given the question (and the context), select the answer from the options ["A", "B", "C", "D", "E"]. You should give consice and step-by-step solutions. Finally, conclude the answer in the format of "the answer is [ANSWER]", where [ANSWER] is one from the options ["A", "B", "C", "D", "E"]. For example, "the answer is A", "the answer is B", "the answer is C", "the answer is D", or "the answer is E". If the answer is not in the options, select the most possible option. Then you need to provide a numerical probability with 3 decimal places for the answer, which is a number between 0.000 and 1.000, where 0.000 means the answer is impossible and 1.000 means the answer is certain.

Question: Which property do these two objects have in common?

Context: Select the better answer. Image: A pair of scissors next to a pair of scissors.

Options: (A) hard (B) bendable

Solution: An object has different properties. A property of an object can tell you how it looks, feels, tastes, or smells.\nDifferent objects can have the same properties. You can use these properties to put objects into groups. Look at each object.\nFor each object, decide if it has that property.\nA bendable object can be bent without breaking. Both objects are bendable.\nA hard object keeps its shape when you squeeze it. The rubber gloves are not hard.\nThe property that both objects have in common is bendable.
Therefore, the answer is B.
Probability: 0.925

Question: Select the one substance that is not a mineral.

Context: Select the better answer.

Options: (A) turtle shell is not a pure substance. It is made by a living thing (B) Celestine is a pure substance. It is a solid. (C) Hematite is not made by living things. It is a solid.

Solution: Compare the properties of each substance to the properties of minerals. Select the substance whose properties do not match those of minerals.\nA turtle shell is made by a living thing. But minerals are not made by living things.\nA turtle shell is not a pure substance. But all minerals are pure substances.\nSo, a turtle shell is not a mineral.\nCelestine is a mineral.\nHematite is a mineral.
Therefore, the answer is A.
Probability: 0.960


In case the answer cannot be determined or no image provided and no additional context or information given, you must always select exactly one random answer and must strictly follow the format:
Therefore, the answer is [OPTION] from random selection.\nProbability: [3 decimal places float ranging 0 to 1]
"""


# chameleon ICL based on GPT-4, enhanced stability on ScienceQA-4241, ScienceQA-3568, and ScienceQA-100
prompt_chameleon = """
Given the question (and the context), select the answer from the options ["A", "B", "C", "D", "E"]. You should give consice and step-by-step solutions. Finally, conclude the answer in the format of "the answer is [OPTION]", where [OPTION] is one from the options ["A", "B", "C", "D", "E"]. For example, "the answer is A", "the answer is B", "the answer is C", "the answer is D", or "the answer is E". If the answer is not in the options or more than one correct answer, select the most possible option. Then you need to provide a numerical probability with 3 decimal places for the answer, for example "Probability: 0.900", which is a number between 0.000 and 1.000, where 0.000 means the answer is impossible and 1.000 means the answer is certain. In case more than one answer or the answer cannot be determined or no image provided and no additional context or information given, you must always fill the [OPTION] with exactly one option from options provided and must strictly follow the format:
Therefore, the answer is [OPTION] from random selection.\nProbability: [3 decimal places float ranging 0 to 1]

Question: Which property do these two objects have in common?

Context: Select the better answer.

Options: (A) hard (B) bendable

Metadata: {'pid': 6493, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}

Image caption: A pair of scissors next to a pair of scissors.

Detected text with coordinates in the image: [([[53, 185], [121, 185], [121, 199], [53, 199]], 'jump rope'), ([[233, 183], [323, 183], [323, 201], [233, 201]], 'rubber gloves')] 

Retrieved knowledge: 
- This question is about comparing the properties of two objects: rubber gloves and rain boots.
- The objects are related to the topic of physics and the skill of comparing properties of objects.
- Properties of objects can include physical characteristics such as color, texture, shape, size, weight, and material. In this case, the two objects have the property of being bendable in common.

Bing search response: The most common materials used for disposable gloves are Latex, Vinyl and Nitrile. Each material has its benefits and drawbacks. Latex Gloves are constructed from Natural Rubber Latex and are the most popular type of disposable glove.

Solution: 
Given the objects in the question are a jump rope and rubber gloves, we need to compare their properties and determine whether they are more likely to be "hard" or "bendable."
- Jump Rope: A jump rope is typically made from materials like PVC, leather, or nylon. These materials are chosen for their durability and flexibility, allowing the rope to bend and flex as it's swung and used for jumping. This indicates that a jump rope is bendable.
- Rubber Gloves: Rubber gloves are usually made from materials like latex, nitrile, or vinyl. These materials are chosen for their flexibility and ability to provide a snug fit while allowing the hands to move freely. This means rubber gloves are also designed to be bendable.
Comparing these properties, it's evident that both objects, a jump rope and rubber gloves, are designed to be flexible or bendable rather than hard.
Given options: (A) (B)
Therefore, the answer is B (bendable).
Probability: 0.925


Question: Select the one substance that is not a mineral.

Context: Select the better answer.

Options: (A) turtle shell is not a pure substance. It is made by a living thing (B) Celestine is a pure substance. It is a solid. (C) Hematite is not made by living things. It is a solid.

Metadata: {'pid': 16241, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}

Bing search response: A nonmineral is a substance found in a natural environment that does not satisfy the definition of a mineral and is not even a mineraloid. Many nonminerals are mined and have industrial or other uses similar to minerals, such as jewelry.

Retrieved knowledge:
- Minerals are naturally occurring, inorganic solids that have a definite chemical composition and a crystalline structure.
- Minerals are formed by geological processes and can be found in rocks, soils, and bodies of water.
- Turtle shells, celestine, and hematite are all solid substances, but turtle shells are not minerals because they are made by living things.

Solution:
Given the descriptions of the substances and the definition of a mineral, we can analyze each option:
- Turtle Shell (A): Turtle shells are indeed made by living things (turtles), specifically from their bone and keratin. This characteristic disqualifies turtle shells from being considered a mineral, as minerals are inorganic and not made by living organisms.
- Celestine (B): Celestine, also known as Celestite, is a mineral composed of strontium sulfate. It is a naturally occurring, inorganic solid with a definite chemical composition and crystalline structure, fitting the definition of a mineral.
- Hematite (C): Hematite is an iron oxide and is one of the main sources of iron. It is a naturally occurring, inorganic solid with a definite chemical composition and crystalline structure. It is not made by living things, fitting the definition of a mineral.
Comparing these options with the definition of a mineral, it's clear that the turtle shell is not a mineral because it is organic and made by a living thing.
Given options: (A) (B)
Therefore, the answer is A (turtle shell).
Probability: 0.960


In the end you must conclude the answer in the format of "the answer is [OPTION]", where [OPTION] is one from the "Given options". For example, "the answer is A", "the answer is B", "the answer is C", "the answer is D", or "the answer is E".
If more than one correct answer, you must force yourself to select only one most possible option:
Therefore, the answer is [OPTION] from random selection.\nProbability: [3 decimal places float ranging 0 to 1]
If the answer is not in the options, you must randomly select only one option. Then you need to provide a numerical probability with 3 decimal places for the answer, for example "Probability: 0.900", which is a number between 0.000 and 1.000, where 0.000 means the answer is impossible and 1.000 means the answer is certain. In case more than one answer or the answer cannot be determined or no image provided and no additional context or information given, you must always fill the [OPTION] with exactly one option from options provided and must strictly follow the format:
Therefore, the answer is [OPTION] from random selection.\nProbability: [3 decimal places float ranging 0 to 1]
"""


# BCoT-TICoh prompt large version
prompt_bcot_ticoh_l = """
We have a science question that requires a careful analysis to identify the correct answer. The decision-making process is structured into a series of steps, each focusing on specific aspects of the information provided. Let's approach this systematically:

Assess Knowledge Relevance (Z1):
- Question: [Insert Question]
- Context: [Insert Context]
- Retrieved Knowledge: [Insert Retrieved Knowledge]
- Bing Search Response: [Insert Bing Search Response]
- Detected Text: [Insert Detected Text]
Based on these inputs, evaluate the relevance of each piece of information to the question. You must provide a detailed step-by-step description that reflects your evaluation.  Assign a relevance score with 3 decimal places from 0 to 1 for each, where 1 indicates highly relevant.

Analyze Text-Image Coherence (Z2):
- Image Caption: [Insert Image Caption]
- Detected Text: [Insert Detected Text]
- Relevance Scores: [Insert Relevance Scores from Z1]
Analyze the coherence between the image caption and the detected text. Consider the relevance scores from Z1 in your analysis. Is there a significant discrepancy or a strong coherence? Provide a coherence score from 0 to 1, where 1 indicates strong coherence.

Evaluate and Compare Answer Options (Z3):
- Answer Options: [Insert Answer Options]
- Information from Z1 and Z2: [Summarize the key information from Z1 and Z2]
Compare each answer option against the question and the context, using the information evaluated in Z1 and Z2. Discuss the strengths and weaknesses of each option and how they relate to the provided information.

Construct Reasoning Pathway (Z4):
Based on the evaluations from Z3, construct a detailed reasoning pathway for each answer option. This should be a logical sequence of thoughts that leads to a conclusion about each option's validity. You must provide the reasoning pathway as text as detailed as possible, do not take anything as guaranteed, you must explain every claim you make.

Make a Decision with Confidence (Z5):
Integrate the evaluations and reasoning from Z1 to Z4. For each answer option, provide a probability with 3 decimal places that represents your confidence in the option being correct. Ensure that the probabilities sum up to 1.

Proceed with the analysis, ensuring that each step is logically derived from the provided information and the outcomes of the preceding steps. Finally, conclude the answer in the form of "The answer is <correct option> with numerical probability <numerical probability>", for example, "The answer is A with numerical probability 0.85" or "The answer is B with numerical probability 0.9".

Consider the following examples:

Example 1:
Question: Which property do these two objects have in common?

Context: Select the better answer.

Options: (A) hard (B) bendable

Metadata: {'pid': 6493, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}

Image caption: A pair of scissors next to a pair of scissors.

Detected text with coordinates in the image: [([[53, 185], [121, 185], [121, 199], [53, 199]], 'jump rope'), ([[233, 183], [323, 183], [323, 201], [233, 201]], 'rubber gloves')] 

Retrieved knowledge: 
- This question is about comparing the properties of two objects: a jump rope and rubber gloves.
- The focus is on the topic of physics under the category of Materials, specifically addressing the skill of comparing properties of objects in Grade 2.
- Properties of materials commonly compared in this context include physical characteristics such as hardness and flexibility.
- A jump rope is typically made of materials that are flexible and bendable to allow for the ease of movement and looping during use.
- Rubber gloves are made from materials that are also flexible and bendable, designed to fit comfortably over the hands while providing protection and maintaining dexterity.
- Understanding the characteristics of hardness and bendability can help in determining the common property between these two objects. Hardness relates to the resistance of a material to deformation or indentation, while bendability refers to the material's capacity to bend without breaking.

Bing search response: The most common materials used for disposable gloves are Latex, Vinyl and Nitrile. Each material has its benefits and drawbacks. Latex Gloves are constructed from Natural Rubber Latex and are the most popular type of disposable glove.

Solution:
Assess Knowledge Relevance (Z1):
Inputs:
1. Question: Which property do these two objects have in common?
2. Context: Select the better answer.
3. Retrieved Knowledge: The question pertains to comparing properties of two objects, focusing on physical characteristics such as hardness and flexibility. A jump rope is bendable, while rubber gloves are made from materials that are also flexible and bendable.
4. Bing Search Response: Common materials for disposable gloves include Latex, Vinyl, and Nitrile, highlighting that they are made from materials that have certain degrees of flexibility.
Evaluation:
- Question Relevance: The question directly asks to identify a common property between the two given objects (jump rope and rubber gloves).
- Context Relevance: The context focuses on comparing two options: hard and bendable, which aligns with the comparison of physical characteristics of the objects.
- Retrieved Knowledge Relevance: The retrieved knowledge provides insight into the physical properties of the objects in question, aligning closely with the context and the question's requirement.
- Bing Search Response Relevance: The response provides details about the materials of one of the objects (rubber gloves), which is relevant for understanding their properties.
Relevance Scores:
- Question: 0.991 (directly addresses the requirement)
- Context: 0.989 (directly related to the options provided)
- Retrieved Knowledge: 0.968 (provides necessary information about the properties of the objects)
- Bing Search Response: 0.792 (useful for understanding the properties of rubber gloves)

Analyze Text-Image Coherence (Z2):
Inputs:
- Image Caption: A pair of scissors next to a pair of scissors.
- Detected Text: 'jump rope' and 'rubber gloves'
Relevance Scores from Z1: [0.991, 0.989, 0.968, 0.792]
Analysis:
The image caption does not match the detected text, which mentions 'jump rope' and 'rubber gloves'. This discrepancy suggests an issue either with the image caption or the text detection. However, the relevance scores from Z1 indicate that the information about 'jump rope' and 'rubber gloves' is highly relevant to the question.
Coherence Score:
Score: 0.185 (significant discrepancy between the image caption and detected text, but the detected text is relevant to the question)

Evaluate and Compare Answer Options (Z3):
Answer Options:
- (A) hard
- (B) bendable
Information from Z1 and Z2:
- The question and context focus on identifying a common property between a jump rope and rubber gloves.
- Retrieved knowledge and search response suggest that both objects are characterized by flexibility and bendability.
Evaluation:
- Option A (hard): Neither a jump rope nor rubber gloves are typically characterized as 'hard'. This option does not align well with the retrieved knowledge or the bing search response.
- Option B (bendable): Both a jump rope and rubber gloves are described as flexible and bendable, aligning well with the retrieved knowledge and the bing search response.
Strengths and Weaknesses:
- Strength of Option B: Direct alignment with the retrieved knowledge and bing search response about the properties of the objects.
- Weakness of Option A: Does not correlate with the known properties of the objects in question.

Construct Reasoning Pathway (Z4):
For Option A (hard):
- Step 1: Assess the properties of a jump rope and rubber gloves.
- Step 2: Compare these properties with the characteristic 'hard'.
- Step 3: Conclude that 'hard' does not align with the known properties of flexibility and bendability for both objects.
For Option B (bendable):
- Step 1: Assess the properties of a jump rope and rubber gloves.
- Step 2: Compare these properties with the characteristic 'bendable'.
- Step 3: Conclude that 'bendable' aligns well with the known properties of both objects, indicating it is the common property.

Make a Decision with Confidence (Z5):
- For Option A (hard): Probability = 0.094 (Low probability due to misalignment with known properties of the objects)
- For Option B (bendable): Probability = 0.906 (High probability due to strong alignment with known properties of the objects)

Based on the comprehensive analysis, the decision is:
The answer is B (bendable) with numerical probability 0.906.


Example 2:
Question: Select the one substance that is not a mineral.

Context: Select the better answer.

Options: (A) turtle shell is not a pure substance. It is made by a living thing (B) Celestine is a pure substance. It is a solid. (C) Hematite is not made by living things. It is a solid.

Metadata: {'pid': 16241, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}

Bing search response: A nonmineral is a substance found in a natural environment that does not satisfy the definition of a mineral and is not even a mineraloid. Many nonminerals are mined and have industrial or other uses similar to minerals, such as jewelry.

Retrieved knowledge:
- This question involves the concept of minerals and how to distinguish them from non-mineral substances based on specific criteria.
- Minerals are naturally occurring, inorganic substances with a definite chemical composition and a crystalline structure. They are not made by living organisms.
- The question is part of a Grade 2 natural science curriculum, focusing on the topic of physics under the category of Materials, specifically addressing the skill of comparing properties of objects.
- Understanding the nature of minerals involves recognizing certain key characteristics: they are inorganic, solid, have a definite chemical composition, and a crystalline structure.
- Turtle shells are organic in nature, made by living organisms, specifically turtles. They are composed of substances like keratin and do not fit the criteria for being a mineral.
- Celestine (also known as celestite) is a mineral composed primarily of strontium sulfate. It is inorganic, naturally occurring, and crystalline.
- Hematite is an iron oxide and is a common mineral. It is inorganic, naturally occurring, and has a crystalline structure.
- Comparing these properties can help in determining which substance does not meet the criteria to be classified as a mineral.

Solution:
Assess Knowledge Relevance (Z1):
Inputs:
1. Question: Select the one substance that is not a mineral.
2. Context: Select the better answer.
3. Retrieved Knowledge: Key characteristics of minerals include being inorganic, solid, having a definite chemical composition, and a crystalline structure. Turtle shells are organic, Celestine and Hematite are inorganic and meet the criteria for minerals.
4. Bing Search Response: Defines nonminerals as substances that do not satisfy the definition of a mineral, sometimes used similarly to minerals.
Evaluation:
- Question Relevance: The question directly asks to identify the substance that is not a mineral.
- Context Relevance: The context provides a clear choice between three options, focusing on distinguishing characteristics relevant to mineral classification.
- Retrieved Knowledge Relevance: Provides detailed information about what constitutes a mineral and the nature of the given substances, aligning closely with the context and the question's requirement.
- Bing Search Response Relevance: Provides a general definition of nonminerals, supplementing the understanding of what does not constitute a mineral.
Relevance Scores:
- Question: 1.0 (directly addresses the requirement)
- Context: 1.0 (provides clear options for comparison)
- Retrieved Knowledge: 1.0 (offers crucial information for making the distinction)
- Bing Search Response: 0.7 (useful but less specific than the retrieved knowledge)
Analyze Text-Image Coherence (Z2):
Since there is no mention of specific image content or detected text in the inputs provided for this question, this step will not be applicable for the current analysis. We will proceed based on the relevance scores from Z1 and the provided information.
Coherence Score:
- Score: N/A (no image content or detected text provided)

Evaluate and Compare Answer Options (Z3):
Answer Options:
- (A) Turtle shell is not a pure substance. It is made by a living thing.
- (B) Celestine is a pure substance. It is a solid.
- (C) Hematite is not made by living things. It is a solid.
Information from Z1:
- Minerals are inorganic, not made by living things, solid, and have a specific crystalline structure.
- Turtle shells are organic and made by living things.
- Celestine and Hematite meet the criteria for being minerals.
Evaluation:
- Option A (Turtle shell): Matches the criteria for a nonmineral as it is made by a living thing (organic).
- Option B (Celestine): Does not match the criteria for a nonmineral as it is an inorganic and solid substance with a crystalline structure.
- Option C (Hematite): Does not match the criteria for a nonmineral as it is an inorganic and solid substance with a crystalline structure.
Strengths and Weaknesses:
- Strength of Option A: Directly aligns with the key characteristic of nonminerals (being organic or made by living things).
- Weakness of Options B and C: Both are inorganic and meet the criteria for being classified as minerals.

Construct Reasoning Pathway (Z4):
For Option A (Turtle shell):
- Step 1: Identify the defining characteristics of a mineral.
- Step 2: Assess that turtle shells are made by living organisms and are organic.
- Step 3: Conclude that turtle shells do not meet the criteria for being a mineral.
For Options B (Celestine) and C (Hematite):
- Step 1: Identify the defining characteristics of a mineral.
- Step 2: Recognize that both Celestine and Hematite are inorganic, solid, and have a crystalline structure.
- Step 3: Conclude that both Celestine and Hematite meet the criteria for being classified as minerals.

Make a Decision with Confidence (Z5):
- For Option A (Turtle shell): Probability = 0.9 (High probability due to alignment with nonmineral characteristics)
- For Options B (Celestine): Probability = 0.05 (Low probability due to alignment with mineral characteristics)
- For Options C (Hematite): Probability = 0.05 (Low probability due to alignment with mineral characteristics)

Based on the comprehensive analysis, the decision is:
The answer is A (Turtle shell is not a pure substance. It is made by a living thing) with numerical probability 0.9.
"""


# # BCoT-TICoh prompt for ScienceQA-100
# prompt_bcot_ticoh_s = """
# We have a science question that requires a careful analysis to identify the correct answer. The decision-making process is structured into a series of steps, each focusing on specific aspects of the information provided. Let's approach this systematically:
#
# Understanding Knowledge and Context (Variable Z1):
# - Start by analyzing the question and the provided context. What is the main topic, and what specific knowledge does it require? Consider the retrieved knowledge and the Bing search response. What essential information do these sources provide?
# - Calculate the probability of Z1 capturing the essential knowledge and context required for solving the question. Use the formula: P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response).
#
# Analyzing Textual and Visual Information (Variable Z2):
# - Examine the detected text in the image and the image caption. What are the key pieces of information each source provides? Are there any discrepancies between them?
# - Estimate the probability of Z2 accurately reflecting the meaning difference between detected text and image caption, and deciding the weightage of each based on the discrepancy. Use the formula: P(Z2 | Z1, Detected Text, Image Caption).
#
# Make a Decision with Confidence (Variable Z3):
# - Integrate the evaluations and reasoning from Z1 to Z2. For each answer option, provide a probability that represents your confidence in the option being correct. Ensure that the probabilities sum up to 1.
# - Proceed with the analysis, ensuring that each variable is logically derived from the provided information and the outcomes of the depending variables.
#
# Finally, you must conclude exact one answer in the form of "The answer is <correct option> with numerical probability of <correct option’s numerical probability with 3 decimal places>", for example, "The answer is A with numerical probability of 0.852" or "The answer is B with numerical probability of 0.904". Note that all probabilities you calculated should be in 3 decimal places, and you should make the reasoning of Bayesian inference be more concise. If you encountered more than one option with the same highest probability, you should randomly select one with the highest probability.
#
#
# Consider the following examples:
# Example 1:
# Question: Which property do these two objects have in common?
#
# Context: Select the better answer.
#
# Options: (A) hard (B) bendable
#
# Metadata: {'pid': 6493, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}
#
# Image caption: A pair of scissors next to a pair of scissors.
#
# Detected text with coordinates in the image: [([[53, 185], [121, 185], [121, 199], [53, 199]], 'jump rope'), ([[233, 183], [323, 183], [323, 201], [233, 201]], 'rubber gloves')]
#
# Retrieved knowledge:
# - This question is about comparing the properties of two objects: rubber gloves and rain boots.
# - The objects are related to the topic of physics and the skill of comparing properties of objects.
# - Properties of objects can include physical characteristics such as color, texture, shape, size, weight, and material. In this case, the two objects have the property of being bendable in common.
#
# Bing search response: The most common materials used for disposable gloves are Latex, Vinyl and Nitrile. Each material has its benefits and drawbacks. Latex Gloves are constructed from Natural Rubber Latex and are the most popular type of disposable glove.
#
# Solution:
# Understanding Knowledge and Context (Variable Z1)
# Analysis:
# - Main Topic: Comparing the physical properties of two objects.
# - Specific Knowledge Required: Knowledge of the material and properties of the objects mentioned: rubber gloves and jump rope.
# - Contextual Discrepancy: There's a discrepancy between the metadata (mentioning rubber gloves and rain boots) and the detected text in the image (mentioning jump rope and rubber gloves). However, the image caption refers to a pair of scissors, which is not relevant to the objects in the detected text or the context provided. This inconsistency needs to be addressed.
# - Retrieved Knowledge & Bing Search Response: Focus on material properties, especially the bendability of materials like rubber (common in gloves).
# Given the inconsistencies in the provided information and the focus on material properties, especially bendability, the probability of Z1 capturing the essential knowledge and context accurately is moderately high, considering the clear information about rubber gloves but ambiguous information about the second object (jump rope vs. rain boots).
# Probability:
# P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response)=0.700
#
# Analyzing Textual and Visual Information (Variable Z2)
# Analysis:
# - Detected Text: Refers to a 'jump rope' and 'rubber gloves'.
# Image Caption: Mentions a 'pair of scissors', which is inconsistent with the detected text and the context.
# - Discrepancy: There's a significant discrepancy between the detected text and the image caption. The decision should weigh more on the detected text as it aligns better with the retrieved knowledge about rubber gloves.
# Given the alignment of detected text with the retrieved knowledge and the notable discrepancy with the image caption, the probability of Z2 accurately reflecting the meaning difference and assigning appropriate weightage is relatively high.
# Probability:
# P(Z2 | Z1,Detected Text, Image Caption)=0.800
#
# Make a Decision with Confidence (Variable Z3)
# Analysis:
# - Option A (hard): Not strongly supported. Rubber gloves are known for their flexibility, not hardness. The property of a jump rope (if considered) also aligns more with flexibility than hardness.
# - Option B (bendable): Strongly supported. Both rubber gloves and jump ropes (assuming the jump rope is the second object) are known for their bendable nature.
# Given the analysis and considering the higher weightage of the detected text (rubber gloves and jump rope) which supports the bendability of the objects, the confidence in each option being correct is as follows, and we need to ensure that these probabilities sum up to 1:
# Probabilities:
# P(Z3_{Option A} | Z2)=0.100
# P(Z3_{Option B} | Z2)=0.900
#
# Conclusion:
# The answer is B with a numerical probability of 0.900.
#
#
# Example 2:
# Question: Select the one substance that is not a mineral.
#
# Context: Select the better answer.
#
# Options: (A) turtle shell is not a pure substance. It is made by a living thing (B) Celestine is a pure substance. It is a solid. (C) Hematite is not made by living things. It is a solid.
#
# Metadata: {'pid': 16241, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}
#
# Bing search response: A nonmineral is a substance found in a natural environment that does not satisfy the definition of a mineral and is not even a mineraloid. Many nonminerals are mined and have industrial or other uses similar to minerals, such as jewelry.
#
# Retrieved knowledge:
# - This question involves the concept of minerals and how to distinguish them from non-mineral substances based on specific criteria.
# - Minerals are naturally occurring, inorganic substances with a definite chemical composition and a crystalline structure. They are not made by living organisms.
# - The question is part of a Grade 2 natural science curriculum, focusing on the topic of physics under the category of Materials, specifically addressing the skill of comparing properties of objects.
# - Understanding the nature of minerals involves recognizing certain key characteristics: they are inorganic, solid, have a definite chemical composition, and a crystalline structure.
# - Turtle shells are organic in nature, made by living organisms, specifically turtles. They are composed of substances like keratin and do not fit the criteria for being a mineral.
# - Celestine (also known as celestite) is a mineral composed primarily of strontium sulfate. It is inorganic, naturally occurring, and crystalline.
# - Hematite is an iron oxide and is a common mineral. It is inorganic, naturally occurring, and has a crystalline structure.
# - Comparing these properties can help in determining which substance does not meet the criteria to be classified as a mineral.
#
# Solution:
# Understanding Knowledge and Context (Variable Z1)
# Analysis:
# - Main Topic: Identification of substances as minerals or non-minerals.
# - Specific Knowledge Required: Understanding the characteristics of minerals: inorganic, naturally occurring, definite chemical composition, and crystalline structure. Minerals are not made by living organisms.
# - Contextual Information: The context provides insights into the nature of turtle shell, celestine, and hematite, relating them to the criteria of minerals.
# - Retrieved Knowledge & Bing Search Response: Emphasizes the distinction between minerals and non-minerals, especially highlighting the organic vs. inorganic origin.
# - Given the clarity in the definition of minerals and the distinct characteristics of each substance mentioned, the probability of Z1 capturing the essential knowledge and context accurately is high.
# Probability:
# P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response)=0.950
#
# Analyzing Textual and Visual Information (Variable Z2)
# For this question, there's no textual or visual information from an image to analyze, so Z2 is not applicable in this scenario. We proceed directly to Z3, integrating the understanding of the concept of minerals with the specifics of each substance mentioned.
#
# Make a Decision with Confidence (Variable Z3)
# Analysis:
# - Option A (turtle shell): Strongly supported. Turtle shells are organic and made by living organisms, which does not align with the definition of minerals.
# - Option B (Celestine): Not supported. Celestine meets the criteria for being a mineral: inorganic, naturally occurring, solid, and crystalline.
# - Option C (Hematite): Not supported. Hematite meets the criteria for being a mineral: inorganic, naturally occurring, solid, and crystalline.
# Considering the clear definition of minerals and the nature of each substance, and we need to ensure that these probabilities sum up to 1:
# Probabilities:
# P(Z3_{Option A} | Z1)=0.950
# P(Z3_{Option B} | Z1)=0.025
# P(Z3_{Option C} | Z1)=0.025
#
# Conclusion:
# The answer is A with a numerical probability of 0.950.
#
#
# IMPORTANT: If there are more than one option with the same highest probability, you must randomly select one with the highest probability and strictly follow the format of "The answer is <correct option> with numerical probability of <correct option’s numerical probability with 3 decimal places>", for example, "The answer is A with numerical probability of 0.852" or "The answer is B with numerical probability of 0.904".
# """


# BCoT-TICoh prompt small version for enhanced stability on ScienceQA-4241 and ScienceQA-3568
prompt_bcot_ticoh_s = """
We have a science question that requires a careful analysis to identify the correct answer. The decision-making process is structured into a series of steps, each focusing on specific aspects of the information provided. Let's approach this systematically:

Understanding Knowledge and Context (Variable Z1):
- Start by analyzing the question and the provided context. What is the main topic, and what specific knowledge does it require? Consider the retrieved knowledge and the Bing search response. What essential information do these sources provide?
- Calculate the probability of Z1 capturing the essential knowledge and context required for solving the question. Use the formula: P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response).

Analyzing Textual and Visual Information (Variable Z2):
- Examine the detected text in the image and the image caption. What are the key pieces of information each source provides? Are there any discrepancies between them?
- Estimate the probability of Z2 accurately reflecting the meaning difference between detected text and image caption, and deciding the weightage of each based on the discrepancy. Use the formula: P(Z2 | Z1, Detected Text, Image Caption).

Make a Decision with Confidence (Variable Z3):
- Integrate the evaluations and reasoning from Z1 to Z2. For each answer option, provide a probability that represents your confidence in the option being correct. Ensure the probabilities sum up to 1.
- Proceed with the analysis, ensuring that each variable is logically derived from the provided information and the outcomes of the depending variables. 

Finally, you must conclude exact one answer in the form of "The answer is <correct option> with numerical probability of <correct option’s numerical probability with 3 decimal places>", for example, "The answer is A with numerical probability of 0.852" or "The answer is B with numerical probability of 0.904". Note that all probabilities you calculated should be in 3 decimal places, and you should make the reasoning of Bayesian inference be more concise. If you encountered more than one option with the same highest probability, you should randomly select one with the highest probability.


Consider the following examples:
Example 1:
Question: Which property do these two objects have in common?

Context: Select the better answer.

Options: (A) hard (B) bendable

Metadata: {'pid': 6493, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}

Image caption: A pair of scissors next to a pair of scissors.

Detected text with coordinates in the image: [([[53, 185], [121, 185], [121, 199], [53, 199]], 'jump rope'), ([[233, 183], [323, 183], [323, 201], [233, 201]], 'rubber gloves')] 

Retrieved knowledge: 
- This question is about comparing the properties of two objects: rubber gloves and rain boots.
- The objects are related to the topic of physics and the skill of comparing properties of objects.
- Properties of objects can include physical characteristics such as color, texture, shape, size, weight, and material. In this case, the two objects have the property of being bendable in common.

Bing search response: The most common materials used for disposable gloves are Latex, Vinyl and Nitrile. Each material has its benefits and drawbacks. Latex Gloves are constructed from Natural Rubber Latex and are the most popular type of disposable glove.

Solution:
Understanding Knowledge and Context (Variable Z1)
Analysis:
- Main Topic: Comparing the physical properties of two objects.
- Specific Knowledge Required: Knowledge of the material and properties of the objects mentioned: rubber gloves and jump rope.
- Contextual Discrepancy: There's a discrepancy between the metadata (mentioning rubber gloves and rain boots) and the detected text in the image (mentioning jump rope and rubber gloves). However, the image caption refers to a pair of scissors, which is not relevant to the objects in the detected text or the context provided. This inconsistency needs to be addressed.
- Retrieved Knowledge & Bing Search Response: Focus on material properties, especially the bendability of materials like rubber (common in gloves).
Given the inconsistencies in the provided information and the focus on material properties, especially bendability, the probability of Z1 capturing the essential knowledge and context accurately is moderately high, considering the clear information about rubber gloves but ambiguous information about the second object (jump rope vs. rain boots).
Probability:
P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response)=0.700

Analyzing Textual and Visual Information (Variable Z2)
Analysis:
- Detected Text: Refers to a 'jump rope' and 'rubber gloves'.
Image Caption: Mentions a 'pair of scissors', which is inconsistent with the detected text and the context.
- Discrepancy: There's a significant discrepancy between the detected text and the image caption. The decision should weigh more on the detected text as it aligns better with the retrieved knowledge about rubber gloves.
Given the alignment of detected text with the retrieved knowledge and the notable discrepancy with the image caption, the probability of Z2 accurately reflecting the meaning difference and assigning appropriate weightage is relatively high.
Probability:
P(Z2 | Z1,Detected Text, Image Caption)=0.800

Make a Decision with Confidence (Variable Z3)
Options: (A) hard (B) bendable
Analysis:
- Option A (hard): Not strongly supported. Rubber gloves are known for their flexibility, not hardness. The property of a jump rope (if considered) also aligns more with flexibility than hardness.
- Option B (bendable): Strongly supported. Both rubber gloves and jump ropes (assuming the jump rope is the second object) are known for their bendable nature.
There are total of 2 options provided in the question. Given the analysis and considering the higher weightage of the detected text (rubber gloves and jump rope) which supports the bendability of the objects, the confidence in each option being correct is as follows, and we need to ensure that these probabilities sum up to 1:
Probabilities:
P(Z3_{Option A} | Z2)=0.100
P(Z3_{Option B} | Z2)=0.900

Conclusion:
The answer is B with a numerical probability of 0.900.


Example 2:
Question: Select the one substance that is not a mineral.

Context: Select the better answer.

Options: (A) turtle shell is not a pure substance. It is made by a living thing (B) Celestine is a pure substance. It is a solid. (C) Hematite is not made by living things. It is a solid.

Metadata: {'pid': 16241, 'has_image': True, 'grade': 2, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'}

Bing search response: A nonmineral is a substance found in a natural environment that does not satisfy the definition of a mineral and is not even a mineraloid. Many nonminerals are mined and have industrial or other uses similar to minerals, such as jewelry.

Retrieved knowledge:
- This question involves the concept of minerals and how to distinguish them from non-mineral substances based on specific criteria.
- Minerals are naturally occurring, inorganic substances with a definite chemical composition and a crystalline structure. They are not made by living organisms.
- The question is part of a Grade 2 natural science curriculum, focusing on the topic of physics under the category of Materials, specifically addressing the skill of comparing properties of objects.
- Understanding the nature of minerals involves recognizing certain key characteristics: they are inorganic, solid, have a definite chemical composition, and a crystalline structure.
- Turtle shells are organic in nature, made by living organisms, specifically turtles. They are composed of substances like keratin and do not fit the criteria for being a mineral.
- Celestine (also known as celestite) is a mineral composed primarily of strontium sulfate. It is inorganic, naturally occurring, and crystalline.
- Hematite is an iron oxide and is a common mineral. It is inorganic, naturally occurring, and has a crystalline structure.
- Comparing these properties can help in determining which substance does not meet the criteria to be classified as a mineral.

Solution:
Understanding Knowledge and Context (Variable Z1)
Analysis:
- Main Topic: Identification of substances as minerals or non-minerals.
- Specific Knowledge Required: Understanding the characteristics of minerals: inorganic, naturally occurring, definite chemical composition, and crystalline structure. Minerals are not made by living organisms.
- Contextual Information: The context provides insights into the nature of turtle shell, celestine, and hematite, relating them to the criteria of minerals.
- Retrieved Knowledge & Bing Search Response: Emphasizes the distinction between minerals and non-minerals, especially highlighting the organic vs. inorganic origin.
- Given the clarity in the definition of minerals and the distinct characteristics of each substance mentioned, the probability of Z1 capturing the essential knowledge and context accurately is high.
Probability:
P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response)=0.950

Analyzing Textual and Visual Information (Variable Z2)
For this question, there's no textual or visual information from an image to analyze, so Z2 is not applicable in this scenario. We proceed directly to Z3, integrating the understanding of the concept of minerals with the specifics of each substance mentioned.

Make a Decision with Confidence (Variable Z3)
Options: (A) turtle shell is not a pure substance. It is made by a living thing (B) Celestine is a pure substance. It is a solid. (C) Hematite is not made by living things. It is a solid.
Analysis:
- Option A (turtle shell): Strongly supported. Turtle shells are organic and made by living organisms, which does not align with the definition of minerals.
- Option B (Celestine): Not supported. Celestine meets the criteria for being a mineral: inorganic, naturally occurring, solid, and crystalline.
- Option C (Hematite): Not supported. Hematite meets the criteria for being a mineral: inorganic, naturally occurring, solid, and crystalline.
There are total of 3 options provided in the question. Considering the clear definition of minerals and the nature of each substance, and we need to ensure that these probabilities sum up to 1:
Probabilities:
P(Z3_{Option A} | Z1)=0.950
P(Z3_{Option B} | Z1)=0.025
P(Z3_{Option C} | Z1)=0.025

Conclusion:
The answer is A with a numerical probability of 0.950.


IMPORTANT: If there are more than one option with the same highest probability, you must randomly select one with the highest probability and strictly follow the format of:
Conclusion:
Due to the absence of any supporting evidence for any option, the answer is [option] with numerical probability of [option’s numerical probability with 3 decimal places] from random selection

For example:
Conclusion:
Due to the absence of any supporting evidence for any option, the answer is A with numerical probability of 0.852 from random selection".
"""
