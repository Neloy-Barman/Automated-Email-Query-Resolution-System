## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
# Clone the repo
git clone https://github.com/Neloy-Barman/Automated-Email-Query-Resolution-System

# Navigate to the project directory
cd Automated-Email-Query-Resolution-System
```

---

### 2️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Automated-Email-Query-Resolution-System
QDRANT_COLLECTION=<collection_name>
```

> ⚠️ **Important:** The `QDRANT_COLLECTION` value is referenced by the workflow. Ensure it is consistent.


---

### 3️⃣ Start Docker Containers

Ensure Docker Desktop is running, then start all services:

```bash
docker compose up -d
```

This will spin up:

| Service | URL | Purpose |
|---------|-----|---------|
| n8n | `http://localhost:5678` | Workflow automation platform |
| Qdrant | `http://localhost:6333` | Vector database |

---

### 4️⃣ Start LM Studio Server

1. Open **LM Studio** application
2. Load `mxbai-embed-large-v1` model
3. Load `llama-3.2-3b-instruct` model
4. Navigate to the **Local Server** tab
5. Click **Start Server** (default port: `1234`)
6. Note your machine's IP address (e.g., `192.168.56.1`)

> ⚠️ Keep LM Studio running throughout usage. Both workflows depend on the local server being active.

---

### 5️⃣ Access n8n Interface

Open your browser and navigate to:

```
http://localhost:5678
```

Create an account or log in if prompted.

---

### 6️⃣ Import the Workflow

Both the **Knowledge Base Ingestion** and **Email Query Resolution** pipelines are combined in a single workflow file.

1. From the **Home** page, click the **Create Workflow** button (top-right corner)
2. Once the workflow canvas opens, click the **`...`** menu (top-right corner)
3. Select **Import from File**
4. Choose `Automated-Email-Query-Resolution.json` from the project directory

---

### 7️⃣ Configure Credentials in n8n

> 📘 All credentials can be configured from the same path: **Home → Credentials → Add Credential**. Select the respective credential service from the list below.

| Credential | Service to Select | Required Values |
|------------|------------------|-----------------|
| **Gmail** | Gmail OAuth2 API | Client ID, Client Secret |
| **Google Drive** | Google Drive OAuth2 API | Client ID, Client Secret |
| **Qdrant** | Qdrant API | REST URL: `http://host.docker.internal:6333` |
| **LM Studio** | OpenAi | API Key: any placeholder value<br>Base URL: `http://<LM_STUDIO_IP>:1234/v1`|

> 📘 Refer to [Prerequisites → Credentials Checklist](#-credentials-checklist) for detailed setup instructions.

---

### 8️⃣ Update Workflow Parameters

**Credentials:**

| Credential | Nodes |
|------------|-------|
| **OpenAi** | Message a model |
| **Gmail OAuth2 API** | Gmail Trigger, Send Reply Email |
| **Google Drive OAuth2 API** | Google Drive Trigger, Download File |
| **QDrant API** | Check If Collection Exists, Delete Collection, Create Collection, Upsert Points, Similarity Search |

**Parameters:**

| Node | Parameter | Value |
|------|-----------|-------|
| **Google Drive Trigger** | File | By ID → Your FAQ JSON File ID |
| **Download File** | File | By ID → Your FAQ JSON File ID |
| **Embedding Generation** | URL | http://<LM_STUDIO_IP>:1234/v1/embeddings |
| **Query Embedding** | URL | http://<LM_STUDIO_IP>:1234/v1/embeddings |

---

### 9️⃣ Activate the Workflows

1. Toggle the **Active** switch in the top-right corner
2. Status should show **Active** (green)

---

### ✅ Setup Complete!

Your system is now live. Upload or update your FAQ JSON file in Google Drive and send a test email to your configured Gmail address to see the pipeline in action! 🎉

> 💡 Head over to [📘 Usage](#-usage) to learn how to test and manage the system.