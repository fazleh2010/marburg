from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('RomArchivePageEn_1.5.html')  # HTML must be in a "templates/" folder

if __name__ == '__main__':
    app.run(debug=True)
