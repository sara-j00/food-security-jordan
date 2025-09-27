from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
import requests
from flask_cors import CORS


app = Flask(__name__)


with open(os.path.join("data", "rarePlants.json"), "r", encoding="utf-8") as f:
    rare_plants = json.load(f)
    
with open(os.path.join("data", "rareCrops.json"), "r", encoding="utf-8") as f:
    rare_crops = json.load(f)


@app.route("/")
def index():
    return render_template("index.html", rare_plants=rare_plants, rare_crops=rare_crops)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/details/<string:item_id>")
def details(item_id):
    item = next((p for p in rare_plants if p["id"] == item_id), None)
    
    if not item:
        item = next((c for c in rare_crops if c["id"] == item_id), None)
    
    if not item:
        return "Item not found", 404

    return render_template("details.html", item=item)


@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = []

    if query:
        results = [
            p for p in rare_plants if query in p["name"].lower() or query in p["common_name"].lower()
        ] + [
            c for c in rare_crops if query in c["name"].lower() or query in c["common_name"].lower()
        ]

    return render_template("search.html", query=query, results=results)



@app.route("/charts")
def charts():
    return render_template("charts.html", plants=rare_plants, crops=rare_crops)




@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "").strip().lower()

    if not user_message:
        return jsonify({"reply": "Please send a valid message."})

    # Simple keyword-based responses (more reliable than external API)
    if any(word in user_message for word in ['hello', 'hi', 'hey']):
        return jsonify({"reply": "Hello! I can tell you about rare Jordanian plants like Black Iris, Oak trees, or medicinal herbs."})
    
    elif any(word in user_message for word in ['black iris', 'iris']):
        return jsonify({"reply": "The Black Iris (Iris nigricans) is Jordan's national flower! It's a rare, beautiful plant found mainly in Jordan."})
    
    elif any(word in user_message for word in ['oak', 'querqus']):
        return jsonify({"reply": "Jordan has several rare oak species like Quercus ithaburensis and Quercus calliprinos. They're important for local ecosystems."})
    
    elif any(word in user_message for word in ['almond', 'prunus']):
        return jsonify({"reply": "The Jordanian Almond (Prunus arabica) is a rare species native to the region. It's different from common almond varieties."})
    
    elif any(word in user_message for word in ['medicinal', 'herb', 'medicine']):
        return jsonify({"reply": "Jordan has many rare medicinal plants like Achillea fragrantissima and Artemisia herba-alba used in traditional medicine."})
    
    elif any(word in user_message for word in ['rare', 'endangered']):
        return jsonify({"reply": "Jordan has several rare plants including Iris nigricans, Prunus arabica, and various oak species. Many are protected."})
    
    elif any(word in user_message for word in ['thank', 'thanks']):
        return jsonify({"reply": "You're welcome! Ask me about any specific Jordanian plant you're curious about."})
    
    else:
        return jsonify({"reply": "I specialize in rare Jordanian plants. Try asking about Black Iris, oak trees, almonds, or medicinal herbs!"})
    
        
    
app.secret_key = "key"
CONTACT_FILE = "contact_messages.json"

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Load existing messages
        if os.path.exists(CONTACT_FILE):
            with open(CONTACT_FILE, "r") as f:
                messages = json.load(f)
        else:
            messages = []

        # Add new message
        messages.append({
            "name": name,
            "email": email,
            "message": message
        })

        # Save back to file
        with open(CONTACT_FILE, "w") as f:
            json.dump(messages, f, indent=4)

        flash("Your message has been received. Thank you!")
        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
