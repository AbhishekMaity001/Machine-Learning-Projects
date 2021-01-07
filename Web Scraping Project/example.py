from bs4 import BeautifulSoup
import requests

with open('sample.html') as html :
    soup = BeautifulSoup(html,'lxml')

# print(soup.prettify())
# match = soup.title.text ### we use class_ bcoz in python _ is a special keyword but in case of id we dont use it
# match = soup.find('div',class_='footer')
#article  = soup.find('div',class_='article') ### find will return only 1 object but find_all will return a list with all tags
for article in soup.find_all('div',class_='article') :
    #print(article, '\n')

    headline = article.h2.a.text
    print(headline)

    summary = article.p.text
    print(summary)
    print()
