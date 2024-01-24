# 
prompt = """
Read the following question, generate the background knowledge as the context information that could be helpful for answering the question.

Question: Which property do these three objects have in common? 

Options: (A) hard (B) soft (C) yellow

Metadata: {'pid': 43, 'has_image': True, 'grade': 4, 'subject': 'natural science', 'topic': 'physics', 'category': 'Materials', 'skill': 'Compare properties of objects'} 

Detected text in the image: ['handkerchief', 'slippers', 'leisure suit']

Knowledge:
- This question is about identifying a common property among three different objects: a handkerchief, slippers, and a leisure suit. It's part of a Grade 4 natural science curriculum, focusing on the topic of physics under the category of Materials, specifically addressing the skill of comparing properties of objects.
- A handkerchief is typically made of a soft, thin fabric designed for personal hygiene purposes or as an accessory. Common materials include cotton, linen, or silk, all of which are characterized by their soft texture.
- Slippers are light footwear designed for indoor use. They are usually made from soft materials to provide comfort and warmth. The materials can vary but often include soft textiles, padded materials, or soft leathers.
- A leisure suit is a casual outfit, often made from comfortable, soft fabrics. The emphasis is on comfort and ease of movement, leading to the use of materials that are generally soft to the touch.
- The option "hard" is generally not associated with these items, as they are designed for comfort and personal use, where a soft texture is typically preferred.
- The color "yellow" is not a material property and can vary widely among handkerchiefs, slippers, and leisure suits. These items can be made in any color, so it's not a distinguishing feature.

Question: The diagrams below show two pure samples of gas in identical closed, rigid containers. Each colored ball represents one gas particle. Both samples have the same number of particles. 

Options: (A) neither; the samples have the same temperature (B) sample A (C) sample B

Metadata: {'pid': 19, 'has_image': True, 'grade': 8, 'subject': 'natural science', 'topic': 'physics', 'category': 'Particle motion and energy', 'skill': 'Identify how particle motion affects temperature and pressure'}

Knowledge:
- The kinetic theory of gases posits that the temperature of a gas is directly proportional to the average kinetic energy of its particles. This means that if the particles in a gas sample move more rapidly on average, the temperature of the gas is higher.
- In a closed, rigid container, the volume of the gas and the number of particles are constant. Therefore, any differences in temperature between two gas samples under these conditions would be due to differences in the average kinetic energy of the particles.
- Pressure in a closed container is caused by gas particles colliding with the container walls. The frequency and force of these collisions can be affected by the speed (kinetic energy) of the particles and their number. In this scenario, as the number of particles is the same in both samples, any difference in pressure would be due to differences in the average speed or kinetic energy of the particles.
- If the diagrams show particles in one sample moving more rapidly or spread out than in the other, it would suggest a higher temperature for that sample, as more rapid motion or more spread-out particles indicate higher kinetic energy.
- If the diagrams show a similar pattern of motion and distribution of particles in both samples, it would suggest that the samples have the same temperature, as the kinetic energy of the particles would be similar.

Question: Think about the magnetic force between the magnets in each pair. Which of the following statements is true?

Context: The images below show two pairs of magnets. The magnets in different pairs do not affect each other. All the magnets shown are made of the same material, but some of them are different shapes.  

Options: (A) The magnitude of the magnetic force is greater in Pair 1. (B) The magnitude of the magnetic force is greater in Pair 2. (C) The magnitude of the magnetic force is the same in both pairs.

Metadata: {'pid': 270, 'has_image': True, 'grade': 6, 'subject': 'natural science', 'topic': 'physics', 'category': 'Velocity, acceleration, and forces', 'skill': 'Compare magnitudes of magnetic forces'}

Knowledge:
- Magnetic force is the attraction or repulsion that arises between electrically charged particles due to their motion. This force is observed between two magnets or between a magnet and a ferromagnetic material.
- The strength of the magnetic force between two magnets is influenced by several factors including:
-- The material of the magnets: Different materials have different magnetic strengths. However, in this case, it's stated that all the magnets are made of the same material, so this factor is constant.
-- The distance between the magnets: The force is stronger when the magnets are closer together and weaker when they are further apart, following an inverse square law.
-- The shape and size of the magnets: Different shapes can influence how the magnetic field lines are concentrated or spread out. For example, a bar magnet has a more concentrated field at its poles, while a horseshoe magnet might have a strong field between its poles due to the shape directing the field lines.
-- The orientation of the magnets: Like poles repel each other, while opposite poles attract. The direction and magnitude of the magnetic force depend on how the poles of the two magnets are aligned.

Read the following question, generate the background knowledge as the context information that could be helpful for answering the question.
"""