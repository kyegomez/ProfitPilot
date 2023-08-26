from urllib.parse import urlparse


def extract_domain_name(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Split the netloc by dots
    domain_parts = parsed_url.netloc.split(".")
    # Get the second last part (usually the main domain name)
    domain_name = domain_parts[-2] if len(domain_parts) > 1 else domain_parts[0]
    return domain_name
