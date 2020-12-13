from database import DB
from comment import Comment


class Post:
    def __init__(self, post_id, name, author, content):
        self.post_id = post_id
        self.name = name
        self.author = author
        self.content = content

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM posts').fetchall()
            return [Post(*row) for row in rows]

    @staticmethod
    def find(post_id):
        with DB() as db:
            row = db.execute('SELECT * FROM posts WHERE post_id = ?', (post_id,)).fetchone()
            if row is None:
                return
            return Post(*row)

    def create(self):
        with DB() as db:
            values = (self.name, self.author, self.content)
            row = db.execute('INSERT INTO posts (name, author, content) VALUES (?, ?, ?)', values)
            return self

    def save(self):
        with DB() as db:
            values = (self.name, self.author, self.content, self.post_id)
            db.execute('UPDATE posts SET name = ?, author = ?, content = ? WHERE post_id = ?', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM posts WHERE post_id = ?', (self.post_id,))

    def comments(self):
        return Comment.find_by_post(self)