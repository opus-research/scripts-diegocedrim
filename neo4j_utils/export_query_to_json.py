from py2neo import Graph
import json


def export_to_json(cursor, filename):
    result = []
    with open(filename, "w") as jsonfile:
        for record in cursor:
            result.append(dict(record))
        result_json = json.dumps(result, indent=4)
        jsonfile.write(result_json)

query = """
match (b:Bug)-->(br:BugReport)-->(c:Comment) return b, br, collect(c) as comments
"""

filename = "bugs_classified.json"
graph = Graph(password="boil2.eat")
tx = graph.begin()
cursor = tx.run(query)
export_to_json(cursor, filename)
tx.commit()

