from datetime import datetime, date, timedelta
import os
import requests
from bs4 import BeautifulSoup


class settings:
    bot_token = os.environ.get("BOT_TOKEN")
    bot_url = "https://api.telegram.org/bot{}/sendMessage"
    bot_chat_id = os.environ.get("BOT_CHAT_ID")


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
    msg += f'parsing page: <a href="{URL}">Новая опера</a> \n'

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


def parse_moskino() -> str:

    msg = ""
    res = []

    today = date.today()
    tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    day_after_tomorrow = (today + timedelta(days=2)).strftime("%Y-%m-%d")

    # tomorrow
    url = f"https://mos-kino.ru/schedule/?date={tomorrow}"
    msg += f'parsing page: <a href="{url}">Москино (завтра, {tomorrow})</a> \n'

    try:
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        films = soup.findAll(
            lambda e: e.name == "div"
            and e.get("class") == ["schedule-item"]
            and e.findChild("span", class_="price").text == "Регистрация"
        )

        films_parsed = {}

        for film in films:
            title = film.findChild("div", class_="title").contents[0].strip()
            info = film.findChild("div", class_="title").findChild("small").text
            time = film.findChild("span", class_="time").text
            link = film.findChild("a", href=True).get("href")

            if title in films_parsed:
                films_parsed[title]["time"].append((time, link))
            else:
                films_parsed[title] = {
                    "time": [(time, link)],
                    "info": info,
                }
            print(f"{time}: {title} (link: {link})")

        for film in films_parsed:
            info = films_parsed[film]["info"]
            times = [f'<a href="{t[1]}">{t[0]}</a>' for t in films_parsed[film]["time"]]
            record = f"{film} {info}: {', '.join(times)}"
            res.append(record)

    except Exception as e:
        print(e.args)
        msg += f"error: {e.args}"
    else:
        msg += " - " + "\n - ".join(res) if res else "ничего на завтра :("

    # day after tomorrow
    res = []
    url = f"https://mos-kino.ru/schedule/?date={day_after_tomorrow}"
    msg += f'\n\nparsing page: <a href="{url}">Москино (послезавтра, {day_after_tomorrow})</a> \n'

    try:
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        films = soup.findAll(
            lambda e: e.name == "div"
            and e.get("class") == ["schedule-item"]
            and e.findChild("span", class_="price").text == "Регистрация"
        )

        films_parsed = {}

        for film in films:
            title = film.findChild("div", class_="title").contents[0].strip()
            info = film.findChild("div", class_="title").findChild("small").text
            time = film.findChild("span", class_="time").text
            link = film.findChild("a", href=True).get("href")

            if title in films_parsed:
                films_parsed[title]["time"].append((time, link))
            else:
                films_parsed[title] = {
                    "time": [(time, link)],
                    "info": info,
                }
            print(f"{time}: {title} (link: {link})")

        for film in films_parsed:
            info = films_parsed[film]["info"]
            times = [f'<a href="{t[1]}">{t[0]}</a>' for t in films_parsed[film]["time"]]
            record = f"{film} {info}: {', '.join(times)}"
            res.append(record)

    except Exception as e:
        print(e.args)
        msg += f"error: {e.args}"
    else:
        msg += " - " + "\n - ".join(res) if res else "ничего на завтра :("

    return msg


def parse_illuzion() -> str:

    msg = ""
    res = []

    url = f"https://illuzion-cinema.ru/schedule/"
    msg += f'parsing page: <a href="{url}">Иллюзион</a> \n'

    try:
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        films = soup.findAll(
            lambda e: e.name == "div"
            and e.get("class") == ["schedule-film-available"]
            and "ЗАРЕГИСТРИРОВАТЬСЯ" in e.text
        )

        for film in films:
            day = film.findParent().findParent().findParent().findChild("h2").text
            title = film.findChild("span", class_="schedule-film__name").text.strip()
            time = film.findChild("span", class_="schedule-film__time").text
            link = film.findChild("a", class_="schedule-film__btn")["href"]

            title = title.replace("БОЛЬШОЙ ЗАЛ. Архивное кино. ", "")

            print(f"{day}, {time}: {title} (link: {link})")
            if not ("лекция" in title.lower() or "презентация" in title.lower()):
                res.append(f'{day}, {time}: (<a href="{link}">{title}</a>)')

    except Exception as e:
        print(e.args)
        msg += f"error: {e.args}"
    else:
        msg += " - " + "\n - ".join(res) if res else "ничего на завтра :("

    return msg


if __name__ == "__main__":
    print("start parsing")

    msg = parse_novaya_opera() + "\n\n"
    msg += parse_moskino() + "\n\n"
    msg += parse_illuzion()

    print("------\n")

    print("message: \n", msg)
    print(send_results(msg))
