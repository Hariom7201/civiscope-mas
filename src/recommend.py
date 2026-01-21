def generate_recommendation(evidence):
    """
    Evidence-based recommendation (no hallucination).
    """
    if not evidence:
        return {
            "risk_level": "UNKNOWN",
            "recommendation": "Insufficient evidence to provide recommendation.",
            "confidence": 0.0,
            "evidence": []
        }

    avg_score = sum([hit.score for hit in evidence]) / len(evidence)

    # Simple logic (upgrade later)
    risk_level = "MEDIUM"
    if avg_score > 0.75:
        risk_level = "HIGH"
    elif avg_score < 0.45:
        risk_level = "LOW"

    rec = {
        "risk_level": risk_level,
        "recommendation": f"Risk level assessed as {risk_level}. Review retrieved evidence and take precautionary action.",
        "confidence": round(avg_score, 3),
        "evidence": [
            {
                "id": hit.id,
                "score": round(hit.score, 3),
                "source": hit.payload.get("source"),
                "text": hit.payload.get("text")
            }
            for hit in evidence
        ]
    }
    return rec
