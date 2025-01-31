prompt_vpgm = """
We have a science question that requires a careful analysis to identify the correct answer. The decision-making process is structured into a series of steps, each focusing on specific aspects of the information provided. Let's approach this systematically: 

Understanding Knowledge and Context (Variable Z1): 
- Start by analyzing the question and the provided context. What is the main topic, and what specific knowledge does it require? Consider the retrieved knowledge and the Bing search response. What essential information do these sources provide? 
- Calculate the probability of Z1 capturing the essential knowledge and context required for solving the question. 
Use the formula: 
P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response) = {numerical value}. 

Analyzing Textual and Visual Information (Variable Z2): 
- Examine the detected text in the image and the image caption. What are the key pieces of information each source provides? Are there any discrepancies between them?
- Estimate the probability of Z2 accurately reflecting the meaning difference between detected text and image caption, and deciding the weightage of each based on the discrepancy. 
Use the formula: 
P(Z2 | Z1, Detected Text, Image Caption) = {numerical value}. 

Make a Decision with Confidence (Y): 
- Integrate the evaluations and reasoning from Z1 to Z2. For each answer option, provide a probability that represents your confidence in the option being correct. Ensure the probabilities sum up to 1. 
- Proceed with the analysis, ensuring that each variable is logically derived from the provided information and the outcomes of the dependent variables.
- Present the probabilities for each answer option in the form of 
P(Y = A | Z1, Z2) = {numerical value}
P(Y = B | Z1, Z2) = {numerical value}
P(Y = C | Z1, Z2) = {numerical value}
P(Y = D | Z1, Z2) = {numerical value}
where A, B, C, and D represent the answer options.

Finally, you must conclude exact one answer in the form of "The answer is <correct option> with numerical probability of <correct option’s numerical probability with 3 decimal places>", for example, "The answer is A with numerical probability of 0.852" or "The answer is B with numerical probability of 0.904". Note that all probabilities you calculated should be in 3 decimal places, and you should make the reasoning of Bayesian inference be more concise. If you encountered more than one option with the same highest probability, you should randomly select one with the highest probability. 


Consider the following examples:
Example 1: 
Question: What is typically on top of a cake? 
Options: (A) chocolate (B) icing (C) candles (D) sprinkles 
Image caption: A piece of cake that is sitting on foil. 
Retrieved knowledge: Frosting is a typical topping on a cake. The largest cake present here is covered in a lime green icing. Cakes usually have a creamy glaze made of sugar to add flavor and keep them together. 

Solution:
Understanding Knowledge and Context (Variable Z1)
Analysis:
- Main Topic: Identifying typical toppings on cakes.
- Specific Knowledge Required: Familiarity with common cake decorations.
- Contextual Information: Retrieved knowledge and the image caption provide insights into common toppings like icing and frosting, but do not mention chocolate, candles, or sprinkles directly.
Probability Calculation:
Given the consistent mention of frosting and icing as cake toppings in the retrieved knowledge, the probability that Z1 captures the essential knowledge and context for answering the question correctly is high.
Probability:
P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response) = 0.850

Analyzing Textual and Visual Information (Variable Z2)
Analysis:
- Detected Text and Image Caption: The image caption describes a piece of cake sitting on foil, which doesn’t provide specific details about the toppings beyond the general appearance.
- Key Information: The retrieved knowledge mentions frosting and icing explicitly as typical toppings.
- Discrepancy: There is no discrepancy regarding the mention of icing; however, the absence of details about other toppings like chocolate, candles, or sprinkles means we can't fully assess these options without assumptions.
Probability Calculation:
Given the alignment between the retrieved knowledge about icing and the lack of contradictory information in the image caption, the probability that Z2 accurately reflects this information is high.
P(Z2 | Z1, Detected Text, Image Caption) = 0.900

Make a Decision with Confidence (Y)
Options:
(A) chocolate  
(B) icing  
(C) candles  
(D) sprinkles
Analysis:
- Options A, C, D: While these can be common on cakes for specific occasions (e.g., candles for birthdays), they are not as universally typical as icing.
- Option B (icing): Directly supported and most frequently mentioned in the retrieved knowledge and relevant context. Icing is a common, almost universal topping used for both flavor and decorative purposes on cakes.
Probability Calculation:
Given the focus on icing in both the retrieved knowledge and the lack of conflicting information regarding other options, the confidence in option B being correct is very high.
P(Y = A | Z1, Z2) = 0.100
P(Y = B | Z1, Z2) = 0.700
P(Y = C | Z1, Z2) = 0.100
P(Y = D | Z1, Z2) = 0.100

Conclusion:
The answer is B with a numerical probability of 0.700.


Example 2:
Question: What must be activated so the parked cars stay in place?
Options: (A) headlights (B) sunroof (C) radio (D) emergency brake
Image caption: A row of buildings and a city street on a hill that is pretty steep.
Retrieved knowledge: Cars are parked on a hill on a street. The area is hilly. activating the headlights, radio, or sunroof would not help a car stay in place. The emergency brakes must be activated so that the cars could stay in place on the slope.

Solution:
Understanding Knowledge and Context (Variable Z1)
Analysis:
- Main Topic: Identifying the necessary mechanism to ensure parked cars remain stationary on a steep hill.
- Specific Knowledge Required: Knowledge about car safety features relevant to parking on slopes.
- Contextual Information: The image caption describes a city street on a steep hill, and the retrieved knowledge explicitly states that only the emergency brakes would help a car stay in place in such a scenario.
Probability Calculation:
Given the specific mention that emergency brakes are essential for cars parked on a hill, the probability that Z1 captures the essential knowledge and context accurately is very high.
P(Z1 | Question, Context, Retrieved Knowledge, Bing Search Response) = 0.950

Analyzing Textual and Visual Information (Variable Z2)
Analysis:
- Detected Text and Image Caption: The image caption describes a steep city street, which suggests a scenario where parking would require extra safety measures.
- Key Information: The retrieved knowledge explicitly mentions that activating the headlights, radio, or sunroof would not assist in keeping the cars in place, leaving the emergency brake as the necessary option.
- Discrepancy: There is no discrepancy; the information aligns well and supports the conclusion.
Probability Calculation:
Given the clear support for the emergency brake in the context of a steep hill, the probability that Z2 accurately reflects the detected text and image caption without any discrepancy is extremely high.
P(Z2 | Z1, Detected Text, Image Caption) = 0.980

Make a Decision with Confidence (Y)
Options:
(A) headlights  
(B) sunroof  
(C) radio  
(D) emergency brake
Analysis:
- Options A, B, C: According to the retrieved knowledge, none of these options would help a car stay in place on a slope.
- Option D (emergency brake): Directly supported by both the context of a steep hill and the explicit statement in the retrieved knowledge.
Probability Calculation:
Given the clear and explicit information favoring the emergency brake as the necessary safety measure for cars on a steep hill, the confidence in option D being correct is very high.
P(Y = A | Z1, Z2) = 0.005
P(Y = B | Z1, Z2) = 0.005
P(Y = C | Z1, Z2) = 0.010
P(Y = D | Z1, Z2) = 0.980

Conclusion:
The answer is D with a numerical probability of 0.980.
"""

