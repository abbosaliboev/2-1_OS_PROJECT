import sqlite3

def get_product_info(product_name):
    # 새로운 데이터베이스 연결 열기
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE name = ?", (product_name,))
    product_info = cursor.fetchone()

    # 데이터베이스 연결 닫기
    conn.close()

    return product_info

# 데이터베이스 연결
conn = sqlite3.connect('mydatabase.db')

# 커서 생성
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''CREATE TABLE IF NOT EXISTS products
                (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)''')

# 데이터 삽입
products = [('코카콜라 500ml', 2500), ('칠성사이다 캔 355ml', 1700), ('삼다수 2L', 3000), ('포카리스웨트 500ml', 1500), ('게토레이 500ml', 2000)]
for product in products:
    cursor.execute("SELECT * FROM products WHERE name = ?", (product[0],))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", product)
        
# 데이터 삭제
#cursor.execute("DELETE FROM products WHERE name = ?", ('Alice',))
#cursor.execute("DELETE FROM products WHERE name = ?", ('Bob',))

conn.commit()

# 데이터 조회
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

# 데이터를 문자열로 변환하고 출력
for row in rows:
    print(f"Product ID: {row[0]}, Name: {row[1]}, Price: {row[2]}")

# 특정 조건이 성립하면 테이블 초기화
#cursor.execute("SELECT COUNT(*) FROM products")
#(row,) = cursor.fetchone()
#if row >= 5:
#    cursor.execute("DROP TABLE products")
 #   cursor.execute('''CREATE TABLE products
 #                   (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)''')

# 커밋
conn.commit()

# 연결 종료
conn.close()