# main.py - simple Flask app that stores "regrets" in a local JSON file
from flask import Flask, request, redirect, url_for, render_template_string, abort
import json
import os

app = Flask(__name__)

# file to persist regrets on disk (simple and works in CI)
DATA_FILE = os.path.join(os.path.dirname(__file__), "regrets.json")

# ensure data file exists and has a list
def ensure_datafile():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def read_regrets():
    ensure_datafile()
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def write_regrets(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)

# very small HTML template (kept inline to avoid external templates)
INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Regrets App</title>
  </head>
  <body>
    <h1>Share a regret</h1>
    <form method="post" action="/submit">
      <label for="regret">What's your biggest regret?</label><br/>
      <input type="text" name="regret" id="regret" style="width:400px" required />
      <button type="submit">Submit</button>
    </form>

    <h2>Shared regrets</h2>
    <ul>
      {% for r in regrets %}
        <li>{{ r }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
"""

@app.route("/")
def index():
    regrets = read_regrets()
    # render simple template with the list of regrets
    return render_template_string(INDEX_HTML, regrets=regrets)

@app.route("/submit", methods=["POST"])
def submit():
    text = request.form.get("regret", "").strip()
    if not text:
        # bad request if empty
        abort(400, "Regret is required")
    items = read_regrets()
    items.append(text)
    write_regrets(items)
    # redirect back to index (PRG pattern)
    return redirect(url_for("index"))

if __name__ == "__main__":
    # run on 0.0.0.0 so Jenkins or other machines can reach it if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
