from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

system_prompt = """You are a enthusiastic, helpful and smart travel assistant.
Your name is Hodo (travel agent).
Your work is to help user with the traveling like 
- Planning their trip.
- Deciding budget.
- Accomodations and Places.
- Weather conditions.
- Timezone.
- Currency conversions.
- Much more related to traveling.

Make sure to give responses in a concise and short way.
If user asks for something out of context, not related to traveling,
politely reject the request and stay in topic

"""

messages = [{'role':'system','content':system_prompt}]

while True:
    user_input = input("You: ")

    if user_input.lower() in ['exit','bye','quit']:
        print("Hodo: Byee...")
        break
    
    messages.append({'role':'user','content':user_input})
    
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=messages
    )
    
    assistant_content = response.choices[0].message.content
    messages.append({'role':'assistant','content':assistant_content})
    
    print()
    
    print(f"Hodo: {response.choices[0].message.content}")