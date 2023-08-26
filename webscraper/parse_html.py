from bs4 import BeautifulSoup
import loguru

logger = loguru.logger


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    logger.info("Paragraphs: %s", paragraphs)

    with open("paragraphs.txt", "w", encoding="utf-8") as f:
        f.write(f"\n{paragraphs}")
    return f"\n{paragraphs}"
