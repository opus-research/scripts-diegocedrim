# Computando mudanças por commit

Para computar os batches, precisamos, para todos os projetos saber quais arquivos foram mudados
em cada commit e por qual desenvolvedor. Usamos um comando do próprio git pra isso.
O script `changes_data/code/extract_changes.sh` computa as mudanças para todos os repositórios
listados em `changes_data/code/export.csv`. Para computar essas mudanças para um repositório GIT
qualquer, basta executar o seguinte comando:

```bash
git log --pretty=commit=%H:%ae --name-status
```

# Extraindo re-refatorações

Os batches são computados usando as re-refatorações encontradas no banco. Para computar todas elas
em todos os projetos, basta rodar a query abaixo no Neo4J. As re-refs são uma das entradas pro
algoritmo de deteção de batches, que está em `detect_element_based.py`


```cypher
match (r:Refactoring)-[:CHANGED]->(el:Element)-->(c:Commit)-->(p:Project)
return
    toLower(p.name) as project_name,
    el.name as element,
    c.order as order,
    c.author_email as author_email,
    r.hash_id as ref_id,
    r.type as type,
    c.hash_id as commit_id,
    c.hash as commit_hash,
    el.hash_id as resource_id
order by
    toLower(p.name), toLower(p.name), c.order
```

A versão dos scripts que usam json (scope e version based) usam um arquivo com
o conteudo gerado pela seguinte query

```cypher
match (r:Refactoring)-[:CHANGED]->(el:Element)-->(c:Commit)-->(p:Project)
return r as refactoring, collect(el.name) as elements, c as commit, p as project
order by p.name, c.order
```


# Extraindo commits por desenvolvedor

Precisamos saber os commits que cada desenvolvedor fez na história do projeto para computar
os batches. Para isso, basta rodar a seguinte query:


```cypher
match (c:Commit)-->(p:Project)
return
    toLower(p.name) as project_name,
    c.hash_id as version_id,
    c.author_email as author_email,
    c.order as order
order
    by toLower(p.name),
    c.order
```
