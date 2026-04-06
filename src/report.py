def generate_report(prediction: dict) -> str:
    if "label" not in prediction:
        raise ValueError("Prediction must contain 'label'.")

    if "confidence" not in prediction:
        raise ValueError("Prediction must contain 'confidence'.")

    label = prediction["label"]
    confidence = prediction["confidence"]

    if label == "normal":
        return f"No obvious abnormal region was detected in the ultrasound image (confidence: {confidence:.2f})."
    elif label == "lesion_detected":
        return f"A suspicious lesion-like region was detected in the ultrasound image (confidence: {confidence:.2f})."