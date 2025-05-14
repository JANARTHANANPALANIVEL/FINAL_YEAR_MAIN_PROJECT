import re
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_url(url):
    # Remove any potentially harmful characters
    return re.sub(r'[^a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=]', '', url)