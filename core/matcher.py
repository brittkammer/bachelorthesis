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
        Produzent--(1,*)---herstellen{bauen}
        herstellen{herstellen}--(1,1)---Bauteil 
        herstellen{herstellen}---H1([Jahr])
        Bauteil--(2,3)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteil
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style herstellen fill:#ff0000,stroke:#333,stroke-width:0px
    style P2 fill:#ffff00, stroke:#333,stroke-width:0px
    style B7 fill:#0000ff, stroke:#333,stroke-width:0px
"""
# studentische_loesung = musterloesung
musterloesung_sortiert = parse_into_graph.alhabetisch_sortieren(musterloesung)
studentische_loesung_sortiert = parse_into_graph.alhabetisch_sortieren(studentische_loesung)

muster_graph = parse_into_graph.parse_mermaid_text(musterloesung_sortiert)
studenten_graph = parse_into_graph.parse_mermaid_text(studentische_loesung_sortiert)


def compare_graphs(muster_graph, studenten_graph):
    fehler = {
        # Fehler bei Knoten
        "fehlende_Knoten": [],
        "extra_Knoten": [],
        # "falsche_Knoten": [], # typabweichung, falscher Name. semantischer Fehler
        "falscher_Typ": [],
        "falscher_Name":[],
        "semantischer_Fehler": [],

        # Fehler bei Kanten
        "fehlende_Kanten": [],
        "extra_Kanten": [],
        # "falsche_Kanten": [] # Kardinalität, Beziehung
        "falsche_Kardinalität": [],
        "falsche_Beziehung":[],
    }

# Hinzufügen von fehlenden Kanten und Knoten auf der Fehlerliste
    for node, data in muster_graph.nodes(data=True): 
        if studenten_graph.__contains__(node) == False:
            fehler["fehlende_Knoten"].append(node)

        # if node not in studenten_graph.nodes(data=True): 
        #     fehler["fehlende_Knoten"].append(node)

    for edge1, edge2, data in muster_graph.edges(data=True):
        if studenten_graph.has_edge(edge1,edge2) == False: 
        # if str(edge1 + " " + edge2) not in studenten_graph.edges(data=True): 
            fehler["fehlende_Kanten"].append(edge1 + " zu " + edge2)

# Hinzufügen von zusätzlichen Knoten und Kanten auf der Fehlerliste
    for node, data in studenten_graph.nodes(data=True): 
        if muster_graph.__contains__(node) == False:
            fehler["extra_Knoten"].append(node)
    for edge1, edge2, data in studenten_graph.edges(data=True):
        if muster_graph.has_edge(edge1, edge2) == False: 
            fehler["extra_Kanten"].append(edge1 + " zu " + edge2)
    # for node, data in studenten_graph.nodes(data=True): 
    #     if node not in muster_graph.nodes(data=True): 
    #         fehler["extra_Knoten"].append(node)
    # for edge1, edge2, data in studenten_graph.edges(data=True):
    #     # print(edge1, edge2)
    #     # print(muster_graph.edges(data=True))
    #     if str(edge1 + " " + edge2) not in muster_graph.edges(data=True): 
    #         fehler["extra_Kanten"].append(edge1 + " zu " + edge2)

# Hinzufügen von faschen Knoten und Kanten auf der Fehlerliste 

    for node, data in muster_graph.nodes(data=True):
        # print(node, data)
        blabla = node, data
        # if  value not in studenten_graph.nodes(data=True):
        #     print(value) 
        if node in studenten_graph.nodes(): 
            musterloesung_data = data 
            studentenloesung_data = studenten_graph.nodes[node]
            for key, value in musterloesung_data.items():
                if key not in studentenloesung_data or studentenloesung_data[key] != value:
                    fehler["falscher_Typ"].append("Muster: " + str(blabla) + "Studentische Lösung: " + studentenloesung_data.get(key, None))
                    # print(f"Unterschied in Knoten '{node}': Attribut '{key}' ist im Muster '{value}', aber im Studenten-Graph '{studentenloesung_data.get(key, None)}'")
        
    for edge1, edge2, data in muster_graph.edges(data=True): 
        # blabla = edge1, edge2, data
        # if blabla in studenten_graph.edges(data=True): 
            musterloesung_data = data
            print(edge1, edge2)
            # print(data.items())
            studentenloesung_data = studenten_graph.get_edge_data(edge1, edge2)
            # studentenloesung_data = studenten_graph.edges(data=True)
            # studentenloesung_data = studenten_graph.(data=True)
            # print(studentenloesung_data)
            # print(studentenloesung_data)
            if studenten_graph.has_edge(edge1, edge2):
                # for edge in studenten_graph.get_edge_data(edge1, edge2):
                for edge in studentenloesung_data:
                    print(edge)
            # for key, value in data.items():
            #     print(key, value)
            #     if key not in studentenloesung_data or studentenloesung_data[key] != value: 
            #         print(studentenloesung_data[key], value)
            #         # fehler["falsche_Kardinalität"].append("Muster: " + str(data.items()) + "Studentische Lösung: " + studentenloesung_data.get(key))

    # print(muster_graph.edges(data=True))
    # print(studenten_graph.edges(data=True))
    # print(fehler)
    # print(nx.vf2pp_isomorphism(muster_graph, studenten_graph, node_label="type"))
    # print(nx.vf2pp_all_isomorphisms(muster_graph, studenten_graph, node_label=None))

compare_graphs(muster_graph, studenten_graph)
