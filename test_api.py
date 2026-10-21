from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6KIiiq2VrP0WbgZ_RZDqwEuMCBRfzn6X8mXLXGavhRwRw"
)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Hello"
)

print(response.text)