import tenseal as ts
import pickle
import torch
from shared.s3_utils import download_from_s3

BUCKET_NAME = "your-s3-bucket-name"
CLIENTS = ["client1", "client2"]

def download_encrypted_updates():
    updates = []
    for client in CLIENTS:
        local_file = f"{client}_update.pkl"
        s3_key = f"clients/{client}_update.pkl"
        download_from_s3(BUCKET_NAME, s3_key, local_file)
        with open(local_file, "rb") as f:
            updates.append(pickle.load(f))
    return updates

def aggregate_encrypted_weights(updates):
    aggregated = {}
    for key in updates[0].keys():
        agg = updates[0][key]
        for i in range(1, len(updates)):
            agg += updates[i][key]
        agg /= len(updates)
        aggregated[key] = agg
    return aggregated

def decrypt_weights(encrypted_weights, context):
    decrypted = {}
    for key, enc_vec in encrypted_weights.items():
        plain_tensor = torch.tensor(enc_vec.decrypt(), dtype=torch.float32)
        decrypted[key] = plain_tensor
    return decrypted

def load_context():
    download_from_s3(BUCKET_NAME, "shared/encryption_context.pkl", "encryption_context.pkl")
    with open("encryption_context.pkl", "rb") as f:
        context = ts.context_from(f.read())
    return context

if __name__ == "__main__":
    context = load_context()
    updates = download_encrypted_updates()
    aggregated = aggregate_encrypted_weights(updates)
    decrypted_weights = decrypt_weights(aggregated, context)

    # Use decrypted_weights to update your global model here
    for k, v in decrypted_weights.items():
        print(f"{k}: shape={v.shape}")
