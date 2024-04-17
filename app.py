import os
import json

import requests
import bleach

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://llmmmm.com"}})

def analyze_menu_item(menu_text):
    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://llmmmm.com", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "LLMmMm", # Optional. Shows in rankings on openrouter.ai.
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
    
    response_data = response.json()

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
                tags=allowed_tags, attributes=allowed_attributes, strip=False)
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



