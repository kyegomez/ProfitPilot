import streamlit as st
from profit.main import ProfitPilot


# Define variables for ProfitPilot
AI_NAME = "Athena"
AI_ROLE = "Sales Representative"
EXTERNAL_TOOLS = None
COMPANY_NAME = "ABC Company"
COMPANY_VALUES = "Quality, Innovation, Customer Satisfaction"
CONVERSATION_TYPE = "Cold Email"  
CONVERSATION_PURPOSE = "discuss our new product"
COMPANY_BUSINESS = "APAC AI"
SALESPERSON_NAME = "John Doe"
HUMAN_IN_THE_LOOP = False
PROSPECT_NAME = "Jane Smith"  # Add the prospect's name here

# Create an instance of the ProfitPilot class
pilot = ProfitPilot(
    ai_name=AI_NAME,
    ai_role=AI_ROLE,
    external_tools=EXTERNAL_TOOLS,
    company_name=COMPANY_NAME,
    company_values=COMPANY_VALUES,
    conversation_type=CONVERSATION_TYPE,
    conversation_purpose=CONVERSATION_PURPOSE,
    company_business=COMPANY_BUSINESS,
    salesperson_name=SALESPERSON_NAME,
    human_in_the_loop=HUMAN_IN_THE_LOOP,
    prospect_name=PROSPECT_NAME  # Add the prospect's name as an argument
)

# Define the task you want the agent to perform
# Adjusted for email format
task = f"""
Subject: Introducing {COMPANY_NAME}'s Newest Product—A Perfect Fit for {PROSPECT_NAME}

Hi {PROSPECT_NAME},

I hope this email finds you well. My name is {SALESPERSON_NAME}, and I'm with {COMPANY_NAME}. We specialize in {COMPANY_BUSINESS}, and I'm excited to share some news that aligns closely with your values—{COMPANY_VALUES}.

I'd love the opportunity to discuss our latest product with you. Would you be open to exploring how it could benefit your team?

Looking forward to your response!

Best,
{SALESPERSON_NAME}
"""


def main():
    st.title("ProfitPilot")
    st.write("Welcome to profit pilot enter in your sales leads emails and information for personalized deal flow")

    if st.button("Run"):
        response = pilot.run(task)
        st.write(f"ProfitPilot: {response}")

    user_input = st.text_input("Your response:")
    if st.button("Send"):
        response = pilot.run(user_input)
        st.write(f"Profitpilot: {response}")


if __name__ == "__main__":
    main()


# # Run the task using the ProfitPilot instance
# pilot.run(task)