
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using Gemini based on retrieved context.
    """

    prompt = f"""
    You are an enterprise knowledge assistant.

    Answer the user's question using only the provided context.
    If the answer is not available in the context,
    clearly say that you don't know.

    Context:
    {context}

    User Question:
    {query}

    Answer:
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
