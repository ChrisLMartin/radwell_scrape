from bs4 import BeautifulSoup
import requests
import pandas

input_df = pandas.read_csv("Input_File.csv")

data = []

for part_no in input_df["Part Number Entered"].tolist():
    r = requests.get(f"https://www.radwell.com/en-US/Search/?q={part_no}")
    soup = BeautifulSoup(r.text, 'html.parser')

    search_results = soup('div', id="searchResults")
    if search_results:
        search_rows = search_results[0]('a', {'class': ['searchResult']})

    
    for row in search_rows:
        part_no_found = row('div', {'class': ['partno']})[0].h2.text.strip()
        if part_no_found == part_no:
            data.append(
                {
                    "manufacturer": row('div', {'class': ['mfgr']})[0].h2.text.strip(),
                    "part_no": part_no_found,
                    "new_price": row('p', {'class': ['price', 'fnfp']})[0].span.text.strip(),
                    "item_url": "https://www.radwell.com" + row['href']
                }
            )

output_df = pandas.DataFrame(data)

output_df.to_csv("output.csv")