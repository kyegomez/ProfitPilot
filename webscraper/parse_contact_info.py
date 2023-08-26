import re
import loguru

logger = loguru.logger


def parse_info():
    from bs4 import BeautifulSoup

    # Reading the contents of the uploaded HTML file
    html_file_path = "./html_content.html"

    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Creating a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Displaying the first part of the HTML content to get an overview
    logger.info(soup.prettify()[:1000])


def identify_platform(soup):
    platform_list = []
    wp_generator_tag = soup.find("meta", attrs={"name": "generator"})
    if wp_generator_tag and "WordPress" in wp_generator_tag.get("content", ""):
        platform_list.append("WordPress")

    if soup.find("script", text=lambda x: "Shopify" in str(x)):
        platform_list.append("Shopify")

    if soup.find("script", text=lambda x: "Google Analytics" in str(x)):
        platform_list.append("Google Analytics")

    if soup.find("script", text=lambda x: "Facebook" in str(x)):
        platform_list.append("Facebook")

    if soup.find("script", text=lambda x: "Twitter" in str(x)):
        platform_list.append("Twitter")

    if soup.find("script", text=lambda x: "smartmoving" in str(x)):
        platform_list.append("smartmoving")
    return "unknown" if platform_list[0] is None else platform_list


def identify_integrations(soup):
    integrations = []

    # Looking for Google Analytics
    if soup.find("script", text=lambda x: "google-analytics.com" in str(x)):
        integrations.append("Google Analytics")

    # Looking for Facebook integration
    if soup.find("script", text=lambda x: "facebook.net" in str(x)):
        integrations.append("Facebook")

    # Looking for Twitter integration
    if soup.find("script", text=lambda x: "twitter.com" in str(x)):
        integrations.append("Twitter")

    # Add more integration checks here if needed

    return integrations


# Function to extract contact information
def extract_contact_info(soup):
    contact_info = {}

    # Regular expression to match email addresses
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

    # Regular expression to match phone numbers (simple pattern)
    phone_pattern = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")

    # Extracting email addresses
    email_matches = email_pattern.findall(str(soup))
    if email_matches:
        contact_info["Emails"] = list(set(email_matches))

    # Extracting phone numbers
    phone_matches = phone_pattern.findall(str(soup))
    if phone_matches:
        contact_info["Phone Numbers"] = list(set(phone_matches))

    # Extracting physical address (if available in a specific tag, e.g., footer)
    address_tag = soup.find("address")
    if address_tag:
        contact_info["Address"] = address_tag.get_text()

    return contact_info
