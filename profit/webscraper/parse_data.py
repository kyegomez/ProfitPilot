import re
import loguru
import json

logger = loguru.logger

CONTACT_INFO_PATH = "./docs/collected_data/contact_info.txt"
PLATFORM_INFO_PATH = "./docs/collected_data/platform_information.txt"
INTEGRATIONS_PATH = "./docs/collected_data/integrations.txt"
URL_PATH = "./docs/collected_data/urls.txt"
PARAGRAPH_PATH = "./docs/collected_data/paragraphs.txt"
HTML_CONTENT_PATH = "./docs/collected_data/html_content.html"


def parse_info(html_content_path=HTML_CONTENT_PATH):
    from bs4 import BeautifulSoup

    with open(html_content_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    paragraphs = [p.get_text() for p in soup.find_all("p")]
    logger.info("Paragraphs: %s", paragraphs)
    anchors = [a.get("href") for a in soup.find_all("a")]
    logger.info("Anchors: %s", anchors)
    contact_info = get_contact_info(soup)
    logger.info(contact_info)
    platform_information = get_platform_information(soup)
    logger.info(platform_information)
    integrations = get_integrations(soup)
    logger.info(integrations)

    with open(PARAGRAPH_PATH, "a", encoding="utf-8") as file:
        for paragraph in paragraphs:
            file.write(f"{paragraph}\n")
        file.write("---\n")
    with open(URL_PATH, "a", encoding="utf-8") as file:
        for anchor in anchors:
            file.write(f"{anchor}\n")
        file.write("---\n")
    with open(CONTACT_INFO_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(f"{contact_info}\n---\n", indent=4))
    with open(PLATFORM_INFO_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(f"{platform_information}\n---\n", indent=4))
    with open(INTEGRATIONS_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(f"{integrations}\n---\n", indent=4))

    if not (overview := soup.prettify()):
        raise ValueError(f"{logger.error('Could not parse the HTML content')}")
    logger.info(overview[:500])
    return overview


def get_platform_information(soup):
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

    if soup.find("script", text=lambda x: "LinkedIn" in str(x)):
        platform_list.append("LinkedIn")

    if soup.find("script", text=lambda x: "Pinterest" in str(x)):
        platform_list.append("Pinterest")

    if soup.find("script", text=lambda x: "YouTube" in str(x)):
        platform_list.append("YouTube")

    if soup.find("script", text=lambda x: "SalesForce" in str(x)):
        platform_list.append("SalesForce")

    if soup.find("script", text=lambda x: "HubSpot" in str(x)):
        platform_list.append("HubSpot")

    if soup.find("script", text=lambda x: "Wix" in str(x)):
        platform_list.append("Wix")

    if soup.find("script", text=lambda x: "Squarespace" in str(x)):
        platform_list.append("Squarespace")

    if soup.find("script", text=lambda x: "Shopify" in str(x)):
        platform_list.append("Shopify")

    return "no platforms collected" or platform_list


def get_integrations(soup):
    integrations = []

    if soup.find("script", text=lambda x: "google-analytics.com" in str(x)):
        integrations.append("Google Analytics")

    if soup.find("script", text=lambda x: "facebook.net" in str(x)):
        integrations.append("Facebook")

    if soup.find("script", text=lambda x: "twitter.com" in str(x)):
        integrations.append("Twitter")

    if soup.find("script", text=lambda x: "linkedin.com" in str(x)):
        integrations.append("LinkedIn")

    if soup.find("script", text=lambda x: "pinterest.com" in str(x)):
        integrations.append("Pinterest")

    if soup.find("script", text=lambda x: "youtube.com" in str(x)):
        integrations.append("YouTube")

    if soup.find("script", text=lambda x: "salesforce.com" in str(x)):
        integrations.append("SalesForce")

    if soup.find("script", text=lambda x: "hubspot.com" in str(x)):
        integrations.append("HubSpot")

    if soup.find("script", text=lambda x: "wix.com" in str(x)):
        integrations.append("Wix")

    if soup.find("script", text=lambda x: "squarespace.com" in str(x)):
        integrations.append("Squarespace")

    if soup.find("script", text=lambda x: "shopify.com" in str(x)):
        integrations.append("Shopify")

    if soup.find("script", text=lambda x: "wordpress.com" in str(x)):
        integrations.append("WordPress")

    return "no integrations collected" or integrations


def get_contact_info(soup):
    contact_info = {}

    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

    phone_pattern = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")

    if email_matches := email_pattern.findall(str(soup)):
        contact_info["Emails"] = list(set(email_matches))

    if phone_matches := phone_pattern.findall(str(soup)):
        contact_info["Phone Numbers"] = list(set(phone_matches))

    if address_tag := soup.find("address"):
        contact_info["Address"] = address_tag.get_text()

    return contact_info or "no contact information collected"


if __name__ == "__main__":
    parse_info()
