from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

api_url = 'http://jservice.io'
news_url = 'https://www.sports.ru'
news_param = '/football/news'


page = requests.get(f'https://www.sports.ru{news_param}')
soup = BeautifulSoup(page.text, 'html.parser')

@app.route('/')
@app.route('/news')
def news():

    news_link = []

    for n in soup.find_all('a', class_='short-text'):
        news_link.append(n.get('href'))

    news = []

    for i in range(10):
        if 'https' in news_link[i]:
            n = requests.get(news_link[i])
        else:
            n = requests.get(f'https://www.sports.ru{news_link[i]}')
        news_page = BeautifulSoup(n.text, 'html.parser')
        header = news_page.find('h1', class_='h1_size_tiny').text
        content = news_page.find('div', class_='news-item__content js-mediator-article').text
        news_cont = [header, content]
        news.append(news_cont)


    return render_template('news.html', news=news)


@app.route('/api')
def api():

    get = requests.get(f'http://jservice.io/api/random')
    # post = requests.post(f'http://jservice.io/api/random')
    # put = requests.put(f'http://jservice.io/api/random')

    methods = [get.text]

    return render_template('api.html', methods=methods)


if __name__ == '__main__':
    app.run(debug=True)
