import db

def add_comment(destination_id, user_id, comment):
    sql = """
        INSERT INTO Comments (destination_id, user_id, comment) 
        VALUES (?, ?, ?)
    """
    db.execute(sql, [destination_id, user_id, comment])

def get_comments(destination_id):
    sql = """
        SELECT c.comment_id, c.comment, u.username, c.user_id 
        FROM Comments c
        JOIN Users u ON c.user_id = u.user_id
        WHERE c.destination_id = ?
        ORDER BY c.comment_id DESC
    """
    return db.query(sql, [destination_id])


def get_comment(comment_id):
    sql = """
        SELECT c.comment_id, c.destination_id, c.comment, u.username 
        FROM Comments c
        JOIN Users u ON c.user_id = u.user_id
        WHERE c.comment_id = ?
    """
    rows = db.query(sql, [comment_id])
    if not rows:
        return None
    return rows[0]

def remove_comment(comment_id):
    sql = "DELETE FROM Comments WHERE comment_id = ?"
    db.execute(sql, [comment_id])
