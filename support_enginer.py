from pathlib import Path
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"

CATEGORY_KEYWORDS = {
    "order_sync": [
        "order", "online order", "sync", "synchronization",
        "pending order", "delivery order"
    ],
    "printer": [
        "printer", "printing", "receipt", "paper", "print"
    ],
    "device_pairing": [
        "pair", "pairing", "device", "connection", "disconnect"
    ],
    "login": [
        "login", "log in", "password", "sign in", "account"
    ],
}

SEVERITY_KEYWORDS = {
    "high": ["all devices", "all orders", "payment issue", "outage"],
    "medium": ["repeated", "multiple", "keeps failing", "unable"],
    "low": ["slow", "intermittent", "sometimes"],
}


def load_documents():
    documents = []

    if not KNOWLEDGE_DIR.exists():
        return documents

    for path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        content = path.read_text(encoding="utf-8").strip()

        if content:
            documents.append({
                "source": path.name,
                "text": content
            })

    return documents


def classify_incident(text: str) -> str:
    normalized = text.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(
            1 for keyword in keywords
            if keyword in normalized
        )

    if not scores or max(scores.values()) == 0:
        return "unknown"

    best = max(scores.values())
    winners = [
        category for category, score in scores.items()
        if score == best
    ]

    # Avoid guessing when multiple categories tie.
    return winners[0] if len(winners) == 1 else "unknown"


def estimate_severity(text: str) -> str:
    normalized = text.lower()

    for severity in ("high", "medium", "low"):
        if any(
            keyword in normalized
            for keyword in SEVERITY_KEYWORDS[severity]
        ):
            return severity

    return "unassessed"


def analyze_logs(log_text: str) -> list:
    """Identify simple patterns in user-supplied diagnostic text."""
    findings = []

    if not log_text.strip():
        return findings

    patterns = {
        "Connection or network error": r"connection refused|network error|disconnected",
        "Synchronization failure": r"sync failed|synchronization failed|sync timeout",
        "Timeout": r"timeout|timed out",
        "Authentication failure": r"unauthorized|authentication failed|401",
        "Service error": r"server error|internal error|500",
    }

    for label, pattern in patterns.items():
        matches = re.findall(pattern, log_text, flags=re.IGNORECASE)

        if matches:
            findings.append({
                "finding": label,
                "matching_events": len(matches),
                "evidence": list(dict.fromkeys(matches))[:5]
            })

    if not findings:
        findings.append({
            "finding": "No recognized error pattern",
            "matching_events": 0,
            "evidence": []
        })

    return findings


class SupportEngine:
    def __init__(self):
        self.documents = load_documents()
        self.vectorizer = None
        self.matrix = None

        if self.documents:
            self.vectorizer = TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                stop_words="english"
            )
            self.matrix = self.vectorizer.fit_transform(
                [doc["text"] for doc in self.documents]
            )

    def retrieve(self, query: str, top_k: int = 3) -> list:
        if not query.strip() or not self.documents:
            return []

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(
            query_vector, self.matrix
        ).flatten()

        indices = scores.argsort()[::-1][:top_k]
        results = []

        for index in indices:
            score = float(scores[index])

            if score <= 0:
                continue

            results.append({
                "source": self.documents[index]["source"],
                "text": self.documents[index]["text"],
                "score": round(score, 4)
            })

        return results

    def diagnose(self, issue: str, log_text: str = "") -> dict:
        if not issue.strip():
            raise ValueError("Please describe the incident.")

        category = classify_incident(issue)
        evidence = self.retrieve(issue, top_k=3)
        log_findings = analyze_logs(log_text)

        if category == "unknown":
            status = "Needs human review"
        elif evidence:
            status = "Initial assessment"
        else:
            status = "Insufficient documentation"

        return {
            "incident": issue.strip(),
            "category": category,
            "severity": estimate_severity(issue),
            "status": status,
            "possible_causes": [
                "Not established. Verify the device and service state."
            ],
            "recommended_checks": [
                item["source"] for item in evidence
            ],
            "evidence": evidence,
            "log_findings": log_findings,
            "escalation_required": (
                category == "unknown" or not evidence
            ),
            "disclaimer": (
                "This is an initial assessment, not a confirmed root cause. "
                "Verify findings with authorized support personnel."
            )
        }


engine = SupportEngine()


def diagnose(issue: str, log_text: str = "") -> dict:
    return engine.diagnose(issue, log_text)

