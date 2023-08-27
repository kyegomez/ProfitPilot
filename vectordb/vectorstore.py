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
        persistent_directory="docs/vectorstore",
        name="chroma_vectorstore",
    ):
        super().__init__()
        self.vector_store = default_vector_store.value
        self.chorma_vector_store = VectorStoreOptions.CHROMA
        self.embeddings_selector = EmbeddingSelector()
        self.embeddings = self.get_embeddings(default_embeddings)
        self.retriever_selector = RetrieverSelector()
        self.retriever = self.get_retriever(default_retriever)
        self.splitter_selector = SplitterSelector()
        self.splitter = self.get_splitter(default_splitter)
        self.loader_selector = LoaderSelector()
        self.loader = self.get_loader(default_loader)
        self.persistent_directory = persistent_directory
        self.name = name
        self.vectorstore_maps = {}
        self.vectorstore_index = {}
        self.initialize_maps(VectorStoreOptions)
        self.vectorstore = self.get_vectorstore(default_vector_store)
        self.vectorstore = self.vectorstore(
            embedding_function=self.embeddings,
            collection_name=self.name,
            persistent_directory=self.persistent_directory,
        )
        self.base_retriever = self.get_base_retriever(
            search_type=default_search_type,
            kwarg_options=default_kwarg_options,
        )
        self.compression_retriever = self.get_compression_retriever()
        self.document_compressor = self.get_document_compressor()

    def get_vectorstore(self, name):
        logger.info("Getting Vectorstore", name)
        self.vectorstore = self.select(name)
        return self.vectorstore

    def get_embeddings(self, name):
        logger.info("Getting Embeddings", name)
        return self.embeddings_selector.select(name)

    def get_splitter(self, name):
        logger.info("Getting Splitter")
        return self.splitter_selector.select(name)

    def get_loader(self, name):
        logger.info("Getting Loader")
        return self.loader_selector.select(name)

    def get_retriever(self, name):
        logger.info("Getting Retriever")
        return self.retriever_selector.select(name)

    def add_document(self, documents: List[Document]):
        self.vector_store.add_documents(self=self.vectorstore, documents=documents)
        return

    def remove_document(self, documents: str):
        self.vectorstore.delete(self=self.vectorstore, kwargs={"documents": documents})

    def similarity_search(self, query):
        self.vectorstore.similarity_search(
            self=self.vectorstore, query=query, kwargs={"k": 5}
        )

    def similarity_search_by_vector(self, query):
        self.vectorstore.similarity_search(query=query, kwargs={"k": 5})

    def max_marginal_relevance_search(self, query):
        self.vectorstore.max_marginal_relevance_search(
            query=query, kwargs={"k": 3, "fetch_k": 10}
        )

    def get_collection(self, collection_id):
        self.vectorstore.get(ids=collection_id)

    def get_base_retriever(self, search_type, kwarg_options):
        logger.info("Getting base retriever")
        if kwarg_options is None:
            kwarg_options = {"k": 8}
        return self.vectorstore.as_retriever(
            search_type=search_type, kwargs=kwarg_options
        )

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
        return self.retriever.aget_relevant_documents(query=query)
