from app.parse_into_graph import parse_mermaid_text
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
        B3([Größe])---C4([Länge])
        B3([Größe])---C5([Breite])
        B3([Größe])---C6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent--(1,*)---bauen{bauen}
        bauen{bauen}--(1,1)---Bauteil 
        bauen{bauen}---F1([Jahr])
        Bauteil--(2,3)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteil
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
"""
# muster_graph = parse_mermaid_text(musterloesung)
# studenten_graph = parse_mermaid_text(studentische_loesung)
# print(studenten_graph.nodes())

def compare_graphs(muster_graph, studenten_graph):
    fehler = {
# Fehler bei Knoten
        "richtige_Knoten": [],
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
        "richtige_Knoten": [],
        "fehlende_Knoten_Info": [],
        "extra_Knoten_gelb": [],
        "falscher_Typ_Knoten_rot": [],
        "falscher_Name_Knoten_rot": [],
        "fehlende_Kanten_Info": [],
        "extra_Kanten_gelb": [],
        "falsche_Kanten_rot": [],
        "richtige_Kanten_grün": []
    }

# Hinzufügen von fehlenden Kanten und Knoten auf der Fehlerliste
    # for node, data in muster_graph.nodes(data=True): 
    #     if studenten_graph.__contains__(node) == False:
    #         fehler["fehlende_Knoten"].append(node)
    #         fehler_visualisierung["fehlende_Knoten_Info"].append(f"   fehlerFehlendeKnoten[Fehler: Es fehlen noch Enitäten, Attribute oder Relationships!] \n    style fehlerFehlendeKnoten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;")
    #         for knoten, daten in studenten_graph.nodes(data=True):
    #             # wenn alle Kanten von node und Knoten gleich sind, dann Fehler für falscher_Name_Knoten
    #             if muster_graph.__contains__(knoten) == False:
    #                 if data == daten and sorted(list(muster_graph.neighbors(node))) == sorted(list(studenten_graph.neighbors(knoten))) and sorted(list(muster_graph.predecessors(node)))==sorted(list(studenten_graph.predecessors(knoten))):
    #                     fehler["falscher_Name_Knoten"].append(f"Muster: {node} ist gemeint mit: {knoten}")
    #                     fehler_visualisierung["falscher_Name_Knoten_rot"].append(f"   style {knoten} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;")
# Hinzufügen von fehlenden Kanten und Knoten auf der Fehlerliste
    for node, data in muster_graph.nodes(data=True): 
        if studenten_graph.has_node(node): 
            fehler["richtige_Knoten"].append(node)
            fehler_visualisierung["richtige_Knoten"].append(f"   style {node} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
        if not studenten_graph.has_node(node):
            fehler["fehlende_Knoten"].append(node)
            fehler_visualisierung["fehlende_Knoten_Info"].append(
                f"   fehlerFehlendeKnoten[Fehler: Es fehlen noch Enitäten, Attribute oder Relationships!] \n    style fehlerFehlendeKnoten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;"
            )
            for knoten, daten in studenten_graph.nodes(data=True):
                # Prüfen, ob der Knoten nicht in der Musterlösung enthalten ist
                if not muster_graph.has_node(knoten):
                    if data['type'] == daten['type'] and data['type']!='Attribut' and daten['type']!='Attribut':
                        # print(knoten, daten)
                        # print(node, data)
                        # muster_nachbarn = sorted(list(muster_graph.neighbors(node))) + sorted(list(muster_graph.predecessors(node)))
                        # studenten_nachbarn = sorted(list(studenten_graph.neighbors(knoten))) + sorted(list(studenten_graph.predecessors(knoten)))
                        muster_nachbarn = sorted(
                            [muster_graph.nodes[n]['label'] for n in muster_graph.neighbors(node)] +
                            [muster_graph.nodes[n]['label'] for n in muster_graph.predecessors(node)]
                        )

                        studenten_nachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(knoten)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(knoten)]
                        )                       
                        # print(muster_nachbarn)
                        # print(studenten_nachbarn)
                        nicht_gefunden = set(studenten_nachbarn) - set(muster_nachbarn)
                        if len(nicht_gefunden) <= 3:  # Maximal ein/zwei Nachbar unterscheidet sich (zwei damit mehr Fehler erkannt werden?)
                            fehler["falscher_Name_Knoten"].append(
                                f"Muster: {node}, {data} Studentische Lösung: {knoten}"
                            )
                            fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                f"   style {knoten} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                            )
                        for nachbar in muster_nachbarn:
                            # print(nachbar)
                            if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(knoten, nachbar): 
                                muster_kard = muster_graph.get_edge_data(node, nachbar)
                                studenten_kard = studenten_graph.get_edge_data(knoten, nachbar)
                                # print(node, data, muster_nachbarn)
                                # print(knoten, daten, studenten_nachbarn)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                            
                            elif muster_graph.has_edge(nachbar, node) and studenten_graph.has_edge(nachbar, knoten):
                                muster_kard = muster_graph.get_edge_data(nachbar,node)
                                studenten_kard = studenten_graph.get_edge_data(nachbar, knoten)
                                # print(node, data, muster_nachbarn)
                                # print(knoten, daten, studenten_nachbarn)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")  
                    elif data['type'] == daten['type'] and data['type']=='Attribut' and data['label'] == daten['label']: #or data['type']=='mehrwertiges Attribut' or data['type']=='Primärschlüssel-Attribut'
                        # muster_nachbarn = sorted(list(muster_graph.neighbors(node))) + sorted(list(muster_graph.predecessors(node)))
                        # studenten_nachbarn = sorted(list(studenten_graph.neighbors(knoten))) + sorted(list(studenten_graph.predecessors(knoten)))
                        muster_nachbarn = sorted(
                            [muster_graph.nodes[n]['label'] for n in muster_graph.neighbors(node)] +
                            [muster_graph.nodes[n]['label'] for n in muster_graph.predecessors(node)]
                        )

                        studenten_nachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(knoten)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(knoten)]
                        ) 
                        labels_in_fehler = [fehler_str.split(" ")[-1] for fehler_str in fehler["falscher_Name_Knoten"]]
                        if muster_nachbarn != studenten_nachbarn and studenten_nachbarn[0] not in labels_in_fehler: 
                            fehler["falscher_Name_Knoten"].append(
                                f"Muster: {node}, {data} Studentische Lösung: {knoten}"
                            )
                            fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                f"   style {knoten} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                            )
                        else:
                            fehler_visualisierung["richtige_Knoten"].append(f"   style {knoten} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                            fehler["richtige_Knoten"].append(knoten)
                        for nachbar in muster_nachbarn:
                            if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(knoten, nachbar): 
                                muster_kard = muster_graph.get_edge_data(node, nachbar)
                                studenten_kard = studenten_graph.get_edge_data(knoten, nachbar)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                            
                            elif muster_graph.has_edge(nachbar, node) and studenten_graph.has_edge(nachbar, knoten):
                                muster_kard = muster_graph.get_edge_data(nachbar,node)
                                studenten_kard = studenten_graph.get_edge_data(nachbar, knoten)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                    
                    elif data['type'] == daten['type'] and data['type']=='mehrwertiges Attribut' and data['label'] == daten['label']:
                        # muster_nachbarn = sorted(list(muster_graph.neighbors(node))) + sorted(list(muster_graph.predecessors(node)))
                        # studenten_nachbarn = sorted(list(studenten_graph.neighbors(knoten))) + sorted(list(studenten_graph.predecessors(knoten)))
                        muster_nachbarn = sorted(
                            [muster_graph.nodes[n]['label'] for n in muster_graph.neighbors(node)] +
                            [muster_graph.nodes[n]['label'] for n in muster_graph.predecessors(node)]
                        )

                        studenten_nachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(knoten)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(knoten)]
                        )                                    
                        labels_in_fehler = [fehler_str.split(" ")[-1] for fehler_str in fehler["falscher_Name_Knoten"]]
                        if muster_nachbarn != studenten_nachbarn and studenten_nachbarn[0] not in labels_in_fehler: 
                            fehler["falscher_Name_Knoten"].append(
                                f"Muster: {node}, {data} Studentische Lösung: {knoten}"
                            )
                            fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                f"   style {knoten} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                            )
                        else:
                            fehler_visualisierung["richtige_Knoten"].append(f"   style {knoten} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                            fehler["richtige_Knoten"].append(knoten)
                        for nachbar in muster_nachbarn:
                            if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(knoten, nachbar): 
                                muster_kard = muster_graph.get_edge_data(node, nachbar)
                                studenten_kard = studenten_graph.get_edge_data(knoten, nachbar)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität") : 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                            
                            elif muster_graph.has_edge(nachbar, node) and studenten_graph.has_edge(nachbar, knoten):
                                muster_kard = muster_graph.get_edge_data(nachbar,node)
                                studenten_kard = studenten_graph.get_edge_data(nachbar, knoten)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                    
                    elif data['type'] == daten['type'] and data['type']=='Primärschlüssel-Attribut' and data['label'] == daten['label']:
                        # muster_nachbarn = sorted(list(muster_graph.neighbors(node))) + sorted(list(muster_graph.predecessors(node)))
                        # studenten_nachbarn = sorted(list(studenten_graph.neighbors(knoten))) + sorted(list(studenten_graph.predecessors(knoten)))
                        muster_nachbarn = sorted(
                            [muster_graph.nodes[n]['label'] for n in muster_graph.neighbors(node)] +
                            [muster_graph.nodes[n]['label'] for n in muster_graph.predecessors(node)]
                        )

                        studenten_nachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(knoten)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(knoten)]
                        )            
                        labels_in_fehler = [fehler_str.split(" ")[-1] for fehler_str in fehler["falscher_Name_Knoten"]]
                        if muster_nachbarn != studenten_nachbarn and studenten_nachbarn[0] not in labels_in_fehler: 
                            fehler["falscher_Name_Knoten"].append(
                                f"Muster: {node}, {data} Studentische Lösung: {knoten}"
                            )
                            fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                f"   style {knoten} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                            )
                        else:
                            fehler_visualisierung["richtige_Knoten"].append(f"   style {knoten} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                            fehler["richtige_Knoten"].append(knoten)
                        for nachbar in muster_nachbarn:
                            if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(knoten, nachbar): 
                                muster_kard = muster_graph.get_edge_data(node, nachbar)
                                studenten_kard = studenten_graph.get_edge_data(knoten, nachbar)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                            
                            elif muster_graph.has_edge(nachbar, node) and studenten_graph.has_edge(nachbar, knoten):
                                muster_kard = muster_graph.get_edge_data(nachbar,node)
                                studenten_kard = studenten_graph.get_edge_data(nachbar, knoten)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                    
                    elif data['type'] == daten['type'] and data['type']=='zusammengesetzes Attribut' and data['label'] == daten['label']:
                        # muster_nachbarn = sorted(list(muster_graph.neighbors(node))) + sorted(list(muster_graph.predecessors(node)))
                        # studenten_nachbarn = sorted(list(studenten_graph.neighbors(knoten))) + sorted(list(studenten_graph.predecessors(knoten)))
                        muster_nachbarn = sorted(
                            [muster_graph.nodes[n]['label'] for n in muster_graph.neighbors(node)] +
                            [muster_graph.nodes[n]['label'] for n in muster_graph.predecessors(node)]
                        )

                        studenten_nachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(knoten)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(knoten)]
                        )            

                        labels_in_fehler = [fehler_str.split(" ")[-1] for fehler_str in fehler["falscher_Name_Knoten"]]
                        if muster_nachbarn != studenten_nachbarn and studenten_nachbarn[0] not in labels_in_fehler:
                            fehler["falscher_Name_Knoten"].append(
                                f"Muster: {node}, {data} Studentische Lösung: {knoten}"
                            )
                            fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                f"   style {knoten} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                            )
                        else:
                            fehler_visualisierung["richtige_Knoten"].append(f"   style {knoten} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                            fehler["richtige_Knoten"].append(knoten)
                        for nachbar in muster_nachbarn:
                            if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(knoten, nachbar): 
                                muster_kard = muster_graph.get_edge_data(node, nachbar)
                                studenten_kard = studenten_graph.get_edge_data(knoten, nachbar)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                            
                            elif muster_graph.has_edge(nachbar, node) and studenten_graph.has_edge(nachbar, knoten):
                                muster_kard = muster_graph.get_edge_data(nachbar,node)
                                studenten_kard = studenten_graph.get_edge_data(nachbar, knoten)
                                if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung')and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") == studenten_kard.get("Kardinalität"): 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                    fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                    
    for edge1, edge2, data in muster_graph.edges(data=True):
        if studenten_graph.has_edge(edge1,edge2) == False: 
            fehler["fehlende_Kanten"].append(edge1 + " zu " + edge2)
            fehler_visualisierung["fehlende_Kanten_Info"].append(f"   fehlerFehlendeKanten[ Es fehlen noch Beziehungen zwischen Enitäten, Attributen oder Relationships!] \n    style fehlerFehlendeKanten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;")
        else: 
            studentenDaten = studenten_graph.get_edge_data(edge1, edge2)
            if studentenDaten == data or studentenDaten.get('Beziehung') == data.get('Beziehung') and studentenDaten.get('Kardinalität') == data.get('Kardinalität'):
                fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studentenDaten.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
            # elif studentenDaten.get('Beziehung') == data.get('Beziehung'):
                # fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studentenDaten.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")

# Hinzufügen von zusätzlichen Knoten und Kanten auf der Fehlerliste
    for node, data in studenten_graph.nodes(data=True): 
        if muster_graph.__contains__(node) == False:
           
            # muster_nachbarn = sorted(list(muster_graph.neighbors(node))) + sorted(list(muster_graph.predecessors(node)))
            studenten_nachbarn = sorted(list(studenten_graph.neighbors(node))) + sorted(list(studenten_graph.predecessors(node)))        
            if node not in fehler["falscher_Name_Knoten"] and node not in fehler["falscher_Typ_Knoten"] and node not in fehler["richtige_Knoten"]: # Prüfen, ob der Knoten ein falscher Knoten ist und deshalb nicht existiert oder ob er wirklich zusätzlich ist
                fehler["extra_Knoten"].append(node)
                fehler_visualisierung["extra_Knoten_gelb"].append(f"   style {node} fill:#FFD966,stroke:#FFD966,stroke-width:2px")

    for edge1, edge2, data in studenten_graph.edges(data=True):
        if muster_graph.has_edge(edge1, edge2) == False: 
            # print(edge1, edge2, data)
            fehler["extra_Kanten"].append(edge1 + " zu " + edge2)
            falsche_Kante_Nummer = data["Nummer"]
            fehler_visualisierung["extra_Kanten_gelb"].append(f"   linkStyle {falsche_Kante_Nummer} color:#FFD966,stroke:#FFD966,stroke-width:4px;")
            # print(fehler_visualisierung["extra_Kanten_gelb"])

# Hinzufügen von falschen Knoten und Kanten auf der Fehlerliste 
    for node, data in muster_graph.nodes(data=True):
        if node in studenten_graph.nodes(): 
            musterloesung_data = data 
            studentenloesung_data = studenten_graph.nodes[node]
            for key, value in musterloesung_data.items():
                if key == "type" and studentenloesung_data.get(key) != value:
                    fehler["falscher_Typ_Knoten"].append(f"Muster: {node}, {data} Studentische Lösung: {studentenloesung_data.get(key, None)}")
                    fehler_visualisierung["falscher_Typ_Knoten_rot"].append(f"   style {node} fill:#F4CCCC,stroke:#CC0000,stroke-width:2px") 
                elif key == "label" and studentenloesung_data[key] != value: 
                    fehler["falscher_Name_Knoten"].append(f"Muster: {node}, {data} Studentische Lösung: {studentenloesung_data.get(key, None)}")
                    fehler_visualisierung["falscher_Name_Knoten_rot"].append(f"   style {node} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000, stroke-width:2px")
    for edge1, edge2, data in muster_graph.edges(data=True): 
        for u, v, dataaa in studenten_graph.edges(data=True): 
            if (u,v) == (edge1, edge2) and data != dataaa:  
                for key, value in data.items(): 
                    if key == "Kardinalität" and dataaa[key] != value: 
                        falsche_Kante_Nummer = dataaa["Nummer"]
                        fehler["falsche_Kanten"].append(f"Muster: {edge1} zu {edge2} mit {data}, Studentische Lösung: {u} zu {v} {dataaa}")
                        fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {falsche_Kante_Nummer} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
    
    # extra Kanten entfernen, wenn sie mit einem falsch geschriebenen Knoten zusammenhängen
    for kante in fehler["extra_Kanten"]: 
        for knoten in fehler["falscher_Name_Knoten"]: 
            knoten_falsch = knoten.split()[-1]
            knoten_falsch = knoten_falsch.replace("{", "")
            knoten_falsch = knoten_falsch.replace("}", "")
            knoten_falsch = knoten_falsch.replace("'", "")
            if knoten_falsch in kante.split()[0] or knoten_falsch in kante.split()[2]: 
                kante1 = kante.split()[0]
                kante2 = kante.split()[2]
                kanten_nummer = studenten_graph.get_edge_data(kante1, kante2)["Nummer"]
                fehler_visualisierung["extra_Kanten_gelb"] = [
                    kanten for kanten in fehler_visualisierung["extra_Kanten_gelb"]
                    if f"linkStyle {kanten_nummer}" in kanten
                ]
    # extra Knoten entfernen, wenn diese mit dem falsch geschriebenen Knoten übereinstimmen
    for knoten in fehler["extra_Knoten"]: 
        for node in fehler["falscher_Name_Knoten"]:
            knoten_falsch = node.split()[-1]
            if knoten_falsch in knoten:
                fehler_visualisierung["extra_Knoten_gelb"] = [
                    fehler for fehler in fehler_visualisierung["extra_Knoten_gelb"]
                    if f"style {knoten_falsch}" not in fehler
                ]
    # for kante in fehler["extra_Kanten"]:
    #     for knoten in fehler["falscher_Name_Knoten"]:
    #         if knoten in kante:
    #             fehler_visualisierung["extra_Kanten_gelb"] = [
    #                 k for k in fehler_visualisierung["extra_Kanten_gelb"]
    #                 if f"linkStyle {kante}" not in k
    #             ]
                
    # print(f"Kanten in muster_graph: {muster_graph.edges(data=True)}")
    # print(f"Kanten in studenten_graph: {studenten_graph.edges(data=True)}")
    feedback = visualisieren(fehler_visualisierung, studentische_loesung)
    return feedback

# Visualieren des Feedbakcs (Hinzufügen zu der studentischen Lösung)
def visualisieren(fehler, studentische_loesung):
    for x in fehler:
        for y in  fehler[x]:
            if y not in studentische_loesung: 
                studentische_loesung = studentische_loesung + f"\n {y}"
        
    return studentische_loesung