
---

## 🌐 Overview

The **Automated Email Query Resolution System** is a fully self-hosted, AI-powered pipeline that automatically handles incoming email queries by matching them against a university FAQ knowledge base and generating human-friendly responses — all without manual intervention.

The system is divided into two core pipelines:

- **📥 VectorDB Data Ingestion** — Watches a Google Drive JSON file for changes, generates vector embeddings from FAQ pairs, and upserts them into a Qdrant vector database.
- **📤 Email Response Automation** — Listens for incoming Gmail messages, performs semantic similarity search against the embedded FAQ data, generates a contextual reply using a local LLM, and sends a formatted HTML response back to the sender.

Everything runs locally using Docker, LM Studio, and self-hosted n8n — ensuring **zero cloud AI costs** and **complete data privacy**.

---



---



---

## 🔄 Automation Flow

### Part 1 — VectorDB Data Ingestion

```text
         Google Drive File Change Detected (Daily Trigger)
                              ↓
                   Google Drive Trigger
                              ↓
          ┌───────────────────┴───────────────────┐
          ↓                                       ↓
  [Collection Setup Branch]            [Data Ingestion Branch]
          ↓                                       ↓
  Fetch Collection Name               Download File (JSON)
  (from .env: QDRANT_COLLECTION)               ↓
          ↓                             Extract from File
  Check If Collection Exists           (Binary → JSON)
          ↓                                       ↓
    ┌─────┴─────┐                           Data Fetch
    ↓           ↓                      (extract `data` array)
 Exists?   Not Exists?                          ↓
    ↓           ↓                       Data Preprocessing
 Delete         |                  (add `embeddingText` as
 Collection     |                   [topic] question format,
    ↓           |                    add `collection` field)
    └─────┬─────┘                               ↓
          ↓                             Embedding Generation
   Create Collection                  (POST to LM Studio:
  (size: 1024, Cosine)               mxbai-embed-large-v1)
          ↓                                       ↓
          └───────────────────┬───────────────────┘
                              ↓
                        Upsert Points
               (id, payload: {id, topic, question,
                answer, embeddingText}, vector)
                              ↓
                    ✅ Ingestion Complete
```

---

### Part 2 — Email Response Automation

```text
           New Email Received in Gmail Inbox
                           ↓
                    Gmail Trigger
                           ↓
                  Fields Preparation
        (from, name, to, email_id, thread_id,
                 subject, email_body)
                           ↓
          ┌────────────────┴────────────────┐
          ↓                                 ↓
   Query Embedding                Collection Name Fetch
   (POST to LM Studio:            (from .env: QDRANT_COLLECTION)
   mxbai-embed-large-v1
   on email_body)
          ↓                                 ↓
          └────────────────┬────────────────┘
                           ↓
                         Merge
               (combine embedding vector
                + collection name)
                           ↓
                   Similarity Search
              (Qdrant: top 3 results,
               score threshold: 0.7)
                           ↓
                  Message a Model
           (llama-3.2-3b-instruct via LM Studio)
           System Prompt: generate user-friendly
           HTML email response
           User Message: name, email_body,
           top 3 results {score, topic,
                          question, answer}
                           ↓
                     Email Format
              (merge LLM output with
               pre-defined HTML template)
                           ↓
                  Send Reply Email
             (reply to same Gmail thread
              using original Message ID)
                           ↓
               ✅ Response Sent to Sender
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following set up:

---

### 🖥️ Software Requirements

| Software | Version | Purpose | Installation Guide |
|----------|---------|---------|-------------------|
| Docker | 20.10.0+ | Container runtime for n8n and Qdrant | [Install Docker](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.0.0+ | Multi-container orchestration | [Install Compose](https://docs.docker.com/compose/install/) |
| LM Studio | 0.3.0+ | Local hosting for embedding model and LLM | [Download LM Studio](https://lmstudio.ai/) |

**Verify Installation:**

```bash
# Check Docker
docker --version
# Expected: Docker version 20.10.0 or higher

