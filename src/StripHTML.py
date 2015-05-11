from bs4 import BeautifulSoup
from urllib import urlopen

url = "http://www.cnn.com/2015/05/08/politics/uk-eu-referendum-usa/"
html = urlopen(url).read()
soup = BeautifulSoup(html)

print soup.get_text()
