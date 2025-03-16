"""
AI service for interacting with Anthropic's Claude API
"""

import os
import re
import json
from typing import List, Dict, Tuple

import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Anthropic API key
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables or .env file")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Constants
MAX_TOKENS = 1000
CONFIDENCE_THRESHOLD = 0.4
MODEL_PROGRESSION = [
    "claude-3-7-sonnet-20250219",  # Start with the balanced model
    "claude-3-opus-20240229",      # Use the most powerful model for difficult questions
]
DEFAULT_MODEL = MODEL_PROGRESSION[0]


def clean_html(html_content: str) -> str:
    """Remove HTML tags from content"""
    clean_text = re.sub(r'<.*?>', '', html_content)
    return clean_text


def get_memory_tags(term: str, original_query: str, model: str) -> List[str]:
    """Generate memory tags for the search term"""
    system_prompt = """
    You are a helpful assistant that generates memory tags for search terms.
    Your task is to create 3-5 related words or short phrases that might help the user remember this term in the future.
    These should be single words or very short phrases (1-3 words) that are strongly associated with the main term.
    Do not include the original term itself.
    Format your response as a JSON array of strings.
    """

    user_message = f"""
    Original query: {original_query}
    Term to generate memory tags for: {term}

    Generate 3-5 memory tags that would help someone remember this term.
    """

    try:
        response = client.messages.create(
            model=model,
            max_tokens=100,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract JSON array from response
        content = response.content[0].text
        # Find anything that looks like a JSON array
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                tags = json.loads(json_str)
                # Ensure we have a list of strings
                tags = [str(tag).strip() for tag in tags if tag]
                return tags[:5]  # Limit to 5 tags
            except json.JSONDecodeError:
                return []
        return []
    except Exception as e:
        print(f"Error generating memory tags: {e}")
        return []


def query_ai(query: str, conversation_history: List[Dict], model: str) -> Tuple[str, float, str]:
    """
    Query the AI model with the given query and conversation history
    Returns: (answer, confidence, model_used)
    """
    # Prepare conversation history for the AI
    messages = []

    # Add conversation history
    for entry in conversation_history:
        if entry.get("role") == "user":
            messages.append({"role": "user", "content": entry.get("content", "")})
        elif entry.get("role") == "assistant":
            messages.append({"role": "assistant", "content": entry.get("content", "")})

    # Add the current query if not already in history
    if not messages or messages[-1]["role"] != "user" or messages[-1]["content"] != query:
        messages.append({"role": "user", "content": query})

    system_prompt = """
    You are WhatsThatAgain, an AI assistant specialized in helping people remember things that are "on the tip of their tongue."

    When responding to queries:
    1. Provide a direct, concise answer to what the person is trying to remember
    2. Include a confidence score between 0.0 and 1.0 on a separate line in the format "Confidence: X.X"
    3. If you're not sure, say so and provide your best guess with a lower confidence score
    4. Do not include explanations unless specifically asked

    Example response format:
    The actor you're thinking of is Tom Hanks.
    Confidence: 0.9

    If you're uncertain:
    I believe the song you're thinking of is "Wonderwall" by Oasis, but I'm not entirely sure.
    Confidence: 0.6
    """

    try:
        response = client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=messages
        )

        answer = response.content[0].text.strip()

        # Extract confidence score
        confidence_match = re.search(r'Confidence:\s*(\d+\.\d+)', answer)
        confidence = float(confidence_match.group(1)) if confidence_match else CONFIDENCE_THRESHOLD

        # Remove confidence line from answer
        answer = re.sub(r'Confidence:\s*\d+\.\d+', '', answer).strip()

        return answer, confidence, model
    except Exception as e:
        return f"Error: {str(e)}", 0.0, model


def process_answer(answer: str, query: str, confidence: float) -> str:
    """Process and format the AI's answer"""
    if confidence < 0.3:
        return f"I'm not confident about this, but: {answer}"
    return answer
