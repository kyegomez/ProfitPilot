import asyncio
import os

# Tools
from contextlib import contextmanager
from typing import Optional

import pandas as pd
from langchain.agents import tool
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.docstore.document import Document
from langchain.memory.chat_message_histories import FileChatMessageHistory
from langchain.tools.human.tool import HumanInputRun

ROOT_DIR = "./data/"

#gmail
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.chains.qa_with_sources.loading import BaseCombineDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import Clarifai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool, DuckDuckGoSearchRun
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials
from pydantic import Field


llm = Clarifai(
    pat="890cdb0cb5aa4795ba51af9670120a1e", 
    user_id="meta", 
    app_id="Llama-2", 
    model_id="llama2-70b-chat"
)





# from langchain.agents.agent_toolkits import ZapierToolkit
# from langchain.utilities.zapier import ZapierNLAWrapper


@contextmanager
def pushd(new_dir):
    """Context manager for changing the current working directory."""
    prev_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)


@tool
def process_csv(
    llm, csv_file_path: str, instructions: str, output_path: Optional[str] = None
) -> str:
    """Process a CSV by with pandas in a limited REPL.\
 Only use this after writing data to disk as a csv file.\
 Any figures must be saved to disk to be viewed by the human.\
 Instructions should be written in natural language, not code. Assume the dataframe is already loaded."""
    with pushd(ROOT_DIR):
        try:
            df = pd.read_csv(csv_file_path)
        except Exception as e:
            return f"Error: {e}"
        agent = create_pandas_dataframe_agent(llm, df, max_iterations=30, verbose=False)
        if output_path is not None:
            instructions += f" Save output to disk at {output_path}"
        try:
            result = agent.run(instructions)
            return result
        except Exception as e:
            return f"Error: {e}"


async def async_load_playwright(url: str) -> str:
    """Load the specified URLs using Playwright and parse using BeautifulSoup."""
    from bs4 import BeautifulSoup
    from playwright.async_api import async_playwright

    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()
            soup = BeautifulSoup(page_source, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            results = "\n".join(chunk for chunk in chunks if chunk)
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


def run_async(coro):
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coro)


@tool
def browse_web_page(url: str) -> str:
    """Verbose way to scrape a whole webpage. Likely to cause issues parsing."""
    return run_async(async_load_playwright(url))


def _get_text_splitter():
    return RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
    )


class WebpageQATool(BaseTool):
    name = "query_webpage"
    description = (
        "Browse a webpage and retrieve the information relevant to the question."
    )
    text_splitter: RecursiveCharacterTextSplitter = Field(
        default_factory=_get_text_splitter
    )
    qa_chain: BaseCombineDocumentsChain

    def _run(self, url: str, question: str) -> str:
        """Useful for browsing websites and scraping the text information."""
        result = browse_web_page.run(url)
        docs = [Document(page_content=result, metadata={"source": url})]
        web_docs = self.text_splitter.split_documents(docs)
        results = []
        # TODO: Handle this with a MapReduceChain
        for i in range(0, len(web_docs), 4):
            input_docs = web_docs[i : i + 4]
            window_result = self.qa_chain(
                {"input_documents": input_docs, "question": question},
                return_only_outputs=True,
            )
            results.append(f"Response from window {i} - {window_result}")
        results_docs = [
            Document(page_content="\n".join(results), metadata={"source": url})
        ]
        return self.qa_chain(
            {"input_documents": results_docs, "question": question},
            return_only_outputs=True,
        )

    async def _arun(self, url: str, question: str) -> str:
        raise NotImplementedError

query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))

# !pip install duckduckgo_search
# web_search = DuckDuckGoSearchRun()

# get from https://nla.zapier.com/docs/authentication/ after logging in):
# os.environ["ZAPIER_NLA_API_KEY"] = os.environ.get("ZAPIER_NLA_API_KEY", "")

# zapier = ZapierNLAWrapper()
# zapier_toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
# zapier_tools = zapier_toolkit.get_tools()




# # Gmail
# class GmailTool:
#     def __init__(
#         self,
#         token_file:  str = "token.json",
#         scopes = ["https://mail.google.com/"],
#         client_secrets_file = "credientials.json",
#     ):
#         super().__init__()
#         self.token_file = token_file
#         self.scopes = scopes
#         self.client_secrets_file = client_secrets_file   
#     def run(self):
#         self.credentials = get_gmail_credentials(
#             token_file=self.token_file,
#             scopes=self.scopes,
#             client_secrets_file=self.client_secrets_file
#         )

#         self.api_resource = build_resource_service(credentials=self.credentials)
#         self.toolkit = GmailToolkit(api_resource=self.api_resource)
#         self.tools = self.toolkit.get_tools()
#         return self.tools
# gmailtool = GmailTool()
# gmailtool = gmailtool.run()