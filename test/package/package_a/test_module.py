import torch
from torch.fx import wrap

wrap("a_non_torch_leaf")


class Mod(torch.nn.Module):
    def __init__(self, script_mod):
        super().__init__()
        self.script_mod = script_mod

    def forward(self, x):
        return self.script_mod(x)


class SharedTensorsMod(torch.nn.Module):
    def __init__(self, tensor, script_mod):
        super().__init__()
        # have script_mod be a ScriptModule that
        # itself holds x as a tensor
        self.tensor = tensor
        self.script_mod = script_mod

    def forward(self, x):
        return self.script_mod(x) + self.tensor

class SimpleTest(torch.nn.Module):
    def forward(self, x):
        x = a_non_torch_leaf(x, x)
        return torch.relu(x + 3.0)


def a_non_torch_leaf(a, b):
    return a + b
