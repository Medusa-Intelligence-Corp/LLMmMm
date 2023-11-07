from flask import Flask, jsonify, request, render_template_string
import os
import openai

app = Flask(__name__)

# Your OpenAI API key should be set in your environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')

def analyze_menu_item(menu_text):
    messages = [
        {
            "role": "user",
            "content": f"""Embrace the role of a master sommelier. I will present you with a selection from the menu, and your task is to provide the best wine pairings to pair with a given menu item. For each dish, specify the ideal wine variety, region, vintage, and any pertinent pairing nuances. Should a dish favor an alternative beverage—be it beer, coffee, cocktail, or another—advise accordingly. Your recommendations should be captivating and informed, as they are crucial for my professional endeavors. Also please format your response in html and add emojis for flair.

Menu item: 
{menu_text}
"""
        }
    ]
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        menu_item = request.form['menu_item']
        analysis = analyze_menu_item(menu_item)
        return render_template_string(HOME_TEMPLATE, result=analysis, menu_item=menu_item)
    return render_template_string(HOME_TEMPLATE)

@app.route('/api/v1/pairings', methods=['POST'])
def pairings():
    # Use this endpoint with the following curl command:
    # curl -X POST http://localhost:5000/api/v1/pairings -H "Content-Type: application/json" -d '{"menu_item":"Spaghetti Carbonara"}'
    data = request.json
    analysis = analyze_menu_item(data['menu_item'])
    return jsonify(analysis=analysis), 200

# Improved HTML template with inline CSS
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu Item Analysis</title>
    <script>
        function showAnalyzingText() {
            document.getElementById('analyze-button').value = 'Analyzing...';
            document.getElementById('analyze-button').disabled = true;
            document.getElementById('loading').style.display = 'block';
        }
    </script>
</head>
<body>
    <h1>Robot Sommelier</h1>
    <img src="{{ url_for('static', filename='robot.png') }}" height=400 width=400>
    <form action="/" method="post" onsubmit="showAnalyzingText()">
        <label for="menu_item">Enter a menu item:</label>
        <input type="text" id="menu_item" name="menu_item" value="{{ menu_item|default('') }}" required>
        <input type="submit" id="analyze-button" value="Analyze">
        <div id="loading" style="display: none;">...</div>
    </form>
    {% if result %}
        <div class="result">
            <h2>Analysis Result:</h2>
            {{ result | safe }}
        </div>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

