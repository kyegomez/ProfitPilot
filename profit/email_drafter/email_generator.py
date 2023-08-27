import os
import subprocess
import json
import openai
from langchain.text_splitter import TokenTextSplitter
from dotenv import load_dotenv
from urllib.parse import urlparse


def extract_domain_name(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Split the netloc by dots
    domain_parts = parsed_url.netloc.split(".")
    # Get the second last part (usually the main domain name)
    domain_name = domain_parts[-2] if len(domain_parts) > 1 else domain_parts[0]
    return domain_name


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def call_openai(prospect_report):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prospect_report}],
    )
    return response.choices[0].message.content


def run_email_draft():
    with open("docs/collected_data/results.txt", "r") as doc:
        doc = doc.read()
    with open("docs/input.txt", "r") as url:
        url = url.read()
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=50)
    prospect_data = text_splitter.split_text(doc)
    json_email_schema = """[{
"draft_email":"[DRAFT_EMAIL_RESPONSE]",
"user_email":"[USER_EMAIL_RESPONSE]",
"draft_email_subject":"[DRAFT_EMAIL_SUBJECT_RESPONSE]"
}]"""
    your_company = "ProfitPilot"
    your_company_profile = """
Saas start up breaking new ground in AI marketing. 
- Customized ai automation soluations with a specialty in sales and marketing
- Automated email marketing
- Automated cold calling
- Automated lead generation
"""
    prospect = extract_domain_name(url=url)
    reports = []
    for doc in prospect_data:
        prospect_report = f"""Below is a section of a website about {prospect}.
Write a concise summary about {prospect}. If the information is not about {prospect}, exclude it from your summary. The purpose of this report is sales prospecting for internal use.
---{prospect.capitalize()} INFO---
{prospect_data}
---
CONCISE SUMMARY:"""
        reports.append(call_openai(prospect_report))
    consolidate_report = "\n".join(reports)
    prospect_data = call_openai(consolidate_report)
    final_report = f"""
You are a sales guru. You are a specialist in SaaS marketing. You have been hired by a start up called Move Right. You are drafting sales emails to go out to {prospect}. 
You are working for {your_company}. We are looking to drive prospects into a sales funnel to ensure a continious flow of leads. 
Only include factual information. If you are not sure if the information is factual, do not include it.
If you encounter an error in the data please just respond with the error message.
This is the profile of our company:
---OUR COMPANY---
{your_company_profile}
---
Select one or two options that would be the best fit for {prospect}.

This is the information we have collected on {prospect}:
---PROSPECT INFO---
{prospect_data}
---

Provide your responses in valid JSON format with this schema:
---SCHEMA---
{json_email_schema}
---
Please review your response and ensure it is valid JSON before submitting. 
        """
    # =================
    # FEED THIS INTO YOUR LLAMA MODEL
    # =================
    final_result = call_openai(final_report)
    json_response = json.loads(final_result)
    print(json_response)
    user_email = json_response[0]["user_email"]
    draft_email = json_response[0]["draft_email"]
    draft_email_subject = json_response[0]["draft_email_subject"]
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
    with open("./docs/output.txt", "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    run_email_draft()