prompt_chameleon_vc = """
Given the question (and the context), select the answer from the options ["A", "B", "C", "D"]. You should give consice and step-by-step solutions.
Finally, conclude the answer in the format of "The answer is <correct option> with a numerical probability of <correct option’s numerical probability with 3 decimal places>", where <correct option> is one from the options ["A", "B", "C", "D"].
For example, "The answer is A with a numerical probability of 0.852" or "The answer is B with a numerical probability of 0.904".
If you cannot decide the answer then you should randomly select one from the options with the same highest probability.
For example, "From random choice. The answer is A with a numerical probability of 0.250" or "From random choice. The answer is B with a numerical probability of 0.500".


Consider the following examples:
Example 1:
Question: What is typically on top of a cake? 
Options: (A) chocolate (B) icing (C) candles (D) sprinkles 
Image caption: A piece of cake that is sitting on foil. 
Retrieved knowledge: Frosting is a typical topping on a cake. The largest cake present here is covered in a lime green icing. Cakes usually have a creamy glaze made of sugar to add flavor and keep them together. 

Solution:
Step 1: Identify the typical topping on a cake
The question asks what is typically on top of a cake, and the retrieved knowledge mentions that frosting (or icing) is a common topping on cakes. It also specifically notes that cakes usually have a creamy glaze made of sugar, which aligns with the concept of icing.

Step 2: Analyze the options
- (A) Chocolate: While chocolate can be a topping, it is not as universally typical as icing.
- (B) Icing: According to the retrieved knowledge, icing is the most common topping on a cake.
- (C) Candles: Candles are often placed on cakes, but only for special occasions, not as a typical topping.
- (D) Sprinkles: Sprinkles are sometimes added to cakes, but they are less common than icing.

Conclusion:
The answer is B with a numerical probability of 0.900.


Example 2:
Question: What must be activated so the parked cars stay in place?
Options: (A) headlights (B) sunroof (C) radio (D) emergency brake
Image caption: A row of buildings and a city street on a hill that is pretty steep.
Retrieved knowledge: Cars are parked on a hill on a street. The area is hilly. activating the headlights, radio, or sunroof would not help a car stay in place. The emergency brakes must be activated so that the cars could stay in place on the slope.

Solution:
Step 1: Identify what must be activated to keep parked cars in place.
The question asks what must be activated to ensure that parked cars stay in place. The retrieved knowledge clarifies that the emergency brakes must be activated to keep cars stationary on a slope, as activating the headlights, radio, or sunroof would not contribute to this function.

Step 2: Analyze the options
- (A) Headlights: Headlights provide visibility but do not contribute to keeping a car stationary.
- (B) Sunroof: The sunroof is unrelated to maintaining a car’s position.
- (C) Radio: The radio is for entertainment and does not help in keeping a car in place.
- (D) Emergency brake: According to the retrieved knowledge, the emergency brake is the correct mechanism to keep a car in place on a slope.

Conclusion:
The answer is D with a numerical probability of 0.900.
"""