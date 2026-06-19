Here is your **README.md in proper “write mode” (clean, ready to paste directly into file)**:

---

```md
# 💬 Mini ChatGPT Clone

A simple ChatGPT-style chatbot built using **Streamlit** and **Google Gemini API (1.5 Flash)**.
---

## 🚀 Features

- 💬 ChatGPT-like conversational UI  
- 🤖 Powered by Google Gemini 1.5 Flash  
- 🧠 Session-based memory (chat history)  
- ⚡ Fast AI responses  
- 🎨 Clean Streamlit interface  
- 🔐 Secure API key using `.env` file  

---

## 📁 Project Structure

```

mini-chatgpt-clone/
│
├── app.py              # Streamlit UI
├── ai.py               # Gemini API logic
├── config.py          # (optional) configuration loader
├── requirements.txt    # dependencies
├── .env.example       # environment variables template
└── README.md

````

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/mini-chatgpt-clone.git
cd mini-chatgpt-clone
````

---

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup API Key

Get your Gemini API key from:
👉 [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 🧠 How it works

1. User enters a message in the chat UI
2. Message is sent to Gemini API
3. AI generates response
4. Response is displayed in chat
5. Conversation is stored in session memory

---

## 🛠️ Tech Stack

* Python 🐍
* Streamlit 🎈
* Google Gemini API 🤖
* python-dotenv 🔐

---

## ⚠️ Important Notes

* Never expose your API key publicly
* Always use `.env` file
* Restart app after changing environment variables
* Do not commit `.env` to GitHub

---

## 👨‍💻 Developer

**dronamadhuri**

---

## 📌 Future Improvements

* Sidebar chat history
* Persistent database (SQLite)
* Streaming responses (typing effect)
* Dark mode improvements
* Voice input/output chatbot

---
