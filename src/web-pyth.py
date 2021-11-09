import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'


class Scrapper:

    def find_news_by_bitcoin(self, currency: str):
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"}
        link = "https://www.google.com/search?hl=en&q=after:" + str((datetime.now() - timedelta(days=30)).date()) + \
               "+site%3Acoinmarketcap.com/headlines/news/+" + currency
        site_text = requests.get(link, headers=headers).text
        soup = BeautifulSoup(site_text, "html.parser")
        g = soup.find('div', class_='main')
        anchors = g.find_all('a')
        news = []
        if anchors:
            for link in anchors:
                try:
                    description = link.parent.parent.find_all('div', recursive=False)[1].find("div",
                                                                                              recursive=False).text
                    title = link.find('h3').text
                    news.append({'title': title, 'link': link['href'], 'description': description})
                except (AttributeError, IndexError):
                    pass
        return news


def setup_db():
    open("database.db", "w").close()
    with sqlite3.connect("database.db") as _con:
        _cursor = _con.cursor()
        _cursor.execute(
            "CREATE TABLE IF NOT EXISTS Articles ('title' TEXT, 'description' TEXT, "
            "'link' TEXT)")
        _con.commit()


def add_news_of_currencies_to_db(*coin_names: str):
    for i in coin_names:
        scrapper = Scrapper()
        for j in scrapper.find_news_by_bitcoin(i):
            add_article_to_db(j)


def get_articles_from_db(coin_name: str):
    with sqlite3.connect("database.db") as _con:
        _cursor = _con.cursor()
        like_statement = '%' + coin_name + '%'
        _cursor.execute(
            "SELECT * FROM Articles WHERE description LIKE ? OR title LIKE ?", (like_statement, like_statement))
        return _cursor.fetchall()


def add_article_to_db(article: dict):
    with sqlite3.connect("database.db") as _con:
        _cursor = _con.cursor()
        _cursor.execute(
            "INSERT INTO Articles('title', 'description', 'link') VALUES(?, ?, ?)",
            (article['title'], article['description'], article['link']))
        _con.commit()


@app.route('/coin')
def coin():
    coin_name = request.args.get("coin")
    input_value = coin_name if coin_name is not None else ""
    response = '<!DOCTYPE HTML>' \
               '<html>' \
               '<head>' \
               '<title>Title</title>' \
               '</head>' \
               '<body style="padding:20px">' \
               '<form method="get" action="/coin" style="padding-bottom: 60px">' \
               '<input type="text" value="' + input_value + '" name="coin" style="height:30px;">' \
               '<button type="submit" style="height:40px;background-color: #FFFFFF;margin-left: 20px; padding-left: 20px; padding-right: 20px;">CHECK</button>' \
               '</form>'
    if coin_name:
        for i in get_articles_from_db(coin_name):
            response += '<p><a href="' + i[2] + '">' + i[0] + '</a><br>' + i[1] + '<br></p>'
    response += '</body>' \
                '</html>'
    return response


if __name__ == '__main__':
    setup_db()
    # list here coins you want to add to db, separated by comma
    add_news_of_currencies_to_db('bitcoin', 'ethereum')
    app.run(debug=True)
