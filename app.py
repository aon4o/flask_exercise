from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth

from post import Post
from comment import Comment
from user import User

app = Flask("Demo_Flask_app")

auth = HTTPBasicAuth()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def list_posts():
    return render_template('posts.html', posts=Post.all())


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.find(post_id)
    
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.find(post_id)
    if request.method == 'GET':
        return render_template('edit_post.html', post=post)
    elif request.method == 'POST':
        post.name = request.form['name']
        post.author = request.form['author']
        post.content = request.form['content']
        post.save()
        
        return redirect(url_for('show_post', post_id=post.post_id))


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.find(post_id)
    post.delete()
    
    return redirect(url_for('list_posts'))


@app.route('/posts/new', methods=['GET', 'POST'])
@auth.login_required
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')
    elif request.method == 'POST':
        values = (None, request.form['name'], request.form['author'],
                  request.form['content'])
        Post(*values).create()
        return redirect(url_for('list_posts'))


@app.route('/comments/new', methods=['POST'])
def new_comment():
    if request.method == 'POST':
        post = Post.find(request.form['post_id'])
        values = (None, post, request.form['message'])
        Comment(*values).create()
        
        return redirect(url_for('show_post', post_id=post.post_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password'])
        )
        User(*values).create()

        return redirect('/')


@auth.verify_password
def verify_password(username, password):
    user = User.find_by_username(username)
    if user:
        return user.verify_password(password)

    return False
