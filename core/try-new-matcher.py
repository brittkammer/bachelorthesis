import bachelorthesis.app.parse_into_graph as parse_into_graph
import networkx as nx

musterloesung = """mermaid
    flowchart
    subgraph SG1 [ ]
        Produzent---P1(["`<ins>ProdId</ins>`"])
        Produzent---P2([Name])
        Produzent---P3(((Zertifikate)))
    end
    subgraph SG2 [ ]
        Bauteil---B1(["`<ins>Name</ins>`"])
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe])
        B3([Größe])---B4([Länge])
        B3([Größe])---B5([Breite])
        B3([Größe])---B6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent--(1,*)---herstellen{herstellen}
        herstellen{herstellen}--(1,1)---Bauteil 
        herstellen{herstellen}---H1([Jahr])
        Bauteil--(0,*)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteil
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
"""

studentische_loesung = """mermaid
flowchart
    subgraph SG1 [ ]
        Produzent---P1(["`<ins>ProdId</ins>`"])
        Produzent---P3(((Zertifikate)))
    end
    subgraph SG2 [ ]
        Bauteile---B1(["`<ins>Name</ins>`"])
        Bauteile---B2([Gewicht])
        Bauteile---B3([Größe])
        Bauteile---B7([Farbe])
        B3([Größe])---B4([Länge])
        B3([Größe])---B5([Breite])
        B3([Größe])---B6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent--(1,*)---bauen{bauen}
        bauen{bauen}--(1,1)---Bauteile 
        bauen{bauen}---H1([Jahr])
        Bauteile--(2,3)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteile
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
"""
# musterGraph = parse_into_graph.parse_mermaid_text(musterloesung)
# studentenGraph = parse_into_graph.parse_mermaid_text(studentischeLoesung)

import bachelorthesis.app.parse_into_graph as parse_into_graph
import networkx as nx
from difflib import get_close_matches

def finde_knoten_ersatz(knoten, muster_knoten_liste):
    matches = get_close_matches(knoten, muster_knoten_liste, n=1, cutoff=0.8)
    return matches[0] if matches else None

muster_graph = parse_into_graph.parse_mermaid_text(musterloesung)
studenten_graph = parse_into_graph.parse_mermaid_text(studentische_loesung)

# Überprüfung auf falsch geschriebene Knoten
korrektur_map = {}
for node in studenten_graph.nodes():
    if node not in muster_graph.nodes():
        ersatz = finde_knoten_ersatz(node, muster_graph.nodes())
        if ersatz:
            korrektur_map[node] = ersatz

# Knoten umbenennen, falls Fehler gefunden wurden
studenten_graph = nx.relabel_nodes(studenten_graph, korrektur_map)

def compare_graphs(muster_graph, studenten_graph):
    fehler = {
        "fehlende_Knoten": [],
        "extra_Knoten": [],
        "falscher_Typ_Knoten": [],
        "falscher_Name_Knoten": [],
        "fehlende_Kanten": [],
        "extra_Kanten": [],
        "falsche_Kanten": []
    }
    
    # Überprüfung fehlender und zusätzlicher Knoten
    for node in muster_graph.nodes():
        if not studenten_graph.has_node(node):
            fehler["fehlende_Knoten"].append(node)
    
    for node in studenten_graph.nodes():
        if not muster_graph.has_node(node):
            fehler["extra_Knoten"].append(node)

    # Überprüfung fehlender Kanten
    for edge in muster_graph.edges(data=True):
        if not studenten_graph.has_edge(edge[0], edge[1]):
            fehler["fehlende_Kanten"].append(f"{edge[0]} -> {edge[1]}")

    # Überprüfung zusätzlicher Kanten
    for edge in studenten_graph.edges(data=True):
        if not muster_graph.has_edge(edge[0], edge[1]):
            fehler["extra_Kanten"].append(f"{edge[0]} -> {edge[1]}")

    # Überprüfung der Kardinalitäten
    for edge1, edge2, data in muster_graph.edges(data=True):
        if studenten_graph.has_edge(edge1, edge2):
            studenten_data = studenten_graph.get_edge_data(edge1, edge2)
            if studenten_data.get('Kardinalität') != data.get('Kardinalität'):
                fehler["falsche_Kanten"].append(f"Muster: {edge1} zu {edge2} mit {data}, Studentische Lösung: {edge1} zu {edge2} {studenten_data}")
    print(fehler)
    return fehler

fehler = compare_graphs(muster_graph, studenten_graph)

# Fehler visualisieren
def visualisieren(fehler, studentische_loesung):
    for x in fehler:
        for y in fehler[x]:
            if str(y) not in studentische_loesung:
                studentische_loesung = studentische_loesung + f"\n {y}"
    print(studentische_loesung)

visualisieren(fehler, studentische_loesung)
