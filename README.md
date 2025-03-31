# Legal Risk Analyzer

## Overview
A FastAPI-based application to analyze legal contract clauses for high-risk terms.

## Setup

### Using Docker
```sh
docker-compose up --build
```

### Running Locally
1. Install dependencies:
```sh
pip install -r requirements.txt
```
2. Start FastAPI server:
```sh
uvicorn app.main:app --reload
```

## API Endpoints
- `GET /flagged-contracts?use_sample=true` - Flags high-risk contracts

## Configuration
Modify `.env` to enable different risk detection techniques.
