# /// script
# dependencies = [
#     "requests",
# ]
# ///
import re
import requests

url = 'https://hts.usitc.gov/reststop/exportList?from=0000&to=9999.99.9999&format=CSV&styles=false'
response = requests.get(url)
response.raise_for_status()
csv_content = response.text

pattern = re.compile(r'[^"]$')
lines = csv_content.splitlines()

with open('htscode.csv', 'w', encoding='utf-8') as f:
    f.write(lines[0] + '\n')  # write the header
    for line in lines[1:]:
        if pattern.search(line):
            f.write(line)
        else:
            f.write(line + '\n')
