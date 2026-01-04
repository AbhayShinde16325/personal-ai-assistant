# 🧠 Personal Offline AI Assistant

A **local, offline, privacy-first AI assistant** built using **Ollama + Mistral + Python**.
The assistant can read personal documents (PDFs, notes), answer questions using them (RAG),
maintain long-term memory, and help with daily study planning — all without internet access.

---

## ✨ Features

- 🔒 **Fully Offline & Private** (no cloud APIs)
- 📚 **Document-Aware (RAG)** – answers from your PDFs & notes
- 🧠 **Persistent Memory** (with user consent)
- 📅 **Daily Planner Mode**
- 🖥️ **Desktop UI (Tkinter)**
- ⚡ **Optimized for CPU-only systems**

---

## 🏗️ Architecture Overview

- **Ollama + Mistral** → Local LLM inference  
- **Python** → Orchestration & logic  
- **Keyword-based Retrieval (RAG)** → Lightweight & fast  
- **Tkinter** → Desktop UI  
- **JSON Memory** → Safe, explicit long-term memory  

---

## 📂 Project Structure

personal_ai_assistant/
├── assistant.py # Core logic (RAG, memory, planner)
├── ui.py # Desktop UI
├── memory.json # Persistent memory store
├── ai_docs/ # User documents (PDF/TXT)
├── requirements.txt
└── README.md


---

## 🚀 How to Run

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt

#start ollama and pull model
ollama pull mistral

#run the assistant UI
python ui.py



🧪 Example Commands

plan my day

Explain OSI model

Remember that I am studying Computer Networks



🧠 Learning Outcomes

Built a full RAG pipeline from scratch

Designed safe memory management

Optimized LLM usage for low-resource systems

Implemented threaded UI for responsiveness

Learned practical LLM system design



📌 Future Improvements

Semantic embeddings for retrieval

PDF OCR support

Web or mobile UI

Model switching (Mistral / LLaMA)


👤 Author

Abhay
Computer Engineering Student
Interested in AI Systems, Data Engineering, and LLMs

