import unittest
from vectordb.splitters import (
    SplitterSelector,
    SplitterOptions,
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TextSplitter,
    MarkdownHeaderTextSplitter,
    NLTKTextSplitter,
    PythonCodeTextSplitter,
    SentenceTransformersTokenTextSplitter,
    TokenTextSplitter,
)


class TestSplitterSelector(unittest.TestCase):
    def setUp(self):
        self.selector = SplitterSelector(
            default_splitter=SplitterOptions.RECURSIVE_CHARACTER_TEXT_SPLITTER
        )

    def test_lazy_initialization_recursive_character(self):
        splitter = self.selector.get_recursive_character_text_splitter()
        self.assertEqual(splitter, RecursiveCharacterTextSplitter)

    def test_lazy_initialization_character(self):
        splitter = self.selector.get_character_text_splitter()
        self.assertEqual(splitter, CharacterTextSplitter)

    def test_lazy_initialization_recursivecharactertextsplitter(self):
        splitter = self.selector.get_recursive_character_text_splitter()
        self.assertEqual(splitter, RecursiveCharacterTextSplitter)

    def test_lazy_initialization_charactertextsplitter(self):
        splitter = self.selector.get_character_text_splitter()
        self.assertEqual(splitter, CharacterTextSplitter)

    def test_lazy_initialization_textsplitter(self):
        splitter = self.selector.get_text_splitter()
        self.assertEqual(splitter, TextSplitter)

    def test_lazy_initialization_markdownheadertextsplitter(self):
        splitter = self.selector.get_markdown_header_text_splitter()
        self.assertEqual(splitter, MarkdownHeaderTextSplitter)

    def test_lazy_initialization_nltktextsplitter(self):
        splitter = self.selector.get_nltk_text_splitter()
        self.assertEqual(splitter, NLTKTextSplitter)

    def test_lazy_initialization_pythoncodetextsplitter(self):
        splitter = self.selector.get_python_code_text_splitter()
        self.assertEqual(splitter, PythonCodeTextSplitter)

    def test_lazy_initialization_sentencetransformerstokentextsplitter(self):
        splitter = self.selector.get_sentence_transformers_token_text_splitter()
        self.assertEqual(splitter, SentenceTransformersTokenTextSplitter)

    def test_lazy_initialization_tokentextsplitter(self):
        splitter = self.selector.get_token_text_splitter()
        self.assertEqual(splitter, TokenTextSplitter)


if __name__ == "__main__":
    unittest.main()
