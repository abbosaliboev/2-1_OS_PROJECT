#import camera code

#send picture to yolo

#extract product name

#find name from database
cur.execute("SELECT * FROM product WHERE name=?", (result[0],))
result = cur.fetchone()
print("\nfrom product:")
print(result[0])    #name
print(result[1])    #brand company
print(result[2])    #price
print(result[3])    #capacity
print(result[4])    #calorie

#con.close()

#show on screen

#other features
