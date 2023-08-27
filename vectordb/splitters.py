from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TextSplitter,
    MarkdownHeaderTextSplitter,
    NLTKTextSplitter,
    PythonCodeTextSplitter,
    SentenceTransformersTokenTextSplitter,
    TokenTextSplitter,
)
from enum import Enum
from vectordb.selector import BaseSelector
import loguru

logger = loguru.logger


class SplitterOptions(Enum):
    RECURSIVE_CHARACTER_TEXT_SPLITTER = RecursiveCharacterTextSplitter
    CHARACTER_TEXT_SPLITTER = CharacterTextSplitter
    TEXT_SPLITTER = TextSplitter
    MARKDOWN_HEADER_TEXT_SPLITTER = MarkdownHeaderTextSplitter
    NLTK_TEXT_SPLITTER = NLTKTextSplitter
    PYTHON_CODE_TEXT_SPLITTER = PythonCodeTextSplitter
    SENTENCE_TRANSFORMERS_TOKEN_TEXT_SPLITTER = SentenceTransformersTokenTextSplitter
    TOKEN_TEXT_SPLITTER = TokenTextSplitter


class SplitterSelector(BaseSelector):
    def __init__(
        self, default_splitter=SplitterOptions.RECURSIVE_CHARACTER_TEXT_SPLITTER
    ):
        super().__init__()
        self.RECURSIVE_CHARACTER_TEXT_SPLITTER = (
            SplitterOptions.RECURSIVE_CHARACTER_TEXT_SPLITTER
        )
        self.CHARACTER_TEXT_SPLITTER = SplitterOptions.CHARACTER_TEXT_SPLITTER
        self.TEXT_SPLITTER = SplitterOptions.TEXT_SPLITTER
        self.MARKDOWN_HEADER_TEXT_SPLITTER = (
            SplitterOptions.MARKDOWN_HEADER_TEXT_SPLITTER
        )
        self.NLTK_TEXT_SPLITTER = SplitterOptions.NLTK_TEXT_SPLITTER
        self.PYTHON_CODE_TEXT_SPLITTER = SplitterOptions.PYTHON_CODE_TEXT_SPLITTER
        self.SENTENCE_TRANSFORMERS_TOKEN_TEXT_SPLITTER = (
            SplitterOptions.SENTENCE_TRANSFORMERS_TOKEN_TEXT_SPLITTER
        )
        self.TOKEN_TEXT_SPLITTER = SplitterOptions.TOKEN_TEXT_SPLITTER
        self.splitter = default_splitter
        self.initialize_maps(SplitterOptions)

    def get_recursive_character_text_splitter(self):
        logger.info("Getting recursive_character_text_splitter")
        return self.select("RECURSIVE_CHARACTER_TEXT_SPLITTER")

    def get_character_text_splitter(self):
        logger.info("Getting character_text_splitter")
        return self.select("CHARACTER_TEXT_SPLITTER")

    def get_text_splitter(self):
        logger.info("Getting text_splitter")
        return self.select("TEXT_SPLITTER")

    def get_markdown_header_text_splitter(self):
        logger.info("Getting markdown_header_text_splitter")
        return self.select("MARKDOWN_HEADER_TEXT_SPLITTER")

    def get_nltk_text_splitter(self):
        logger.info("Getting nltk_text_splitter")
        return self.select("NLTK_TEXT_SPLITTER")

    def get_python_code_text_splitter(self):
        logger.info("Getting python_code_text_splitter")
        return self.select("PYTHON_CODE_TEXT_SPLITTER")

    def get_sentence_transformers_token_text_splitter(self):
        logger.info("Getting sentence_transformers_token_text_splitter")
        return self.select("SENTENCE_TRANSFORMERS_TOKEN_TEXT_SPLITTER")

    def get_token_text_splitter(self):
        logger.info("Getting token_text_splitter")
        return self.select("TOKEN_TEXT_SPLITTER")
