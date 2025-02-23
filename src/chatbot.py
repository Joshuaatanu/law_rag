# Updated imports for LangChain 0.2.x
from langchain_openai import OpenAI  # Correct OpenAI import
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.evaluation import load_evaluator  # Correct evaluation import
import gradio as gr
import os
from dotenv import load_dotenv

# Local imports
from data_processing import create_vector_store, process_constitution

# Load environment variables
load_dotenv()

# Initialize OpenAI with error handling
try:
    llm = OpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo-instruct",
        openai_api_key=os.getenv("OPENAI_API_KEY")  # Get from .env
    )
except Exception as e:
    raise ValueError("Failed to initialize OpenAI. Check your API key.") from e

def create_legal_chain(vector_store):
    """Create the QA chain with proper error handling"""
    try:
        return RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            chain_type="map_reduce",
            retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True,
            chain_type_kwargs={
                "combine_prompt": PromptTemplate(
                    template="""You are a senior legal advisor to Nigeria's National Assembly specializing in the 1999 Constitution (as amended). 

**Constitutional Analysis Guidelines:**
1. Begin responses with "Under Nigerian Constitutional Law:"
2. Cite provisions using [Article X(Section Y)] format (e.g. [Article 21(Section 1)])
3. When referencing chapters: "Chapter IV on Fundamental Rights"
4. If context contains multiple provisions:
   - Prioritize hierarchical order: Articles > Sections > Schedules
   - Compare similar provisions (e.g. "While Article 12 states... Article 14 clarifies...")
5. For ambiguous queries:
   - Identify relevant constitutional chapters
   - State "This interpretation considers [Articles X-Y] regarding..."

**Current Context:**
{summaries}

**Query:**
{question}

**Required Response Format:**
[Main Answer] 
[Supporting Provision 1] 
[Supporting Provision 2 (if applicable)]
[Relevant Chapter Context (when needed)]""",
                    input_variables=["summaries", "question"]
                )
            }
        )
    except Exception as e:
        raise RuntimeError("Failed to create QA chain") from e

def format_legal_response(result):
    """Format response with error handling for missing metadata"""
    try:
        answer = result['answer']
        sources = []
        
        for doc in result.get('source_documents', []):
            refs = []
            if doc.metadata.get('article'):
                refs.append(f"Article {', '.join(doc.metadata['article'])}")
            if doc.metadata.get('section'):
                refs.append(f"Section {', '.join(doc.metadata['section'])}")
            
            sources.append(
                f"Page {doc.metadata.get('page', 'N/A')}: {' & '.join(refs)}"
            )
        
        return f"{answer}\n\nREFERENCES:\n" + "\n".join(sources)
    except KeyError as e:
        return "Error formatting response. Please try again."

def validate_question(query):
    """Validate questions with error handling"""
    try:
        ambiguity = load_evaluator("ambiguity")
        amb_score = ambiguity.evaluate_strings(prediction=query)['score']
        
        keywords = ['article', 'section', 'constitution', 'law', 'rights']
        relevance = any(kw in query.lower() for kw in keywords)
        
        return {
            'needs_clarification': amb_score > 0.6,
            'off_topic': not relevance
        }
    except Exception as e:
        print(f"Validation error: {e}")
        return {'needs_clarification': False, 'off_topic': False}

def chat_interface(query, history):
    """Main chat interface with error handling"""
    try:
        validation = validate_question(query)
        
        if validation['off_topic']:
            return "Please ask questions about the Nigerian Constitution."
        
        if validation['needs_clarification']:
            return "Could you specify which article or legal aspect you're asking about?"
        
        result = qa_chain.invoke({"question": query})  # Updated invocation
        return format_legal_response(result)
    except Exception as e:
        print(f"Error processing query: {e}")
        return "An error occurred. Please try again."

def launch_app():
    """Launch the application with proper initialization"""
    try:
        docs = process_constitution()
        vector_store = create_vector_store(docs)
        global qa_chain
        qa_chain = create_legal_chain(vector_store)
        
        gr.ChatInterface(
            fn=chat_interface,
            title="🇳🇬 Nigerian Constitution AI",
            description="Ask legal questions about Nigeria's Constitution",
            examples=[
                "What does Article 21 say about cultural rights?",
                "Explain the legislative powers in Section 4"
            ]
        ).launch(share=True)
    except Exception as e:
        print(f"Failed to launch app: {e}")
        raise

if __name__ == "__main__":
    launch_app()