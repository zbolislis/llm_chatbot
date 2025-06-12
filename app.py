import streamlit as st
import uuid
from backend import chain_with_history

# Assigns a unique session ID per user/browser session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initializes frontend-visible message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configures the Streamlit page layout and title
st.set_page_config(page_title="Basic LLM Chatbot")
st.title("Chat with Mistral 7B")

# Displays previous messages in chat format
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Captures user input
user_input = st.chat_input("Ask anything")

if user_input:
    # Shows the user's message in the user interface
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Sends the input to the backend chain with the current session ID
    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": st.session_state.session_id}}
    )

    # Shows chatbot's response in the user interface
    st.chat_message("assistant").write(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
