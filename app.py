import streamlit as st
import os
from rag_engine import initialize_rag, get_answer

st.set_page_config(page_title="VCF RAG Chatbot", page_icon="🧬")

st.title("🧬 VCF RAG Chatbot")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    vcf_folder = st.text_input("VCF Data Folder", value="./data")
    
    if st.button("Initialize / Refresh Index"):
        if not openai_api_key:
            st.error("Please enter an OpenAI API Key.")
        else:
            with st.spinner("Indexing VCF files... This may take a moment."):
                try:
                    # Clear chat history on re-index
                    st.session_state.chat_history = []
                    st.session_state.qa_chain, msg = initialize_rag(vcf_folder, openai_api_key)
                    st.success(msg)
                except Exception as e:
                    st.error(f"Error: {e}")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about your VCF files..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Generate response
    if st.session_state.qa_chain:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Convert chat history for LangChain
                    lc_history = [(m["content"], "") for m in st.session_state.chat_history if m["role"] == "user"]
                    # We might need to handle history better, but for now simple passing
                    
                    answer, sources = get_answer(st.session_state.qa_chain, prompt, lc_history)
                    
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    
                    with st.expander("View Sources"):
                        for doc in sources:
                            st.markdown(f"**Source:** {doc.metadata['source']}")
                            st.markdown(f"**Content:**\n{doc.page_content}")
                            st.divider()
                            
                except Exception as e:
                    st.error(f"Error generating answer: {e}")
    else:
        st.warning("Please initialize the index in the sidebar first.")
