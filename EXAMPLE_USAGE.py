from email_drafter import email_generator
from webscraper.parse_data import parse_info
from webscraper.scraper import main
from profit.tools import scrape_data, draft_email

# YOU NEED A SERVICE AGENT JSON OBJECT AND A CLIENT JSON OBJECT FROM GOOGLE TO ENABLE EMAIL
# PIPE THE RESULT INTO LLAMA
# RUN SCRAPER BEFORE YOU RUN THE DRAFTER

if __name__ == "__main__":
    # Web Scraper
    # main("https://huggingface.co/")
    # parse_info()
    scrape_data("https://huggingface.co/")

    # Generate Report
    # email_generator.run_email_draft()
    draft_email()
