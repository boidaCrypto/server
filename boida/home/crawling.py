import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import urllib.request
import time

from exchange.models import Crypto
import boto3
from botocore.client import Config

AWS_ACCESS_KEY_ID = 'AKIARZNCNJPLGWSFJJG7'
AWS_SECRET_ACCESS_KEY = '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'


def coin_crawling(coin_name):
    # 크롬 드라이버가 위치한 경로
    path = 'C:/Users/qudrh/Desktop/chromedriver.exe'
    options = Options()
    options.add_argument('--start-fullscreen')
    driver = webdriver.Chrome(path, chrome_options=options)

    driver.get('https://coinmarketcap.com/ko/')
    # 온전히 크롬 창이 열릴때까지 2초 기다린다.
    time.sleep(2)
    # coinmarketcap에서 검색을 클릭하여 검색창이 뜨게한다.
    driver.find_element_by_class_name("gffsPR").click()
    # 검색창에 해당 코인 이름을 넣는다.
    element = driver.find_element_by_class_name("jUraic")
    element.send_keys(coin_name)
    element.send_keys(Keys.RETURN)
    # 현재 페이지 창의 url을 가져온다.
    current_url = driver.current_url
    driver.quit()
    # Beautifulsoup로 이미지를 다운받는다.
    response = requests.get(current_url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.select_one('div.nameHeader > img')
        img_url = img['src']
        urllib.request.urlretrieve(img_url, '{0}.jpg'.format(img['alt']))

        # s3에 파일 업로드
        coin_name = coin_name.upper()

        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # s3 이미지 파일 경로 설정
        s3_img_path = "crypto/image/" + coin_name + "/explain/" + coin_name + ".png"

        response = s3_client.upload_file(
            "C:/Users/qudrh/Documents/GitHub/server/boida/" + coin_name + ".jpg",
            "boida",
            s3_img_path
        )

        # coin 데이터에 넣기.
        crypto = Crypto.objects.create(
            crypto_name=coin_name,
            image=s3_img_path,
        )
        return crypto
    else:
        # 여기에 로그 쌓이게 나중
        print("status_code = 400")
        return 400
