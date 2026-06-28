import db

def get_destinations(page, page_size):
    sql = """
        SELECT
            d.destination_id,
            d.name,
            d.description,
            d.user_id,
            u.username,
            COUNT(c.comment_id) AS total, 
            MAX(c.sent_at) AS last
        FROM Destinations d
        JOIN Users u ON d.user_id = u.user_id
        LEFT JOIN Comments c ON d.destination_id = c.destination_id
        GROUP BY d.destination_id
        ORDER BY d.destination_id DESC
        LIMIT ? OFFSET ?
    """
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def add_destination(name, description, user_id, categories):
    sql = "INSERT INTO Destinations (user_id, name, description) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, name, description])
    destination_id = db.last_insert_id()

    sql = "INSERT INTO DestinationCategories (destination_id, title, value) VALUES (?, ?, ?)"
    for title, value in categories:
        db.execute(sql, [destination_id, title, value])

    return destination_id

def get_destination(destination_id):
    sql = """
        SELECT
            d.destination_id,
            d.name,
            d.description,
            d.user_id,
            u.username
        FROM Destinations d
        JOIN Users u ON d.user_id = u.user_id
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

def get_categories():
    sql = """
        SELECT title, value FROM Categories ORDER BY category_id
    """
    result = db.query(sql)

    categories = {}
    for title, value in result:
        categories[title] = []
    for title, value in result:
        categories[title].append(value)

    return categories

def get_destination_categories(destination_id):
    sql = "SELECT title, value FROM DestinationCategories WHERE destination_id = ?"
    categories = db.query(sql, [destination_id])
    return categories

def destination_count():
    sql = "SELECT COUNT(destination_id) AS count FROM Destinations"
    return db.query(sql, [])[0]["count"]