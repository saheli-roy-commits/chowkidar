from features import extract_features

def evaluate_policy(message: str) -> dict:
    f = extract_features(message)
    triggered_rules = []
    risk = "low"

    if f["impersonates_bank_or_official"] and f["has_urgency_words"] and f["demands_callback"]:
        triggered_rules.append("bank_impersonation_urgency_callback")
        risk = "high"

    if f["promises_money_or_prize"] and (f["has_url_or_link"] or f["demands_callback"]):
        triggered_rules.append("prize_scam_with_link_or_callback")
        risk = "high"

    if f["requests_otp_or_pin"]:
        triggered_rules.append("otp_pin_request")
        risk = "high"

    if not triggered_rules and f["has_urgency_words"]:
        triggered_rules.append("urgency_only_low_signal")
        risk = "low"

    return {
        "policy_risk": risk,
        "policy_rules_triggered": triggered_rules,
        "features": f
    }

if __name__ == "__main__":
    test1 = "Aapka SBI account block ho gaya hai. Turant is number par call karke KYC update karein: 9876543210"
    test2 = "Hi, your Amazon order has been shipped and will arrive tomorrow."
    print("Scam test:", evaluate_policy(test1))
    print("Safe test:", evaluate_policy(test2))
