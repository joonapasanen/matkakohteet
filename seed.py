import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM Users")
db.execute("DELETE FROM Destinations")
db.execute("DELETE FROM Comments")

user_count = 1000
destination_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), 1])

for i in range(1, destination_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO Destinations (name, description, user_id) VALUES (?, ?, ?)",
               ["destination" + str(i), "test description", user_id])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    destintion_id = random.randint(1, destination_count)
    db.execute("""INSERT INTO Comments (comment, sent_at, destination_id, user_id)
                  VALUES (?, datetime('now'), ?, ?)""",
               ["message" + str(i), destintion_id, user_id])

db.commit()
db.close()
