"""
app.py
Clean, modern Streamlit web chat interface for the AI Customer Message Assistant.
Connects directly to CustomerSupportAssistant in assistant.py without modifying it.
"""

import os
import streamlit as st
from dotenv import load_dotenv

from assistant import CustomerSupportAssistant
from knowledge_base import BUSINESS_DATA

# Load local .env file if present (useful for local development)
load_dotenv()

BUSINESS_INFO = BUSINESS_DATA["business_info"]

WELCOME_MESSAGE = (
    f"Hello! Welcome to **{BUSINESS_INFO['name']}** support. 👋\n\n"
    "How can I help you today? You can ask me about our products, prices, delivery charges, "
    "or return policy in **English** or **বাংলা (Bengali)**."
)


def resolve_api_key() -> str | None:
    """Retrieves GEMINI_API_KEY from Streamlit secrets first, then environment variables."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except FileNotFoundError:
        # No secrets.toml file present; fall back to environment variables
        pass
    return os.getenv("GEMINI_API_KEY")


def initialize_session_state(api_key: str) -> None:
    """Initializes the assistant instance and UI message history in st.session_state."""
    if "assistant" not in st.session_state:
        st.session_state.assistant = CustomerSupportAssistant(
            model_name="gemini-2.5-flash",
            api_key=api_key,
        )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]


def reset_chat() -> None:
    """Clears both the Gemini backend memory and the Streamlit UI chat log."""
    if "assistant" in st.session_state:
        st.session_state.assistant.reset_conversation()
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]


def render_sidebar() -> str | None:
    """Renders business info, session controls, and clickable sample prompts in the sidebar."""
    selected_sample = None

    with st.sidebar:
        st.title(f"🛍️ {BUSINESS_INFO['name']}")
        st.caption(BUSINESS_INFO["tagline"])

        st.divider()

        if st.button("🔄 New Conversation", use_container_width=True, type="primary"):
            reset_chat()
            st.rerun()

        st.subheader("Quick Test Prompts")
        st.caption("Click a sample message to test the assistant:")

        samples = [
            ("🇬🇧 Product & Shipping", "Hi! How much is the Nakshi Kantha throw, and do you ship outside Dhaka?"),
            ("🇬🇧 Free Delivery Check", "If I order two Nakshi Kantha throws, do I qualify for free shipping?"),
            ("🇧🇩 বাংলা জিজ্ঞাসা", "আপনাদের সুন্দরবনের মধুর দাম কত এবং রিটার্ন পলিসি কী?"),
            ("🇧🇩 Banglish Stock Check", "Terracotta tea set ta ki stock e ache?"),
        ]

        for label, prompt_text in samples:
            if st.button(label, use_container_width=True):
                selected_sample = prompt_text

        st.divider()
        st.subheader("Support Info")
        st.markdown(
            f"**Hours:** {BUSINESS_INFO['support_hours']}  \n"
            f"**Email:** {BUSINESS_INFO['contact_email']}  \n"
            f"**Phone:** {BUSINESS_INFO['contact_phone']}"
        )

    return selected_sample


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title=f"{BUSINESS_INFO['name']} | Customer Support",
        page_icon="💬",
        layout="centered",
    )

    api_key = resolve_api_key()
    if not api_key:
        st.error(
            "**Missing API Key:** `GEMINI_API_KEY` was not found.\n\n"
            "Please add `GEMINI_API_KEY` to your `.env` file, system environment variables, "
            "or `.streamlit/secrets.toml` and reload the page."
        )
        st.stop()

    try:
        initialize_session_state(api_key)
    except Exception as init_err:
        st.error(f"Failed to initialize the assistant: {init_err}")
        st.stop()

    # Main header
    st.title("💬 Customer Support Assistant")
    st.caption(f"Powered by Gemini • {BUSINESS_INFO['name']} (English & বাংলা)")

    # Render sidebar and check if user clicked a sample prompt button
    sample_prompt = render_sidebar()

    # Display full conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept input either from the chat box or a sidebar sample button
    chat_box_input = st.chat_input("Type your message in English or বাংলা...")
    user_prompt = chat_box_input or sample_prompt

    if user_prompt:
        # 1. Render and store the customer's message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # 2. Fetch and render the assistant's reply
        with st.chat_message("assistant"):
            with st.spinner("Typing..."):
                reply = st.session_state.assistant.send_message(user_prompt)
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()

