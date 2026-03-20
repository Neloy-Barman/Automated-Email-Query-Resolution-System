## 🔄 Automation Flow

### Part 1 — Knowledge Base Ingestion

```text
         Google Drive File Change Detected (Daily Trigger)
                              ↓
                   Google Drive Trigger
                              ↓
          ┌───────────────────┴───────────────────┐
          ↓                                       ↓
  [Collection Setup Branch]            [Data Ingestion Branch]
          ↓                                       ↓
  Fetch Collection Name                     Download File
          ↓                                       ↓
  Check If Collection Exists              Extract from File
          ↓                                       ↓
    ┌─────┴─────┐                            Data Fetch
    ↓           ↓                                 ↓
 Exists?   Not Exists?                   Data Preprocessing
    ↓           ↓                                 ↓
 Delete         |                       Embedding Generation
 Collection     |                                 ↓
    ↓           |                                 |
    └─────┬─────┘                                 |
          ↓                                       |
   Create Collection                              | 
          ↓                                       |
          └───────────────────┬───────────────────┘
                              ↓
                        Upsert Points
                              ↓
                    ✅ Ingestion Complete
```

---

### Part 2 — Email Query Resolution

```text
           New Email Received in Gmail Inbox
                           ↓
                    Gmail Trigger
                           ↓
                  Fields Preparation
                           ↓
          ┌────────────────┴────────────────┐
          ↓                                 ↓
   Query Embedding              Collection Name Fetch
          ↓                                 ↓
          └────────────────┬────────────────┘
                           ↓
                         Merge
                           ↓
                    Similarity Search
                           ↓
                    Message a Model
                           ↓
                      Email Format
                           ↓
                   Send Reply Email
                           ↓
               ✅ Response Sent to Sender
```