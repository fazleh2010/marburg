from neo4j import GraphDatabase

# Neo4j connection config
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"  # 🔒 Replace with your password

# Create driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define Cypher query
cypher_query = """
CREATE (a:Person {name: 'Alice'})
CREATE (b:Person {name: 'Bob'})
CREATE (c:Person {name: 'Charlie'})
CREATE (a)-[:KNOWS]->(b)
CREATE (b)-[:KNOWS]->(c)
"""

# Run query
with driver.session() as session:
    session.run(cypher_query)
    print("Data successfully added to Neo4j!")

# Close driver
driver.close()
