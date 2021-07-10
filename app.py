from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisissecret!"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////home/brice/PycharmProjects/flask-login/login.db'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "You can't access that page, you need too login first"
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            return '<h1>User does not exist!</h1>'

        login_user(user)

        return '<h1>You are now logged in!</h1>'

    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return f'<h1> You are in the protected area, {current_user.username}!</h1>'

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "<h1>You are now logged out!</h1>"


if __name__ == '__main__':
    app.run(debug=True)
