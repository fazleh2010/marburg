from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"  # replace with your password

driver = GraphDatabase.driver(uri, auth=(username, password))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/graph-data")
def get_graph_data():
    query = "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50"

    nodes = {}
    edges = []

    with driver.session() as session:
        result = session.run(query)
        for record in result:
            n = record["n"]
            m = record["m"]
            r = record["r"]

            for node in [n, m]:
                node_id = str(node.element_id)
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": list(node.labels)[0],
                        "title": dict(node)
                    }

            edges.append({
                "from": str(n.element_id),
                "to": str(m.element_id),
                "label": r.type
            })

    return jsonify({"nodes": list(nodes.values()), "edges": edges})


if __name__ == "__main__":
    app.run(debug=True)
