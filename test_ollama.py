import requests

def analyze_message(message: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": f"Analyze this message for scam/fraud red flags and explain in simple terms: '{message}'",
            "stream": False
        }
    )
    return response.json()["response"]

if __name__ == "__main__":
    test_message = "Aapka SBI account block ho gaya hai. Turant is number par call karke KYC update karein: 9876543210"
    result = analyze_message(test_message)
    print(result)
