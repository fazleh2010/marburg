from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase

app = Flask(__name__, static_url_path='/static')

# Configure your Neo4j connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_nodes():
    with driver.session() as session:
        result = session.run("MATCH (n:Person) RETURN n.name AS name LIMIT 10")
        return [record["name"] for record in result]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/nodes")
def nodes():
    data = get_nodes()
    return jsonify(data)

@app.route('/sections/')
def sections():
    return render_template('sections.html')  # or any logic here

@app.route('/visual_art')
def visual_art():
    return render_template("visual_art.html")

@app.route('/audio')
def audio():
    return render_template("audio.html")

@app.route('/video')
def video():
    return render_template("video.html")

@app.route('/book')
def book():
    return render_template("book.html")

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/context-project/')
def context_project():
    return render_template('context_project.html')

@app.route('/history-of-romarchive/')
def history_of_romarchive():
    return render_template('history_of_romarchive.html')

@app.route('/curators/')
def curators():
    return render_template('curators.html')

@app.route('/ethical-guidelines/')
def ethical_guidelines():
    return render_template('ethical_guidelines.html')

@app.route('/collection-policy/')
def collection_policy():
    return render_template('collection_policy.html')

@app.route('/faq/')
def faq():
    return render_template('faq.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/terms/')
def terms():
    return render_template('terms.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/collection/politics-of-photography/')
def politics_of_photography():
    return render_template('politics_of_photography.html')  # or return some content

@app.route('/supporters/')
def supporters():
    return '<h1>Supporters Page</h1>'

@app.route('/imprint/')
def imprint():
    return '<h1>Imprint Page</h1>'

@app.route('/privacy/')
def privacy():
    return '<h1>Privacy Statement</h1>'




if __name__ == "__main__":
    app.run(debug=True)
