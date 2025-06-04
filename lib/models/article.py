from lib.db.connection import get_connection

class Article:
    def __init__(self, title, magazine_id, author_id, id=None):
        self.id = id
        self.title = title
        self.magazine_id = magazine_id
        self.author_id = author_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        if self.id:
            cursor.execute(
                "UPDATE articles SET title = ?, magazine_id = ?, author_id = ? WHERE id = ?",
                (self.title, self.magazine_id, self.author_id, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO articles (title, magazine_id, author_id) VALUES (?, ?, ?)",
                (self.title, self.magazine_id, self.author_id)
            )
            self.id = cursor.lastrowid

        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        articles = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return articles

    def author(self):
        from .author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from .magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)
