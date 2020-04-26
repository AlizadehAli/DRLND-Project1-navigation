# DRLND-Project1-navigation
This repository contains my implementation of navigation project for Deep Reinforcement Learning Nano Degree program. For this project, I will train an agent to navigate and collect yellow bananas and avoid blue ones in a square world. The agent uses Deep Q-Networks (DQN)/DQN-variant to collect as many yellow bananas as possible.

## Goal of the Project
Since the task is episodic, the trained agent must **score +13 over 100 consecutive episodes** in order to consider it a successful implementation.

## Environment
The environement used in this project is a variant of Unity [ML_agents ](https://github.com/Unity-Technologies/ml-agents) banana-collector environment which can be downloaded from the following links for different operatin systems:
   - Linux: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Linux.zip)
   - Mac OSX: [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana.app.zip)
   - Windows (32-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Windows_x86.zip)
   - Windows (64-bit): [click here](https://s3-us-west-1.amazonaws.com/udacity-drlnd/P1/Banana/Banana_Windows_x86_64.zip)

   (_For Windows users_) Check out [this link](https://support.microsoft.com/en-us/help/827218/how-to-determine-whether-a-computer-is-running-a-32-bit-version-or-64) if you need help with determining if your computer is running a 32-bit version or 64-bit version of the Windows operating system.

## State/Action Space and Reward
The **state space** has 37 dimensions which contains the agent's velocity, along with ray-based perception of objects around agent's forward direction.
The **action space** is comprised of 4 discrete actions, corresponding to:
- **`0`** - move forward
- **`1`** - move backward
- **`2`** - turn left
- **`3`** - turn right
The **reward** for this environment is +1 when the agent collects yellow banana and -1 once blue banana is collected.

## Instructions
1. Activate the conda environment `drlnd` as established in [Udacity deep reinforcement learning repository](https://github.com/udacity/deep-reinforcement-learning)
2. Open `Navigation.ipynb` and follow the instructions in it.
3. Change kernel to `drlnd` in `Navigation.ipynb`
4. Unzip the downloaded banana-collector environment and give its path to `file_name="..."` in `Navigation.ipynb`.
5. Execute the code cell in `Navigation.ipynb` from beginning to the end. The trained agent will be saved in `checkpoint.pth` as the average score > +13.0.

