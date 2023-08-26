from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    TextLoader,
    PythonLoader,
    DirectoryLoader,
    PlaywrightURLLoader,
)
from enum import Enum
from loguru import logger
from vectordb.selector import BaseSelector


class LoaderOptions(Enum):
    pypdf_loader: PyPDFLoader
    unstructured_markdown_loader: UnstructuredMarkdownLoader
    text_loader: TextLoader
    python_loader: PythonLoader
    directory_loader: DirectoryLoader
    playwright_url_loader: PlaywrightURLLoader


class LoaderSelector(BaseSelector):
    def __init__(self, default_loader=LoaderOptions.pypdf_loader):
        super().__init__()
        logger.info("Initializing LoaderSelector")
        self.py_pdf_loader = LoaderOptions.pypdf_loader
        self.unstructured_markdown_loader = LoaderOptions.unstructured_markdown_loader
        self.text_loader = LoaderOptions.text_loader
        self.python_loader = LoaderOptions.python_loader
        self.directory_loader = LoaderOptions.directory_loader
        self.playwright_url_loader = LoaderOptions.playwright_url_loader
        self.loader = default_loader
        self.initialize_maps(list(LoaderOptions))

    def get_py_pdf_loader(self):
        return self.select("pypdf_loader")

    def get_unstructured_markdown_loader(self):
        return self.select("unstructured_markdown_loader")

    def get_text_loader(self):
        return self.select("text_loader")

    def get_python_loader(self):
        return self.select("python_loader")

    def get_directory_loader(self):
        return self.select("directory_loader")

    def get_playwright_url_loader(self):
        return self.select("playwright_url_loader")
