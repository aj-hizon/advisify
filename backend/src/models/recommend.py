from pydantic import BaseModel
from typing import List


class RecommendationInput(BaseModel):
    thesis_title: str
    project_types: List[str] = []


class AdviserRecommendation(BaseModel):
    name: str
    expertise_description: str
    thesis_supervised: str
    expertise_description_similarity: float
    thesis_supervised_similarity: float
    overall_similarity: float


class RecommendationOutput(BaseModel):
    recommendations: List[AdviserRecommendation]
