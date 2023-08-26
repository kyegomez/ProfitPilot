from src.embeddings import EmbeddingSelector
import unittest


class TestEmbeddingSelector(unittest.TestCase):
    def test_get_embedding_maps(self):
        selector = EmbeddingSelector()
        selector.get_embedding_maps()
        assert selector.embedding_map is not None
        assert selector.index_map is not None

    def test_get_openai_embeddings(self):
        selector = EmbeddingSelector()
        selector.get_openai_embeddings()
        assert selector.openai_embeddings is not None

    def test_get_sentence_transformer_embeddings(self):
        selector = EmbeddingSelector()
        selector.get_sentence_transformer_embeddings()
        assert selector.sent_trans_embeddings is not None

    def test_select_embedding(self):
        selector = EmbeddingSelector()
        selector.select_embedding("text-embedding-ada-002")
        assert selector.embedding is not None
