from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw
import json
import loguru
import argparse

logger = loguru.logger

MODE = "scout"
RESULTS_PATH = "docs/collected_data/results.txt"
HTML_PATH = "docs/collected_data/html_content.html"
INPUT_URL_LIST = "docs/input.txt"


def get_driver():
    seleniumwire_options = {"disable_encoding": True, "verify_ssl": False}
    return webdriver.Chrome(seleniumwire_options=seleniumwire_options)


def set_mode(mode):
    global MODE
    if not isinstance(mode, str):
        raise TypeError("Mode must be a string")
    MODE = mode


def scout_request_urls(driver, target_url):
    logger.info("Scouting target URL: %s", target_url)
    driver.get(target_url)
    html_content = driver.page_source
    with open(HTML_PATH, "w", encoding="utf-8") as file:
        file.write(html_content)
    if MODE == "collect":
        responses = grab_responses(driver)
        with open(RESULTS_PATH, "w", encoding="utf-8") as file:
            file.write(json.dumps(responses))
        return responses, html_content
    else:
        urls = [{"url": request.url} for request in driver.requests]
        logger.debug("Request URLs: %s", urls)
        with open(RESULTS_PATH, "w", encoding="utf-8") as file:
            file.write(json.dumps(urls))

        return urls, html_content


def grab_responses(driver):
    logger.info("Grabbing responses")
    responses = []
    decoded_data = ""
    for request in driver.requests:
        if request.response is None:
            continue
        logger.debug(
            f"Request URL: {request.url}, Content-Type: {request.response.headers.get('Content-Type', '')}"
        )

        content_type = request.response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            continue
        data = decodesw(
            request.response.body,
            request.response.headers.get("Content-Encoding", "identity"),
        )
        logger.debug(f"Response data: {data}")
        try:
            decoded_data = data.decode("utf-8")
            responses.append(json.loads(decoded_data))
        except json.JSONDecodeError:
            logger.warning(f"Failed to decode response as JSON: {decoded_data}")
        except UnicodeDecodeError:
            logger.warning(f"Failed to decode response using UTF-8 encoding: {data}")
    return responses


def collect_data(driver, target_url):
    logger.info("Collecting data")
    urls, html_content = scout_request_urls(driver, target_url)
    return {"urls": urls, "html_content": html_content}


def main(url=None):
    if url is None:
        url = INPUT_URL_LIST
    target_url = ""
    with open(url, "r", encoding="utf-8") as file:
        target_url = file.read()
        if not target_url.startswith("http"):
            target_url = f"http://{target_url}"
        driver = get_driver()
        try:
            result = collect_data(driver, target_url)
            logger.debug(f"Result: {result}")
            return result
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
    logger.debug(f"Running with args: {args}")
    if args.mode is None:
        args.mode = "collect"
    set_mode(args.mode)
    main()
