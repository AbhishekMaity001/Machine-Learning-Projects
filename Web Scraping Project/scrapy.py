from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://coreyms.com').text

soup = BeautifulSoup(source,'lxml')

csv_file = open('cms_scraper.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Headline','summary','video_link'])

# article = soup.find('article')
# print(article.prettify())

for article in soup.find_all('article'):

    headline = article.h2.a.text
    print(headline)

    summary = article.find('div', class_='entry-content').p.text
    print(summary)

    try :
        vid_src = article.find('iframe', class_="youtube-player")[
            'src']  # here we want the value of an attribute of a tag...so access it like a dict. !!
        # print(vid_src)

        vid_id = vid_src.split('/')[4]  # '?' specifies that where the parameters of that url begin
        vid_id = vid_id.split('?')[0]
        # print(vid_id)

        yt_link = 'https://youtube.com/watch?v={}'.format(vid_id)

    except :
        yt_link = None

    print(yt_link)
    print()

    csv_writer.writerow([headline,summary, headline, yt_link])

csv_file.close()




