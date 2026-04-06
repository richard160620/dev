import pytest
from src.report import generate_report

def test_generate_report_for_normal():
    prediction = {"label": "normal", "confidence": 0.95}
    report = generate_report(prediction)
    assert "No obvious abnormal region" in report

def test_generate_report_for_lesion():
    prediction = {"label": "lesion_detected", "confidence": 0.85}
    report = generate_report(prediction)
    assert "suspicious lesion-like region" in report

def test_generate_report_missing_label():
    with pytest.raises(ValueError):
        generate_report({"confidence": 0.95})