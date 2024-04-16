import os
import json

import requests

from flask import Flask, jsonify, request, render_template_string
#from flask_cors import CORS

app = Flask(__name__)

#CORS(app, resources={r"/api/*": {"origins": "https://yourwebsite.com"}})

#def validate_origin(func):
#    def wrapper(*args, **kwargs):
#        # Validate the request origin
#        if request.headers.get('Origin') != 'https://yourwebsite.com':
#            return jsonify({'error': 'Forbidden'}), 403
#        return func(*args, **kwargs)
#    return wrapper


def analyze_menu_item(menu_text):
    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
        #"HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
        #"X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
      },
      data=json.dumps({
        "model": "mistralai/mistral-7b-instruct:free", # Choose from https://openrouter.ai/docs#models 
        "messages": [
          {"role": "user", "content": f"""Embrace the role of a master sommelier. I will present you with a selection from the menu, and your task is to provide the best wine pairings to pair with a given menu item. For each dish, specify the ideal wine variety, region, vintage, and any pertinent pairing nuances. Should a dish favor an alternative beverage—be it beer, coffee, cocktail, or another—advise accordingly. Your recommendations should be captivating and informed, as they are crucial for my professional endeavors. Also please format your response in html and add emojis for flair.

    Menu item: 
    {menu_text}
    """
    }
        ]
      })
    )
    return response

# @validate_origin # add this after @app.route
@app.route('/api/v1/pairings', methods=['POST'])
def pairings():
    # Use this endpoint with the following curl command:
    # curl -X POST http://localhost:5000/api/v1/pairings -H "Content-Type: application/json" -d '{"menu_item":"Spaghetti Carbonara"}'
    data = request.json
    analysis = analyze_menu_item(data['menu_item'])
    print(analysis)
    return jsonify(analysis="test"), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

