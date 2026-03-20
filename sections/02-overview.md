## 🌐 Overview

The **Automated Email Query Resolution System** is a fully self-hosted, AI-powered pipeline that automatically handles incoming email queries by matching them against a university FAQ knowledge base and generating human-friendly responses — all without manual intervention.

The system is divided into two core pipelines:

- **📥 VectorDB Data Ingestion** — Watches a Google Drive JSON file for changes, generates vector embeddings from FAQ pairs, and upserts them into a Qdrant vector database.
- **📤 Email Response Automation** — Listens for incoming Gmail messages, performs semantic similarity search against the embedded FAQ data, generates a contextual reply using a local LLM, and sends a formatted HTML response back to the sender.

Everything runs locally using Docker, LM Studio, and self-hosted n8n — ensuring **zero cloud AI costs** and **complete data privacy**.