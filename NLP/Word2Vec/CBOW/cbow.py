import torch
import torch.nn as nn

class CBOW(nn.Module):
    def __init__(self, vocab_size, d_model, hidden_dim):
        super(CBOW, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.fc1 = nn.Linear(d_model, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = torch.mean(self.embedding(x), dim=1) # (batch_size, d_model)
        print(x.shape)
        x = self.fc1(x) # (batch_size, hidden_dim)
        x = self.fc2(x) # (batch_size, vocab_size)
        return x

x = torch.randint(1, 10, (32, 12))
model = CBOW(10, 512, 64)
print(model(x).shape)