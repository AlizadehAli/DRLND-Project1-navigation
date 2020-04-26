import numpy as np
import random
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
from collections import namedtuple, deque
from model import QNetwork
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Global parameters to be used throughout the code
BUFFER_SIZE = int(1e5)  
BATCH_SIZE = 64         
GAMMA = 0.999           # discount factor        
TAU = 1e-3              # grain for soft update
LR = 1e-4               # learning rate 
UPDATE_RATE = 4         # update rate for current model to target model



class DQN_Agent():
    def __init__(self, state_size, action_size, seed=0, mode = 'DQN'):
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)
        self.qnetwork_local = QNetwork(state_size, action_size, seed).to(device)
        self.qnetwork_target = QNetwork(state_size, action_size, seed).to(device)
        self.optimizer = optim.Adam(self.qnetwork_local.parameters(), lr=LR)
        self.mode = mode
        self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)        # Replay memory
        self.t_step = 0
        self.train_steps = 0
    
    def step(self, state, action, reward, next_state, done):
        self.memory.add(state, action, reward, next_state, done)
        self.train_steps += 1
        self.t_step = (self.t_step + 1) % UPDATE_RATE
        if self.t_step == 0:
            if len(self.memory) > BATCH_SIZE: # check the length of memory to see if enough samples are available
                experiences = self.memory.sample()
                self.learn(experiences, GAMMA)

    def get_action(self, state, eps=0.):
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        self.qnetwork_local.eval()
        with torch.no_grad():
            action_values = self.qnetwork_local(state)
        self.qnetwork_local.train()

        if random.random() > eps: # Epsilon-greedy action selection
            return np.argmax(action_values.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_size))

    def learn(self, experiences, gamma):
        states, actions, rewards, next_states, dones = experiences

        if self.mode == 'Double_DQN':
            Q_local_argmax = self.qnetwork_local(next_states).detach().max(1)[1].unsqueeze(1)

            Q_targets_next = self.qnetwork_target(next_states).gather(1, Q_local_argmax)

        else: # standard DQN
            Q_targets_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)
        
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))
        Q_expected = self.qnetwork_local(states).gather(1, actions)

        loss = F.mse_loss(Q_expected, Q_targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.soft_update(self.qnetwork_local, self.qnetwork_target, TAU) # update target network               

    def soft_update(self, local_model, target_model, tau):
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)
           
class ReplayBuffer:
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, action_size, buffer_size, batch_size, seed):
        """Initialize a ReplayBuffer object.
        Params
        ======
            action_size (int): dimension of each action
            buffer_size (int): maximum size of buffer
            batch_size (int): size of each training batch
            seed (int): random seed
        """
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)  
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(seed)
    
    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)
    
    def sample(self):
        """Randomly sample a batch of experiences from memory."""
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
  
        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)

