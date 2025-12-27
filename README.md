# VCF RAG Chatbot

A generic RAG (Retrieval-Augmented Generation) chatbot for interpreting VCF (Variant Call Format) files. This application uses LangChain and OpenAI to parse VCF files, index them into a local Chroma vector database, and provide a conversational interface via Streamlit.

## Features

- **VCF Parsing**: Automatically parses standard VCF files.
- **Semantic Search**: Indexes variant information for natural language querying.
- **Chat Interface**: Simple Streamlit UI to ask questions about your genomic data.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vinoydna/RAG_VCF_files.git
   cd RAG_VCF_files
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file or provide your OpenAI API Key in the UI.

## Usage

1. Place your `.vcf` or `.vcf.gz` files in the `data/` directory (create it if it doesn't exist).
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Enter your OpenAI API Key in the sidebar.
4. Click "Initialize / Refresh Index" to process your VCF files.
5. Start chatting!

## Requirements

- Python 3.8+
- OpenAI API Key

