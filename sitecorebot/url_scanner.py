from urllib.parse import urlparse
from bot_memory import BotUrlMemory

IGNORE_DOMAINS = ["reddit.com", "stackexchange.com", "linkedin.com"]

def url_scanner(text):
    words = text.split()
    urls = []
    for word in words:
        parsed = urlparse(word.strip("<>.,").split("|")[0])
        if parsed.scheme and parsed.netloc:
            include = True
            for ignored in IGNORE_DOMAINS:
                if ignored in parsed.netloc:
                    include = False
                    break
            if include: urls.append(parsed)

    for url in urls:
        print(f"URL: {url.scheme}://{url.netloc}{url.path}")
        bot_url_memory: BotUrlMemory = BotUrlMemory(url)
        bot_url_memory.start()

print(f"URL Scanner Online.")
