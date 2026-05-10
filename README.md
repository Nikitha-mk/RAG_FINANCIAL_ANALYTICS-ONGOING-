# RAG Financial Analytics Chatbot

A Retrieval-Augmented Generation (RAG) based financial analytics chatbot built using React and Claude API.
The project demonstrates how LLM-powered financial assistants can answer questions using retrieved financial context, detect anomalies, and generate spending insights from transaction data.

This repository currently contains:

* **V1:** A lightweight prototype using rule-based retrieval and a synthetic dataset
* **V2 (In Progress):** An advanced semantic RAG pipeline using FAISS vector search and embeddings with LLM-powered retrieval

---

# Overview

The chatbot enables users to interact with financial data using natural language queries such as:

* “How much did I spend on food?”
* “What are my unusual transactions?”
* “What is my savings rate?”
* “Compare monthly expenses”
* “How much did I invest this quarter?”

The system retrieves relevant financial context and generates grounded responses using an LLM.

---

# Version 1 — Prototype

V1 is a client-side prototype designed to demonstrate the complete RAG workflow in a simplified environment.

## Features

| Module                 | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| 💬 Chat Assistant      | Ask finance-related questions in natural language               |
| 📊 Analytics Dashboard | Monthly income vs expenses, category spending, savings overview |
| 📋 Transactions View   | Transaction history with categories and debit/credit indicators |
| ⚠️ Anomaly Detection   | Statistical outlier detection using standard deviation          |

---

## RAG Workflow (V1)

```text
User Query
   ↓
Keyword-Based Retrieval
   ↓
Relevant Financial Context
   ↓
Claude API
   ↓
Grounded Financial Response
```

The retrieval layer uses deterministic keyword-topic matching to simulate a basic RAG pipeline.

---

## Dataset

Synthetic financial dataset containing 30 transactions across January–March 2024.

### Summary

* Total Income: ₹1,65,000
* Total Expenses: ₹84,686
* Categories:

  * Food
  * Transport
  * Shopping
  * Rent
  * Utilities
  * Entertainment
  * Health
  * Investment

### Detected Anomalies

| Transaction                 | Observation                    |
| --------------------------- | ------------------------------ |
| Electronics Store – ₹15,000 | Significant high-value expense |
| Flipkart – ₹8,900           | Unusual shopping spike         |
| Stock Investment – ₹10,000  | Large investment deviation     |

---

## Tech Stack (V1)

* React (JSX)
* Custom CSS-in-JS
* Claude Sonnet API
* Rule-based retrieval
* SVG-based analytics charts
* Z-score anomaly detection

---

# Version 2 — Semantic RAG System (Currently Being Built)

V2 upgrades the prototype into a more production-oriented RAG architecture using semantic retrieval and vector databases.

## Planned Enhancements

| V1                            | V2                                |
| ----------------------------- | --------------------------------- |
| Keyword matching              | Semantic vector retrieval         |
| Hardcoded knowledge base      | Dynamic embedding-based retrieval |
| Simple prototype              | Scalable RAG architecture         |
| Client-side API calls         | Secure backend integration        |
| Statistical anomaly detection | ML-based anomaly detection        |

---

## V2 Architecture

```text
User Query
   ↓
Embedding Model
   ↓
FAISS Vector Search
   ↓
Relevant Transaction Chunks
   ↓
LLM Context Injection
   ↓
Financial Insights & Responses
```

---

## Technologies Planned for V2

* FAISS Vector Database
* Sentence Transformers / Embedding Models
* Python FastAPI Backend
* React Frontend
* Claude / OpenAI LLM Integration
* Secure API Proxy
* Machine Learning-based anomaly detection

---

# Future Scope

* Real bank statement ingestion
* CSV/PDF financial parsing
* Plaid API integration
* Personalized budgeting insights
* Predictive expense analytics
* Multi-user authentication
* Real-time dashboard updates

---

# Status

✅ Version 1 Completed
🚧 Version 2 Under Development (FAISS + Semantic Retrieval + LLM Integration)
