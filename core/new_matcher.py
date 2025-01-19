import parse_into_graph
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
        Bauteil---B1(["`<ins>Name</ins>`"])
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe])
        Bauteil---B7([Farbe])
        B3([Größe])---B4([Länge])
        B3([Größe])---B5([Breite])
        B3([Größe])---B6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent--(1,*)---bauen{bauen}
        bauen{bauen}--(1,1)---Bauteil 
        bauen{bauen}---H1([Jahr])
        Bauteil--(2,3)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteil
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
"""
muster_graph = parse_into_graph.parse_mermaid_text(musterloesung)
studenten_graph = parse_into_graph.parse_mermaid_text(studentische_loesung)

def compare_graphs(muster_graph, studenten_graph):
    fehler = {
# Fehler bei Knoten
        "fehlende_Knoten": [],
        "extra_Knoten": [],
        "falscher_Typ_Knoten": [], #typabweichung
        "falscher_Name_Knoten":[], # label
# Fehler bei Kanten
        "fehlende_Kanten": [],
        "extra_Kanten": [],
        "falsche_Kanten": [] # Kardinalität, Beziehung?
    }
    fehler_visualisierung= {
        "fehlende_Knoten_Info": [],
        "extra_Knoten_gelb": [],
        "falscher_Typ_Knoten_rot": [],
        "falscher_Name_Knoten_rot": [],
        "fehlende_Kanten_Info": [],
        "extra_Kanten_gelb": [],
        "falsche_Kanten_rot": []
    }

    for node, data in muster_graph.nodes(data=True): 
        # if data["type"] == "Entität": 
        #     print("Entitäten")
        #     print(node, data)
        # elif data["type"] == "Attribut" or data["type"] == "Primärschlüssel-Attribut" or data["type"] == "mehrwertiges Attribut" or data["type"] == "zusammengesetztes Attribut":  
        #     print("Attribute")
        #     print(node, data) 

        # elif data["type"] == "Relationship": 
        #     print("Relationships")
        #     print(node, data)

    # for node, data entiät in data["type"] == "Entität": 
            print(entität)
compare_graphs(muster_graph, studenten_graph)