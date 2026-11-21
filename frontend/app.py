
import streamlit as st
import requests

# ==========================================
# Configuration
# ==========================================

API_URL = "http://127.0.0.1:8000"

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# Custom Styling
# ==========================================

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.stButton button {
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# Sidebar Navigation
# ==========================================

st.sidebar.title("🤖 Enterprise AI")
st.sidebar.caption("Knowledge Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "AI Chat", "Upload Documents"]
)


# ==========================================
# Backend Connection
# ==========================================

def get_document_count():
    try:
        response = requests.get(
            f"{API_URL}/documents/count",
            timeout=10
        )

        if response.status_code == 200:
            return response.json().get(
                "total_stored_chunks", 0
            )

        return "Unavailable"

    except requests.RequestException:
        return "Offline"


# ==========================================
# Dashboard
# ==========================================

if page == "Dashboard":

    st.title("Enterprise AI Knowledge Assistant")

    st.write(
        "Your intelligent enterprise document assistant."
    )

    col1, col2 = st.columns(2)

    count = get_document_count()

    with col1:
        st.metric(
            "Stored Document Chunks",
            count
        )

    with col2:
        status = (
            "Online"
            if isinstance(count, int)
            else "Offline"
        )

        st.metric(
            "Backend Status",
            status
        )

    st.divider()

    st.subheader("Welcome!")

    st.write("""
    This platform allows you to:

    - Upload enterprise PDF documents.
    - Ask questions using AI.
    - Retrieve relevant document information.
    - Generate context-aware answers using RAG.
    """)


# ==========================================
# AI Chat
# ==========================================

elif page == "AI Chat":

    st.title("💬 AI Knowledge Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    question = st.chat_input(
        "Ask something about your documents..."
    )

    if question:

        # Store user message
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner("Searching knowledge base..."):

                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        params={
                            "query": question,
                            "top_k": 3
                        },
                        timeout=120
                    )

                    response.raise_for_status()

                    result = response.json()

                    answer = result.get(
                        "answer",
                        "No answer generated."
                    )

                    st.markdown(answer)

                    # Display sources
                    sources = result.get("sources", [])

                    if sources:

                        with st.expander("View Sources"):
                            st.write(sources)

                    # Store assistant response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except requests.RequestException as e:

                    error_message = f"Backend error: {e}"

                    st.error(error_message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })


# ==========================================
# Upload Documents
# ==========================================

elif page == "Upload Documents":

    st.title("📄 Upload Enterprise Documents")

    st.write(
        "Upload PDF documents to your knowledge base."
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )

    if uploaded_file:

        st.info(
            f"Selected file: {uploaded_file.name}"
        )

        if st.button("Upload Document"):

            with st.spinner("Processing document..."):

                try:
                    response = requests.post(
                        f"{API_URL}/documents/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        timeout=180
                    )

                    if response.status_code == 200:

                        st.success(
                            "Document uploaded successfully!"
                        )

                        st.json(response.json())

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except requests.RequestException as e:

                    st.error(
                        f"Connection error: {e}"
                    )
