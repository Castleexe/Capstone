import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidde_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidde_size)
        self.linear2 = nn.Lienar(hidde_size, output_size)

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
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        #loss function
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        pass