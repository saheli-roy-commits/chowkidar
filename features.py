import re

URGENCY_WORDS = [
    "turant", "immediately", "urgent", "now", "abhi", "ekhoni", "এখনই",
    "তুরন্ত", "तुरंत", "जल्दी", "within", "1 hour", "expire"
]
BANK_OFFICIAL_WORDS = [
    "sbi", "rbi", "kyc", "bank", "account", "ব্যাংক", "अकाउंट", "ব্যাংক অ্যাকাউন্ট",
    "income tax", "aadhaar", "aadhar", "pan card"
]
PRIZE_WORDS = [
    "lottery", "won", "winner", "prize", "reward", "congratulations",
    "जीत", "लॉटरी", "পুরস্কার", "জিতেছেন"
]
OTP_PIN_WORDS = ["otp", "pin", "cvv", "password", "ओटीपी", "ওটিপি"]
CALLBACK_WORDS = ["call this number", "call karke", "call kore", "कॉल करें", "কল করে", "call now"]

def has_any(text: str, words: list) -> bool:
    text_lower = text.lower()
    return any(w.lower() in text_lower for w in words)

def has_phone_number(text: str) -> bool:
    return bool(re.search(r'\b\d{10}\b', text))

def has_url(text: str) -> bool:
    return bool(re.search(r'(https?://|bit\.ly|www\.)', text, re.IGNORECASE))

def extract_features(message: str) -> dict:
    return {
        "has_urgency_words": has_any(message, URGENCY_WORDS),
        "has_phone_number": has_phone_number(message),
        "has_url_or_link": has_url(message),
        "requests_otp_or_pin": has_any(message, OTP_PIN_WORDS),
        "impersonates_bank_or_official": has_any(message, BANK_OFFICIAL_WORDS),
        "demands_callback": has_any(message, CALLBACK_WORDS) or (has_phone_number(message) and has_any(message, URGENCY_WORDS)),
        "promises_money_or_prize": has_any(message, PRIZE_WORDS),
    }

if __name__ == "__main__":
    test1 = "Aapka SBI account block ho gaya hai. Turant is number par call karke KYC update karein: 9876543210"
    test2 = "Hi, your Amazon order has been shipped and will arrive tomorrow."
    print("Scam test:", extract_features(test1))
    print("Safe test:", extract_features(test2))
