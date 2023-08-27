import unittest
from vectordb.loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    TextLoader,
    PythonLoader,
    DirectoryLoader,
    PlaywrightURLLoader,
    LoaderSelector,
    LoaderOptions,
)  # Replace 'your_package' with the actual package name


class TestLoaderSelector(unittest.TestCase):
    def setUp(self):
        self.selector = LoaderSelector(default_loader=LoaderOptions.PYPDF_LOADER)

    def test_lazy_initialization_pypdf(self):
        loader = self.selector.get_py_pdf_loader()
        self.assertEqual(loader, PyPDFLoader)

    def test_lazy_initialization_text(self):
        loader = self.selector.get_text_loader()
        self.assertEqual(loader, TextLoader)

    def test_lazy_initialization_pypdfloader(self):
        loader = self.selector.get_py_pdf_loader()
        self.assertEqual(loader, PyPDFLoader)

    def test_lazy_initialization_unstructuredmarkdownloader(self):
        loader = self.selector.get_unstructured_markdown_loader()
        self.assertEqual(loader, UnstructuredMarkdownLoader)

    def test_lazy_initialization_textloader(self):
        loader = self.selector.get_text_loader()
        self.assertEqual(loader, TextLoader)

    def test_lazy_initialization_pythonloader(self):
        loader = self.selector.get_python_loader()
        self.assertEqual(loader, PythonLoader)

    def test_lazy_initialization_directoryloader(self):
        loader = self.selector.get_directory_loader()
        self.assertEqual(loader, DirectoryLoader)

    def test_lazy_initialization_playwrighturlloader(self):
        loader = self.selector.get_playwright_url_loader()
        self.assertEqual(loader, PlaywrightURLLoader)
