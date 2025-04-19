import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.models.recommend import RecommendationInput
from src.utils.embeddings import encode_text, load_embeddings
from src.models.recommend import AdviserRecommendation, RecommendationOutput

df, expertise_embeddings, past_thesis_embeddings = load_embeddings()
weight_expertise = 0.3
weight_past_thesis = 0.7


def get_recommendations(input_data: RecommendationInput) -> RecommendationOutput:
    input_text = input_data.thesis_title.strip()
    if input_data.project_types:
        input_text += f"({', '.join(input_data.project_types)})"

    user_embedding = encode_text(input_text)

    sim_expertise = cosine_similarity(user_embedding, expertise_embeddings)
    sim_past_thesis = cosine_similarity(user_embedding, past_thesis_embeddings)

    overall_similarity = (
        weight_expertise * sim_expertise + weight_past_thesis * sim_past_thesis
    )

    df["adviser_area_of_expertise_similarity"] = np.clip(sim_expertise[0], 0, 1)
    df["adviser_past_thesis_supervised_similarity"] = np.clip(sim_past_thesis[0], 0, 1)
    df["overall_similarity"] = np.clip(overall_similarity[0], 0, 1)

    top_recommendations = df.nlargest(5, "overall_similarity")

    recommendations = []
    for _, row in top_recommendations.iterrows():
        recommendations.append(
            AdviserRecommendation(
                name=row["name"],
                expertise_description=row["area_of_expertise_description"],
                thesis_supervised=row["past_thesis_topics_supervised"],
                expertise_description_similarity=row[
                    "adviser_area_of_expertise_similarity"
                ],
                thesis_supervised_similarity=row[
                    "adviser_past_thesis_supervised_similarity"
                ],
                overall_similarity=row["overall_similarity"],
            )
        )
    return RecommendationOutput(recommendations=recommendations)
