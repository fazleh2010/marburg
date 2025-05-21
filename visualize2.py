from flask import Flask, render_template, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Configure Neo4j connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"  # ← Replace with your password
driver = GraphDatabase.driver(uri, auth=(username, password))


@app.route("/")
def index():
    return render_template("index2.html")


@app.route("/query", methods=["POST"])
def query():
    data = request.json
    cypher_query = data.get("query", "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25")

    nodes = {}
    edges = []

    with driver.session() as session:
        results = session.run(cypher_query)
        for record in results:
            n = record["n"]
            m = record["m"]
            r = record["r"]

            for node in [n, m]:
                node_id = str(node.element_id)
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": node.get("name", list(node.labels)[0]),
                        "title": str(dict(node))
                    }

            edges.append({
                "from": str(n.element_id),
                "to": str(m.element_id),
                "label": r.type
            })

    return jsonify({"nodes": list(nodes.values()), "edges": edges})


if __name__ == "__main__":
    app.run(debug=True)
