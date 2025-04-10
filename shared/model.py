# shared/model.py

import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_size=10):  # Default input size is 10 (override if needed)
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)
