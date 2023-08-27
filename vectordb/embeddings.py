import os
import openai
import loguru
from enum import Enum
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from dotenv import load_dotenv
from vectordb.selector import BaseSelector

api_key = os.environ.get("OPENAI_API_KEY")

load_dotenv()

logger = loguru.logger


class EmbeddingOptions(Enum):
    OPENAI_EMBEDDINGS = OpenAIEmbeddings
    SENTENCE_TRANSFORMERS_EMBEDDING = SentenceTransformerEmbeddings


EmbeddingOptions.OPENAI_EMBEDDINGS.value.openai_api_key = api_key


class EmbeddingSelector(BaseSelector):
    def __init__(self, default_embedding=EmbeddingOptions.OPENAI_EMBEDDINGS):
        super().__init__()
        self.embedding = self.select(str(default_embedding))
        logger.info("Initializing EmbeddingSelector")
        self.openai_embeddings = EmbeddingOptions.OPENAI_EMBEDDINGS
        self.sentence_transformer_embeddings = (
            EmbeddingOptions.SENTENCE_TRANSFORMERS_EMBEDDING
        )
        self.initialize_maps(EmbeddingOptions)

    def get_openai_embeddings(self):
        logger.info("Getting OpenAI Embeddings")
        embedding = self.select("OPENAI_EMBEDDINGS")
        if not isinstance(embedding, OpenAIEmbeddings):
            self.openai_embeddings = self.openai_embeddings.value(
                openai_api_key=os.environ.get("OPENAI_API_KEY"),
                client=openai,
                model="text-embedding-ada-002",
                show_progress_bar=True,
                request_timeout=60,
            )
        return

    def get_sentence_transformer_embeddings(self):
        logger.info("Getting Sentence Transformer Embeddings")
        if not isinstance(
            self.sentence_transformer_embeddings, SentenceTransformerEmbeddings
        ):
            self.sentence_transformer_embeddings = SentenceTransformerEmbeddings()
        return self.select("sentence_transformer_embeddings")
