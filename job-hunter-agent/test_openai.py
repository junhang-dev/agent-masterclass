import os
import dotenv
from openai import OpenAI

# .env 파일에서 환경 변수를 불러옵니다.
dotenv.load_dotenv()

print("--- OpenAI Embedding Test ---")

# OpenAI 클라이언트를 초기화합니다.
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in .env file.")
    else:
        print("API Key loaded successfully.")
        client = OpenAI(api_key=api_key)

        # 오류가 발생하는 정확한 모델로 임베딩을 요청합니다.
        print(f"Requesting embedding for 'test text' using model 'text-embedding-3-small'...")
        
        response = client.embeddings.create(
            input="This is a test sentence.",
            model="text-embedding-3-small"
        )
        
        # 성공 시, 결과의 일부를 출력합니다.
        print("\nSUCCESS! Embedding created successfully.")
        print(f"Number of embeddings: {len(response.data)}")
        print(f"Vector dimensions: {len(response.data[0].embedding)}")

except Exception as e:
    # 실패 시, 에러 메시지를 출력합니다.
    print(f"\nFAILED! An error occurred: {e}")

print("--- Test Finished ---")