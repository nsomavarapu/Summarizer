from bs4 import BeautifulSoup
from urllib import urlopen
import sys

url = sys.argv[-1]
outfile = open('../resources/Alaska_Air_clean', 'w')

url = url
html = urlopen(url).read()
soup = BeautifulSoup(html)

outfile.write(soup.get_text().encode('ascii', 'ignore'))
