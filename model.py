import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

#model class that inherits from nn.Module
class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        #2 fully connected layers
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name="model.pth"):
        model_foler_path = './model'
        if not os.path.exists(model_foler_path):
            os.makedirs(model_foler_path)
        
        file_name = os.path.join(model_foler_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        #optimizer
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        #loss function
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        #(n,x)

        if len(state.shape) == 1:
            #  (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, ) 
        
        #1 predicted q values with the current state
        pred = self.model(state)

        target = pred.clone()

        for index in range(len(game_over)):
            Q_new = reward[index]
            if not game_over[index]:
                Q_new = reward[index] + self.gamma * torch.max(self.model(next_state[index]))

           # target[index][torch.argmax(action[index]).item()] = Q_new
            target[index][torch.argmax(action[index]).item()] = Q_new.detach()


        #2 Q_new = r + y * max(next_predicted q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
