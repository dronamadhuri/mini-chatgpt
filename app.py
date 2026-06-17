import streamlit as st
import streamlit.components.v1 as components
import os
import time
import logging
import db
import ai
from config import Config

# Initialize Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("app_main")

# Initialize SQLite Database
db.init_db()

# Streamlit Page Config
st.set_page_config(
    page_title="Mini ChatGPT Clone",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject ChatGPT Styling CSS
st.markdown("""
<style>
/* Import Outfit Google Font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Apply font globally */
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif;
    background-color: #212121;
}

/* App Header gradient */
.chat-header {
    text-align: center;
    background: linear-gradient(135deg, #10a37f, #00A67E, #14b8a6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-size: 3rem;
    margin-bottom: 5px;
    margin-top: -30px;
}

.chat-subtitle {
    text-align: center;
    color: #8a8a8a;
    font-size: 1.1rem;
    margin-bottom: 20px;
    font-weight: 300;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #171717 !important;
    border-right: 1px solid #2f2f2f;
}

/* Sidebar Columns Spacing */
[data-testid="stSidebar"] [data-testid="column"] {
    padding: 0 !important;
}

/* Sidebar Chat Session Buttons Styling */
[data-testid="stSidebar"] button {
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 8px 12px !important;
    font-size: 0.9rem !important;
    border-radius: 8px !important;
    height: 38px !important;
    line-height: 38px !important;
    width: 100% !important;
}

/* Style active primary button to look like ChatGPT green */
[data-testid="stSidebar"] button[kind="primary"] {
    background-color: #10a37f !important;
    color: white !important;
    border: 1px solid #10a37f !important;
}
[data-testid="stSidebar"] button[kind="primary"]:hover {
    background-color: #1a7f65 !important;
    border-color: #1a7f65 !important;
    transform: none !important;
}

/* Style secondary buttons in sidebar to be flat and subtle */
[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: transparent !important;
    border: 1px solid transparent !important;
    color: #c5c5d2 !important;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background-color: #2a2b32 !important;
    color: white !important;
    border-color: transparent !important;
    transform: none !important;
}

/* Plus button custom visual border */
[data-testid="stSidebar"] div.stButton:first-of-type button {
    border: 1px dashed #4d4d4d !important;
    background-color: transparent !important;
    color: #ececec !important;
    justify-content: center !important;
}
[data-testid="stSidebar"] div.stButton:first-of-type button:hover {
    border-color: #10a37f !important;
    background-color: #2d2d2d !important;
    color: #10a37f !important;
}

/* Style trash icon (the second button/column in the row) */
[data-testid="stSidebar"] [data-testid="column"]:nth-child(2) button {
    background-color: transparent !important;
    border: none !important;
    color: #8e8ea0 !important;
    padding: 0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
}
[data-testid="stSidebar"] [data-testid="column"]:nth-child(2) button:hover {
    color: #ff4b4b !important;
    background-color: rgba(255, 75, 75, 0.1) !important;
    transform: scale(1.05);
}

/* Scrollable Container Styling */
div[data-testid="stElementContainer"] > div[style*="height"] {
    border: 1px solid #2f2f2f !important;
    border-radius: 16px !important;
    background-color: #1a1a1a !important;
    padding: 20px !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5) !important;
}

/* Remove default Streamlit background and padding from chat messages */
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    padding: 5px 0 !important;
    margin-bottom: 15px !important;
    box-shadow: none !important;
}

/* Smooth message slide-up animation */
div[data-testid="stChatMessage"] {
    animation: slideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Flexbox layout for user messages (right-aligned) */
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]),
.stChatMessage:has([data-testid="chatAvatarIcon-user"]),
.stChatMessage:has(span[data-testid="stChatMessageAvatarUser"]),
.stChatMessage:has(div[class*="user"]) {
    flex-direction: row-reverse !important;
}

/* Flexbox layout for assistant messages (left-aligned) */
.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]),
.stChatMessage:has([data-testid="chatAvatarIcon-assistant"]),
.stChatMessage:has(span[data-testid="stChatMessageAvatarAssistant"]) {
    flex-direction: row !important;
}

/* User Bubble Custom CSS - ChatGPT Green */
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"],
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"],
.stChatMessage:has(span[data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"],
.stChatMessage:has(div[class*="user"]) [data-testid="stChatMessageContent"] {
    background-color: #10a37f !important;
    color: #ffffff !important;
    border-radius: 20px 20px 4px 20px !important;
    padding: 12px 18px !important;
    margin-right: 12px !important;
    margin-left: 20% !important;  /* Ensure user bubbles don't stretch too wide */
    box-shadow: 0 4px 12px rgba(16, 163, 127, 0.2) !important;
    border: none !important;
}

/* Assistant Bubble Custom CSS - Dark Charcoal */
.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"],
.stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"],
.stChatMessage:has(span[data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background-color: #2f2f2f !important;
    color: #ececec !important;
    border-radius: 20px 20px 20px 4px !important;
    padding: 12px 18px !important;
    margin-left: 12px !important;
    margin-right: 20% !important; /* Ensure AI bubbles don't stretch too wide */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    border: 1px solid #3d3d3d !important;
}

/* Avatar positioning and scaling */
[data-testid="stChatMessageAvatarUser"], 
[data-testid="stChatMessageAvatarAssistant"] {
    font-size: 1.6rem !important;
    width: 38px !important;
    height: 38px !important;
    background-color: #2d2d2d !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 1px solid #3d3d3d !important;
}

/* Hide streamlit default header/footer for white-label look */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Input box styling styling */
[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 1px solid #3d3d3d !important;
    background-color: #2a2a2a !important;
    transition: all 0.3s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #10a37f !important;
    box-shadow: 0 0 10px rgba(16, 163, 127, 0.25) !important;
}

/* Clean up button hover scales */
.stButton>button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton>button:hover {
    transform: scale(1.02);
}

/* Custom Typing Indicator Bouncing Dots */
.typing-indicator {
    display: inline-flex;
    align-items: center;
    column-gap: 5px;
    background-color: #2f2f2f;
    border: 1px solid #3d3d3d;
    padding: 12px 18px;
    border-radius: 20px 20px 20px 4px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    margin-left: 12px;
    margin-top: 5px;
}
.typing-indicator span {
    height: 8px;
    width: 8px;
    background-color: #8e8ea0;
    border-radius: 50%;
    display: block;
    animation: bounce 1.3s infinite ease-in-out;
}
.typing-indicator span:nth-child(1) { animation-delay: 0s; }
.typing-indicator span:nth-child(2) { animation-delay: 0.15s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.3s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-6px); }
}

/* Custom code block styling overrides inside markdown */
code {
    background-color: #1e1e1e !important;
    color: #f43f5e !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-family: 'Courier New', Courier, monospace !important;
}
pre code {
    background-color: #18181b !important;
    color: #e4e4e7 !important;
    display: block !important;
    padding: 12px !important;
    border-radius: 8px !important;
    border: 1px solid #27272a !important;
    overflow-x: auto !important;
}
</style>
""", unsafe_allow_html=True)

def copy_button(text: str):
    """
    Renders an inline-sandboxed copy-to-clipboard button using Streamlit components.
    Includes fallback compatibility for secure/non-secure contexts.
    """
    escaped_text = text.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    html_code = f"""
    <button id="copy-btn" style="
        background-color: #2f2f2f;
        color: #c5c5d2;
        border: 1px solid #4d4d4d;
        border-radius: 6px;
        padding: 5px 10px;
        font-size: 0.75rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 5px;
        font-family: 'Outfit', sans-serif;
        transition: all 0.2s ease;
        margin-top: 5px;
    ">
        📋 Copy Response
    </button>
    <script>
    function copyText(text) {{
        if (navigator.clipboard && navigator.clipboard.writeText) {{
            return navigator.clipboard.writeText(text);
        }} else {{
            var textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.position = "fixed";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {{
                var successful = document.execCommand('copy');
                document.body.removeChild(textArea);
                return successful ? Promise.resolve() : Promise.reject();
            }} catch (err) {{
                document.body.removeChild(textArea);
                return Promise.reject(err);
            }}
        }}
    }}
    document.getElementById('copy-btn').addEventListener('click', function() {{
        copyText('{escaped_text}').then(function() {{
            var btn = document.getElementById('copy-btn');
            btn.innerHTML = '✅ Copied!';
            btn.style.borderColor = '#10a37f';
            btn.style.color = '#10a37f';
            setTimeout(function() {{
                btn.innerHTML = '📋 Copy Response';
                btn.style.borderColor = '#4d4d4d';
                btn.style.color = '#c5c5d2';
            }}, 2000);
        }}).catch(function(err) {{
            console.error('Failed to copy text: ', err);
        }});
    }});
    </script>
    """
    components.html(html_code, height=35)

# Custom Title Header
st.markdown('<div class="chat-header">Mini ChatGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Powered by Gemini 2.5 Flash</div>', unsafe_allow_html=True)

# Sidebar layout
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg", width=50)
st.sidebar.title("Configuration")

# Environment key loading - Strictly verified via Config loader class
if not Config.validate():
    st.sidebar.error("❌ Gemini API Key is missing or invalid in your `.env` file.")
    st.error("🔒 **Access Denied**: Please configure your `GEMINI_API_KEY` in the `.env` file to start using the chatbot.")
    st.info("💡 To setup your key, create a `.env` file in the root folder of the project containing: \n`GEMINI_API_KEY=your_actual_key` and restart the application.")
    st.stop()
else:
    st.sidebar.success("🔑 API Key verified from environment.")

# Initialize the Gemini API client globally using google-generativeai
try:
    ai.configure_gemini()
except Exception as e:
    st.error(f"Failed to initialize Gemini API: {e}")
    st.stop()

# Sidebar Settings
st.sidebar.markdown("---")
st.sidebar.subheader("Model Settings")

system_instruction = st.sidebar.text_area(
    "System Instructions",
    value="You are Mini ChatGPT, a helpful, polite, and intelligent AI assistant. Keep answers concise and structured using Markdown.",
    help="Set the behavior and role of the assistant."
)

temperature = st.sidebar.slider(
    "Temperature (Creativity)",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
    help="Higher values make output more random, lower values make it more focused."
)

# SQLite Session Management
st.sidebar.markdown("---")
st.sidebar.subheader("Conversations")

# Create New Chat
if st.sidebar.button("➕ New Chat", use_container_width=True):
    new_id = db.create_new_chat()
    st.session_state.current_chat_id = new_id
    if "chat" in st.session_state:
        del st.session_state.chat
    st.rerun()

# Load all chats from database
all_chats = db.list_chats()

# Assign default if none exists
if "current_chat_id" not in st.session_state or st.session_state.current_chat_id is None:
    if all_chats:
        st.session_state.current_chat_id = all_chats[0]["chat_id"]
    else:
        st.session_state.current_chat_id = db.create_new_chat()
        all_chats = db.list_chats()

# List past conversations
for chat in all_chats:
    is_active = st.session_state.current_chat_id == chat["chat_id"]
    btn_type = "primary" if is_active else "secondary"
    
    col1, col2 = st.sidebar.columns([0.82, 0.18])
    with col1:
        if st.button(f"💬 {chat['title']}", key=f"chat_{chat['chat_id']}", use_container_width=True, type=btn_type):
            st.session_state.current_chat_id = chat["chat_id"]
            if "chat" in st.session_state:
                del st.session_state.chat
            st.rerun()
    with col2:
        if st.button("🗑️", key=f"del_{chat['chat_id']}", help="Delete chat"):
            db.delete_chat(chat["chat_id"])
            if st.session_state.current_chat_id == chat["chat_id"]:
                st.session_state.current_chat_id = None
            st.rerun()

# Recreate chat session if model configuration settings change
config_hash = (system_instruction, temperature)
if "config_hash" not in st.session_state:
    st.session_state.config_hash = config_hash

if st.session_state.config_hash != config_hash:
    st.session_state.config_hash = config_hash
    if "chat" in st.session_state:
        del st.session_state.chat

# Retrieve thread history
messages = db.load_chat(st.session_state.current_chat_id)

# Start Gemini chat session
if "chat" not in st.session_state:
    try:
        history = ai.format_history_for_gemini(messages)
        st.session_state.chat = ai.create_chat_session(
            history=history,
            system_instruction=system_instruction,
            temperature=temperature
        )
    except Exception as e:
        st.error(f"Error starting AI session: {e}")
        st.stop()

# Create a scrollable container for chat history
chat_container = st.container(height=550)

# Display message history
with chat_container:
    for msg in messages:
        # Hide internal API errors from the main message log layout
        if msg["content"].startswith("⚠️ [Error:"):
            with st.chat_message("assistant", avatar="🤖"):
                st.error(msg["content"])
            continue
            
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                copy_button(msg["content"])

# User Chat Input
if prompt := st.chat_input("How can I help you today?"):
    # Save user message to database
    db.save_message(st.session_state.current_chat_id, "user", prompt)
    logger.info(f"App: Received prompt for session: '{st.session_state.current_chat_id}'")
    
    # Render user message
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

    # Render assistant response with dual-stage loading
    with chat_container:
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Render custom CSS bouncing dots typing indicator (acts as loading state while AI responds)
            message_placeholder.markdown("""
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            """, unsafe_allow_html=True)
            
            # Retrieve generator
            response_generator = ai.generate_stream(st.session_state.chat, prompt)
            
            error_occurred = False
            try:
                # Phase 1: Blocks until first chunk is returned (replaces animation with initial word)
                first_chunk = next(response_generator)
                full_response += first_chunk
                message_placeholder.markdown(full_response + "▌")
                
                # Phase 2: Render typewriter streaming of subsequent tokens
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)  # Smooth transition pacing
                
                # Render clean final text (remove cursor)
                message_placeholder.markdown(full_response)
                
                # Display Copy Response Button
                copy_button(full_response)
                
                # Save assistant response to database
                db.save_message(st.session_state.current_chat_id, "assistant", full_response)
                
            except StopIteration:
                # No content returned from generator
                if not full_response:
                    full_response = "No response generated by the model."
                    message_placeholder.markdown(full_response)
                    db.save_message(st.session_state.current_chat_id, "assistant", full_response)
            except Exception as e:
                # Catch actual API or network errors, log them, and show in UI
                error_occurred = True
                logger.error(f"Failed to generate AI response: {e}", exc_info=True)
                
                # Display clear, raw error description in place of dots
                message_placeholder.empty()
                st.error(f"⚠️ **Gemini API Error**: {str(e)}")
                
                # Save details of the error under the assistant tag
                db.save_message(
                    st.session_state.current_chat_id,
                    "assistant",
                    f"⚠️ [Error: {str(e)}]"
                )
            
            # Only rerun to refresh sidebar titles and state if no error occurred
            if not error_occurred:
                st.rerun()
