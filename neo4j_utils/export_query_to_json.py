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
match (r:Refactoring)-[:CHANGED]->(el:Element)-->(c:Commit)-->(p:Project)
return r as refactoring, collect(el.name) as elements, c as commit, p as project
order by p.name, c.order
"""

filename = "../batch_refactoring/refactorings_and_all_elements.json"
graph = Graph(password="boil2.eat")
tx = graph.begin()
cursor = tx.run(query)
export_to_json(cursor, filename)
tx.commit()

