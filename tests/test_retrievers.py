import unittest
from vectordb.retrivers import (
    RetrieverSelector,
    RetrieverOptions,
    SelfQueryRetriever,
    EnsembleRetriever,
    ContextualCompressionRetriever,
)


class TestRetrieverSelector(unittest.TestCase):
    def setUp(self):
        self.selector = RetrieverSelector(
            default_retriever=RetrieverOptions.SELF_QUERY_RETRIEVER
        )

    def test_lazy_initialization_self_query(self):
        retriever = self.selector.get_self_query_retriever()
        self.assertEqual(retriever, SelfQueryRetriever)

    def test_lazy_initialization_ensemble(self):
        retriever = self.selector.get_ensemble_retriever()
        self.assertEqual(retriever, EnsembleRetriever)

    def test_select(self):
        retriever = self.selector.select("SELF_QUERY_RETRIEVER")
        self.assertEqual(retriever, SelfQueryRetriever)


if __name__ == "__main__":
    unittest.main()
