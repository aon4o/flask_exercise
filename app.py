from flask import Flask, url_for, render_template, request, redirect
from post import Post

app = Flask(__name__)

db = {1: Post(1, 'Post 1', 'Gosho', 'Content 1')}


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/posts')
def list_posts():
    return render_template('posts.html', posts=db.values())


@app.route('/posts/<int:id>')
def show_post(id):
    post = db[id]
    return render_template('post.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')
    elif request.method == 'POST':
        next_id = max(db.keys()) + 1
        post = Post(next_id, request.form['name'], request.form['author'],
                    request.form['content'])
        db[next_id] = post
        return redirect(url_for('list_posts'))
