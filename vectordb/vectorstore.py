import loguru
from enum import Enum
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.base import (
    DocumentCompressorPipeline,
)
from langchain.document_transformers import (
    EmbeddingsClusteringFilter,
    EmbeddingsRedundantFilter,
)
from typing import List
from vectordb.embeddings import EmbeddingSelector, EmbeddingOptions
from vectordb.retrivers import RetrieverSelector, RetrieverOptions
from vectordb.splitters import SplitterSelector, SplitterOptions
from vectordb.loaders import LoaderSelector, LoaderOptions
from vectordb.selector import BaseSelector


logger = loguru.logger


class VectorStoreOptions(Enum):
    CHROMA = Chroma


class SearchOptions(Enum):
    SIMILARITY_SEARCH = "similarity_search"
    SIMILARITY_SEARCH_BY_VECTOR = "similarity_search_by_vector"
    MAX_MARGINAL_RELEVANCE_SEARCH = "max_marginal_relevance_search"


class VectorStoreSelector(BaseSelector):
    def __init__(
        self,
        default_vector_store=VectorStoreOptions.CHROMA,
        default_embeddings=EmbeddingOptions.OPENAI_EMBEDDINGS,
        default_retriever=RetrieverOptions.SELF_QUERY_RETRIEVER,
        default_splitter=SplitterOptions.RECURSIVE_CHARACTER_TEXT_SPLITTER,
        default_loader=LoaderOptions.PYPDF_LOADER,
        default_search_type=SearchOptions.SIMILARITY_SEARCH,
        default_kwarg_options={"k": 8},
        persistent_directory="docs/vector_store",
    ):
        super().__init__()
        logger.info("Initializing Vectorstore")
        self.embeddings_selector = EmbeddingSelector()
        self.embeddings = self.embeddings_selector.select(str(default_embeddings))
        self.retriever_selector = RetrieverSelector()
        self.retriever = self.retriever_selector.select(str(default_retriever))
        self.splitter_selector = SplitterSelector()
        self.splitter = self.splitter_selector.select(str(default_splitter))
        self.loader_selector = LoaderSelector()
        self.loader = self.loader_selector.select(str(default_loader))
        self.persistent_directory = persistent_directory
        self.vector_store_map = {}
        self.vector_store_index = {}
        self.initialize_maps(VectorStoreOptions)
        logger.debug(f"Selected Initialized Maps:{self.vector_store_map}")
        self.chorma_vector_store = VectorStoreOptions.CHROMA
        self.vector_store = self.select(str(default_vector_store))
        self.vectordb = self.get_vector_store.value(
            embedding_function=self.embeddings,
            collection_name=default_vector_store.value,
            persistent_directory=self.persistent_directory,
        )
        self.base_retriever = self.get_base_retriever(
            search_type=default_search_type,
            kwarg_options=default_kwarg_options,
        )
        self.compression_retriever = self.get_compression_retriever()
        self.document_compressor = self.get_document_compressor()

    def get_vector_store(self, name):
        logger.info("Getting Vector_store", name)
        self.vector_store = self.select(name)
        logger.debug("Selected Vector_store:", self.vector_store)
        return self.vector_store

    def get_chroma(self, name):
        logger.info("Getting Chroma", name)
        return self.select("CHROMA")

    def add_document(self, documents: List[Document]):
        logger.info("Adding document")
        return self.vectordb.add_documents(self=self.vectordb, documents=documents)

    def remove_document(self, documents: str):
        logger.info("Removing document")
        self.vectordb.delete(self=self.vectordb, kwargs={"documents": documents})

    def similarity_search(self, query):
        logger.info("similarity_search")
        return self.vectordb.similarity_search(
            self=self.vectordb, query=query, kwargs={"k": 5}
        )

    def similarity_search_by_vector(self, query):
        logger.info("similarity_search_by_vector")
        return self.vectordb.similarity_search(query=query, kwargs={"k": 5})

    def max_marginal_relevance_search(self, query):
        logger.info("max_marginal_relevance_search")
        return self.vectordb.max_marginal_relevance_search(
            query=query, kwargs={"k": 3, "fetch_k": 10}
        )

    def get_collection(self, collection_id):
        logger.info("Getting collection")
        return self.vectordb.get(ids=collection_id)

    def get_base_retriever(self, search_type, kwarg_options):
        logger.info("Getting base retriever")
        if kwarg_options is None:
            kwarg_options = {"k": 8}
        return self.vectordb.as_retriever(search_type=search_type, kwargs=kwarg_options)

    def get_document_compressor(self):
        logger.info("Getting document compressor")
        return DocumentCompressorPipeline(
            transformers=[
                EmbeddingsRedundantFilter(
                    embeddings=self.embeddings,
                ),
                EmbeddingsClusteringFilter(embeddings=self.embeddings),
            ]
        )

    def get_compression_retriever(self):
        logger.info("Getting compression retriever")
        retriever = self.retriever_selector.get_contextual_compression_retriever()
        self.retriever = retriever(
            base_compressor=self.document_compressor,
            base_retriever=self.base_retriever,
        )
        return self.retriever

    def compression_search(self, query):
        logger.info("Running compression search")
        if self.retriever != ContextualCompressionRetriever:
            self.compression_retriever = self.get_compression_retriever()
        return self.retriever.get_relevant_documents(query=query)
