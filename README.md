# AI Customer Message Assistant

A modular, production-ready customer support chatbot built with Python and the official **Google Gen AI SDK (`google-genai`)**. Designed for small businesses and e-commerce stores, it delivers empathetic, accurate responses grounded strictly in your business catalog and policies—supporting seamless multi-turn conversations in both **English** and **Bengali (বাংলা)**.

---

## Features

- **Empathetic & Grounded Persona:** Configured via system instructions to act as a polite, professional support agent that relies strictly on your defined business data without hallucinating prices or policies.
- **Stateful Conversation Memory:** Uses `client.chats.create()` to maintain full session context, allowing customers to ask follow-up questions naturally.
- **Bilingual Support (English & Bengali):** Automatically detects whether a customer writes in English, Bengali script (`বাংলা`), or Banglish, and replies naturally in the matching language.
- **Centralized Knowledge Base:** Business details, product catalogs, pricing, delivery rules, and return policies live in a single Python dictionary (`knowledge_base.py`) for effortless updates.
- **Resilient Error Handling:** Includes automatic exponential backoff retries for transient API rate limits (`429`) or server hiccups (`500`, `503`), along with clean fallback messages.
- **Interactive Rich CLI:** Built-in terminal interface with Markdown rendering, loading spinners, and session management commands.

---

## Project Structure

```text
customer_assistant/
├── .env                 # Environment variables (stores your secret GEMINI_API_KEY)
├── requirements.txt     # Python package dependencies
├── knowledge_base.py    # Editable business details, product catalog, and policies
├── assistant.py         # Core Gemini chat engine, memory management, and error handling
├── app.py               # Interactive Command-Line Interface (CLI)
└── README.md            # Project documentation
```

---

## Prerequisites

- **Python 3.9+** installed on your system.
- A free or paid **Gemini API Key** from [Google AI Studio](https://google.com).

---

## Setup & Installation

### 1. Clone or Create the Project Folder
Place all project files inside a dedicated directory:

```bash
mkdir customer_assistant
cd customer_assistant
```

### 2. Create and Activate a Virtual Environment
Isolate your dependencies using Python's built-in `venv`:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

> **Security Note:** Never commit your `.env` file to GitHub or public repositories. Add `.env` to your `.gitignore` file.

---

## Usage

Start the interactive assistant from your terminal:

```bash
python app.py
```

### Interactive CLI Commands
Once the chat session starts, you can use these built-in commands:

| Command | Description |
| :--- | :--- |
| `/help` | Display sample English, Bengali, and Banglish test prompts. |
| `/reset` | Clear the current conversation history and start a fresh session. |
| `/exit` | Exit the application cleanly (`exit` or `quit` also work). |

### Example Test Prompts
- **English:** *"Hi! How much is the Nakshi Kantha throw, and do you ship outside Dhaka?"*
- **Follow-up (Memory Test):** *"If I order two of them, do I get free delivery?"*
- **Bengali:** *"আপনাদের সুন্দরবনের মধুর দাম কত এবং রিটার্ন পলিসি কী?"*
- **Banglish:** *"Terracotta tea set ta ki stock e ache?"*

---

## Customization

### Updating Products, Prices, or Policies
Open `knowledge_base.py` and edit the `BUSINESS_DATA` dictionary. You do not need to modify `assistant.py` or `app.py`—the system prompt is rebuilt automatically whenever the application starts.

### Integrating with a Web UI or Messaging Platform
Because `CustomerSupportAssistant` in `assistant.py` is decoupled from terminal input/output, you can import it directly into **Streamlit**, **FastAPI**, **Flask**, or a **WhatsApp/Messenger webhook**:

```python
from dotenv import load_dotenv
from assistant import CustomerSupportAssistant

load_dotenv()
bot = CustomerSupportAssistant(model_name="gemini-2.5-flash")

response = bot.send_message("What are your support hours?")
print(response)
```

---

## License

This project is open-source and available under the [MIT License](https://opensource.org).
