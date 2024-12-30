import re 
import networkx as nx

def parse_nodes(line, graph):
    node_pattern = r"(\w+)---(\w+)\(\[\"<ins>(.*?)</ins>\"\]\)"  # Regex für Knoten
    matches = re.findall(node_pattern, line)
    for entity, attr_id, attribute in matches:
        graph.add_node(entity, type="entity")
        graph.add_node(attr_id, type="attribute", label=attribute)
        graph.add_edge(entity, attr_id, relationship="has")


def parse_relationships(line, graph):
    relationship_pattern = r"(\w+) -- \((\d+,\*|\d+,\d+)\) --- (\w+)\{(.*?)\} -- \((\d+,\*|\d+,\d+)\) --- (\w+)"
    match = re.search(relationship_pattern, line)
    if match:
        entity1, card1, rel_id, label, card2, entity2 = match.groups()
        graph.add_node(rel_id, type="relationship", label=label)
        graph.add_edge(entity1, rel_id, cardinality=card1)
        graph.add_edge(rel_id, entity2, cardinality=card2)


def parse_mermaid(mermaid_code): 
    graph = nx.DiGraph()
    lines = mermaid_code.split("\n")
    for line in lines: 
        if "---" in line and "[" in line:
            parse_nodes(line, graph)
        elif "--" in line and "{" in line:
            parse_relationships(line, graph)

    return graph

mermaid_code = """mermaid
flowchart
        Produzent---P1(["`<ins>ProdId</ins>`"])
        Produzent---P2([Name])
        Produzent---P3(((Zertifikate)))
        Bauteil---B1(["`<ins>Name</ins>`"])
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe])
        B3---B4([Länge])
        B3---B5([Breite])
        B3---B6([Höhe])
        Produzent -- (1,*) --- herstellen{herstellen}
        herstellen -- (1,1) --- Bauteil 
        herstellen---H1([Jahr])
        Bauteil -- (0,*) --- bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus} -- (0,*) --- Bauteil 
"""

graph = parse_mermaid(mermaid_code)

# Ausgeben der Graph-Knoten und -Kanten
print("Knoten:")
for node, data in graph.nodes(data=True):
    print(node, data)

print("\nKanten:")
for u, v, data in graph.edges(data=True):
    print(u, v, data)