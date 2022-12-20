from config import *
from main import bot
import requests
import asyncio
import db


def check(url):
    try:
        req = requests.get(url)
        if req.status_code // 100 == 2:
            return 1
    except:
        return 0


def change_domain(url):
    req = requests.get(f"https://fenix.top/api/set_domain_offer/{api_key}?offer_id={offer_id}&url={url}", timeout=2)
    print(req.json())
    try:
        return req.json()["error"]
    except KeyError:
        return 1


async def main():
    url = db.get_current_url()[0]
    if not check(url):
        new_url = db.change_domain()
        if new_url == "error":
            await bot.send_message(user_id, f"Закончились домены")
            session = await bot.get_session()
            await session.close()
            return
        is_changed = change_domain(new_url)
        if is_changed == 1:
            await bot.send_message(user_id, f"сменили домен на {new_url}")
        else:
            await bot.send_message(user_id, f"Ошибка при смене домена\n\n{is_changed}")
    session = await bot.get_session()
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
