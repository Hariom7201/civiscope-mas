def apply_memory_decay(payload, decay_rate=0.95):
    """
    Simple memory decay: reduces confidence score over time.
    """
    conf = payload.get("confidence", 1.0)
    payload["confidence"] = round(conf * decay_rate, 4)
    return payload
