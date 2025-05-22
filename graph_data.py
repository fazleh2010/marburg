from flask import Flask, render_template, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j credentials MATCH (n) RETURN n LIMIT 5
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"  # change to your actual password
driver = GraphDatabase.driver(uri, auth=(username, password))


def run_cypher_query(cypher_query):
    with driver.session() as session:
        try:
            result = session.run(cypher_query)
            keys = result.keys()
            records = [record.data() for record in result]
            return keys, records, None
        except Exception as e:
            return [], [], str(e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query", methods=["GET", "POST"])
def query():
    keys, records, error, submitted_query = [], [], None, ""

    if request.method == "POST":
        submitted_query = request.form.get("cypher_query")
        keys, records, error = run_cypher_query(submitted_query)

    return render_template("query.html", keys=keys, records=records, error=error, query=submitted_query)


if __name__ == "__main__":
    app.run(debug=True)
