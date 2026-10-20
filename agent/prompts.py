"""
TrapWire - Agent Prompt Templates & Decoy Synthesis Rules
"""
import random
import string

DECOY_FIRST_NAMES = ["Amit", "Rahul", "Priya", "Vikram", "Sneha", "David", "Sarah", "Alex", "Elena", "Michael"]
DECOY_LAST_NAMES = ["Sharma", "Verma", "Patel", "Singh", "Gupta", "Miller", "Johnson", "Smith", "Williams"]
DECOY_BANKS = ["HDFC", "SBI", "ICICI", "Chase", "Wells Fargo", "Barclays"]

def generate_synthetic_decoy(form_inputs: list) -> dict:
    """
    Synthesizes ultra-realistic decoy honey-credentials tailored to intercepted form fields.
    Feeds fake credentials to the scammer's database to poison malicious datasets.
    """
    fname = random.choice(DECOY_FIRST_NAMES)
    lname = random.choice(DECOY_LAST_NAMES)
    rand_num = random.randint(100, 999)
    
    decoy_data = {}
    for inp in form_inputs:
        name = inp.get("name", "").lower()
        inp_type = inp.get("type", "text").lower()

        if "user" in name or "login" in name or "email" in name or "id" in name:
            decoy_data[inp.get("name") or "username"] = f"{fname.lower()}.{lname.lower()}{rand_num}@gmail.com"
        elif "pass" in name or inp_type == "password":
            chars = string.ascii_letters + string.digits + "!@#$"
            decoy_data[inp.get("name") or "password"] = "".join(random.choice(chars) for _ in range(12))
        elif "otp" in name or "pin" in name or "code" in name:
            decoy_data[inp.get("name") or "otp"] = str(random.randint(100000, 999999))
        elif "account" in name or "acc" in name:
            decoy_data[inp.get("name") or "account_number"] = f"50100{random.randint(10000000, 99999999)}"
        elif "phone" in name or "mobile" in name:
            decoy_data[inp.get("name") or "phone"] = f"+91-98{random.randint(10000000, 99999999)}"
        else:
            decoy_data[inp.get("name") or "field"] = f"{fname} {lname}"

    if not decoy_data:
        decoy_data = {
            "username": f"{fname.lower()}{rand_num}@gmail.com",
            "password": "SecureDecoyPassword#2026",
            "otp_token": str(random.randint(100000, 999999))
        }

    return decoy_data
