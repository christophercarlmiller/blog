import sys
from flask import Flask, render_template, send_from_directory
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
STATIC_DIR = 'static'
CATEGORIES = [
    'quick-thoughts',
    'php',
    'javascript',
    'python',
    'sql',
    'go-lang',
    'software-design-patterns',
    'software-optimisation-patterns',
    'apis',
    'packages-i-wrote',
    'packages-i-use',
    'software-i-use',
]

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)
app.config['STATIC_DIR'] = STATIC_DIR

@app.route('/')
def root():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    posts = posts[:3]
    return render_template('posts.html', posts=posts, categories=CATEGORIES)
    
@app.route('/posts/<path:category>')
def posts(category):
    posts = [p for p in flatpages if p.path.startswith(POST_DIR + '/' + category)]
    posts.sort(key=lambda item:item['date'], reverse=False)
    return render_template('posts.html', posts=posts, categories=CATEGORIES)


@app.route('/post/<path:name>')
def post(name: str):
    path = '{}/{}'.format(POST_DIR , name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post, categories=CATEGORIES) 

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['STATIC_DIR'], filename)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)
