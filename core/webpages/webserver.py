from flask import Flask, request, render_template_string
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# HTML template
HTML = '''
<!DOCTYPE html>
<html>
<head><title>Neo4j Person Lookup</title></head>
<body>
    <h1>Find Person by Name</h1>
    <form method="post">
        <input type="text" name="name" placeholder="Enter a name" required>
        <input type="submit" value="Search">
    </form>

    {% if results %}
        <h2>Results:</h2>
        <ul>
            {% for row in results %}
                <li>{{ row['name'] }} (Age: {{ row['age'] }})</li>
            {% endfor %}
        </ul>
    {% elif error %}
        <h2>Error:</h2>
        <pre>{{ error }}</pre>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None

    if request.method == "POST":
        name_input = request.form["name"]

        query = """
        MATCH (p:Person)
        WHERE toLower(p.name) = toLower($name)
        RETURN p.name AS name, p.age AS age
        """

        try:
            with driver.session() as session:
                records = session.run(query, name=name_input)
                results = [record.data() for record in records]
        except Exception as e:
            error = str(e)

    return render_template_string(HTML, results=results, error=error)

if __name__ == "__main__":
    app.run(debug=True)
