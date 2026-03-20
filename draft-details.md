## Project Details

### Project Name

Automated Email Query Resolution System

### High-Level Overview

User can upload data into a folder in Google Drive. It will automatically create the embeddings and upsert the the Vector Database. When the user receives an email to the specified address, the system automatically fetches the email body, perform similarity search with the embedded data, retrieve similarity points and prepare the response using LLM and send back a formatted response in the reply email. The embedding data is mainly a FAQ pairs from a university where all types of possible queries are covered.

### Tech Stacks

- Automation Tool:
  - n8n
  - Self-Hosted
- Vector Database:
  - QDrant DB
  - Self-Hosted
- Embedding Model:
  - text-embedding-mxbai-embed-large-v1
  - Host: LM Studio
- LLM:
  - llama-3.2-3b-instruct
  - Host: LM Studio
- Hosting:
  - Using docker-compose.yml and docker
- Email Service: Gmail

### In Depth Explanation

The whole system consists of 2 parts.

- The VectorDB Datapoints Ingestion
- The Email Response Automation

Let's describe both the parts.

### The VectorDB Datapoints Ingestion

We are using `Google Drive` trigger. It gets triggered on changes to the specified file. The File is specified using `ID`. The file is in `JSON` format. Each Data point within the list is a python dict. Each dict consists of 4 key-value pairs, id, topic, question, answer. The trigger runs everyday, to check for changes. If any changes found, it gets triggered. After the trigger, 2 combinations run in parallel.

The first part combinely perform the collection creation.

- The `Fetch Collection Name` is a Javascript Code node. It fetches the collection name defined using `QDRANT_COLLECTION` variable in the .env file.
- The `Check If Collection Exists` checks if the collection exists in the QdrantDB.
- Based on the previous node result, there are 2 paths defined from `If` node,
- If the collection exists, then the `Delete Collection` node, deletes the collection.
- Then it creates the collection with the name using `Create Collection` node with the vectors settings of size to 1024 and distance to Cosine.
- If the collection doesn't exist, then it directly creates the collection with the `Create Collection` node, with the mentioned vector settings.

The second part downloads the JSON, generate embeddings and insert points to the created collection.

- The `Download File` node, downloads the JSON file using the specified file ID,
- The `Extract from File` node, converts the Binary to JSON.
- The `Data Fetch` node, fetches the array of data within the `data` field.
- The `Data Preprocessing` node, fetches the array. It along with the keys id, topic, question and answer, it creates a 2 new key-value pairs, one is the `embeddingText` which is created using `[topic] question` format for actual embedding, and another one is `collection` whose value is the collection name. This is done for all the points and pushed to the array and passed to the next node.
- The `Embedding Generation` is a HTTP post request node, which sends the embdedding request to to the locally hosted embedding server with the `embeddingText`.
- Finally `Upsert Points` inserts the vector points to the created collection. It consists of `id`, `payload` and `vector`. `id` is the actual data id from the json. The `payload` is the metadata consists of data key-value pairs. The id, topic, question, answer and the embeddingText. The `vector` is the actual embeeding generated from the server.

### Email Response Automation

- The `Gmail Trigger` gets triggered on when a new email is recieved in the gmail.
- `Fields Preparation` node extracts the fields `from`, `name`, `to`, `email_id`, `thread_id`, `subject` and `email_body`.
- The `Query Embedding` node sends an embed request to the same embedding model hosting server to generate the vector embedding of the email body.
- The `Collection Name Fetch` node fetches the collection name defined in `.env`.
- The `Merge` node, combines the output from embedding and collection name fetching nodes.
- The `Similarity Search` node, performs simiarity search across the vector collection in respect to the embedded query. The score threshold is 0.7 and the search result is limit to 3.
- In the `Message a model` node, there is a system prompt defined, to prepare a user-friendly response, based on the given user input data. As a user message, the `name`, `email_body` and the 3 answer's `score`, `topic`, `question` and `answer` is passed. Consuming these data, the `llama-3.2-3b-instruct` generates a response email with the `html` elements.
- The `Email Format` is a formation node, where the response email is merged with the pre-defined template.
- The `Send Reply Email` takes the response email and replies back to the same email thread with the `Message ID` defined.

