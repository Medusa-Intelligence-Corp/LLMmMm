import os
import json
import random

import bleach

from smartenough import get_smart_answer

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://llmmmm.com"}})

@app.route('/api/v1/pairings', methods=['POST'])
def pairings():
    # Use this endpoint with the following curl command:
    # curl -X POST -H "Origin: https://llmmmm.com" http://localhost:5000/api/v1/pairings -H "Content-Type: application/json" -d '{"menu_item":"Spaghetti Carbonara"}'
    data = request.json
    
    instructions = """Embrace the role of a master sommelier. I will present you with a selection from the menu, and your task is to provide the best wine pairings to pair with a given menu item. For each dish, specify the ideal wine variety, region, vintage, and any pertinent pairing nuances. Should a dish favor an alternative beverage—be it beer, coffee, cocktail, or another—advise accordingly. Your recommendations should be captivating and informed, as they are crucial for my professional endeavors. Also please format your response in valid html and add emojis for flair.

    Menu item: 
    """

    text_response = get_smart_answer(instructions, data['menu_item'], "OpenRouter", "html")
        
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
    return jsonify(analysis=sanitized_html), 200


@app.route('/api/v1/test', methods=['POST'])
def test():
    # Use this endpoint with the following curl command:
    # curl -X POST -H "Origin: https://llmmmm.com" http://localhost:5000/api/v1/test -H "Content-Type: application/json" -d '{"menu_item":"Spaghetti Carbonara"}'
    return jsonify(analysis="wet wine"), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000)



