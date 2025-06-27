# Java Parser Demo Backend

This repository provides a simple backend service for generating JUnit tests
from Java source code. The service exposes a small Flask API that extracts
methods using `javaparser` and generates tests via an LLM.

## Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

A Java runtime is required for the `ExtractMethod` class. Make sure the
`javaparser-core-3.25.4.jar` is present in the repository.

Set the `OPENAI_API_KEY` environment variable if you want to use the OpenAI
API for generating tests.

## Running the server

```bash
python app.py
```

Send a POST request to `/generate` with JSON containing either `file_path` or
`code`.

Example:

```bash
curl -X POST http://localhost:8000/generate -H 'Content-Type: application/json' \
    -d '{"file_path": "HelloWorld.java"}'
```

The response contains the generated JUnit test.
