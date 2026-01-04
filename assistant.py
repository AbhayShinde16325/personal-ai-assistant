import os
import re
import ollama
import json
import fitz


def load_memory():
    with open("memory.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_memory(memory):
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def clean_memory_entry(entry):
    return entry.strip().lower()

def extract_topic(entry):
    phrases_to_remove = [
        "remember that i am",
        "remember that i'm",
        "remember that",
        "i am",
        "i'm",
        "preparing for",
        "studying",
        "learning"
    ]

    topic = entry.lower()

    for phrase in phrases_to_remove:
        topic = topic.replace(phrase, "")

    return topic.strip()

def infer_subject_from_exam(text):
    exam_map = {
        "cn": "computer networks",
        "computer networks": "computer networks",
        "os": "operating systems",
        "dbms": "dbms",
        "ai": "artificial intelligence"
    }

    for key, subject in exam_map.items():
        if key in text.lower():
            return subject

    return None

def generate_daily_plan(memory):
    focus = memory.get("current_focus", "general learning")
    topics = memory.get("ongoing_topics", [])

    plan = {
        "morning": [],
        "afternoon": [],
        "evening": []
    }

    # Prefer concrete study topics over generic goals
    study_topic = None

    for t in reversed(topics):
        cleaned = extract_topic(t)

        inferred = infer_subject_from_exam(cleaned)
        if inferred:
            study_topic = inferred
            break

        if "exam" not in cleaned and len(cleaned.split()) <= 4:
            study_topic = cleaned
            break

    if not study_topic:
        study_topic = focus

    plan["morning"].append(f"Revise core concepts of {study_topic}")
    plan["afternoon"].append(f"Practice questions or problems from {study_topic}")
    plan["evening"].append(f"Light revision + note weak areas in {study_topic}")

    return plan


pending_memory_update = None


DOCS_FOLDER = "ai_docs"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 100
TOP_K = 2

SYSTEM_PROMPT = """
You are a personal, offline AI assistant for Abhay.

You must answer questions using ONLY the provided context.
If the answer is not in the context, say you don’t know.
Keep responses concise and to the point unless explicitly asked to go deep.
If the question is about learning or understanding a topic, provide a slightly expanded explanation with examples.


Tone rules:
- Chill, supportive senior
- Clear structure
- Light emojis
- Never overcomplicate

Always:
- Explain WHY before HOW
- Warn what could go wrong
- End with a short recap and one next action

Memory rules:
- You may READ user memory freely.
- You must NEVER modify memory automatically.
- If the user asks to remember or change something, ask for explicit confirmation first.
- Only proceed after the user clearly says yes.

"""


def load_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".txt") or filename.endswith(".md"):
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append({
                    "filename": filename,
                    "content": f.read()
                })

        elif filename.endswith(".pdf"):
            pdf_text = load_pdf_text(file_path)
            documents.append({
                "filename": filename,
                "content": pdf_text
            })

    return documents


def load_pdf_text(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


def chunk_text(text, size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def score_chunk(chunk, query_tokens):
    tokens = tokenize(chunk)
    return sum(tokens.count(t) for t in query_tokens)


def retrieve_relevant_chunks(query, chunks):
    query_tokens = tokenize(query)
    scored = []

    for chunk in chunks:
        score = score_chunk(chunk["content"], query_tokens)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:TOP_K]]


# ---------- Build knowledge base ----------
docs = load_documents(DOCS_FOLDER)

all_chunks = []
for doc in docs:
    for i, chunk in enumerate(chunk_text(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)):
        all_chunks.append({
            "filename": doc["filename"],
            "chunk_id": i,
            "content": chunk
        })
# Load user memory

memory = load_memory()

def detect_memory_intent(user_input):
    keywords = ["remember", "save", "keep in mind", "note that"]
    return any(k in user_input.lower() for k in keywords)

def handle_query(query, memory, all_chunks):
    # Planner command
    if query.lower() in ["plan my day", "daily plan", "help me plan today"]:
        plan = generate_daily_plan(memory)

        output = "📅 Your Daily Plan\n\n"
        output += "🌅 Morning:\n"
        for task in plan["morning"]:
            output += f"- {task}\n"

        output += "\n🌤️ Afternoon:\n"
        for task in plan["afternoon"]:
            output += f"- {task}\n"

        output += "\n🌙 Evening:\n"
        for task in plan["evening"]:
            output += f"- {task}\n"

        output += "\n✨ Start small. Momentum beats motivation."
        return output

    # Normal RAG flow
    relevant_chunks = retrieve_relevant_chunks(query, all_chunks)

    context = "\n\n".join(
        f"[From {c['filename']} | chunk {c['chunk_id']}]\n{c['content']}"
        for c in relevant_chunks
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\n\nUser memory:\n{memory}"},
        {
            "role": "user",
            "content": f"""
Use the context below to answer the question.

Context:
{context}

Question:
{query}
"""
        }
    ]

    response = ollama.chat(model="mistral", messages=messages)
    return response["message"]["content"]

#print("🤖 Document-aware assistant ready. Type 'exit' to quit.\n")