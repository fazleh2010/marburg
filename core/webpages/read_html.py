from bs4 import BeautifulSoup


dir='/home/melahi/code/webpage/'
filename='RomArchive.html'

# Read the HTML file
with open(dir+filename, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Example: Extract all links
for link in soup.find_all('a'):
    print(link.get('href'))
