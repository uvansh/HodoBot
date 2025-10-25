# 🌍 HoDo Bot ( Your AI Travel Agent )

An intelligent AI travel assistant combining RAG (Retrieval Augmented Generation) 
and real-time API integration for comprehensive travel planning.

## Features
- 📚 Query multiple travel documents (PDFs & text)
- 🌤️ Real-time weather information
- 💱 Live currency conversion
- 💬 Context-aware conversations
- 📄 Source attribution for all answers
- 💡 History management 
- 😵‍💫 Context window management (less to no halluciantions) 

## Tech Stack
- LangChain for RAG pipeline
- Groq (Llama 3.3 70b) as LLM
- ChromaDB for vector storage
- HuggingFace embeddings
- OpenWeatherMap API
- ExchangeRate API

## Installation
Make sure to make a virtual environment before any installation for isolated workflow.
After that type following command on you terminal or CMD. (Make sure that you are inside project directory)
Just write pip install -r requirements.txt or pip freeze > requirements.txt
Enter your api key by making a .env file or if not using in anywhere sensitive like: cloud, just put it directly into the place where "GROQ_API_KEY" is written.

## Usage
Run the code by typing python main.py or using play button on vs code.

Type your questions
AI will response BOOOMMMM!!!!!!

## Demo
In future...

```

---

## 🧪 Comprehensive Test Scenarios

### Test 1: Pure RAG
```
You: What are the visa requirements for Thailand?
Expected: Answer from documents only
```

### Test 2: Pure Function Calling
```
You: What's the weather in Bangkok right now?
Expected: Real-time API call
```

### Test 3: Hybrid Query
```
You: What's the weather in Tokyo and what should I pack?
Expected: API call + document search, combined answer
```

### Test 4: Conversational Context
```
You: Tell me about Thailand
AI: [answers]
You: What's the weather there?
Expected: Understands "there" = Thailand, calls weather API
```

### Test 5: Multi-step Planning
```
You: I have 50000 INR. Can I afford 10 days in Thailand?
Expected: Currency conversion + budget document search + calculation