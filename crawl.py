import requests, os, hashlib, json, time
from iselenium import SafeSeleniumDriver
from bs4 import BeautifulSoup
from tqdm import tqdm


lang_src = "en-US"
lang_tgt = "ko"

ITEM_TYPE = [
    # "europe-rail",
    "china-high-speed-rail",
    "japan-rail",
    "japan-rail/shinkansen",
]


def hash_url(url: str):
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def crawl_url(url: str, cache=True, cache_dir=".cache/", file_name=None):
    return "deprecated"
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


def crawl_with_selenium(urls: list[str]) -> list[str]:
    htmls = []
    with SafeSeleniumDriver("http://klook.hufs.jae.one:4444/wd/hub") as driver:
        for url in urls:
            driver.get(url)

            htmls.append(driver.page_source)
            print(f"crawled: {driver.current_url}")

            # print(f"title: {driver.title}")

            # h2_tags = driver.find_elements(By.TAG_NAME, "h2")
            # titles = [tag.text for tag in h2_tags if tag.text]

            # print("===== titles =====")
            # print(titles)

            # markdown_elements = driver.find_elements(By.CLASS_NAME, "markdown-content")
            # contents = [tag.text for tag in markdown_elements if tag.text]

            # print("===== contents =====")
            # print(contents)

    return htmls


def extract_trails(htmls: list[str]) -> dict[str, list[str]]:
    trails = []
    for html in htmls:
        soup = BeautifulSoup(html, "html.parser")

        titles = [tag.get_text(strip=True) for tag in soup.select("h2")]
        contents = [
            text
            for tag in soup.select(".markdown-content")
            if (text := tag.get_text(strip=True))
        ]

        trails.append({"titles": titles, "contents": contents})
    return trails


def get_trains_translations(file_name: str):
    trans = []

    with open(file_name, "w", encoding="utf-8") as f:
        for item_type in tqdm(ITEM_TYPE):
            url_src = f"https://www.klook.com/{lang_src}/{item_type}"
            url_tgt = f"https://www.klook.com/{lang_tgt}/{item_type}"

            file_name = f"{lang_src}_{item_type}"
            htmls = crawl_with_selenium([url_src, url_tgt])
            trails = extract_trails(htmls)

            for key in ["titles", "contents"]:
                for src, tgt in zip(trails[0][key], trails[1][key]):
                    item = {"item_type": item_type, "key": key, "src": src, "tgt": tgt}
                    trans.append(item)
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return trans


if __name__ == "__main__":
    # url_src = f"https://www.klook.com/ko/europe-rail"

    # htmls = crawl_with_selenium([url_src])
    # print(htmls[0])

    trans = get_trains_translations("translations/klook_trains_translations.jsonl")
    print(trans[0])
