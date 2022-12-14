import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootroot",
  database="mydb"
)

mycursor = mydb.cursor()

sql = "INSERT INTO users (username, password, salt) VALUES (%s, %s, %s)"
val = ("user24", "", "")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")