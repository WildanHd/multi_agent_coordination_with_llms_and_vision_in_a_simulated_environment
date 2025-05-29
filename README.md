# multi_agent_coordination_with_llms_and_vision_in_a_simulated_environment
 This repository contains the code for multi agent coordination project. The project integrate LLMs and Vision machine learning algorithm to execute different task. This time I consider simple simulated environment for example on object location detection and moving object task. \\
 The design could be found here:  \
 https://docs.google.com/spreadsheets/d/1jpUQnwA8zCu-duwMjVCKZt5OCxphyJNBrwxBqImbw78/edit?usp=sharing

a. Project Title: Multi-Agent Grid Navigation in a Simulated Environment \
b. Description: Developed a modular AI system consisting of multiple agents interacting within a 2D grid world. \
c. Vision Agent: Interprets a grid map using either YOLO or template matching to identify objects, start/finish positions. \
d. Planning Agent: Computes the optimal path using rule-based BFS while avoiding detected obstacles. This project also try to integrate OpenRouter.ai-based LLM for natural-language route planning and explanation. \
e. Action Agent: Visualizes the path in an animated environment using Pygame. \
f. Built fully in Python; supports modular expansion and communication between agents.
