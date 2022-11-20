from datetime import datetime
import requests
from bs4 import BeautifulSoup
from settings import settings


def send_results(msg: str) -> str:
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", now)
    msg = f"currently it is: {now} \n" + msg
    msg = msg

    params = {
        "chat_id": settings.bot_chat_id,
        "parse_mode": "HTML",
        "disable_notification": True,
        "disable_web_page_preview": True,
        "text": msg,
    }
    r = requests.get(url=settings.bot_url.format(settings.bot_token), params=params)
    return r.json()


def parse_novaya_opera() -> str:

    msg = ""
    res = []

    URL = "https://novayaopera.ru/events/news/promokod-dlya-studentov-na-spektakli-novoy-opery/"
    print(f"parsing page: {URL}")
    msg += f'parsing page: <a href="{URL}">Новая опера</a> \n\n'
    msg += f"<b>results: </b> \n"

    try:
        page = requests.get(URL, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")
        article = soup.find("article", class_="ui-article")
        lis = article.find_all(lambda e: e.name == "li" and e.findChildren("a", href=True))
        for li in lis:
            link = li.find("a", href=True)
            print(f"{li.text} (link: {link.get('href')})")
            res.append(f"{li.text} (<a href=\"{link.get('href')}\">link</a>) ")
    except Exception as e:
        print(e.args)
        msg += f"error: {e.args}"
    else:
        msg += " - " + "\n - ".join(res)

    return msg


if __name__ == "__main__":
    print("start parsing")
    # send_results(parse_novaya_opera())
    msg = parse_novaya_opera()
    print("message: \n", msg)
    print(send_results(msg))
