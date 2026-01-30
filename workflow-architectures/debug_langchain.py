from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Test 1: The user's current method
try:
    print("Initializing with 'openai:gpt-4o-2024-08-06'...")
    llm1 = init_chat_model("openai:gpt-4o-2024-08-06")
    print(f"Resulting object type: {type(llm1)}")
    if hasattr(llm1, 'model_name'):
        print(f"Model name: {llm1.model_name}")
    elif hasattr(llm1, 'model'):
        print(f"Model: {llm1.model}")
    else:
        print("Could not find model name attribute.")
    
    print("Invoking model...")
    response = llm1.invoke("Hello")
    print(f"Response: {response.content}")

except Exception as e:
    print(f"Error: {e}")

# Test 2: Alternative method
try:
    print("\nInitializing with model='gpt-4o-2024-08-06', model_provider='openai'...")
    llm2 = init_chat_model("gpt-4o-2024-08-06", model_provider="openai")
    print(f"Resulting object type: {type(llm2)}")
    if hasattr(llm2, 'model_name'):
        print(f"Model name: {llm2.model_name}")
except Exception as e:
    print(f"Error: {e}")
