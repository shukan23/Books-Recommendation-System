# Import required modules
import csv
import sqlite3



connection = sqlite3.connect('project.db')

cursor = connection.cursor()
a = 4
with open('books_v2.csv', newline='' , encoding='latin-1') as csvfile:
    contents = csv.reader(csvfile, delimiter=';')

    insert_records = "INSERT INTO Books (isbn, title, author, yop,publisher, img_s, img_m, img_l, price, rating, raters, reviews, description) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor.executemany(insert_records, contents)

# raws = cursor.execute("SELECT * FROM user").fetchall()
# print(raws)
print("Jay Swaminarayan")




connection.commit()

connection.close()
