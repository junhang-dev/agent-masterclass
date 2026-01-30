from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text)