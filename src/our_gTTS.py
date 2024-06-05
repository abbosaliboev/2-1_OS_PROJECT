import os
from gtts import gTTS
import pygame
import pygame.examples
from database import get_product_info

#제품 정보를 음성으로 출력하는 함수
def announce_product_info(product_name, basket=None):
    
    if basket is None:
        # 제품 이름을 사용하여 제품 정보를 로드합니다.
        product_info = get_product_info(product_name)
        if product_info is not None:
            id, name, korean_name, brand, price, capacity, calories = product_info
            # 제품 정보를 한국어로 출력합니다.
            tts_text = f"해당 제품은 {korean_name} {capacity}입니다. 제조사는 {brand}입니다. 편의점 가격은 {price}원입니다."
        else:
            tts_text = "죄송합니다. 현재 해당 제품은 등록되어 있지 않습니다."
    else:
        # 장바구니의 제품 이름을 사용하여 제품 정보를 로드하고, 이를 한국어로 출력합니다.
        total_price = 0
        product_names = []
        for product in basket:
            product_info = get_product_info(product)
            if product_info is not None:
                id, name, korean_name, brand, price, capacity, calories = product_info
                total_price += price
                product_names.append(korean_name)
        product_names_str = ', '.join(product_names)
        tts_text = f"장바구니에는 {product_names_str}이 있습니다. 총 가격은 {total_price}원입니다."

    # gTTS를 사용하여 텍스트를 음성 파일로 저장합니다.
    tts = gTTS(text=tts_text, lang='ko', slow=False)
    
def main(product_name):
    # 해당 제품의 정보를 음성으로 출력
    announce_product_info(product_name)

if __name__ == "__main__":
    main()