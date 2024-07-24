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
    
    instructions = """
You are a master sommelier. Your task is to provide expert wine pairings for given menu items. For each dish:

1. Recommend the best wine pairing, specifying:
   - Wine variety
   - Region
   - Vintage (if applicable)
   - Key pairing notes

2. If a non-wine beverage is more suitable (e.g., beer, cocktail, coffee), recommend it instead.

3. Provide brief, engaging explanations for your choices.

4. Use emojis to add visual flair to your response.

Your recommendations are for professional use, so ensure they are well-informed and compelling.

Example recommendation in HTML:

```html
<div class="wine-pairing">
  <h2>🍝 Pasta Primavera</h2>
  <h3>🍷 Recommended Pairing: Sauvignon Blanc</h3>
  <ul>
    <li><strong>Variety:</strong> Sauvignon Blanc</li>
    <li><strong>Region:</strong> Loire Valley, France</li>
    <li><strong>Vintage:</strong> 2022</li>
    <li><strong>Pairing Notes:</strong> The crisp acidity and herbaceous notes of a Loire Valley Sauvignon Blanc beautifully complement the fresh vegetables in Pasta Primavera. The wine's zesty citrus flavors enhance the dish's light cream sauce, while its mineral undertones provide a refreshing contrast. 🌿🍋</li>
  </ul>
  <p>This pairing elevates the spring-like qualities of the dish, creating a harmonious and refreshing dining experience. 🌸👨‍🍳</p>
</div>


Below is the menu item I want you to create a pairing for. Ensure you return the response in HTML format. Only return valid html.

## Menu Item: {{ menu_item }}
```
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



