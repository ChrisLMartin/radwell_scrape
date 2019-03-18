from bs4 import BeautifulSoup
import requests
import csv

# open the file in universal line ending mode 
with open('Input_File.csv', 'rU') as infile:
  # read the file as a dictionary for each row ({header : value})
  reader = csv.DictReader(infile)
  data = {}
  for row in reader:
    for header, value in row.items():
      try:
        data[header].append(value)
      except KeyError:
        data[header] = [value]

# extract the variables you want
part_no_list = data['Part Number Entered']

data_dict = {}

for part_no in part_no_list:
    r = requests.get(f"https://www.radwell.com/en-US/Search/?q={part_no}")
    soup = BeautifulSoup(r.text, 'html.parser')

    # search_results = [div['id'] for div in soup('div', id = True)]

    search_results = soup('div', id="searchResults")
    if search_results:
        search_rows = search_results[0]('a', {'class': ['searchResult']})

    items = []

    for row in search_rows:
        part_no_found = row('div', {'class': ['partno']})[0].h2.text.strip()
        if part_no_found == part_no:
            items.append(
                {
                    "m": row('div', {'class': ['mfgr']})[0].h2.text.strip(),
                    "pn": part_no_found,
                    "np": row('p', {'class': ['price', 'fnfp']})[0].span.text.strip(),
                    "i": "https://www.radwell.com" + row['href']
                }
            )
    data_dict[part_no] = items

with open("radwell_info2.txt", "w") as data_file:
    print(data_dict, file=data_file)


with open('test2.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in data_dict.items():
       writer.writerow([key, value])