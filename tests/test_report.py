from src.report import generate_report

def test_generate_report_for_normal():
    prediction = {"label": "normal", "confidence": 0.95}
    report = generate_report(prediction)
    assert "No obvious abnormal region" in report