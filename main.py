import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    return facts[0].getText()


def get_addr(fact):
    print(fact)
    payload = {'input_text': fact}
    response = requests.post('https://hidden-journey-62459.herokuapp.com/piglatinize/', data=payload, allow_redirects=False)
    return response.headers['Location']


@app.route('/')
def home():
    fact = get_fact().strip()
    addr = get_addr(fact)
    body = "<p><a href={addr}>{addr}</a></p>".format(addr=addr)
    return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

