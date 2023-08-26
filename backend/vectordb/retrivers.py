from langchain.retrievers import (
    SelfQueryRetriever,
    EnsembleRetriever,
    ContextualCompressionRetriever,
)
from enum import Enum
import loguru
from vectordb.selector import BaseSelector

logger = loguru.logger


class RetrieverOptions(Enum):
    self_query_retriever = SelfQueryRetriever
    ensemble_retriever = EnsembleRetriever
    contextual_compression_retriever = ContextualCompressionRetriever


class RetrieverSelector(BaseSelector):
    def __init__(self, default_retriever=RetrieverOptions.self_query_retriever):
        super().__init__()
        logger.info("Initializing RetrieverSelector")
        self.self_query_retriever: RetrieverOptions = (
            RetrieverOptions.self_query_retriever
        )
        self.ensemble_retriever: RetrieverOptions = RetrieverOptions.ensemble_retriever
        self.contextual_compression_retriever: RetrieverOptions = (
            RetrieverOptions.contextual_compression_retriever
        )
        self.retriever = default_retriever
        self.initialize_maps(list(RetrieverOptions))

    def get_self_query_retriever(self):
        logger.info("Getting  self_query_retriver")
        return self.select("self_query_retriever")

    def get_ensemble_retriever(self):
        logger.info("Getting  ensemble_retriver")
        return self.select("ensemble_retriever")

    def get_contextual_compression_retriever(self):
        logger.info("Getting  contextual_compression_retriver")
        return self.select("contextual_compression_retriever")
