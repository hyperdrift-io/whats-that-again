"""
Search router for the WhatsThatAgain API
"""

import uuid
import random
from typing import List, Dict

from fastapi import APIRouter, HTTPException

from app.models.schemas import SearchRequest, SearchResponse
from app.services.ai_service import (
    query_ai, get_memory_tags, process_answer,
    MODEL_PROGRESSION, DEFAULT_MODEL
)
from app.services.usage_service import check_usage_limit

router = APIRouter()

# In-memory storage for conversation history
# In a production app, this would be a database
conversation_history = {}


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search endpoint for querying the AI
    """
    # Check usage limit
    limit_reached, usage_info = check_usage_limit()
    if limit_reached:
        raise HTTPException(status_code=429, detail="Daily query limit reached")

    query = request.query
    session_id = request.sessionId or str(uuid.uuid4())
    try_next_model = request.tryNextModel

    # Get or create conversation history for this session
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    history = conversation_history[session_id]

    # Determine which model to use
    model_level = 0
    if try_next_model and history:
        # Get the last model used
        last_model = None
        for entry in reversed(history):
            if entry.get("model"):
                last_model = entry.get("model")
                break

        if last_model:
            try:
                current_index = MODEL_PROGRESSION.index(last_model)
                # Move to next model if available
                if current_index < len(MODEL_PROGRESSION) - 1:
                    model_level = current_index + 1
            except ValueError:
                # If model not found in progression, use default
                model_level = 0

    model = MODEL_PROGRESSION[model_level]

    # Query the AI
    answer, confidence, model_used = query_ai(query, history, model)

    # Process the answer
    processed_answer = process_answer(answer, query, confidence)

    # Generate memory tags
    memory_tags = get_memory_tags(processed_answer, query, model_used)

    # Update conversation history
    history.append({
        "role": "user",
        "content": query
    })
    history.append({
        "role": "assistant",
        "content": processed_answer,
        "model": model_used
    })

    # Limit history size
    if len(history) > 20:
        history = history[-20:]

    # Update the conversation history
    conversation_history[session_id] = history

    # Return the response
    return SearchResponse(
        answer=processed_answer,
        confidence=confidence,
        usage_info=usage_info,
        memoryTags=memory_tags,
        sessionId=session_id,
        model=model_used,
        modelLevel=model_level
    )
