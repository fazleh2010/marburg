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

@app.route('/visual_art')
def visual_art():
    return render_template("Archive.html")

@app.route('/audio')
def audio():
    return render_template("audio.html")

@app.route('/video')
def video():
    return render_template("video.html")

@app.route('/book')
def book():
    return render_template("book.html")

@app.route('/about/context-project/')
def context_project():
    return render_template('context_project.html')

@app.route('/about/history-of-romarchive/')
def history_of_romarchive():
    return render_template('history_of_romarchive.html')

@app.route('/about/curators/')
def curators():
    return render_template('curators.html')

@app.route('/about/ethical-guidelines/')
def ethical_guidelines():
    return render_template('ethical_guidelines.html')

@app.route('/about/collection-policy/')
def collection_policy():
    return render_template('collection_policy.html')

@app.route('/about/frequently-answered-questions/')
def faq():
    return render_template('faq.html')

if __name__ == "__main__":
    app.run(debug=True)
