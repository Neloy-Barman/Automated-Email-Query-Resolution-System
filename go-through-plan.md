- Dataset Creation. ✅
- Tech Stacks:
  - Automation: n8n
  - Vector Database: QDrant DB
  - Embedding Model: text-embedding-mxbai-embed-large-v1
  - LLM: llama-3.2-3b-instruct
  - Orchestration: docker & docker-compose.yml
  - Email Trigger: Gmail
  - 
- Example Embedding outputs:
  ```
      f"[{topic}] {question}"
      "[Admissions and Applications] How do I apply to Crestwood University?"
      "[Fee Payment and Financial Aid] What is the last date to pay tuition fees?"
      "[IT Support and Student Portal] How do I reset my student portal password?"
  ```
- Square Brackets in Embedding Text — Do They Cause Issues?
  - No. Square brackets [ ] will NOT cause any issues in embedding creation. Here is why:
    - Embedding models are trained on massive text corpora
    - That corpus includes all kinds of special characters including [ ] { } ( ) etc.
    - The tokenizer handles [ ] as regular characters
    - They get tokenized and processed just fine

- MetaData:
  ```
    {
        "id": 1,
        "topic": "Admissions and Applications",
        "question": "How do I apply to Crestwood University?",
        "answer": "You can apply to Crestwood University by visiting
        portal.crestwooduniversity.edu and filling out
        the online application form...",
        "embedding_text": "[Admissions and Applications] How do I
        apply to Crestwood University?"
    }
  ```
- There will be 2 workflows:
  1. Embedding Generation triggered on the data change.
  2. Email Automation triggered on email recieve.
- Embedding Generation:

```
    Step 1 — Upload faq_dataset.json to Google Drive
    → Create a dedicated folder in Drive
    → Example folder name: "AEQRS_Data"
    → Upload your faq_dataset.json there

    Step 2 — Trigger: Google Drive Trigger Node
    → Use n8n "Google Drive Trigger" node
    → Set it to watch your "AEQRS_Data" folder
    → Event: "File Updated" or "File Created"

    Step 3 — Download the Updated File
    → Use "Google Drive" node
    → Operation: "Download File"
    → This gives you the latest JSON content

    Step 4 — Parse the JSON Content
    → Use "Code" node or "Edit Fields" node
    → Parse the downloaded file content
    → Convert to usable JSON array

    Step 5 — Delete Previous Embeddings
    → Vector Store node
    → Delete entire collection/index

    Step 6 — Recreate Empty Collection
    → Vector Store node
    → Create fresh collection

    Step 7 — Loop Through Each FAQ Item
    → "Split In Batches" node
    → Batch size 5 or 10

    Step 8 — Prepare Embedding Text
    → "Edit Fields / Set" node
    → Format: "Topic: Question"

    Step 9 — Generate Embedding
    → "Embeddings Ollama" node
    → Get vector back

    Step 10 — Insert into Vector Store
    → Vector Store node
    → Store vector + metadata

    Step 11 — Notify Completion
    → Gmail or Slack node
    → "Embeddings updated successfully"
```

- Find Out why Embedding Model is returning all with 0 values.
