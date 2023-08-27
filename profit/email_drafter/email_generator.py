import os
import subprocess
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import TokenTextSplitter
from dotenv import load_dotenv
from email_drafter.message_templates import TemplateManager
from webscraper.main import main as webscraper_main

templates = TemplateManager()

WEBSITE_INPUT = "docs/input.txt"
EXAMPLE_INPUT = "docs/input.json"
TEXT_OUTPUT = "docs/output.txt"
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def get_prospect_data():
    with open(EXAMPLE_INPUT, "r", encoding="utf-8") as file:
        prospect_websites = file.readlines()
        for website in prospect_websites:
            

    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(doc)
    chat = ChatOpenAI(temperature=0.1)
    with open("./docs/input.json", "r", encoding="utf-8") as file:
        example_messages = json.loads(file.read())
    templates.(company=)

    content = chat(messages).content
    # print(content)
    json_response = json.loads(content)
    print(json_response)
    user_email = json_response["response"][0]["user_email"]
    draft_email = json_response["response"][0]["draft_email"]
    draft_email_subject = json_response["response"][0]["draft_email_subject"]
    print(user_email, draft_email_subject, draft_email)
    with open("./docs/output.txt", "w", encoding="utf-8") as f:
        f.write(user_email + "\n" + draft_email_subject + "\n" + draft_email)

    def send_draft_email(user_email, draft_email, draft_email_subject):
        subprocess.Popen(
            [
                "python",
                "./scripts/gmail.py",
                "--draft_email",
                draft_email,
                "--user_email",
                user_email,
                "--draft_email_subject",
                draft_email_subject,
            ],
            bufsize=1024,
        )

    send_draft_email(
        user_email=user_email,
        draft_email=draft_email,
        draft_email_subject=draft_email_subject,
    )
