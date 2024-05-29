import sqlite3

# 제품 정보를 삽입하고 테이블을 재구성하는 함수
def initialize_database():
    # 데이터베이스 연결
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # 기존 테이블 삭제
    cursor.execute('DROP TABLE IF EXISTS products')

    # 테이블 재구성
    cursor.execute('''CREATE TABLE products
                      (id INTEGER PRIMARY KEY, name TEXT, korean_name TEXT, brand TEXT, price INTEGER, capacity TEXT)''')

    # 데이터 삽입
    products = [
        ("Cocacola", "코카콜라", "코카콜라", 2000, "355ml"),
        ("Sprite", "스프라이트", "코카콜라", 1700, "355ml"),
        ("Pepsi", "펩시 콜라", "펩시코", 1900, "355ml"),
        ("Chilsung", "칠성 사이다", "롯데 칠성", 1600, "355ml"),
        ("Narangd", "나랑드 사이다", "나랑드", 1700, "355ml")
    ]
    for product in products:
        cursor.execute("INSERT INTO products (name, korean_name, brand, price, capacity) VALUES (?, ?, ?, ?, ?)", product)
    
    # 커밋
    conn.commit()
    # 연결 종료
    conn.close()

# 특정 제품의 정보를 조회하는 함수
def get_product_info(product_name):
    # 데이터베이스 연결
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE name = ? OR korean_name = ?", (product_name, product_name))
    product_info = cursor.fetchone()

    # 데이터베이스 연결 닫기
    conn.close()

    return product_info

# 데이터베이스 초기화
initialize_database()

# 데이터베이스에서 모든 제품 정보를 조회하고 출력
def print_all_products():
    # 데이터베이스 연결
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    # 데이터를 문자열로 변환하고 출력
    for row in rows:
        print(f"Product ID: {row[0]}, Name: {row[1]}, Korean Name: {row[2]}, Brand: {row[3]}, Price: {row[4]}, Capacity: {row[5]}")

    # 연결 종료
    conn.close()

print_all_products()

