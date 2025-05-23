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

if __name__ == "__main__":
    app.run(debug=True)
