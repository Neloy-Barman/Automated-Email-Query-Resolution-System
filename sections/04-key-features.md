## ✨ Key Features

- 📂 **Google Drive Triggered Ingestion** — Automatically detects file changes in Google Drive and re-ingests updated FAQ data 
- 🧠 **Semantic Vector Embeddings** — Converts FAQ pairs into high-dimensional vectors using `mxbai-embed-large-v1` for accurate similarity matching
- 🗃️ **Self-Hosted Vector Database** — Stores and queries embeddings with Qdrant DB using Cosine distance and 1024-dimensional vectors
- 📬 **Real-Time Email Trigger** — Gmail trigger instantly picks up new incoming emails and kicks off the resolution pipeline
- 🔍 **Similarity Search with Threshold** — Retrieves the top 3 most relevant FAQ answers with a minimum score threshold of 0.7 for quality control
- 🤖 **Local LLM Response Generation** — Uses `llama-3.2-3b-instruct` via LM Studio to craft professional, personalised HTML email responses
- 💌 **Threaded Email Replies** — Replies are sent back within the same Gmail thread using the original Message ID for seamless conversation tracking
- 🔄 **Dynamic Collection Management** — Automatically handles Qdrant collection creation, deletion, and recreation on each ingestion cycle
- 🏠 **Fully Self-Hosted Architecture** — n8n, Qdrant, and LM Studio all run locally via Docker with no third-party AI API dependencies
- 💸 **100% Free & Open Source** — Built entirely on open-source tools with no ongoing AI inference costs