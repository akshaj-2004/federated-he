import tenseal as ts
import numpy as np
import pickle
from shared.s3_utils import upload_to_s3, download_from_s3

BUCKET_NAME = "your-s3-bucket-name"
CLIENT_NAME = "client2"

# Download encryption context from S3
download_from_s3(BUCKET_NAME, "shared/encryption_context.pkl", "encryption_context.pkl")

# Load context
with open("encryption_context.pkl", "rb") as f:
    context = ts.context_from(f.read())

# Encrypt local data
local_data = np.random.rand(10)
vec = ts.ckks_vector(context, local_data.tolist())

# Save and upload encrypted update
with open(f"{CLIENT_NAME}_update.pkl", "wb") as f:
    pickle.dump(vec, f)
upload_to_s3(BUCKET_NAME, f"{CLIENT_NAME}_update.pkl", f"clients/{CLIENT_NAME}_update.pkl")
