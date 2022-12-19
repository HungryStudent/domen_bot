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
    req = requests.get("https://ppdomain.com/api/set_domain_offer/%7Bapi_key%7D?offer_id=%7Boffer_id%7D&url=%7Burl%7D")


async def main():
    url = db.get_current_url()
    print(check(url))
    if not check(url):
        new_url = db.change_domain()
        if new_url == "error":
            await bot.send_message(796644977, f"Закончились домены")
        change_domain(new_url)
        await bot.send_message(796644977, f"сменили домен на {new_url}")
    session = await bot.get_session()
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