# Check Docker Compose
docker compose version
# Expected: Docker Compose version v2.0.0 or higher
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
| Base URL | `http://<YOUR_IP>:1234/v1/embeddings` |
| Output Dimensions | 1024 |

#### LLM (Response Generation)

| Requirement | Details |
|-------------|---------|
| Model | llama-3.2-3b-instruct |
| Format | GGUF |
| Server Port | 1234 (default, shared server) |
| Base URL | `http://<YOUR_IP>:1234/v1` |

**Setup Steps:**

- [ ] Download and install LM Studio
- [ ] Download `mxbai-embed-large-v1` model (GGUF)
- [ ] Download `llama-3.2-3b-instruct` model (GGUF)
- [ ] Load models in LM Studio
- [ ] Start the local server (default port: `1234`)
- [ ] Note your machine's local IP address for Base URL configuration

> 📘 **Guide:** [LM Studio Local Server Setup](https://lmstudio.ai/docs/developer/core/server)

---

### 🔐 Account & API Requirements

| Service | Free Tier | Purpose | Signup / Setup |
|---------|-----------|---------|----------------|
| Gmail | ✅ Yes | Incoming email trigger & outbound reply | [Google Account](https://accounts.google.com/) |
| Google Drive | ✅ Yes | FAQ JSON file hosting and change detection | [Google Drive](https://drive.google.com/) |
| Qdrant DB | ✅ Yes (Self-Hosted) | Vector database for FAQ embeddings | Included via Docker Compose |
| n8n | ✅ Yes (Self-Hosted) | Workflow automation platform | Included via Docker Compose |

---

### 🔑 Credentials Checklist

Ensure you have the following credentials ready before configuring n8n:

#### Gmail (OAuth2)
- [ ] Google Cloud Project created
- [ ] Gmail API enabled
- [ ] OAuth2 Client ID and Client Secret
- [ ] Redirect URI configured: `http://localhost:5678/rest/oauth2-credential/callback`
- [ ] Gmail scope: `https://mail.google.com/`

> 📘 **Guide:** [n8n Gmail OAuth2 Setup](https://docs.n8n.io/integrations/builtin/credentials/google/)

#### Google Drive (OAuth2)
- [ ] Same Google Cloud Project (reuse Gmail credentials or create separate)
- [ ] Google Drive API enabled
- [ ] OAuth2 Client ID and Client Secret
- [ ] File ID of the FAQ JSON file in Google Drive

> 📘 **Guide:** [n8n Google Drive Credentials](https://docs.n8n.io/integrations/builtin/credentials/google/)

#### Qdrant DB
- [ ] Host: `qdrant` (Docker service name) or `localhost`
- [ ] Port: `6333` (default REST API)
- [ ] API Key: *(optional for self-hosted, leave blank or configure in docker-compose)*

#### LM Studio (OpenAI-Compatible API)
- [ ] API Key: any placeholder string (e.g., `lm-studio`)
- [ ] Base URL: `http://<YOUR_IP>:1234/v1`

> ⚠️ **Note:** LM Studio does not enforce API key validation. Any non-empty string works.

---

### 📁 FAQ JSON File Format

The FAQ data file hosted on Google Drive must follow this structure:

```json
{
  "data": [
    {
      "id": 1,
      "topic": "Admissions",
      "question": "What are the admission requirements?",
      "answer": "Applicants must have completed their secondary education with a minimum GPA of 3.0..."
    },
    {
      "id": 2,
      "topic": "Fees & Finance",
      "question": "How do I apply for a scholarship?",
      "answer": "Scholarship applications open every March. You can apply via the student portal..."
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

> ⚠️ **Important:** The embedding is generated from `[topic] question` format (e.g., `[Admissions] What are the admission requirements?`). Ensure topics are concise and descriptive.

---

### 🌐 Network Configuration

| Service | Local URL | Port | Access Method |
|---------|-----------|------|---------------|
| n8n | `http://localhost:5678` | 5678 | Browser |
| Qdrant REST API | `http://localhost:6333` | 6333 | API / Browser Dashboard |
| Qdrant Dashboard | `http://localhost:6333/dashboard` | 6333 | Browser |
| LM Studio | `http://<YOUR_IP>:1234/v1` | 1234 | API only |

> ⚠️ **Important:** Use your machine's actual local IP (e.g., `192.168.1.x`) in the LM Studio Base URL — not `localhost` — as Docker containers resolve `localhost` to themselves, not your host machine.

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
# Clone the repo
git clone https://github.com/<your-username>/automated-email-query-resolution.git

# Navigate to the project directory
cd automated-email-query-resolution
```

---

### 2️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Qdrant Collection Name
QDRANT_COLLECTION=university_faq

# n8n Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_secure_password

# Qdrant Configuration
QDRANT_PORT=6333
```

> ⚠️ **Important:** The `QDRANT_COLLECTION` value is referenced by both the ingestion and email response workflows. Ensure it is consistent.

---

### 3️⃣ Configure Docker Compose

Review the `docker-compose.yml` to ensure ports and service names match your environment:

```yaml
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=${N8N_BASIC_AUTH_ACTIVE}
      - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - qdrant

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  n8n_data:
  qdrant_data:
```

---

### 4️⃣ Start Docker Containers

Ensure Docker Desktop is running, then start all services:

```bash
docker compose up -d
```

This will spin up:

| Service | URL | Purpose |
|---------|-----|---------|
| n8n | `http://localhost:5678` | Workflow automation platform |
| Qdrant | `http://localhost:6333` | Vector database |
| Qdrant Dashboard | `http://localhost:6333/dashboard` | Visual database management |

**Verify containers are running:**

```bash
docker compose ps
```

Expected output:

```
NAME         STATUS    PORTS
n8n          running   0.0.0.0:5678->5678/tcp
qdrant       running   0.0.0.0:6333->6333/tcp
```

---

### 5️⃣ Start LM Studio Server

1. Open **LM Studio** application
2. Load `mxbai-embed-large-v1` model
3. Load `llama-3.2-3b-instruct` model
4. Navigate to the **Local Server** tab
5. Click **Start Server** (default port: `1234`)
6. Note your local machine IP (e.g., `192.168.1.100`)

> ⚠️ Keep LM Studio running throughout usage. Both workflows depend on the local server being active.

---

### 6️⃣ Access n8n Interface

Open your browser and navigate to:

```
http://localhost:5678
```

Log in with the credentials configured in your `.env` file.

---

### 7️⃣ Import the Workflows

Import both workflow files into n8n:

1. Click the **`...`** menu (top-right corner)
2. Select **Import from File**
3. Import `workflows/vectordb-ingestion.json`
4. Repeat and import `workflows/email-response-automation.json`

---

### 8️⃣ Configure Credentials in n8n

Set up all required credentials:

| Credential | Navigation | Required Values |
|------------|------------|-----------------|
| **Gmail OAuth2** | Settings → Credentials → Add → Gmail OAuth2 API | Client ID, Client Secret |
| **Google Drive OAuth2** | Settings → Credentials → Add → Google Drive OAuth2 API | Client ID, Client Secret |
| **Qdrant** | Settings → Credentials → Add → Qdrant | Host: `qdrant`, Port: `6333` |
| **LM Studio (HTTP)** | Settings → Credentials → Add → Header Auth | API Key placeholder |

> 📘 Refer to [Prerequisites → Credentials Checklist](#-credentials-checklist) for detailed setup instructions.

---

### 9️⃣ Update Workflow Parameters

Open each imported workflow and update the following nodes:

**VectorDB Ingestion Workflow:**

| Node | Parameter | Value |
|------|-----------|-------|
| **Google Drive Trigger** | File ID | Your FAQ JSON file ID from Google Drive |
| **Download File** | File ID | Same FAQ JSON file ID |
| **Fetch Collection Name** | Variable | Reads from `.env` `QDRANT_COLLECTION` |
| **Embedding Generation** | URL | `http://<YOUR_IP>:1234/v1/embeddings` |

**Email Response Automation Workflow:**

| Node | Parameter | Value |
|------|-----------|-------|
| **Gmail Trigger** | Credentials | Your configured Gmail OAuth2 credential |
| **Query Embedding** | URL | `http://<YOUR_IP>:1234/v1/embeddings` |
| **Message a Model** | Base URL | `http://<YOUR_IP>:1234/v1` |
| **Send Reply Email** | Credentials | Your configured Gmail OAuth2 credential |

---

### 🔟 Activate the Workflows

1. Open the **VectorDB Ingestion** workflow → Toggle **Active** switch → Confirm **Active** (green)
2. Open the **Email Response Automation** workflow → Toggle **Active** switch → Confirm **Active** (green)

---

### ✅ Setup Complete!

Your system is now live. Upload or update your FAQ JSON file in Google Drive and send a test email to your configured Gmail address to see the pipeline in action! 🎉

> 💡 Head over to [📘 Usage](#-usage) to learn how to test and manage the system.

---

## 📘 Usage

### 🎯 User Entry Points

| User Type | Entry Point | Purpose |
|-----------|-------------|---------|
| **Admin** | Google Drive (FAQ JSON file) | Update FAQ knowledge base |
| **End User** | Email (Gmail address) | Send queries to the system |
| **Admin** | n8n Interface (`localhost:5678`) | Monitor and manage workflows |
| **Admin** | Qdrant Dashboard (`localhost:6333/dashboard`) | Inspect stored vector points |

---

### 1️⃣ Updating the FAQ Knowledge Base

To update the knowledge base, simply edit and save the FAQ JSON file in Google Drive.

The ingestion workflow runs **daily** and will automatically detect changes:

1. Log in to [Google Drive](https://drive.google.com/)
2. Navigate to your FAQ JSON file
3. Edit the file — add, update, or remove FAQ entries
4. Save the file
5. The n8n workflow will detect the change and re-ingest all data

**FAQ Entry Format:**

```json
{
  "id": 42,
  "topic": "Library Services",
  "question": "What are the library opening hours?",
  "answer": "The university library is open Monday to Friday from 8:00 AM to 10:00 PM, and on weekends from 10:00 AM to 6:00 PM."
}
```

> 💡 **Tip:** The `topic` field directly influences embedding quality. Use clear, consistent topic names like `Admissions`, `Fees & Finance`, `Campus Life`, `Academic Calendar`, etc.

---

### 2️⃣ Sending Queries via Email

End users simply send an email to the configured Gmail address:

| Field | Example |
|-------|---------|
| **To** | `university-faq@gmail.com` |
| **Subject** | `Question about scholarship application` |
| **Body** | `Hi, I wanted to know when scholarship applications open and what the requirements are. Thank you.` |

The system will:
1. Detect the incoming email
2. Embed the email body
3. Search for the top 3 matching FAQs (score ≥ 0.7)
4. Generate a personalised HTML reply using the LLM
5. Send the reply within the same email thread

---

### 3️⃣ Testing the Workflow

**Test the Ingestion Pipeline:**

1. Ensure LM Studio server is running with both models loaded
2. Open n8n at `http://localhost:5678`
3. Open the **VectorDB Ingestion** workflow
4. Click **Test Workflow** to trigger a manual run
5. Verify each node executes successfully (green checkmarks)
6. Visit `http://localhost:6333/dashboard` to confirm vectors were upserted

**Test the Email Response Pipeline:**

1. Send a test email to your configured Gmail address
2. Monitor the **Email Response Automation** workflow execution in n8n
3. Verify the reply arrives in your inbox

**Sample Test Emails:**

| Scenario | Email Body | Expected Behaviour |
|----------|-----------|-------------------|
| Direct FAQ match | `What documents do I need for admission?` | Top 3 admission-related FAQs retrieved, LLM generates detailed reply |
| Ambiguous query | `Can you help me with fees?` | Fee-related FAQs retrieved, LLM crafts relevant response |
| Low relevance query | `What is the meaning of life?` | No results above 0.7 threshold, LLM responds with fallback message |

---

### 4️⃣ Expected Outputs

**Ingestion Pipeline — Success Indicators:**

| Check | Location | What to Expect |
|-------|----------|----------------|
| Collection created | Qdrant Dashboard | Collection named `university_faq` visible |
| Points upserted | Qdrant Dashboard → Collection → Points | All FAQ entries visible as vector points |
| Payload stored | Click any point | `id`, `topic`, `question`, `answer`, `embeddingText` fields present |

**Email Response Pipeline — Success Indicators:**

| Check | Location | What to Expect |
|-------|----------|----------------|
| Workflow execution | n8n Execution History | All nodes green, no errors |
| Similarity results | `Similarity Search` node output | 1–3 results with scores ≥ 0.7 |
| LLM response | `Message a Model` node output | HTML-formatted email content |
| Reply received | Sender's inbox | Formatted HTML reply within original email thread |

**Sample Outbound Email Structure:**

```html
<!DOCTYPE html>
<html>
  <body>
    <p>Dear [Student Name],</p>
    <p>Thank you for reaching out to us. Based on your query, here is the information we have for you:</p>

    <!-- LLM-generated response based on top 3 FAQ matches -->
    <p>[Generated response incorporating matched FAQ answers]</p>

    <p>If you have further questions, feel free to reply to this email.</p>
    <p>Best regards,<br/>University Support Team</p>
  </body>
</html>
```

---

### 5️⃣ Monitoring Workflows

**Check Workflow Execution History:**

1. Open n8n at `http://localhost:5678`
2. Navigate to **Executions** (left sidebar)
3. Filter by workflow name to view individual run histories
4. Click any execution to inspect node-level input/output data

**Monitor Qdrant Collection:**

1. Open Qdrant Dashboard at `http://localhost:6333/dashboard`
2. Select your collection (e.g., `university_faq`)
3. View total points count, vector dimensions, and distance metric
4. Use the **Search** tab to manually test similarity queries

---

### 6️⃣ Managing the System

**Stop all services:**

```bash
docker compose down
```

**Restart all services:**

```bash
docker compose up -d
```

**View live container logs:**

```bash
# All services
docker compose logs -f

# n8n only
docker compose logs -f n8n

# Qdrant only
docker compose logs -f qdrant
```

**Manually trigger the ingestion workflow:**

1. Open n8n at `http://localhost:5678`
2. Open the **VectorDB Ingestion** workflow
3. Click **Test Workflow** button (top right)

---

### 7️⃣ Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Ingestion workflow not triggering | Google Drive API not authorised | Re-authorise Google Drive OAuth2 credentials in n8n |
| Embeddings not generating | LM Studio server not running | Start LM Studio and load `mxbai-embed-large-v1` |
| Qdrant upsert failing | Container not running or wrong host | Run `docker compose up -d`, verify `qdrant` service |
| No email trigger | Gmail OAuth2 expired or wrong scope | Re-authenticate Gmail credentials with correct scope |
| Similarity search returns no results | Score threshold too high or poor query match | Check embedding quality; verify FAQ data covers the topic |
| LLM response not generated | `llama-3.2-3b-instruct` not loaded in LM Studio | Load the model in LM Studio before activating workflow |
| Reply sent to wrong thread | Incorrect `Message ID` in Send Reply node | Verify `email_id` is correctly extracted in `Fields Preparation` node |
| Docker containers not starting | Port conflict on 5678 or 6333 | Change port mappings in `docker-compose.yml` |

---

### 8️⃣ Qdrant Collection Inspection

Use the Qdrant REST API to inspect your collection directly:

```bash
# List all collections
curl http://localhost:6333/collections

# Get collection info
curl http://localhost:6333/collections/university_faq

# Count total points
curl http://localhost:6333/collections/university_faq/points/count

# Manually search with a vector (replace [...] with actual 1024-dim vector)
curl -X POST http://localhost:6333/collections/university_faq/points/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [...],
    "limit": 3,
    "score_threshold": 0.7,
    "with_payload": true
  }'
```
