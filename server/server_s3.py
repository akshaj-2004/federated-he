import tenseal as ts
import pickle
from shared.s3_utils import upload_to_s3, download_from_s3

BUCKET_NAME = "your-s3-bucket-name"

# Create encryption context
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
context.global_scale = 2 ** 40
context.generate_galois_keys()
context.make_context_public()

# Save and upload encryption context
with open("encryption_context.pkl", "wb") as f:
    f.write(context.serialize())
upload_to_s3(BUCKET_NAME, "encryption_context.pkl", "shared/encryption_context.pkl")

# Download encrypted client updates
download_from_s3(BUCKET_NAME, "clients/client1_update.pkl", "client1_update.pkl")
download_from_s3(BUCKET_NAME, "clients/client2_update.pkl", "client2_update.pkl")

# Load encrypted vectors
with open("client1_update.pkl", "rb") as f:
    encrypted1 = pickle.load(f)
with open("client2_update.pkl", "rb") as f:
    encrypted2 = pickle.load(f)

# Decrypt, aggregate, print result
vec1 = encrypted1.decrypt()
vec2 = encrypted2.decrypt()
aggregated = [(a + b) / 2 for a, b in zip(vec1, vec2)]

print("Aggregated result:", aggregated)
