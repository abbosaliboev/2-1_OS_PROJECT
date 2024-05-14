from gtts import gTTS
import pygame
from database import get_product_info

product_name = input("제품 이름을 입력하세요: ")
product_info = get_product_info(product_name)

if product_info is not None:
    id, name, price = product_info
    tts_text = f"해당 제품은 {name}입니다. 편의점 가격은 {price}원 입니다."
else:
    tts_text = "죄송합니다. 현재 해당 제품은 등록되어 있지 않습니다."

# gTTS를 사용하여 텍스트를 음성 파일로 저장
tts = gTTS(text=tts_text, lang='ko', slow=False)
tts.save("product_info.mp3")

# pygame을 사용하여 음성 파일 재생
pygame.mixer.init()
pygame.mixer.music.load("product_info.mp3")
pygame.mixer.music.play()

# 음성 출력이 끝날 때까지 대기
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
