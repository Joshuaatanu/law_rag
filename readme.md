

# Nigerian Constitution AI Chatbot 🇳🇬

A Retrieval-Augmented Generation (RAG) powered chatbot that answers questions about the Nigerian Constitution with legal citations.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangChain Version](https://img.shields.io/badge/LangChain-0.2.x-green)](https://python.langchain.com/)

## Features

- 📄 PDF Document Processing with Metadata Extraction
- 🧠 RAG Implementation with FAISS Vector Store
- ⚖️ Legal Citation Tracking (Articles & Sections)
- ❓ Ambiguity Detection and Query Validation
- 🤖 Support for Both OpenAI and Local LLMs (Llama.cpp)
- 🌐 Gradio Web Interface

## Installation

1. **Clone Repository**

```bash
git clone https://github.com/Joshuaatanu/law_rag.git
cd law_rag
```

2. **Set Up Virtual Environment**
```bash
python -m venv constitution-env
source constitution-env/bin/activate  # Linux/Mac
# constitution-env\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Download Constitution PDF**
- Place `nigerian_constitution.pdf` in `data/` directory
- Recommended source: [Nigeria Law](https://www.nigeria-law.org/ConstitutionOfTheFederalRepublicOfNigeria.htm)

## Configuration

1. **For OpenAI Users**
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

2. **For Local LLM Users**
```bash
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O models/
```

## Usage

1. **Run the Application**
```bash
python src/chatbot.py
```

2. **Access Web Interface**
- Local URL: `http://localhost:7860`
- Gradio Share URL will be displayed in console

3. **Example Questions**
- "What does Article 21 say about cultural rights?"
- "Explain the impeachment process in Section 143"
- "What are the fundamental rights in Chapter IV?"

## Deployment

### **Option 1: Docker**
```dockerfile
docker build -t constitution-chatbot .
docker run -p 7860:7860 constitution-chatbot
```

### **Option 2: Hugging Face Spaces**
1. Create new Space with Gradio SDK
2. Upload:
   - `src/`
   - `data/`
   - `requirements.txt`
3. Set OpenAI API key in Space secrets

## Project Structure
```
├── data/
│   └── nigerian_constitution.pdf
├── models/
│   └── mistral-7b-instruct-v0.1.Q4_K_M.gguf
├── src/
│   ├── chatbot.py
│   ├── data_processing.py
│   └── config.py
├── requirements.txt
├── .env.example
└── README.md
```

## Troubleshooting

**Common Issues:**
- API Key Errors: Verify `.env` file exists with correct credentials
- Model Not Found: Check model path in `chatbot.py`
- PDF Extraction Issues: Ensure PDF is not scanned/image-based

**Performance Tips:**
- Use `n_ctx=4096` for longer context with local models
- Reduce `chunk_size` in `config.py` for better relevance
- Enable GPU acceleration for local models

## Disclaimer

⚠️ This application provides general constitutional information and should not be considered legal advice. Always consult qualified legal professionals for official matters.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or PR for:
- Additional legal provisions
- Improved citation tracking
- Local language support (Hausa/Yoruba/Igbo)

## Acknowledgments
- [LangChain Framework](https://python.langchain.com/)
- [Gradio](https://www.gradio.app/)
- [Nigerian Law Repository](https://www.nigeria-law.org)
- Mistral-7B model by [TheBloke](https://huggingface.co/TheBloke)
```

