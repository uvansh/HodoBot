from langchain_groq import ChatGroq
from config.prompts import system_prompt,contextual_prompt
from config.tools_schema import tools
from dotenv import load_dotenv
from core.rag_engine import RAGEngine
from core.tool_handler import ToolHandler
from core.router import route_query
from utils.vector_store import create_vectorstore, load_vectorstore
from langchain_classic.schema import HumanMessage, AIMessage
import os
from utils.document_loader import split_documents, load_document_from_directory

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
    
    while True:
        question = input("You: ")
        
        result = route_query(
            question=question,
            chat_history=chat_history,
            rag_engine=rag_engine,
            tool_handler=tool_handler
            )
        
        if question.lower() in ['exit','bye','quit']:
            print("Hodo: Byee...")
            break
        
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=result['answer']))

        print()
        
        print(f"Hodo: {result['answer']}")

        if len(chat_history)>10:
            chat_history = chat_history[-10:]
        
if __name__ =="__main__":
    main()