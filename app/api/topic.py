from fastapi import APIRouter, HTTPException, Query
from rag.retriever import retrieve_context
from rag.generator import generate_explanation

router = APIRouter()


@router.get("/topic")
def get_topic_explanation(
    query: str = Query(..., description="The topic to explain"),
    provider: str = Query("openai", description="LLM provider"),
    model: str = Query("gpt-4.1-nano", description="LLM: Model name"),
):
    """
    Get an explanation for a given topic using the specified LLM provider using RAG (Retrieval-Augmented Generation).
    """

    try:
        context = retrieve_context(query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    explanation = generate_explanation(query, context, provider, model)
    return {
        "topic": query,
        "context": context,
        "explanation": explanation,
    }
