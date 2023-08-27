import os
import json
import openai
import loguru
import pandas as pd
from dotenv import load_dotenv

from langchain.document_loaders import JSONLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from webscraper.main import main as webscraper
from webscraper.main import INPUT_URL_LIST, HTML_PATH, RESULTS_PATH
from webscraper.parse_data import (
    parse_info,
    CONTACT_INFO_PATH,
    INTEGRATIONS_PATH,
    PLATFORM_INFO_PATH,
    URL_PATH,
    PARAGRAPH_PATH,
)
from email_drafter import url_parse, message_templates

OUTPUT_PATH = "./docs/collected_data/output.txt"

logger = loguru.logger

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")



def get_company_page():
    url_list = []
    with open("INPUT_URL_LIST", "r", encoding="utf-8") as file:
        url_list = file.readlines()
    for url in url_list:
        url = url.strip()
        company_name = url_parse.extract_domain_name(url=url)
        if not url.startswith("https://"):
            url = f"https://{url}"
            url_list.append(url)

        webscraper(url=url)

        parse_info(HTML_PATH)

        with open(PARAGRAPH_PATH, "r", encoding="utf-8") as file:
            paragraph = file.read()
        with open(URL_PATH, "r", encoding="utf-8") as file:
            url = file.read()
        with open(CONTACT_INFO_PATH, "r", encoding="utf-8") as file:
            contact_info = file.read()
        with open(PLATFORM_INFO_PATH, "r", encoding="utf-8") as file:
            platform_info = file.read()
        with open(INTEGRATIONS_PATH, "r", encoding="utf-8") as file:
            integrations = file.read()
        company_information = [
            {
                "paragraph": paragraph,
            },
            {
                "url": url,
            },
            {
                "contact_info": contact_info,
            },
            {
                "platform_info": platform_info,
            },
            {"integrations": integrations},
        ]
        company_information_schema = [
            {
                paragraph: str,
                url: str,
                contact_info: str,
                platform_info: str,
                integrations: str,
            }
        ]
        for entry in company_information:
            with open(RESULTS_PATH, "a", encoding="utf-8") as file:
                file.write(json.dumps(entry, indent=4))
        print(f"You have {len(company_information)} document(s)")
        loader = JSONLoader(
            file_path=RESULTS_PATH,
            jq_schema=json.dumps(company_information_schema),
            text_content=True,
        )
        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=50
        )

        docs = text_splitter.split_documents(data)

        print(f"You now have {len(docs)} documents")

        manager = message_templates.TemplateManager()
        for doc in docs:
            prospect_profile = manager.prospect_profile(
                prospect_name=company_name, prospect_data=json.dumps(doc)
            )

            prospect_report = manager.prospect_report(
                prospect_data=prospect_profile, prospect_name=company_name
            )

             # =========================
            # pipe this to llama. function is just there for show.
            # call_a_llama(prospect_report)
            # =========================

            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                message={"role": "user", "content": prospect_report},
            )
            output = response.choices[0].message

            with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
                f.write(output + "\n---\n")

            return output["output_text"]


i__name__ == "__main__":
    print(get_company_page())
