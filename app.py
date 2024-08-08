from flask import Flask, render_template, request, redirect, url_for
import os
from io import BytesIO
from PIL import Image
import requests

app = Flask(__name__)

# Define the users dictionary here
users = {
    'john_doe': {
        'username': 'john_doe',
        'bio': 'Gamer, developer, and tech enthusiast.',
        'games': ['The Legend of Zelda', 'Super Mario', 'Halo'],
        'social_links': {
            'Twitter': 'https://twitter.com/johndoe',
            'GitHub': 'https://github.com/johndoe'
        }
    },
    'jane_doe': {
        'username': 'jane_doe',
        'bio': 'Casual gamer and artist.',
        'games': ['Animal Crossing', 'Stardew Valley', 'Minecraft'],
        'social_links': {
            'Instagram': 'https://instagram.com/janedoe',
            'LinkedIn': 'https://linkedin.com/in/janedoe'
        }
    }
}

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
API_KEY = "your api key here"

def generate_image_for_game(game_name):
    payload = {
        "inputs": game_name,
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "options": {"wait_for_model": True}
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image_filename = f"static/{game_name}.png"
        
        # Ensure the static directory exists
        os.makedirs(os.path.dirname(image_filename), exist_ok=True)
        
        image.save(image_filename)
        return image_filename
    else:
        print(f"Error generating image: {response.status_code} - {response.text}")
        return None
    

@app.route('/')
def home():
    username = request.args.get('username')
    if username:
        return redirect(url_for('profile', username=username))
    return render_template('home.html', users=users)

@app.route('/profile/<username>')
def profile(username):
    user = users.get(username)
    if user:
        # Generate images for each game
        game_images = {}
        for game in user['games']:
            image_url = generate_image_for_game(game)
            if image_url:
                game_images[game] = image_url

        return render_template('profile.html', user=user, game_images=game_images)
    else:
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
