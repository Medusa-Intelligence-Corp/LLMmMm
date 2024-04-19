import os
import json
import random

import requests
import bleach

from cachetools import TTLCache

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

model_cache = TTLCache(maxsize=5, ttl=3600)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://llmmmm.com"}})

def get_best_free_models():
    first_choice_model = "mistralai/mistral-7b-instruct:free"
    second_choice_model = "openchat/openchat-7b:free"
 
    try: 
        #if the first_choice model is hitting API limits, fall back to the second and a random model
        last_model = model_cache["last_model"]
        if last_model != first_choice_model:
            first_choice_model = "xxxxxxxxxxxxxx"
    except KeyError:
        pass

    try:
        free_models = model_cache["free_models"]
    except KeyError:
        endpoint = "https://openrouter.ai/api/v1/models"
        response = requests.get(endpoint, headers={'Authorization':\
                f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"})
        api_result = response.json()
        free_models = []
        for model in api_result["data"]:
            if model["pricing"]["prompt"] == "0" and model["pricing"]["completion"] == "0":
                free_models.append(model["id"])
        model_cache["free_models"]=free_models

    if first_choice_model in free_models and second_choice_model in free_models:
        models = [first_choice_model, second_choice_model]
    elif first_choice_model in free_models:
        models = [first_choice_model]
        models.append(\
                random.choice([model for model in free_models \
                if model != first_choice_model]))
    elif second_choice_model in free_models:
        models = [second_choice_model]              
        models.append(\
                random.choice([model for model in free_models \
                if model != second_choice_model]))
    else:
        models = random.sample(free_models,2)
    
    return models


def analyze_menu_item(menu_text):

    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://llmmmm.com", 
        "X-Title": "LLMmMm" 
      },
      data=json.dumps({
        "models": get_best_free_models(),
        "route": "fallback",
        "messages": [
          {"role": "user", "content": f"""Embrace the role of a master sommelier. I will present you with a selection from the menu, and your task is to provide the best wine pairings to pair with a given menu item. For each dish, specify the ideal wine variety, region, vintage, and any pertinent pairing nuances. Should a dish favor an alternative beverage—be it beer, coffee, cocktail, or another—advise accordingly. Your recommendations should be captivating and informed, as they are crucial for my professional endeavors. Also please format your response in html and add emojis for flair.

    Menu item: 
    {menu_text}
    """
    }
        ]
      })
    )
    
    response_data = response.json()
    
    if 'model' in response_data:
        model_cache['last_model'] = response_data['model']

    if 'choices' in response_data and len(response_data['choices']) > 0:
        text_response = response_data['choices'][0]\
                .get('message', 'No response text found.')\
                .get('content','No content found.')

        # Define a whitelist of allowed tags and attributes
        allowed_tags = [
            'p',  # Paragraph
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # Headings
            'strong', 'b',  # Bold
            'em', 'i',  # Italics
            'u',  # Underline
            's', 'strike',  # Strikethrough
            'blockquote',  # Blockquote for quotations
            'ul', 'ol', 'li',  # Unordered and ordered lists
            'a',  # Hyperlinks
            'br',  # Line break
            'hr',  # Horizontal rule
            'div','span',  # Span for inline elements
            'code', 'pre',  # Code blocks and preformatted text
            'sup', 'sub',  # Superscript and subscript
            'dl', 'dt', 'dd',  # Description lists
        ]

        allowed_attributes = {}

        # Use bleach to clean the HTML
        sanitized_html = bleach.clean(text_response,\
                tags=allowed_tags, attributes=allowed_attributes, strip=True)
        return sanitized_html
    else:
        return "error"

@app.route('/api/v1/pairings', methods=['POST'])
def pairings():
    # Use this endpoint with the following curl command:
    # curl -X POST -H "Origin: https://llmmmm.com" http://localhost:5000/api/v1/pairings -H "Content-Type: application/json" -d '{"menu_item":"Spaghetti Carbonara"}'
    data = request.json
    analysis = analyze_menu_item(data['menu_item'])
    return jsonify(analysis=analysis), 200


@app.route('/api/v1/test', methods=['POST'])
def test():
    # Use this endpoint with the following curl command:
    # curl -X POST -H "Origin: https://llmmmm.com" http://localhost:5000/api/v1/test -H "Content-Type: application/json" -d '{"menu_item":"Spaghetti Carbonara"}'
    return jsonify(analysis="wet wine"), 200



if __name__ == '__main__':
    app.run(host='localhost', port=5000)



