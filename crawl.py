import random, requests, os, hashlib


def hash_url(url: str):
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def crawl_url(url: str, cache=True, cache_dir=".cache/", file_name=None):
    os.makedirs(cache_dir, exist_ok=True)
    if cache:
        cache_path = os.path.join(
            cache_dir, (file_name if file_name else hash_url(url)) + ".html"
        )

        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()

    response = requests.get(url)
    print("crawling:", url)
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    return response.text


lang_src = "en-US"
lang_tgt = "ko"
ITEM_TYPE = [
    "europe-rail",
    "china-high-speed-rail",
    "japan-rail",
    "japan-rail/shinkansen",
]

item_type = random.choice(ITEM_TYPE)


if __name__ == "__main__":
    url = f"https://www.klook.com/{lang_src}/{item_type}"

    file_name = f"{lang_src}_{item_type}"
    html = crawl_url(url, file_name=file_name)
    print(html)
    print("target:", url)
