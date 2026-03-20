## 🛠️ Tech Stack

| Category | Technology | Description | Link |
|----------|------------|-------------|------|
| **Workflow Automation** | n8n Community Edition | Workflow orchestration for both the ingestion pipeline and response automation | [n8n.io](https://docs.n8n.io/hosting/) |
| **Vector Database** | Qdrant DB | Vector database for storing and querying FAQ embeddings | [qdrant.tech](https://qdrant.tech/) |
| **Embedding Model** | mxbai-embed-large-v1 | Text embedding model, producing 1024-dimensional vectors | [MxBai](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1) |
| **LLM** | llama-3.2-3b-instruct | Instruction-tuned LLaMA model for reply email | [LLaMA](https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF) |
| **Model Host** | LM Studio | Hosts both the embedding model and LLM via OpenAI-compatible APIs | [lmstudio.ai](https://lmstudio.ai/) |
| **Email Service** | Gmail | Incoming email trigger and outbound threaded reply service  | [Gmail](https://mail.google.com/) |
| **File Storage** | Google Drive | Hosts the FAQ JSON file and triggers ingestion on file changes | [Google Drive](https://drive.google.com/) |
| **Containerization** | Docker + Docker Compose | Multi-container orchestration for n8n and Qdrant services via `docker-compose.yml` | [Docker](https://www.docker.com/) |