from flask import Flask, render_template_string

app = Flask(__name__)

# Replace with your actual Google Sheet ID (not URL)
GOOGLE_SHEET_ID = "1aBcD12345EXAMPLE"

HTML = f"""
<!DOCTYPE html>
<html>
<head>
  <title>StorylineJS Demo</title>
  <script src="https://cdn.knightlab.com/libs/storyline/latest/js/storyline-min.js"></script>
  <link rel="stylesheet" href="https://cdn.knightlab.com/libs/storyline/latest/css/storyline.css">
</head>
<body>
  <h1>StorylineJS Visualization</h1>
  <div id="storyline-embed" class="storyline">
    <iframe src="https://cdn.knightlab.com/libs/storyline/latest/embed/index.html?data=https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/pubhtml" width="100%" height="600" frameborder="0"></iframe>
  </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
