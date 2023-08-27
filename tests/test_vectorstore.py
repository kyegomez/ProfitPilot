import unittest
from vectordb.vectorstore import (
    VectorStoreSelector,
    VectorStoreOptions,
    EmbeddingOptions,
    RetrieverOptions,
    SplitterOptions,
    SearchOptions,
    Document,
)
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import SelfQueryRetriever
from vectordb.splitters import RecursiveCharacterTextSplitter


class TestVectorStoreSelector(unittest.TestCase):
    def setUp(self):
        self.selector = VectorStoreSelector()

    def test_get_vectorstore(self):
        vectorstore = self.selector.get_vectorstore(VectorStoreOptions.CHROMA)
        self.assertEqual(type(vectorstore), Chroma)

    def test_get_embeddings(self):
        embeddings = self.selector.get_embeddings(EmbeddingOptions.OPENAI_EMBEDDINGS)
        self.assertEqual(type(embeddings), OpenAIEmbeddings)

    def test_get_splitter(self):
        splitter = self.selector.get_splitter(
            SplitterOptions.RECURSIVE_CHARACTER_TEXT_SPLITTER
        )
        self.assertEqual(type(splitter), RecursiveCharacterTextSplitter)

    def test_get_loader(self):
        loader = self.selector.get_loader(PyPDFLoader)
        self.assertEqual(type(loader), PyPDFLoader)

    def test_get_retriever(self):
        retriever = self.selector.get_retriever(RetrieverOptions.SELF_QUERY_RETRIEVER)
        self.assertEqual(type(retriever), SelfQueryRetriever)

    def test_get_base_retriever(self):
        retriever = self.selector.get_base_retriever(
            SearchOptions.SIMILARITY_SEARCH, {"k": 8}
        )
        self.assertEqual(type(retriever), self.selector.retriever)

    def test_add_document(self):
        doc = Document(page_content="Hello world")
        self.selector.add_document([doc])
        self.assertEqual(len(self.selector.vectorstore), 1)

    def test_remove_document(self):
        self.selector.add_document([Document(page_content="Hello world")])
        self.selector.remove_document("Hello world")
        self.assertEqual(len(self.selector.vectorstore), 0)

    def test_similarity_search(self):
        self.selector.add_document([Document(page_content="Hello world")] * 5)
        results = self.selector.similarity_search(query="Hello world")
        self.assertEqual(len(results), 5)

    # Add tests for other methods


if __name__ == "__main__":
    unittest.main()
