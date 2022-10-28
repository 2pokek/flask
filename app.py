from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return 'Hello'



@app.route('/about')
def about():
    return 'About'


@app.route('/user/<string:name>/<int:id>')
def user(name,id):

    return 'User page' + name + '-' + int(id)

if __name__ == '__main__':
    app.run(debug=True)
