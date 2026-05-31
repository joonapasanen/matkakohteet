import db

def get_destinations():
    sql = """SELECT destination_id, name, COUNT(destination_id) total
             FROM Destinations
             GROUP BY destination_id
             ORDER BY destination_id DESC"""
    return db.query(sql)

def add_destination(name, description, user_id):
    sql = "INSERT INTO Destinations (user_id, name, description) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, name, description])
    thread_id = db.last_insert_id()
    return thread_id

def get_destination(destination_id):
    sql = "SELECT destination_id, name FROM Destinations WHERE destination_id = ?"
    return db.query(sql, [destination_id])[0]
