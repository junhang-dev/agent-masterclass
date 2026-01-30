import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key found: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")

if not api_key:
    print("Error: OPENAI_API_KEY not found in environment.")
    exit(1)

client = OpenAI(api_key=api_key)

def test_model(model_name):
    print(f"\nTesting access to model: {model_name}...")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        print(f"✅ Success! Response: {response.choices[0].message.content}")
    except OpenAIError as e:
        print(f"❌ Failed. Error: {e}")

# Test a usually available model
test_model("gpt-3.5-turbo")

# Test the requested model
test_model("gpt-4o-2024-08-06")

# Test base gpt-4o
test_model("gpt-4o")
