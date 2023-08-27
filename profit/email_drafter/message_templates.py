class TemplateManager:
    def __init__(self):
        self.json_email_schema = """[{
"draft_email":"[DRAFT_EMAIL_RESPONSE]",
"user_email":"[USER_EMAIL_RESPONSE]",
"draft_email_subject":"[DRAFT_EMAIL_SUBJECT_RESPONSE]"
}]"""

    def review_template(self, first_draft: str) -> str:
        return f"""
Please review this draft email. Review it and check that it is a well crafted and appropriate marketing email. Correct any spelling or gramatical errors and make any adjustments you think would enhance the email. Do not embelish or fabricate data. Only include true information given that data in the draft.
Please return the response in this format:
---SCHEMA---
{self.json_email_schema}
---

---DRAFT EMAIL---
{first_draft}
---
"""

    def prospect_profile(self, prospect_name: str, prospect_data: str) -> str:
        return f"""Below is a section of a website about {prospect_name}.
Write a concise summary about {prospect_name}. If the information is not about {prospect_name}, exclude it from your summary. The purpose of this report is sales prospecting for internal use.
---{prospect_name.capitalize()} INFO---
{prospect_data}
---
CONCISE SUMMARY:"""

    def marketing_email_draft(
        self,
        your_company: str,
        your_company_profile: str,
        prospect: str,
        prospect_data: str,
        example_emails: str,
    ) -> str:
        your_company = "ProfitPilot"
        your_company_profile = """
Saas start up breaking new ground in AI marketing. 
- Customized ai automation soluations with a specialty in sales and marketing
- Automated email marketing
- Automated cold calling
- Automated lead generation
"""
        return f"""
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

Here are example email draft you can use for reference:
---EXAMPLES---
{example_emails}
---

Provide your responses in valid JSON format with this schema:
---SCHEMA---
{self.json_email_schema}
---
Please review your response and ensure it is valid JSON before submitting. 
"""

    def prospect_report(self, prospect_name: str, prospect_data: str) -> str:
        prospect = prospect_name
        data = prospect_data
        return f"""
Your goal is to write a profile report about {prospect} for the use of your sales team .

Be sure to include important details for the sales process. This should be addressed as an internal report directly to the sales team. Look for ways to leverage the knowledge for sales. You know that your team knows what they are doing so you are breif and to the point. You dont waste time telling them things they already know. You just report the facts.


INFORMATION ABOUT {prospect}:
{data}

INCLUDE THE FOLLOWING PIECES IN YOUR RESPONSE:
- Gather any contact information you can find. Including specific names, emails and numbers you can collect
- A breif on the company including where its located, how long its been in operation, size of the business and anyother relevant information
- Check if social media is available to view and what types. 
- What other software they may be using on their website including forms, and hosting.
- Do not make up any data that is not directly referenced in the documentation
    
Be specific and complete in your response.
Review your response and make corrections if required.

IF YOU RECEIVE AN ERROR:
- Report it as an error and do not write the report.


RESPONSE TEMPLATE:
Company Overview:
- YOUR_RESPONSE
Internet presence:
- YOUR_RESPONSE
Website and software:
- YOUR_RESPONSE
Summary:
- YOUR_RESPONSE
"""
