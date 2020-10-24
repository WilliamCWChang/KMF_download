import json

import pytest
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def get_page_link(page_url):
    pages = []
    r = requests.get(page_url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, "html.parser")
    for a in soup.find_all("a"):
        if "/read/ets/new-order/" in a["href"] and len(a["href"].split("/")) == 6:
            pages.append("https://toefl.kmf.com" + a["href"])
    return pages


def test_get_page_link():
    get_data = get_page_link("https://toefl.kmf.com/read/ets/new-order/1/0")
    expect_data = [
        "https://toefl.kmf.com/read/ets/new-order/1/0",
        "https://toefl.kmf.com/read/ets/new-order/2/0",
        "https://toefl.kmf.com/read/ets/new-order/3/0",
        "https://toefl.kmf.com/read/ets/new-order/4/0",
        "https://toefl.kmf.com/read/ets/new-order/5/0",
        "https://toefl.kmf.com/read/ets/new-order/6/0",
        "https://toefl.kmf.com/read/ets/new-order/7/0",
        "https://toefl.kmf.com/read/ets/new-order/8/0",
        "https://toefl.kmf.com/read/ets/new-order/9/0",
        "https://toefl.kmf.com/read/ets/new-order/10/0",
        "https://toefl.kmf.com/read/ets/new-order/11/0",
        "https://toefl.kmf.com/read/ets/new-order/1/1",
        "https://toefl.kmf.com/read/ets/new-order/1/2",
        "https://toefl.kmf.com/read/ets/new-order/1/3",
    ]
    assert get_data == expect_data


def get_passage_link(page_url):
    passages = {}
    r = requests.get(page_url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, "html.parser")
    for div in soup.find_all("div"):
        title = div.get("data-title")
        detail = div.get("data-detail")
        if title:
            passages[title] = "https://toefl.kmf.com" + detail
    return passages


def test_get_passage_link():
    get_data = get_passage_link("https://toefl.kmf.com/read/ets/new-order/1/3")
    raise AssertionError(get_data)


def get_passage_content(url):
    content = []
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, "html.parser")
    passages = soup.find(id="js-stem-cont").find_all("p")
    for p in passages:
        line = p.get_text(strip=True)
        content.append(line)
    return content


if __name__ == "__main__":
    parents_enable = True
    exist_ok_enable = True
    download_path = "download"

    pages = get_page_link("https://toefl.kmf.com/read/ets/new-order/1/0")
    print(pages)

    passage_dict = {}
    for page in pages:
        passage_dict = {**passage_dict, **get_passage_link(page)}
    print(passage_dict)

    Path(download_path).mkdir(parents=parents_enable, exist_ok=exist_ok_enable)
    all_path = Path(download_path) / "all.md"
    with all_path.open("w", encoding="utf-8") as all_file:
        for title, url in passage_dict.items():
            content = get_passage_content(url)
            single_path = Path(download_path) / (title + ".md")
            print(single_path)
            with single_path.open("w", encoding="utf-8") as file:
                file.write("# " + title + "\n\n\n")
                all_file.write("# " + title + "\n\n\n")
                for c in content:
                    file.write(c)
                    all_file.write(c)
                    file.write("\n")
                    all_file.write("\n")
                file.write("\n-----------------------------\n\n\n")
                all_file.write("\n-----------------------------\n\n\n")
