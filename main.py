from langchain_groq import ChatGroq
from config.tools_schema import tools
from dotenv import load_dotenv
from core.rag_engine import RAGEngine
from core.tool_handler import ToolHandler
from core.router import route_query
from utils.vector_store import create_vectorstore, load_vectorstore
from langchain_classic.schema import HumanMessage, AIMessage
import os
from utils.document_loader import split_documents, load_document_from_directory
from config.prompts import greet_prompt

load_dotenv()

def initialize_llm():
    llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=os.environ.get("GROQ_API_KEY"),
        )
    return llm

def main():
    
    # Load documents
    load_vectorstore()
    doc = load_document_from_directory(directory_path="./documents")
    vectorstore = create_vectorstore(chunks=split_documents(doc))
    print("Vectorstore ready.")
    
    # Initialize LLM
    llm = initialize_llm()
    print("LLM initialized.")
    
    # Initialize RAG Engine
    rag_engine = RAGEngine(vectorstore, llm)
    print("RAG Engine initialized.")
    
    # Initialize Tool Handler
    tool_handler = ToolHandler(llm, tools)
    print("Tool Handler initialized.")
    
    # Stores message objects for RAG context.
    chat_history = []
    
    print("=" * 60)
    print(f"🤖 HodoBot: {llm.invoke(
        greet_prompt
        ).content}")
    print("=" * 60)
    
    while True:
        question = input("\n❓ You: ").strip()
        
        if question.lower() in ['exit','bye','quit']:
            print("Hodo: 👋Byee...")
            break
        
        if question.lower() == 'clear':
            chat_history = []
            print("Hodo: 🧹 Chat history cleared.")
            continue
        
        if not question:
            continue
        
        # Get the answer from the router.
        result = route_query(
            question=question,
            chat_history=chat_history,
            rag_engine=rag_engine,
            tool_handler=tool_handler
            )
        
        print(f"\n🤖 HodoBot: {result['answer']}")
        
        # Show Sources
        if result['sources']:
            unique_sources = list(set(result['sources']))
            print(f"\n📚 Sources: {','.join(unique_sources)}")
            
        # Update chat history
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=result['answer']))

        # Keep history manageable
        if len(chat_history)>10:
            chat_history = chat_history[-10:]
        
        print("\n" + "-" * 60)
        
if __name__ =="__main__":
    main()