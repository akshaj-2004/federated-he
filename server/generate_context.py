import tenseal as ts
import pickle
from shared.s3_utils import upload_to_s3

BUCKET_NAME = "your-s3-bucket-name"

def create_and_upload_context():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.generate_galois_keys()
    context.global_scale = 2**40

    # Save to file
    with open("encryption_context.pkl", "wb") as f:
        f.write(context.serialize(save_secret_key=False))

    upload_to_s3(BUCKET_NAME, "encryption_context.pkl", "shared/encryption_context.pkl")

if __name__ == "__main__":
    create_and_upload_context()
