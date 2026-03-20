## 📋 Prerequisites

Before you begin, ensure you have the following set up:

---

### 🖥️ Software Requirements

| Software  | Version          | Purpose                                      | Installation Guide                                                   |
| --------- | ---------------- | -------------------------------------------- | -------------------------------------------------------------------- |
| Docker    | 28.5.1+          | Container runtime for services               | [Install Docker](https://docs.docker.com/get-docker/)                |
| n8n       | 1.121.3 (latest) | Workflow automation platform                 | [n8n Docker Setup](https://docs.n8n.io/hosting/installation/docker/) |
| LM Studio | 0.3.36+          | Local LLM hosting with OpenAI-compatible API | [Download LM Studio](https://lmstudio.ai/)    

**Verify Installation:**

```bash
# Check Docker
docker --version
# Expected: Docker version 28.0.0 or higher
```

---

### 🤖 LM Studio Setup

Two models need to be loaded in LM Studio:

#### Embedding Model

| Requirement | Details |
|-------------|---------|
| Model | mxbai-embed-large-v1 |
| Format | GGUF |
| Server Port | 1234 (default) |
| Base URL | `http://<LM_STUDIO_IP>:1234/v1/embeddings` |
| Output Dimensions | 1024 |

#### LLM

| Requirement | Details |
|-------------|---------|
| Model | llama-3.2-3b-instruct |
| Format | GGUF |
| Server Port | 1234 (default, shared server) |
| Base URL | `http://<LM_STUDIO_IP>:1234/v1` |

**Setup Steps:**

- [ ] Download and install LM Studio
- [ ] Download `mxbai-embed-large-v1` model (GGUF)
- [ ] Download `llama-3.2-3b-instruct` model (GGUF)
- [ ] Load models in LM Studio
- [ ] Start the local server (default port: `1234`)
- [ ] Note your machine's local IP address where LM Studio server is running to use as `<LM_STUDIO_IP>` in the Base URL

> 📘 **Guide:** [LM Studio Local Server Setup](https://lmstudio.ai/docs/developer/core/server)

---

| Service | Free Tier | Signup / Setup |
|---------|-----------|----------------|
| Google Cloud Console | ✅ Yes (with limits) | [Setup Guide](https://console.cloud.google.com/) |
| Gmail | ✅ Yes | Enabled via Google Cloud |
| Google Drive | ✅ Yes | Enabled via Google Cloud |
| Qdrant DB | ✅ Yes (Docker) | Included via Docker Compose |
| n8n | ✅ Yes (Docker) | Included via Docker Compose |

---

### 🔑 Credentials Checklist

Ensure you have the following credentials ready before configuring n8n:

#### Google (Gmail & Drive)
- [ ] OAuth 2.0 Client ID
- [ ] OAuth 2.0 Client Secret
- [ ] Enabled APIs: Gmail, Google Drive

> 📘 **Guide:** [Setting up Google OAuth for n8n](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/)

> 💡 **Note:** The same Client ID and Client Secret can be used for both the Gmail and Google Drive credentials in n8n. You do not need to create separate OAuth 2.0 credentials for each service.

#### Qdrant DB
- [ ] API Key: *(optional, leave blank for self-hosted)*
- [ ] REST URL: `http://host.docker.internal:6333`
- [ ] Allowed HTTP Request Domains: `All`

#### OpenAI Node (LM Studio)
- [ ] API Key (can be any string, e.g., `lm-studio` or dummy key)
- [ ] Base URL: `http://<LM_STUDIO_IP>:1234/v1`
- [ ] Organization ID: *(optional, leave blank)*
- [ ] Allowed HTTP Request Domains: `All`

> ⚠️ **Note:** Since you're using LM Studio locally, the API Key can be any placeholder value. The Base URL must point to your LM Studio server.

---

### 📁 FAQ JSON File Format

The FAQ data file hosted on Google Drive must follow this structure:

```json
{
  "data": [
    {
      "id": 1,
      "topic": "Admissions and Applications",
      "question": "How do I apply to Crestwood University, and is there an online application?",
      "answer": "You can apply to Crestwood University by completing the online application through the student portal at portal.crestwooduniversity.edu. After you submit the form, you’ll be prompted to upload required documents and provide any additional information needed. If you run into issues accessing the application, contact support@crestwooduniversity.edu for assistance."
    },
    {
      "id": 2,
      "topic": "Admissions and Applications",
      "question": "When are the application deadlines for fall and spring?",
      "answer": "Application deadlines vary by term and program, so the most accurate dates are posted in the admissions section of portal.crestwooduniversity.edu. Crestwood University recommends submitting your application well before the posted deadline to allow time for document review. If you need help confirming the deadline for your program, email helpdesk@crestwooduniversity.edu."
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Unique identifier for the FAQ entry |
| `topic` | String | Category/topic the question belongs to |
| `question` | String | The FAQ question |
| `answer` | String | The corresponding answer |

> ⚠️ **Important:** The embedding is generated from `[topic] question` format (e.g., `[Admissions and Applications] When are the application deadlines for fall and spring?`). Ensure topics are concise and descriptive.

---

### 🌐 Network Configuration

| Service | Local URL | Port | Access Method |
|---------|-----------|------|---------------|
| n8n | `http://localhost:5678` | 5678 | Browser |
| Qdrant Dashboard | `http://localhost:6333/dashboard` | 6333 | Browser Dashboard |
| LM Studio | `http://<LM_STUDIO_IP>:1234/v1` | 1234 | API only |

> ⚠️ **Important:** Use your machine's actual local IP (e.g., `192.168.1.x`) in the LM Studio Base URL — not `localhost` — as Docker containers resolve `localhost` to themselves, not your host machine.