import streamlit as st  # type: ignore
from rag import RagService

st.title("Knowledge Base Chat")

# Initialize the RAG service once per session (it loads models/vector store,
# so we don't want to re-create it on every rerun).
if "rag_service" not in st.session_state:
    with st.spinner("Initializing knowledge base..."):
        st.session_state["rag_service"] = RagService()

# Simple chat history: a list of {"role": "user"/"assistant", "content": str}
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar controls
with st.sidebar:
    st.subheader("Chat controls")
    if st.button("Clear chat history"):
        st.session_state["messages"] = []
        st.rerun()

# Render previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box (pinned to bottom by Streamlit)
user_input = st.chat_input("Ask something about the knowledge base...")

if user_input:
    # Show the user's message immediately
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and show the assistant's reply, passing prior turns as context
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            history_so_far = st.session_state["messages"][:-1]  # exclude current question
            answer = st.session_state["rag_service"].ask(user_input, history_so_far)
            st.markdown(answer)

    st.session_state["messages"].append({"role": "assistant", "content": answer})