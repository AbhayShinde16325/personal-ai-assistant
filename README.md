# 🧠 Personal Offline AI Assistant

A **local, offline, privacy-first AI assistant** built using **Ollama + Mistral + Python**.

This assistant can:
- read your personal documents (PDFs, notes),
- answer questions using them via **RAG (Retrieval-Augmented Generation)**,
- maintain **long-term memory with user consent**, and
- help with **daily study planning**,

—all **without using the internet or cloud APIs**.

---

## ✨ Key Features

- 🔒 **Fully Offline & Private**  
  No cloud APIs, no data leaves your machine.

- 📚 **Document-Aware Q&A (RAG)**  
  Ask questions directly from your PDFs and notes.

- 🧠 **Persistent Memory (Opt-in)**  
  The assistant remembers goals only after your confirmation.

- 📅 **Daily Planner Mode**  
  Generates realistic study plans based on your focus areas.

- 🖥️ **Desktop UI (Tkinter)**  
  Lightweight, responsive desktop interface.

- ⚡ **CPU-Friendly**  
  Designed to run on low-resource systems (no GPU required).

---

## 🏗️ Architecture Overview

- **Ollama + Mistral** → Local LLM inference  
- **Python** → Core orchestration & logic  
- **Keyword-based RAG** → Lightweight retrieval (CPU-friendly)  
- **Tkinter** → Desktop UI  
- **JSON Memory** → Explicit, user-controlled persistence  

---

## 📂 Project Structure

personal_ai_assistant/
├── assistant.py # Core logic (RAG, memory, planner)
├── ui.py # Desktop UI
├── memory.json # Persistent memory (ignored by Git)
├── ai_docs/ # User documents (PDF/TXT)
├── requirements.txt
└── README.md


> ⚠️ `memory.json` and `ai_docs/` are intentionally ignored in Git for privacy.

---

## 🚀 Step-by-Step: How to Run the Project

### ✅ Prerequisites

Make sure you have:
- **Python 3.10+**
- **Git**
- **Ollama installed**

👉 Install Ollama from: https://ollama.com

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/personal-ai-assistant.git
cd personal-ai-assistant

2️⃣ Install Python Dependencies
pip install -r requirements.txt

3️⃣ Pull the LLM Model (One-Time Setup)
ollama pull mistral

4️⃣ Add Your Documents
Place your files inside the ai_docs/ folder:

.txt

.md

.pdf
Example
ai_docs/
├── computer_networks_notes.pdf
├── os_summary.txt

5️⃣ Run the Desktop UI
python ui.py

🧪 Example Commands to Try

plan my day

Explain OSI model

What is TCP/IP from my notes?

Remember that I am studying Computer Networks

What am I currently focusing on?

🧠 Learning Outcomes

By building this project, I learned how to:

Design and implement a full RAG pipeline from scratch

Build safe, explicit memory systems for AI assistants

Optimize LLM workflows for CPU-only environments

Create a responsive threaded UI in Python

Think in terms of LLM system design, not just prompts

📌 Future Improvements

Semantic embeddings for smarter retrieval

OCR support for scanned PDFs

Web or mobile UI

Model switching (Mistral, LLaMA, etc.)

👤 Author

Abhay
Computer Engineering Student
Interested in AI Systems, Data Engineering, and LLM Architectures

