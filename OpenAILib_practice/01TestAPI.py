import os
from openai import OpenAI

# Initialize the OpenAI client pointing to the Gemini API endpoint
client = OpenAI(
    # Make sure to set this environment variable, or paste your API key directly:
    # api_key="AIzaSyYourGeminiKeyHere...",
    api_key="AIzaSyBJ1QzyW8xDxN995h9IsXM48n9RY3eNP2s",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def test_gemini_via_openai():
    print("Sending request to Gemini via OpenAI SDK...\n")
    
    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="gemini-2.5-flash", # You can also use gemini-2.5-pro or gemini-3-flash-preview
            messages=[
                {"role": "system", "content": "You are a helpful and witty coding assistant."},
                {"role": "user", "content": "who are you"}
            ]
        )
        
        # Extract and print the response
        reply = response.choices[0].message.content
        print("Response from Gemini:")
        print("-" * 20)
        print(reply)
        print("-" * 20)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_gemini_via_openai()