This is the whole system designed.

## TASK
Generate the following sections
- Title & Badges
- Overview
- Key Features
- Tech Stack
- Automation Flow
- Prerequisites
- Quick Start
- Usage

analyzing the given project details.

## EXAMPLE
- Take the following example as the reference to generate `readme.md`.
- 
``````
<div align="center">

#  🔗 AI-Powered Customer Feedback Automation

### End-to-End Feedback Processing with AI Analysis & Intelligent Routing

<!-- Tech Stack -->
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat-square&logo=n8n&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Tally.so](https://img.shields.io/badge/Tally.so-4F46E5?style=flat-square&logo=tally&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-5865F2?style=flat-square&logo=discord&logoColor=white)

<!-- AI/ML Stack -->
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Qwen2--VL-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![LM Studio](https://img.shields.io/badge/LM_Studio-6366F1?style=flat-square&logo=ai&logoColor=white)

<!-- Status & License -->
![Status](https://img.shields.io/badge/Status-Active-28A745?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-3DA639?style=flat-square&logo=opensourceinitiative&logoColor=white)
![Local](https://img.shields.io/badge/Deployment-Local-FF6B6B?style=flat-square)

</div>

## ✨ Key Features

- 📝 **Public Feedback Collection** — Collect customer feedback via shareable Tally.so forms (Name, Email, Feedback, optional Image)
- ⚡ **Instant Webhook Processing** — Submissions trigger the workflow in real-time with zero delays
- 🧠 **AI-Powered Sentiment Analysis** — Automatically detect customer sentiment (Positive, Negative, Neutral) using local LLM
- 🏷️ **Zero-Shot Text Classification** — Categorize feedback into pre-defined labels without model training
- 🖼️ **Multimodal Image Analysis** — Extract keywords from uploaded images using Qwen2-VL vision capabilities
- 🔀 **Intelligent Channel Routing** — AI-driven decisions to route feedback to appropriate Discord channels
- 💾 **Automated Data Storage** — All processed feedback stored in PostgreSQL with structured schema
- 💬 **Real-Time Discord Alerts** — Instant embed notifications with feedback details and AI insights
- 🏠 **Fully Local AI Processing** — Privacy-first approach with on-device LLM inference via LM Studio
- 🐳 **Dockerized Deployment** — One-command setup using Docker Compose for PostgreSQL, Adminer, and n8n
- 💸 **100% Free & Open Source** — Built entirely on free-tier services and open-source tools with no ongoing costs

## 🛠️ Tech Stack

| Category | Technology | Description | Link |
|----------|------------|-------------|------|
| **Workflow Automation** | n8n Community Edition | Self-hosted workflow orchestration for form processing, AI analysis, and routing | [n8n.io](https://docs.n8n.io/hosting/) |
| **Form Handling** | Tally.so | Free form builder for public feedback collection (Name, Email, Feedback, optional Image) | [tally.so](https://tally.so/) |
| **AI/ML Inference** | OpenAI Node + LM Studio + Qwen2-VL-7B-Instruct | n8n's OpenAI node configured with custom Base URL pointing to LM Studio's local server hosting Qwen2-VL (GGUF, Q4_K_M).<br><br>Tasks:<br>• Sentiment analysis<br>• Zero-shot text classification<br>• Image keyword extraction<br>• Intelligent routing decisions | [OpenAI Node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.lmchatopenai/) / [LM Studio](https://lmstudio.ai/) / [Qwen2-VL](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct) |
| **Database** | PostgreSQL + Adminer | Relational database for storing processed feedback with lightweight management UI | [PostgreSQL](https://hub.docker.com/_/postgres) / [Adminer](https://www.adminer.org/) |
| **Notifications** | Discord | Channel-based routing for customer feedback to relevant team channels | [discord.com](https://discord.com/) |
| **Containerization** | Docker + Docker Compose | Multi-container orchestration for PostgreSQL, Adminer, and n8n via `docker-compose.yml` | [Docker](https://www.docker.com/) / [Compose](https://docs.docker.com/compose/) |

## 🔄 Automation Flow
```text
                      User submits feedback form (Tally.so)
                                      ↓
                              Tally Trigger
                                      ↓
                               Field Mapping
                                      ↓
        ┌─────────────────────────────┼─────────────────────────────┐
        ↓                             ↓                             ↓
   Sentiment                       Text                        Fetch Image
   Analysis                    Classification                       ↓
        ↓                             ↓                    ┌────────┴────────┐
   Sentiment                   Classification              ↓                 ↓
      LLM                            LLM              Has Image?        No Image?
        ↓                             ↓                    ↓                 ↓
   Sentiment                   Classification           Image            Empty
    Parser                        Parser              Keyword           Keywords
        ↓                             ↓              Extraction          Handler
        │                             │                    ↓                 ↓
        │                             │                    └────────┬────────┘
        │                             │                             ↓
        │                             │                    Image Results Merge
        │                             │                             ↓
        └─────────────────────────────┴─────────────────────────────┘
                                      ↓
                              AI Results Merge
                                      ↓
                              Data Aggregation
                                      ↓
                             Save to PostgreSQL
                                      ↓
                               Decision Logic
                                      ↓
                                Routing LLM
                                      ↓
                                Route Parser
                                      ↓
                               Channel Router
                                      ↓
          ┌───────────────────────────┼───────────────────────────┐
          ↓                           ↓                           ↓
 #general-inquiries           #happy-customers           #support-urgent
          ↓                           ↓                           ↓
          └───────────────────────────┴───────────────────────────┘
                                      ↓
                           Build Discord Message
                                      ↓
                             Format Embed Data
                                      ↓
                         Send Discord Notification
```

## 📋 Prerequisites

Before you begin, make sure you have the following set up:

---

### 🖥️ Software Requirements

| Software  | Version          | Purpose                                      | Installation Guide                                                   |
| --------- | ---------------- | -------------------------------------------- | -------------------------------------------------------------------- |
| Docker    | 28.5.1+          | Container runtime for services               | [Install Docker](https://docs.docker.com/get-docker/)                |
| n8n       | 1.121.3 (latest) | Workflow automation platform                 | [n8n Docker Setup](https://docs.n8n.io/hosting/installation/docker/) |
| LM Studio | 0.3.36+          | Local LLM hosting with OpenAI-compatible API | [Download LM Studio](https://lmstudio.ai/)                           |

---

**Verify Installation:**

```bash
# Check Docker
docker --version
# Expected: Docker version 28.0.0 or higher
```

---

### 🤖 LM Studio Setup

| Requirement  | Details                       |
| ------------ | ----------------------------- |
| Model        | Qwen2-VL-7B-Instruct          |
| Format       | GGUF                          |
| Quantization | Q4_K_M                        |
| Server Port  | 1234 (default)                |
| Base URL     | `http://192.168.56.1:1234/v1` |

**Setup Steps:**

- [ ] Download and install LM Studio
- [ ] Download `Qwen2-VL-7B-Instruct` model (GGUF, Q4_K_M quantization)
- [ ] Load the model in LM Studio
- [ ] Start the local server (default port: 1234)
- [ ] Note your machine's IP address for Base URL configuration

> 📘 **Guide:** [LM Studio Local Server Setup](https://lmstudio.ai/docs/developer/core/server)

---

### 🔐 Account & API Requirements

| Service    | Free Tier      | Purpose                                 | Signup / Setup                        |
| ---------- | -------------- | --------------------------------------- | ------------------------------------- |
| Tally.so   | ✅ Yes          | Form builder for feedback collection    | [Create Account](https://tally.so/)   |
| Discord    | ✅ Yes          | Team notifications & channel routing    | [Create Server](https://discord.com/) |
| PostgreSQL | ✅ Yes (Docker) | Database for storing processed feedback | Included via Docker Compose           |
| Adminer    | ✅ Yes (Docker) | Database management UI                  | Included via Docker Compose           |

---

### 🔑 Credentials Checklist

Ensure you have the following credentials ready before configuring n8n:

#### Tally.so
- [ ] API Key (for webhook authentication)
- [ ] Allowed HTTP Request Domains: `All`

> 📘 **Guide:** [Getting your Tally API Key](https://tally.so/help/n8n-integration)

#### OpenAI Node (LM Studio)
- [ ] API Key (can be any string, e.g., `lm-studio` or dummy key)
- [ ] Base URL: `http://<YOUR_IP>:1234/v1`
- [ ] Organization ID: *(optional, leave blank)*
- [ ] Allowed HTTP Request Domains: `All`

> ⚠️ **Note:** Since you're using LM Studio locally, the API Key can be any placeholder value. The Base URL must point to your LM Studio server.

#### Discord Bot
- [ ] Bot Token (`MTI...`)
- [ ] Allowed HTTP Request Domains: `All`
- [ ] Bot Permissions: `Send Messages`, `Embed Links`
- [ ] Bot added to your Discord server

> 📘 **Guide:** [Creating a Discord Bot](https://discord.com/developers/docs/getting-started)


#### PostgreSQL
- [ ] Host: `db` (Docker service name)
- [ ] Database: `postgres`
- [ ] User: `<user_name>`
- [ ] Password: `<password>`
- [ ] Port: `5432` (default)

> 📘 **Note:** These credentials are configured in your `docker-compose.yml` file.

---

### 📁 Required Setup

Before running the workflow, ensure the following are created:

#### Tally.so Form
- [ ] Create a form with the following fields:

| Field Name | Type        | Required |
| ---------- | ----------- | -------- |
| Name       | Text        | ✅ Yes    |
| Email      | Email       | ✅ Yes    |
| Feedback   | Long Text   | ✅ Yes    |
| Image      | File Upload | ❌ No     |

- [ ] Publish the form and copy the **Form ID** from the URL
- [ ] Configure webhook to point to your n8n instance

#### Discord Server
- [ ] Create a Discord server (or use existing)
- [ ] Create the following channels:

| Channel Name         | Purpose                           |
| -------------------- | --------------------------------- |
| `#general-inquiries` | General feedback & questions      |
| `#happy-customers`   | Positive feedback & testimonials  |
| `#support-urgent`    | Urgent issues & negative feedback |

- [ ] Note the **Channel IDs** for each channel
- [ ] Add your Discord Bot to the server

> 💡 **Tip:** To get Channel ID, enable Developer Mode in Discord settings, then right-click channel → Copy ID

#### PostgreSQL Database
- [ ] Database and table will be auto-created via Docker Compose
- [ ] Verify connection using Adminer at `http://localhost:8080`

---

### 🌐 Network Configuration

| Service   | Local URL                     | Port | Access Method                   |
| --------- | ----------------------------- | ---- | ------------------------------- |
| n8n       | `http://localhost:5678`       | 5678 | Browser                         |
| Adminer   | `http://localhost:8080`       | 8080 | Browser (PostgreSQL management) |
| LM Studio | `http://192.168.56.1:1234/v1` | 1234 | API only                        |

> ⚠️ **Important:** PostgreSQL runs on port `5432` but is not browser-accessible. Use Adminer at `localhost:8080` to manage your database.

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
# Clone the repo
git clone https://github.com/Neloy-Barman/AI-Powered-Customer-Feedback-Automation.git

# Navigate to the project directory
cd AI-Powered-Customer-Feedback-Automation
```

---

### 2️⃣ Configure Docker Environment

Before starting the containers, configure your PostgreSQL credentials in `docker-compose.yml`:

```yaml
# Open docker-compose.yml and update these values
services:
  db:
    environment:
      POSTGRES_USER: <user_name>        # Preferred username
      POSTGRES_PASSWORD: <password>     # Set a secure password
      POSTGRES_DB: postgres             # Database Name
```

> ⚠️ **Important:** Remember these credentials — you'll need them when configuring n8n PostgreSQL connection.

---

### 3️⃣ Start Docker Containers

Ensure Docker Desktop is running in the background, then start the containers:

```bash
# Start the containers in detached mode
docker compose up -d
```

This will spin up:

| Service    | URL                     | Purpose                |
| ---------- | ----------------------- | ---------------------- |
| n8n        | `http://localhost:5678` | Workflow automation    |
| Adminer    | `http://localhost:8080` | Database management UI |
| PostgreSQL | Port `5432`             | Data storage           |

> 💡 Check container logs in Docker Desktop GUI to confirm successful startup.

**Verify PostgreSQL is Running:**

Access Adminer at `http://localhost:8080` and login with:

| Field    | Value                                      |
| -------- | ------------------------------------------ |
| System   | PostgreSQL                                 |
| Server   | `db`                                       |
| Username | `<user_name>` (or your configured username)   |
| Password | `<password>` (your configured password) |
| Database | `postgres` (or your configured database)   |

---

### 3️⃣ Start LM Studio Server

1. Open LM Studio application
2. Load `Qwen2-VL-7B-Instruct` model (GGUF, Q4_K_M)
3. Navigate to **Local Server** tab
4. Click **Start Server** (default port: `1234`)
5. Note your machine's IP address (e.g., `192.168.56.1`)

> ⚠️ Ensure the server is running before activating the n8n workflow.

---

### 4️⃣ Access n8n Interface

Open your browser and navigate to:

```
http://localhost:5678
```

Create an account or log in if prompted.

---

### 5️⃣ Import the Workflow

1. Click the **`...`** menu in the top-right corner
2. Select **Import from File**
3. Choose `AI-Customer-Feedback-Automation.json` from the `workflows` directory

---

### 6️⃣ Configure Credentials

Set up the required credentials in n8n:

| Credential     | Navigation                                 | Required Values                                                  |
| -------------- | ------------------------------------------ | ---------------------------------------------------------------- |
| **Tally.so**   | Settings → Credentials → Add → Tally       | API Key                                                          |
| **OpenAI**     | Settings → Credentials → Add → OpenAI      | API Key (any placeholder), Base URL (`http://<YOUR_IP>:1234/v1`) |
| **PostgreSQL** | Settings → Credentials → Add → Postgres    | Host: `db`, Database: `postgres`, User, Password                  |
| **Discord**    | Settings → Credentials → Add → Discord Bot | Bot Token                                                        |

> 📘 Refer to [Prerequisites](#-prerequisites) for detailed credential setup guides.

---

### 7️⃣ Set Up Discord Server

Create the following channels in your Discord server:

| Channel Name         | Purpose                           |
| -------------------- | --------------------------------- |
| `#general-inquiries` | General feedback & questions      |
| `#happy-customers`   | Positive feedback & testimonials  |
| `#support-urgent`    | Urgent issues & negative feedback |

Then update the workflow nodes with corresponding Channel IDs.

> 💡 **Tip:** Enable Developer Mode in Discord (Settings → Advanced), then right-click channel → Copy ID

---

### 8️⃣ Create Tally.so Form

Create a public form with the following fields:

| Field Name | Type        | Required |
| ---------- | ----------- | -------- |
| Name       | Text        | ✅ Yes    |
| Email      | Email       | ✅ Yes    |
| Feedback   | Long Text   | ✅ Yes    |
| Image      | File Upload | ❌ No     |

Publish the form and connect it to the workflow trigger.

---

### 9️⃣ Update Workflow Parameters

Open the imported workflow and update these nodes:

| Node                   | Parameter   | Value                       |
| ---------------------- | ----------- | --------------------------- |
| **Tally Trigger**      | Form        | Select your Tally form      |
| **Channel Router**     | Channel IDs | Your Discord channel IDs    |
| **Save to PostgreSQL** | Credentials | Your PostgreSQL credentials |

---

### 🔟 Activate the Workflow

1. Toggle the **Active** switch in the top-right corner
2. Status should show **Active** (green)

---

### ✅ Setup Complete!

Your automation is now live. Submit a test feedback through your Tally.so form and watch the magic happen! ✨

> 💡 Head over to [📘 Usage](#-usage) to learn how to test and manage the workflow.

## 📘 Usage

### 🎯 User Entry Points

| User Type    | Entry Point                      | Purpose                               |
| ------------ | -------------------------------- | ------------------------------------- |
| **Customer** | Tally.so Form URL                | Submit feedback with optional image   |
| **Admin**    | n8n Interface (`localhost:5678`) | Monitor and manage workflow           |
| **Admin**    | Adminer (`localhost:8080`)       | View and manage database records      |
| **Team**     | Discord Channels                 | Receive routed feedback notifications |

---

### 1️⃣ Submitting Feedback

Share your Tally.so form URL publicly. Customers fill in the following:

| Field    | Type        | Required | Example                                         |
| -------- | ----------- | -------- | ----------------------------------------------- |
| Name     | Text        | ✅ Yes    | `Jane Smith`                                    |
| Email    | Email       | ✅ Yes    | `jane.smith@example.com`                        |
| Feedback | Long Text   | ✅ Yes    | `The product quality exceeded my expectations!` |
| Image    | File Upload | ❌ No     | `damaged_product.jpg`                           |

> 💡 The **Feedback** content determines sentiment, classification, and channel routing automatically.

---

### 2️⃣ Testing the Workflow

To verify everything works correctly:

1. Ensure LM Studio server is running with model loaded
2. Open n8n interface at `http://localhost:5678`
3. Open the **AI-Powered-Customer-Feedback-Automation** workflow
4. Click on each node sequentially
5. Click **Test Step** to execute individually
6. Verify outputs at each stage

**Sample Test Data:**

| Scenario | Name       | Email                  | Feedback                                      | Expected Channel     |
| -------- | ---------- | ---------------------- | --------------------------------------------- | -------------------- |
| Positive | Jane Smith | jane.smith@example.com | The product quality exceeded my expectations! | `#happy-customers`   |
| Negative | John Doe   | john.doe@example.com   | I got a broken iPhone delivered at my home.   | `#support-urgent`    |
| Neutral  | Alex Brown | alex.brown@example.com | Are you guys available at 12:00 pm?           | `#general-inquiries` |

---

### 3️⃣ Expected Outputs

After a successful submission:

| Output              | Location                 | What to Expect                           |
| ------------------- | ------------------------ | ---------------------------------------- |
| **Database Record** | PostgreSQL (via Adminer) | New row with feedback and AI analysis    |
| **Discord Message** | Routed channel           | Embed notification with feedback details |

**Database Record Structure:**

| Column         | Example Value                                 |
| -------------- | --------------------------------------------- |
| id             | `1`                                           |
| name           | `John Doe`                                    |
| email          | `john.doe@example.com`                        |
| feedback       | `I got a broken iPhone delivered at my home.` |
| sentiment      | `Negative`                                    |
| category       | `Product Quality & Features`                  |
| image_keywords | `broken, cracked, or damaged product`         |
| img_url        | `https://tally.so/uploads/image123.jpg`       |

**Discord Notifications:**

**Positive Feedback → `#happy-customers`**
```
🎉 Happy Customer Alert
Positive feedback from a satisfied customer.

👤 Customer Info
Jane Smith (jane.smith@example.com)

✉️ Feedback
The product quality exceeded my expectations!

📝 Model Analysis
Customer Jane Smith praises our service, noting that it exceeded their expectations.

📝 Automated Feedback Summary
```

**Neutral Feedback → `#general-inquiries`**
```
🔹 General Feedback Alert
A new general feedback or inquiry has been received.

👤 Customer Info
Alex Brown (alex.brown@example.com)

✉️ Feedback
Are you guys available at 12:00 pm?

📝 Model Analysis
Customer Alex Brown inquires about availability at 12:00 pm.

📝 Automated Feedback Summary
```

**Negative Feedback → `#support-urgent`**
```
⚠️ Urgent Support Required
Immediate attention needed for this customer feedback.

👤 Customer Info
John Doe (john.doe@example.com)

✉️ Feedback
I got a broken iPhone delivered at my home.

📝 Model Analysis
Customer John Doe reports a broken iPhone delivered at their home, requiring immediate resolution to prevent further inconvenience.

📝 Automated Feedback Summary
```

---

### 4️⃣ AI Processing Details

Each submission undergoes the following analysis:

**Sentiment Analysis:**

| Output     | Description                                 |
| ---------- | ------------------------------------------- |
| `Positive` | Satisfied customer, praise, recommendations |
| `Negative` | Complaints, issues, urgent problems         |
| `Neutral`  | General questions, inquiries                |

**Text Classification Categories:**

| Category                      | Description                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------- |
| `Product Quality & Features`  | Comments about product performance, durability, functionality, or characteristics     |
| `Shipping & Delivery`         | Issues or feedback about shipping speed, packaging, delivery experience, or logistics |
| `Customer Support Experience` | Interactions with support team, response times, helpfulness of staff                  |
| `Pricing & Billing`           | Comments about prices, charges, payment issues, value for money                       |
| `Return & Refund Request`     | Requests to return products or get refunds, return policy questions                   |
| `Website / App Usability`     | Navigation issues, checkout problems, app bugs, user interface feedback               |
| `Positive Feedback`           | General satisfaction, compliments, recommendations, praise                            |
| `General Inquiry`             | Questions or comments that don't fit other categories                                 |

**Image Keyword Extraction:**

| Keyword                                                 | Description                        |
| ------------------------------------------------------- | ---------------------------------- |
| `broken, cracked, or damaged product`                   | Product defects or physical damage |
| `damaged or torn packaging`                             | Packaging issues during shipping   |
| `showing wrong item delivery`                           | Incorrect item received            |
| `new and intact product`                                | Product in good condition          |
| `a screenshot of a website or order confirmation`       | Digital proof or reference         |
| `a blurry, dark, or unclear photo`                      | Poor image quality                 |
| `an irrelevant photo (e.g., a person, pet, or scenery)` | Non-related image content          |

**Channel Routing Logic:**

| Sentiment | Routed To            | Alert Type                |
| --------- | -------------------- | ------------------------- |
| Positive  | `#happy-customers`   | 🎉 Happy Customer Alert    |
| Negative  | `#support-urgent`    | ⚠️ Urgent Support Required |
| Neutral   | `#general-inquiries` | 🔹 General Feedback Alert  |

---

### 5️⃣ Success Indicators

✅ Submission successful when:

- [ ] New record appears in PostgreSQL database
- [ ] Discord notification received in correct channel
- [ ] Sentiment correctly identified
- [ ] Category properly classified
- [ ] Image keywords extracted (if image provided)
- [ ] Model analysis summary generated

❌ Something went wrong if:

- [ ] No new record in database
- [ ] No Discord notification
- [ ] Error shown in n8n execution log
- [ ] LM Studio server not responding

**Troubleshooting:**

| Issue                 | Possible Cause            | Solution                            |
| --------------------- | ------------------------- | ----------------------------------- |
| No AI analysis        | LM Studio not running     | Start LM Studio server              |
| Database error        | PostgreSQL container down | Run `docker compose up -d`          |
| No Discord message    | Invalid Bot Token         | Verify Discord credentials          |
| Webhook not triggered | Form not connected        | Check Tally.so integration          |
| Wrong channel routing | Sentiment misclassified   | Check LLM model is loaded correctly |

---

### 6️⃣ Managing the Workflow

**Check Workflow Status:**

1. Open n8n interface at `http://localhost:5678`
2. Locate **AI Customer Feedback Automation** workflow
3. Check the toggle — **Green** = Active, **Gray** = Inactive

**Stop the Workflow:**

```bash
docker compose down
```

**Restart the Workflow:**

```bash
docker compose up -d
```

**View Logs:**

```bash
docker compose logs -f
```

**Access Database:**

1. Open Adminer at `http://localhost:8080`
2. Login with PostgreSQL credentials
3. Navigate to feedback table to view all records

---

### 7️⃣ Monitoring & Analytics

Use Adminer to run queries for insights:

```sql
-- Count feedback by sentiment
SELECT sentiment, COUNT(*) FROM feedback GROUP BY sentiment;

-- Recent negative feedback requiring attention
SELECT * FROM feedback WHERE sentiment = 'Negative' ORDER BY id DESC LIMIT 10;

-- Most common categories
SELECT category, COUNT(*) FROM feedback GROUP BY category ORDER BY COUNT(*) DESC;

-- All feedback with images attached
SELECT * FROM feedback WHERE img_url IS NOT NULL;
```

---

```````

## RESPONSE RETURN FORMAT
Return the response as a `.md` within 5-backticks(`````<generated_content>`````) enforced block.
