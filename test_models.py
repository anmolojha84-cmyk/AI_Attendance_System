from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6KIiiq2VrP0WbgZ_RZDqwEuMCBRfzn6X8mXLXGavhRwRw"
)

try:
    for model in client.models.list():
        print(model.name)

except Exception as e:
    print(e)