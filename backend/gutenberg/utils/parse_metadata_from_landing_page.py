import bs4


def parse_metada_from_html(content: str | bytes):
    soup = bs4.BeautifulSoup(content, "html.parser")
    metadata = soup.find("table", {"class": "bibrec"}).find_all("tr")
    metadata_dict = {}
    for row in metadata:
        try:
            key = row.find("th").text.strip()
            value = row.find("td").text.strip()
            metadata_dict[key] = value
        except:
            pass
    return metadata_dict
