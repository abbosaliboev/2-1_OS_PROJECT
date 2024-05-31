import json
import os
from gtts import gTTS
import pygame
import pygame.examples
from database import get_product_info


# 제품 정보를 음성으로 출력하는 함수
def announce_product_info(product_name):
    product_info = get_product_info(product_name)

    if product_info is not None:
        id, name, korean_name, brand, price, capacity = product_info
        tts_text = f"해당 제품은 {korean_name} {capacity}입니다. 제조사는 {brand}입니다. 편의점 가격은 {price}원입니다."
    else:
        tts_text = "죄송합니다. 현재 해당 제품은 등록되어 있지 않습니다."

    # gTTS를 사용하여 텍스트를 음성 파일로 저장
    tts = gTTS(text=tts_text, lang='ko', slow=False)

    if os.path.exists("product_info.mp3"):
        os.remove("product_info.mp3")
    tts.save("product_info.mp3")

    # pygame을 사용하여 음성 파일 재생
    
    pygame.mixer.init()
    pygame.mixer.music.load("product_info.mp3")
    pygame.mixer.music.play()

    # 음성 출력이 끝날 때까지 대기
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit() # Win32 error를 해결하기 위해 pygame.mixer 종료해주기
                        # 종료해주지 않고 다시 실행하면 pygame.mixer가 이용하는 mp3파일이 삭제됨(사용중인 파일을 삭제하는 오류)
    
# main 함수에서 result.json 파일을 읽어와서 처리
def main(product_name):
    # 해당 제품의 정보를 음성으로 출력
    announce_product_info(product_name)

if __name__ == "__main__":
    main()
