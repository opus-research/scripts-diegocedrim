from py2neo import Graph
import csv
import codecs


def export_to_csv(cursor, filename):
    with codecs.open(filename, "w", "utf-8") as csvfile:
        writer = None
        for record in cursor:
            if writer is None:
                writer = csv.DictWriter(csvfile, fieldnames=list(record.keys()))
                writer.writeheader()
            record = dict(record)
            writer.writerow(record)


query = """
match (r:Refactoring)-[:CHANGED]->(el:Element)-->(c:Commit)-->(p:Project)
return
    p.name as project_name,
    el.name as element,
    c.order as order,
    c.author_email as author_email,
    r.hash_id as ref_id,
    r.type as type,
    c.hash_id as commit_id,
    c.hash as commit_hash,
    el.hash_id as resource_id
order by
    p.name, el.name, c.order
"""

filename = "all-rerefs.csv"
graph = Graph(password="boil2.eat")
tx = graph.begin()
cursor = tx.run(query)
export_to_csv(cursor, filename)
tx.commit()
