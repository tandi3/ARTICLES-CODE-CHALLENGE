from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    with open("lib/db/schema.sql", "r") as f:
        schema = f.read()
        cursor.executescript(schema)
    conn.commit()
    conn.close()

def seed_database():
    # Clear existing data
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

    # Create new authors
    authors = [
        Author("Alice Johnson"),
        Author("Bob Smith"),
        Author("Carol White"),
        Author("David Brown"),
        Author("Eva Green")
    ]
    for author in authors:
        author.save()

    # Create new magazines
    magazines = [
        Magazine("Tech Today", "Technology"),
        Magazine("Science Weekly", "Science"),
        Magazine("Business Insights", "Business"),
        Magazine("Artistic Vision", "Arts"),
        Magazine("Health Monthly", "Medicine")
    ]
    for magazine in magazines:
        magazine.save()

    # Create new articles
    articles = [
        Article("AI Transforming the World", magazines[0].id, authors[0].id),
        Article("New Discoveries in Space", magazines[1].id, authors[1].id),
        Article("Market Trends 2024", magazines[2].id, authors[2].id),
        Article("Modern Art Techniques", magazines[3].id, authors[3].id),
        Article("Healthcare Innovations", magazines[4].id, authors[4].id)
    ]
    for article in articles:
        article.save()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
