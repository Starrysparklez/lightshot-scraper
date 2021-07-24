#!/usr/bin/python3
import os, io, string, random, cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

base = "https://prnt.sc/"
proxies = { # in Russia I unable to connect to `prnt.sc`
    "https": "http://enter your proxy",
    "http": "http://enter your proxy"
}
chars = string.ascii_letters + string.digits
ignore_img = "//st.prntscr.com/2021/04/08/1538/img/0_173a7b_211be8ff.png"

def main() -> None:
    while True:
        target = "".join([random.choice(chars) for x in range(6)])

        if target + ".png" in os.listdir("downloads"):
            print(f"Картинка с URL-ссылки", target, "уже была сохранена, пропускаю.")
            continue
        
        response = scraper.get(base + target, proxies=proxies)
        if response.status_code != 200:
            print(f"Запрос к URL-ссылке", target, "прошел неудачно.")
            print(f"Содержимое ответа:", response.text, "\nСсылка:", base + target)
            continue
        try:
            url = BeautifulSoup(response.text, features="html.parser").find("img", id="screenshot-image").get("src")
            if url == ignore_img:
                print(f"Картинка по URL-ссылке", target, "была удалена, пропускаю.")
                continue
        except:
            print(f"По URL-ссылке", target, "не было найдено изображения, пропускаю.")
            continue

        image_response = scraper.get(url, proxies=proxies)
        if image_response.status_code != 200:
            print(f"Не удалось скачать картинку из URL-ссылки", target)
            continue
        
        with io.open(f"downloads/{target}.png", "wb") as file:
            file.write(image_response.content)
        
        print(f"Картинка с URL-ссылки", target, "сохранена.")


if __name__ == "__main__":
    main()