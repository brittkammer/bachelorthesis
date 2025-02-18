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
        Gerät---B1(["`<ins>Name</ins>`"])
        Gerät---B2([Gewicht])
        Gerät---B3([Größe])
        Gerät---B7([Farbe])
        B3([Größe])---B4([Länge])
        B3([Größe])---B5([Breite])
        B3([Größe])---B6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent--(1,*)---bauen{bauen}
        bauen{bauen}--(1,1)---Gerät 
        bauen{bauen}---H1([Jahr])
        Gerät--(2,3)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Gerät
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
        "falscher_Typ_Knoten": [],  # typabweichung
        "falscher_Name_Knoten": [],  # label
        # Fehler bei Kanten
        "fehlende_Kanten": [],
        "extra_Kanten": [],
        "falsche_Kanten": [],  # Kardinalität, Beziehung?
    }
    fehler_visualisierung = {
        "fehlende_Knoten_Info": [],
        "extra_Knoten_gelb": [],
        "falscher_Typ_Knoten_rot": [],
        "falscher_Name_Knoten_rot": [],
        "fehlende_Kanten_Info": [],
        "extra_Kanten_gelb": [],
        "falsche_Kanten_rot": [],
    }

    # Hinzufügen von fehlenden Kanten und Knoten auf der Fehlerliste
    for node, data in muster_graph.nodes(data=True):
        if studenten_graph.__contains__(node) == False:
            fehler["fehlende_Knoten"].append(node)
            fehler_visualisierung["fehlende_Knoten_Info"].append(
                f"   fehlerFehlendeKnoten[Fehler: Es fehlen noch Enitäten, Attribute oder Relationships!] \n    style fehlerFehlendeKnoten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;"
            )
            for knoten, daten in studenten_graph.nodes(data=True):
                # wenn alle Kanten von node und Knoten gleich sind, dann Fehler für falscher_Name_Knoten
                if muster_graph.__contains__(knoten) == False:
                    if (
                        data == daten
                        and sorted(list(muster_graph.neighbors(node)))
                        == sorted(list(studenten_graph.neighbors(knoten)))
                        and sorted(list(muster_graph.predecessors(node)))
                        == sorted(list(studenten_graph.predecessors(knoten)))
                    ):
                        fehler["falscher_Name_Knoten"].append(
                            f"Muster: {node} ist gemeint mit: {knoten}"
                        )
                        fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                            f"   style {knoten} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                        )

    for edge1, edge2, data in muster_graph.edges(data=True):
        if studenten_graph.has_edge(edge1, edge2) == False:
            fehler["fehlende_Kanten"].append(edge1 + " zu " + edge2)
            fehler_visualisierung["fehlende_Kanten_Info"].append(
                f"   fehlerFehlendeKanten[ Es fehlen noch Beziehungen zwischen Enitäten, Attributen oder Relationships!] \n    style fehlerFehlendeKanten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;"
            )

    # Hinzufügen von zusätzlichen Knoten und Kanten auf der Fehlerliste
    for node, data in studenten_graph.nodes(data=True):
        if muster_graph.__contains__(node) == False:
            fehler["extra_Knoten"].append(node)
            fehler_visualisierung["extra_Knoten_gelb"].append(
                f"   style {node} fill:#d9eaf7,stroke:#045a8d,stroke-width:2px"
            )
    for edge1, edge2, data in studenten_graph.edges(data=True):
        if muster_graph.has_edge(edge1, edge2) == False:
            fehler["extra_Kanten"].append(edge1 + " zu " + edge2)
            falsche_Kante_Nummer = data["Nummer"]
            fehler_visualisierung["extra_Kanten_gelb"].append(
                f"   linkStyle {falsche_Kante_Nummer} stroke:#FFD966,stroke-width:4px,color:#FFD966, fill:none;"
            )

    # Hinzufügen von falschen Knoten und Kanten auf der Fehlerliste
    for node, data in muster_graph.nodes(data=True):
        if node in studenten_graph.nodes():
            musterloesung_data = data
            studentenloesung_data = studenten_graph.nodes[node]
            for key, value in musterloesung_data.items():
                if key == "type" and studentenloesung_data[key] != value:
                    fehler["falscher_Typ_Knoten"].append(
                        "Muster: "
                        + str(node, data)
                        + "Studentische Lösung: "
                        + studentenloesung_data.get(key, None)
                    )
                    fehler_visualisierung["falscher_Typ_Knoten_rot"].append(
                        f"   style {node} fill:#F4CCCC,stroke:#CC0000,stroke-width:2px"
                    )
                elif key == "label" and studentenloesung_data[key] != value:
                    fehler["falscher_Name_Knoten"].append(
                        "Muster: "
                        + str(node, data)
                        + "Studentische Lösung: "
                        + studentenloesung_data.get(key, None)
                    )
                    fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                        f"   style {node} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000, stroke-width:2px"
                    )
    for edge1, edge2, data in muster_graph.edges(data=True):
        for u, v, dataaa in studenten_graph.edges(data=True):
            if (u, v) == (edge1, edge2) and data != dataaa:
                for key, value in data.items():
                    if key == "Kardinalität" and dataaa[key] != value:
                        falsche_Kante_Nummer = dataaa["Nummer"]
                        # print(falsche_Kante_Nummer)
                        fehler["falsche_Kanten"].append(
                            f"Muster: {edge1} zu {edge2} mit {data}, Studentische Lösung: {u} zu {v} {dataaa}"
                        )
                        fehler_visualisierung["falsche_Kanten_rot"].append(
                            f"   linkStyle {falsche_Kante_Nummer} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;"
                        )

    # extra Kanten entfernen, wenn sie mit einem falsch geschriebenen Knoten zusammenhängen
    for kante in fehler["extra_Kanten"]:
        for knoten in fehler["falscher_Name_Knoten"]:
            knoten_falsch = knoten.split()[-1]
            if knoten_falsch in kante:
                kante1 = kante.split()[0]
                kante2 = kante.split()[2]
                kanten_nummer = studenten_graph.get_edge_data(kante1, kante2)["Nummer"]

                fehler_visualisierung["extra_Kanten_gelb"] = [
                    kanten
                    for kanten in fehler_visualisierung["extra_Kanten_gelb"]
                    if f"linkStyle {kanten_nummer}" not in kanten
                ]
    # extra Knoten entfernen, wenn diese mit dem falsch geschriebenen Knoten übereinstimmen
    for knoten in fehler["extra_Knoten"]:
        for node in fehler["falscher_Name_Knoten"]:
            knoten_falsch = node.split()[-1]
            if knoten_falsch in knoten:
                # print(knoten_falsch)
                fehler_visualisierung["extra_Knoten_gelb"] = [
                    fehler
                    for fehler in fehler_visualisierung["extra_Knoten_gelb"]
                    if f"style {knoten_falsch}" not in fehler
                ]

    # print(f"Kanten in muster_graph: {muster_graph.edges(data=True)}")
    # print(f"Kanten in studenten_graph: {studenten_graph.edges(data=True)}")
    print(fehler)
    return fehler_visualisierung


fehler = compare_graphs(muster_graph, studenten_graph)


# Visualieren des Feedbakcs (Hinzufügen zu der studentischen Lösung)
def visualisieren(fehler, studentische_loesung):
    for x in fehler:
        for y in fehler[x]:
            if y not in studentische_loesung:
                studentische_loesung = studentische_loesung + f"\n {y}"

    print(studentische_loesung)


visualisieren(fehler, studentische_loesung)
