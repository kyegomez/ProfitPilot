from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw
import json
import loguru
import argparse
from parse_html import extract_text_from_html

logger = loguru.logger

MODE = "scout"


def get_driver():
    seleniumwire_options = {"disable_encoding": True, "verify_ssl": False}
    return webdriver.Chrome(seleniumwire_options=seleniumwire_options)


def set_mode(mode):
    global MODE
    if not isinstance(mode, str):
        raise TypeError("Mode must be a string")
    MODE = mode


def scout_request_urls(driver, target_url):
    driver.get(target_url)
    html_content = driver.page_source
    if MODE == "collect":
        responses = grab_responses(driver)
        return responses, html_content
    else:
        urls = [{"url": request.url} for request in driver.requests]
        return urls, html_content


def grab_responses(driver):
    responses = []
    decoded_data = ""
    for request in driver.requests:
        if request.response is None:
            continue
        logger.info(
            f"Request URL: {request.url}, Content-Type: {request.response.headers.get('Content-Type', '')}"
        )

        content_type = request.response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            continue  # Skip non-JSON content types
        data = decodesw(
            request.response.body,
            request.response.headers.get("Content-Encoding", "identity"),
        )
        try:
            decoded_data = data.decode("utf-8")
            responses.append(json.loads(decoded_data))
        except json.JSONDecodeError:
            logger.warning(f"Failed to decode response as JSON: {decoded_data}")
        except UnicodeDecodeError:
            logger.warning(f"Failed to decode response using UTF-8 encoding: {data}")
    return responses


def collect_data(driver, target_url):
    urls, html_content = scout_request_urls(driver, target_url)
    logger.info(f"Scout request urls: {urls}")
    with open("urls.json", "w", encoding="utf-8") as f:
        json.dump(urls, f, ensure_ascii=False, indent=4)
    with open("html_content.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    extract_text_from_html(html_content)
    return {"urls": urls, "html_content": html_content}


def main():
    target_url = input("URL: ")
    if not target_url.startswith("http"):
        target_url = f"http://{target_url}"
    driver = get_driver()
    try:
        result = collect_data(driver, target_url)
        logger.info(f"Result: {result}")
        with open("result.json", "a", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
    finally:
        driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scout or collect data from a target URL."
    )
    parser.add_argument(
        "--mode",
        type=str,
        help="The mode to use to collect data. Default to scout. Change to collect to gather responses.",
    )
    args = parser.parse_args()
    logger.info(f"Running with args: {args}")
    if args.mode is None:
        args.mode = "collect"
    set_mode(args.mode)
    main()
