def generate_report(prediction: dict) -> str:
    if "label" not in prediction:
        raise ValueError("Prediction must contain 'label'.")

    if prediction["label"] == "normal":
        return "No obvious abnormal region was detected in the ultrasound image."
    elif prediction["label"] == "lesion_detected":
        return "A suspicious lesion-like region was detected in the ultrasound image."