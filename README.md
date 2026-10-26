# Petpooja AI Support & Incident Diagnosis Copilot

An independent AI engineering portfolio project that demonstrates
incident classification, troubleshooting-document retrieval,
diagnostic-log analysis and support-report generation.

**Disclaimer:** This is an independent prototype, not an official
Petpooja product or integration. Sample troubleshooting guides and
incident data are illustrative.

## Features

- Classifies common support incidents.
- Retrieves relevant troubleshooting documents using TF-IDF.
- Analyzes supplied diagnostic text for common error patterns.
- Displays evidence and recommends further checks.
- Flags incidents for human review when evidence is insufficient.
- Exports a structured JSON incident report.
- Provides a Streamlit interface and FastAPI endpoints.

## Architecture

User incident
    -> Incident classification
    -> Troubleshooting document retrieval
    -> Diagnostic log analysis
    -> Evidence-based initial assessment
    -> Streamlit dashboard or FastAPI response

## Technology stack

- Python
- scikit-learn
- Pandas
- Streamlit
- FastAPI
- Pydantic
- pytest
- Docker

## Run locally

Create and activate a virtual environment, then install dependencies:

    python -m venv .venv

Windows PowerShell:

    .venv\Scripts\Activate.ps1

Install packages:

    pip install -r requirements.txt

Start the dashboard:

    streamlit run app.py

Start the API in a separate terminal:

    uvicorn main:app --reload

API documentation:

    http://127.0.0.1:8000/docs

## Run tests

    pytest -q

## Project structure

- app.py: Streamlit interface
- main.py: FastAPI service
- support_engine.py: classification and retrieval
- knowledge_base/: illustrative troubleshooting documents
- data/: synthetic incident examples
- tests/: automated tests
- Dockerfile: Streamlit container

## Current limitations

The current implementation uses keyword classification and TF-IDF
retrieval. It does not yet contain LLM-based answer generation,
semantic embedding retrieval, production integrations or a validated
root-cause prediction model.

Diagnostic findings are preliminary and must be reviewed by a human.

## Planned improvements

1. Semantic retrieval with sentence embeddings.
2. LLM-based RAG with source-grounded answers.
3. A labeled incident evaluation dataset.
4. Retrieval and diagnosis accuracy benchmarks.
5. Improved incident severity assessment.
6. Secure deployment and monitoring.

