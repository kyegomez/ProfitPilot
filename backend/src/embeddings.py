import os
import openai
from pydantic import BaseModel
from typing import List
from langchain.embeddings import OpenAIEmbeddings, sentence_transformer
from dotenv import load_dotenv

openai.api_key = os.environ.get("OPENAI_API_KEY")

load_dotenv()


class Embedding(BaseModel):
    index: int
    model: str


class Mapping(BaseModel):
    index: int
    name: str


class EmbeddingSelector:
    def __init__(self):
        self.embedding: Embedding
        self.embedding_list: List[Embedding] = []
        self.embedding_map = {}
        self.index_map = {}

    def select_embedding(self, name):
        index = len(self.embedding_list)
        self.embedding = Embedding(index=index, model=name)

    def get_embedding_maps(self):
        return self.embedding_map, self.index_map

    def get_openai_embeddings(self):
        self.openai_embeddings = OpenAIEmbeddings(
            client=openai,
            model="text-embedding-ada-002",
            show_progress_bar=True,
            tiktoken_model_name="t5-small",
            chunk_size=256,
        )
        return self.openai_embeddings

    def get_sentence_transformer_embeddings(self):
        self.sent_trans_embeddings = (
            sentence_transformer.SentenceTransformerEmbeddings()
        )
        return self.sent_trans_embeddings
