import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key NOT found!")
    exit()

print("API key found!")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say hello in one short sentence."
    )

    print("Gemini response:")
    print(response.text)

except Exception as e:
    print("Error:")
    print(e)