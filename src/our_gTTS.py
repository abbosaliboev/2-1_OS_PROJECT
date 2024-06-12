import os
from gtts import gTTS
import pygame
import pygame.examples
from database import get_product_info

# 제품 정보를 음성으로 출력하는 함수
def announce_product_info(product_name):
    # 제품 이름을 사용하여 제품 정보를 로드함.
    product_info = get_product_info(product_name)
    if product_info is not None:
        id, name, korean_name, brand, price, capacity, calories = product_info
        # 제품 정보를 한국어로 출력
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

def announce_basket_info(item_counts, total_price):
    # 장바구니의 제품 이름을 사용하여 제품 정보를 로드하고, 이를 한국어로 출력
    product_names_str = ', '.join([f"{name} {info['count']}개" for name, info in item_counts.items()])
    tts_text = f"장바구니에는 {product_names_str}가 있습니다. 총 가격은 {total_price}원입니다."

    tts = gTTS(text=tts_text, lang='ko', slow=False)
    
    if os.path.exists("basket_info.mp3"):
        os.remove("basket_info.mp3")
    tts.save("basket_info.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("basket_info.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    
def main(product_name):
    # 해당 제품의 정보를 음성으로 출력
    announce_product_info(product_name)

if __name__ == "__main__":
    main()