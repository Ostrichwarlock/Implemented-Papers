import torch
import torch.nn as nn
import torch.optim as opt
from torch.utils.data import DataLoader

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from utils import *
from cbow import CBOW
from dataset import TextDataset
from hyperparameters import BATCH_SIZE, CONTEXT_SIZE, D_MODEL, N_EPOCHS, LEARNING_RATE, TRAIN

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(script_dir, "..", "data", "Articles")
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

    # Load the Data
    data = get_data(DATA_PATH)

    # Create windows
    windows = create_windows(data, CONTEXT_SIZE)
    X, y = windows["windows"], windows["labels"]

    # Load the tokenizer and word2idx and idx2word mappings
    _, word_to_idx, idx_to_word, vocabulary = create_tokenizer(data)
    VOCAB_SIZE = len(vocabulary)

    # Create a dataset
    unk_token = word_to_idx["UNK"]
    train_ds = TextDataset(X, y, word_to_idx, unk_token)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)

    model = CBOW(VOCAB_SIZE, D_MODEL).to(DEVICE)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = opt.Adam(model.parameters(), lr=LEARNING_RATE)

    if TRAIN:
        # Train the model
        train_cbow(N_EPOCHS, model, train_loader, criterion, optimizer, DEVICE)
    
    # Test the embeddings
    words_to_test = ["man", "woman", "young", "amazing", "strong"]

    for word in words_to_test:
        print(f"WORDS THAT ARE SIMILAR TO: {word}")
        get_most_similar_words(word, model, word_to_idx, idx_to_word, unk_token, n=3)
        print("------------------------------\n")

if __name__ == "__main__":
    main()


