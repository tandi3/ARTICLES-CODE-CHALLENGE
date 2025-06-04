from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        if self.id:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid

        conn.commit()
        conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributing_authors(self):
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT authors.*, COUNT(articles.id) as article_count
               FROM authors
               JOIN articles ON authors.id = articles.author_id
               WHERE articles.magazine_id = ?
               GROUP BY authors.id
               HAVING article_count > 2""",
            (self.id,)
        )
        authors = [Author(**row) for row in cursor.fetchall()]
        conn.close()
        return authors

    def contributors(self):
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT DISTINCT authors.* FROM authors
               JOIN articles ON authors.id = articles.author_id
               WHERE articles.magazine_id = ?""",
            (self.id,)
        )
        authors = [Author(**row) for row in cursor.fetchall()]
        conn.close()
        return authors

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row["title"] for row in cursor.fetchall()]
        conn.close()
        return titles

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        magazines = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return magazines

    @classmethod
    def with_multiple_authors(cls):
        magazines = cls.all()
        result = []
        for mag in magazines:
            if len(mag.contributors()) > 1:
                result.append(mag)
        return result

    @classmethod
    def article_counts(cls):
        magazines = cls.all()
        counts = {}
        for mag in magazines:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM articles WHERE magazine_id = ?", (mag.id,))
            count = cursor.fetchone()["count"]
            conn.close()
            counts[mag.name] = count
        return counts
