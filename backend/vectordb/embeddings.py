import os
import openai
import loguru
from enum import Enum
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from dotenv import load_dotenv
from vectordb.selector import BaseSelector

openai.api_key = os.environ.get("OPENAI_API_KEY")

load_dotenv()

logger = loguru.logger


class EmbeddingOptions(Enum):
    OPENAI_EMBEDDINGS: OpenAIEmbeddings
    SENTENCE_TRANSFORMERS_EMBEDDING: SentenceTransformerEmbeddings


class EmbeddingSelector(BaseSelector):
    def __init__(self, default_embedding=EmbeddingOptions.OPENAI_EMBEDDINGS):
        super().__init__()
        self.embedding = default_embedding
        logger.info("Initializing EmbeddingSelector")
        self.openai_embeddings = EmbeddingOptions.OPENAI_EMBEDDINGS
        self.sent_trans_embeddings = EmbeddingOptions.SENTENCE_TRANSFORMERS_EMBEDDING
        self.initialize_maps(list(EmbeddingOptions))

    def get_openai_embeddings(self):
        logger.info("Getting OpenAI Embeddings")
        self.openai_embeddings.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_embeddings.model = "text-embedding-ada-002"
        self.openai_embeddings.show_progress_bar = True
        self.openai_embeddings.request_timeout = 60
        return self.select("openai_embeddings")

    def sentence_transformer_embeddings(self):
        logger.info("Getting Sentence Transformer Embeddings")
        self.sent_trans_embeddings.show_progress_bar = True
        self.sent_trans_embeddings.request_timeout = 60
        return self.select("sentence_transformer_embeddings")
