import random

def create_verification_code():
    verification_code = str(random.randint(1, 99999))

    if len(verification_code) < 5:
        verification_code = f"{'0' * (5 - len(verification_code))}{verification_code}"
        
    return verification_code
