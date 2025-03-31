import openai
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import os
from dotenv import load_dotenv
from collections import Counter
import re

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

HIGH_RISK_TERMS = os.getenv("HIGH_RISK_TERMS", "indemnity,liability,termination,damages,breach").split(",")
USE_AI = os.getenv("USE_AI", "false").lower() == "true"
USE_FREQUENT_TERMS = os.getenv("USE_FREQUENT_TERMS", "false").lower() == "true"
USE_SUPERVISED_MODEL = os.getenv("USE_SUPERVISED_MODEL", "false").lower() == "true"


def get_embedding(text):
    """Generate embeddings using OpenAI's embedding model."""
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]


def extract_frequent_terms(clauses):
    """Extract high-risk terms based on frequency analysis."""
    words = []
    for _, text in clauses:
        words.extend(re.findall(r'\b\w+\b', text.lower()))
    common_terms = Counter(words).most_common(50)
    return [word for word, freq in common_terms if freq > 5]


def is_high_risk_ai(text):
    """Use AI to classify if a clause is high-risk."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a legal assistant. Identify if the given clause is high risk."},
            {"role": "user", "content": f"Is this clause high risk? {text}"}
        ]
    )
    return "yes" in response["choices"][0]["message"]["content"].lower()


def train_supervised_model():
    """Train a RandomForest model on labeled high-risk and low-risk clauses."""
    # Sample training data (Replace with real data)
    training_data = [
        ("This contract indemnifies the party against all damages", 1),
        ("Payment must be made within 30 days", 0),
        ("The liability for damages is capped at $1M", 1),
        ("Termination clause states a 60-day notice is required", 1),
        ("Supplier agrees to provide the services as per contract", 0)
    ]
    
    X_train = [get_embedding(text) for text, _ in training_data]
    y_train = [label for _, label in training_data]
    
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

# Train the model once and reuse
SUPERVISED_MODEL = train_supervised_model() if USE_SUPERVISED_MODEL else None


def is_high_risk_supervised(text):
    """Use trained model to classify risk."""
    if SUPERVISED_MODEL:
        embedding = np.array(get_embedding(text)).reshape(1, -1)
        return bool(SUPERVISED_MODEL.predict(embedding)[0])
    return False


def flag_high_risk_contracts(clauses):
    """Flag contracts with high-risk clauses using configurable methods."""
    if USE_FREQUENT_TERMS:
        high_risk_terms = extract_frequent_terms(clauses)
    else:
        high_risk_terms = HIGH_RISK_TERMS

    high_risk_clauses = []
    for cid, text in clauses:
        if USE_AI and is_high_risk_ai(text):
            high_risk_clauses.append((cid, text))
        elif USE_SUPERVISED_MODEL and is_high_risk_supervised(text):
            high_risk_clauses.append((cid, text))
        elif any(term in text.lower() for term in high_risk_terms):
            high_risk_clauses.append((cid, text))

    return set(cid for cid, _ in high_risk_clauses)
