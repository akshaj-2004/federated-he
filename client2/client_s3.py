import tenseal as ts
import numpy as np
import pickle
import torch
import torch.nn as nn
from shared.s3_utils import upload_to_s3, download_from_s3

BUCKET_NAME = "your-s3-bucket-name"
CLIENT_NAME = "client2"

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

def load_encryption_context():
    download_from_s3(BUCKET_NAME, "shared/encryption_context.pkl", "encryption_context.pkl")
    with open("encryption_context.pkl", "rb") as f:
        context = ts.context_from(f.read())
    return context

def encrypt_model_weights(state_dict, context):
    encrypted = {}
    for key, tensor in state_dict.items():
        encrypted[key] = ts.ckks_vector(context, tensor.view(-1).tolist())
    return encrypted

def simulate_training():
    model = DummyModel()
    for param in model.parameters():
        param.data += torch.randn_like(param) * 0.01
    return model.state_dict()

if __name__ == "__main__":
    context = load_encryption_context()
    local_weights = simulate_training()
    encrypted_weights = encrypt_model_weights(local_weights, context)

    with open(f"{CLIENT_NAME}_update.pkl", "wb") as f:
        pickle.dump(encrypted_weights, f)
    upload_to_s3(BUCKET_NAME, f"{CLIENT_NAME}_update.pkl", f"clients/{CLIENT_NAME}_update.pkl")
