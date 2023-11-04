from datetime import datetime
import os
import requests
from sites import parse_novaya_opera, parse_bolshoi


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


if __name__ == "__main__":
    print("start parsing")

    msg = parse_novaya_opera() + "\n\n"
    # msg += parse_moskino() + "\n\n"
    # msg += parse_illuzion()
    msg += parse_bolshoi()

    print("------\n")

    print("message: \n", msg)
    print(send_results(msg))
