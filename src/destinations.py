import db

def get_destinations():
    sql = """
        SELECT
            d.destination_id,
            d.name,
            d.description,
            d.user_id,
            u.username
        FROM Destinations d
        JOIN Users u ON d.user_id = u.user_id
        ORDER BY d.destination_id DESC
    """
    return db.query(sql)

def add_destination(name, description, user_id, price_category_id, rating):
    sql = "INSERT INTO Destinations (user_id, name, description, price_category_id, rating) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, name, description, price_category_id, rating])
    thread_id = db.last_insert_id()
    return thread_id

def get_destination(destination_id):
    sql = """
        SELECT
            d.destination_id,
            d.name,
            d.description,
            d.user_id,
            pc.name AS price_category,
            d.rating,
            u.username
        FROM Destinations d
        JOIN Users u ON d.user_id = u.user_id
        JOIN PriceCategories pc ON d.price_category_id = pc.price_category_id
        WHERE d.destination_id = ?
    """
    rows = db.query(sql, [destination_id])
    if not rows:
        return None
    return rows[0]

def update_destination(destination_id, description):
    sql = "UPDATE Destinations SET description = ? WHERE destination_id = ?"
    db.execute(sql, [description, destination_id])

def remove_destination(destination_id):
    sql = "DELETE FROM Destinations WHERE destination_id = ?"
    db.execute(sql, [destination_id])

def search(query):
    sql = """SELECT destination_id,
                    name,
                    user_id,
                    description
             FROM Destinations
             WHERE description LIKE ? OR name LIKE ?
             ORDER BY destination_id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])

def get_destinations_by_user(user_id):
    sql = """
        SELECT
            d.destination_id,
            d.name,
            d.description,
            d.user_id,
            u.username
        FROM Destinations d
        JOIN Users u ON d.user_id = u.user_id
        WHERE d.user_id = ?
        ORDER BY d.destination_id DESC
    """
    return db.query(sql, [user_id])

def get_user_stats(user_id):
    sql = """
        SELECT COUNT(*) AS destination_count
        FROM Destinations
        WHERE user_id = ?
    """
    rows = db.query(sql, [user_id])
    if not rows:
        return {"destination_count": 0}
    row = rows[0]
    return {
        "destination_count": row["destination_count"],
    }
