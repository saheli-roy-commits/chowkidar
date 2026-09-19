from strands import Agent
from strands.models.ollama import OllamaModel
import json

def create_scam_detector_agent():
    model = OllamaModel(
        host="http://localhost:11434",
        model_id="qwen2.5:7b"
    )
    agent = Agent(
        model=model,
        system_prompt="""You are a fraud detection assistant. Analyze the message for scam/fraud red flags.
Respond ONLY with valid JSON in this exact format, no other text before or after:
{
  "is_scam": true or false,
  "confidence": "high" or "medium" or "low",
  "red_flags": ["flag1", "flag2", ...],
  "explanation": "a short plain-language explanation in the same language as the input message"
}"""
    )
    return agent

def analyze_and_parse(agent, message: str) -> dict:
    result = str(agent(message))
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"is_scam": None, "confidence": None, "red_flags": [], "explanation": result, "raw": True}

if __name__ == "__main__":
    agent = create_scam_detector_agent()
    test_message = "Aapka SBI account block ho gaya hai. Turant is number par call karke KYC update karein: 9876543210"
    result = analyze_and_parse(agent, test_message)
    print(json.dumps(result, indent=2, ensure_ascii=False))
