## 📖 Overview

**Automatically manage your university inbox with an AI that reads student questions, matches them to your approved guidelines, and sends out friendly, consistent replies 24/7 so no one is left waiting.**

### ❌ The Problem

University admissions and support teams are often overwhelmed by their inboxes. Specifically:
- Staff spend countless hours manually reading and replying to the same questions over and over.
- Students are left waiting for answers because human teams can't be online 24/7.
- Different staff members might give slightly different answers to the exact same question.
- Valuable human time is wasted on basic FAQs instead of complex student issues that actually need personal attention.
- There’s no quick, reliable way to instantly match a student's email to the existing knowledge base.

### ✅ The Solution

<div align="center">
  <img src="../assets/automated-email-query-resolution.gif" alt="n8n Workflow Preview" width="85%">
  <p><em>n8n workflow: Incoming email → Semantic search → LLM response → Threaded reply</em></p>
</div>

Think of this as a hyper-efficient, 24/7 assistant for your inbox. Here is how it works behind the scenes:

- **Stays up to date:** It quietly monitors a Google Drive FAQ file, automatically learning new answers as you update them.
- **Understands meaning:** It converts your FAQs into searchable data (vector embeddings), allowing it to understand the actual *intent* behind a student's question, not just exact keywords.
- **Reads and researches:** When an email arrives, it extracts the question and instantly searches the knowledge base for the perfect match.
- **Drafts the perfect reply:** Using an LLM, it writes a polite, personalized, and context-aware email response.
- **Keeps it natural:** It replies directly within the original email thread, exactly like a human would.

> 💡 **The result?** Once deployed, incoming questions are matched, answered, and resolved instantly—day or night—freeing your team up to focus on the work that matters most.