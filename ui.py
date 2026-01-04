import threading
import tkinter as tk
from assistant import handle_query, load_memory, load_documents, chunk_text, DOCS_FOLDER, CHUNK_SIZE, CHUNK_OVERLAP

# Load data once
memory = load_memory()
docs = load_documents(DOCS_FOLDER)

all_chunks = []
for doc in docs:
    for i, chunk in enumerate(chunk_text(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)):
        all_chunks.append({
            "filename": doc["filename"],
            "chunk_id": i,
            "content": chunk
        })

def run_assistant(query):
    response = handle_query(query, memory, all_chunks)

    chat_box.insert(tk.END, f"\n🤖 Assistant:\n{response}\n")
    chat_box.see(tk.END)


def send_query():
    query = user_input.get()
    if not query.strip():
        return

    chat_box.insert(tk.END, f"\n🧑 You: {query}\n")
    chat_box.insert(tk.END, "\n🤖 Assistant is thinking...\n")
    chat_box.see(tk.END)

    user_input.delete(0, tk.END)

    # Run AI in background thread
    thread = threading.Thread(target=run_assistant, args=(query,))
    thread.start()



# UI setup
root = tk.Tk()
root.title("Personal AI Assistant")

chat_box = tk.Text(root, wrap=tk.WORD, height=25, width=80)
chat_box.pack(padx=10, pady=10)
chat_box.insert(
    tk.END,
    "🤖 Personal AI Assistant Ready\n\n"
    "• Ask questions from your documents\n"
    "• Type 'plan my day' for a daily plan 📅\n"
    "• Ask anything — I'm offline & private 🔒\n\n"
)


user_input = tk.Entry(root, width=70)
user_input.pack(side=tk.LEFT, padx=10, pady=10)
user_input.bind("<Return>", lambda event: send_query())
user_input.focus()


send_button = tk.Button(root, text="Send", command=send_query)
send_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()
