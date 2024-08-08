from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy data
users = {
    'john_doe': {
        'username': 'john_doe',
        'bio': 'Gamer and developer.',
        'games': ['Game 1', 'Game 2', 'Game 3'],
        'social_links': {
            'twitter': 'https://twitter.com/john_doe',
            'facebook': 'https://facebook.com/john_doe',
        }
    }
}

@app.route('/')
def home():
    return render_template('home.html', users=users)

@app.route('/profile/<username>')
def profile(username):
    user = users.get(username)
    if user:
        return render_template('profile.html', user=user)
    return "User not found", 404

@app.route('/add_content', methods=['POST'])
def add_content():
    username = request.form['username']
    new_game = request.form['new_game']
    if username in users:
        users[username]['games'].append(new_game)
    return redirect(url_for('profile', username=username))

if __name__ == '__main__':
    app.run(debug=True)
