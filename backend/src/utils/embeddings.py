import os
import ast
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def load_embeddings():
    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )  # Get the backend/src directory
    data_path = os.path.join(base_dir, "data", "advisers_dummy_data.csv")

    df = pd.read_csv(data_path)
    df["expertise_embeddings"] = df["expertise_embeddings"].apply(ast.literal_eval)
    df["past_thesis_embeddings"] = df["past_thesis_embeddings"].apply(ast.literal_eval)

    expertise_embeddings = np.stack(df["expertise_embeddings"].values)
    past_thesis_embeddings = np.stack(df["past_thesis_embeddings"].values)

    return df, expertise_embeddings, past_thesis_embeddings


def encode_text(text: str):
    return model.encode([text])
