import unittest
from vectordb.embeddings import (
    EmbeddingSelector,
    EmbeddingOptions,
)
from langchain.embeddings import (
    OpenAIEmbeddings,
    SentenceTransformerEmbeddings,
)
import loguru

logger = loguru.logger


class TestEmbeddingSelector(unittest.TestCase):
    def setUp(self):
        self.selector = EmbeddingSelector()

    def test_initialization(self):
        self.assertIsNotNone(self.selector.embedding)
        self.assertEqual(self.selector.embedding, EmbeddingOptions.OPENAI_EMBEDDINGS)

    def test_lazy_initialization_openai(self):
        self.selector.get_openai_embeddings()
        logger.info(self.selector.option_index)
        self.assertIsInstance(self.selector.openai_embeddings, OpenAIEmbeddings)

    def test_lazy_initialization_sentence_transformer(self):
        self.selector.get_sentence_transformer_embeddings()
        logger.info(self.selector.option_index)
        self.assertIsInstance(
            self.selector.sentence_transformer_embeddings, SentenceTransformerEmbeddings
        )

    def test_select(self):
        self.selector.select("OPENAI_EMBEDDINGS")
        self.assertEqual(
            self.selector.embedding, EmbeddingOptions.OPENAI_EMBEDDINGS.value
        )


if __name__ == "__main__":
    unittest.main()
