from support_engine import (
    analyze_logs,
    classify_incident,
    diagnose,
    estimate_severity,
)


def test_classifies_printer_issue():
    assert classify_incident(
        "The receipt printer is not printing"
    ) == "printer"


def test_classifies_order_sync_issue():
    assert classify_incident(
        "Online orders are not syncing"
    ) == "order_sync"


def test_unknown_issue_is_not_guessed():
    assert classify_incident(
        "Something unexpected happened"
    ) == "unknown"


def test_severity_estimate():
    assert estimate_severity(
        "All devices are affected"
    ) == "high"


def test_detects_timeout_in_logs():
    findings = analyze_logs("sync timeout")
    assert any(
        item["finding"] == "Timeout"
        for item in findings
    )


def test_diagnosis_includes_safety_note():
    result = diagnose("Online orders are not syncing")
    assert result["category"] == "order_sync"
    assert result["disclaimer"]
    assert "evidence" in result
