from openai import OpenAI
import os
from dotenv import load_dotenv
from config.prompts import system_prompt
from config.tools_schema import tools
from tools.weather import get_weather
from tools.currency import get_currency
from tools.timezone import get_timezone
import json

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

available_functions = {"get_weather":get_weather,"get_currency":get_currency,"get_timezone":get_timezone}

messages = [{'role':'system','content':system_prompt}]

while True:
    user_input = input("You: ")

    if user_input.lower() in ['exit','bye','quit']:
        print("Hodo: Byee...")
        break
    
    messages.append({'role':'user','content':user_input})
    
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=messages,
        tools=tools,
        tool_choice='auto',
    )
    
    message = response.choices[0].message
    
    if message.tool_calls:
        print("Thinking...")
        for tool_call in message.tool_calls:
            function_name=tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
    if function_name in available_functions:
        result = available_functions[function_name](**function_args)
        messages.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":json.dumps(result)
        })
    else:
        result = {"error":"Function not found."}
    
    assistant_content = response.choices[0].message.content
    messages.append({'role':'assistant','content':assistant_content})
    
    print()
    
    print(f"Hodo: {response.choices[0].message.content}")