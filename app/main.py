from fastapi import FastAPI, HTTPException
from app.db import fetch_clauses
from app.model import flag_high_risk_contracts

app = FastAPI()

@app.get("/flagged-contracts")
def get_flagged_contracts(use_sample: bool = True):
    """API endpoint to get flagged contracts."""
    sample_clauses = [
        (1, "The indemnity clause requires the contractor to cover all losses resulting from negligence."),
        (2, "In case of termination, the client must provide a 30-day notice period."),
        (3, "The company shall not be liable for indirect damages caused by third-party vendors."),
        (4, "All payments must be made within 15 days of invoice receipt."),
        (5, "The supplier is responsible for ensuring compliance with all regulatory requirements."),
    ]
    
    clauses = sample_clauses if use_sample else fetch_clauses()
    flagged = flag_high_risk_contracts(clauses)
    return {"flagged_contracts": list(flagged)}
