from fastapi import APIRouter, HTTPException, status
from src.models.recommend import RecommendationOutput, RecommendationInput
from src.services.recommend_service import get_recommendations


recommend_router = APIRouter()


@recommend_router.post("/recommend", response_model=RecommendationOutput)
async def recommend_advisers(input_data: RecommendationInput) -> RecommendationOutput:
    if not input_data.thesis_title.strip() and not input_data.project_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Thesis title or project types must be provided.",
        )
    return get_recommendations(input_data)
