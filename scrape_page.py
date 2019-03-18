from bs4 import BeautifulSoup
import requests

part_no_list = [
    "34017",
    "62269-1",
    "96525458",
    "05507-00420",
    "05946-01401",
    "FS0002594",
    "MIL-DTL-8794-12",
    "MIL-H-8794",
    "M8794-12",
    "12Z33460-12",
    "MIL-H-8794-12",
    "MS24585-1281",
    "MS+24585-1281",
    "10125758",
    "5360001829953",
    "MS24585-1281",
    "12524346",
    "12524346",
    "465-4346",
    "2+0040-094",
    "10126880"
]
data_dict = {}

for part_no in part_no_list:
    r = requests.get(f"https://www.radwell.com/en-US/Search/?q={part_no}")
    soup = BeautifulSoup(r.text, 'html.parser')

    search_results = soup('div', id="searchResults")
    if search_results:
        search_rows = search_results[0]('a', {'class': ['searchResult']})

    items = []

    for row in search_rows:
        part_no_found = row('div', {'class': ['partno']})[0].h2.text.strip()
        if part_no_found == part_no:
            items.append(
                {
                    "manufacturer": row('div', {'class': ['mfgr']})[0].h2.text.strip(),
                    "part_no": part_no_found,
                    "new_price": row('p', {'class': ['price', 'fnfp']})[0].span.text.strip(),
                    "item_url": "https://www.radwell.com" + row['href']
                }
            )
    data_dict[part_no] = items

with open("radwell_info.txt", "w") as data_file:
    print(data_dict, file=data_file)