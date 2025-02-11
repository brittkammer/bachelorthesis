from parse_into_graph import parse_mermaid_text
from solution_parser import parse_solution
import networkx as nx 
from itertools import product


############ LÖSUNGEN ZUM DEBUGGEN ################
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
        Produzent--(1,*)---herstellen{herstellen|bauen}
        herstellen{herstellen|bauen}--(1,1)---Bauteil 
        herstellen{herstellen|bauen}---H1([Jahr|Year])
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
        Bauteil---B11(["`<ins>Name</ins>`"])
        Bauteil---B22([Gewicht])
        Bauteil---B3([Größe])
        Bauteil---B7([Farbe])
        B3([Größe])---C4([Länge])
        B3([Größe])---C5([Breite])
        B3([Größe])---C6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent--(1,*)---bauen{bauen}
        bauen{bauen}--(1,1)---Bauteil 
        bauen{bauen}---F1([Year])
        Bauteil--(2,3)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteil
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
"""

muster_graph = parse_solution(musterloesung)
studenten_graph = parse_mermaid_text(studentische_loesung)

############ MATCHER ######################

def compare_graphs(muster_graph, studenten_graph):
    fehler = {
# Fehler bei Knoten
        "richtige_Knoten": [],
        "falsche_Nachbarn": [],
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
        "falsche_Nachbarn_blau": [],
        "fehlende_Knoten_Info": [],
        "extra_Knoten_gelb": [],
        "falscher_Typ_Knoten_rot": [],
        "falscher_Name_Knoten_rot": [],
        "fehlende_Kanten_Info": [],
        "extra_Kanten_gelb": [],
        "falsche_Kanten_rot": [],
        "richtige_Kanten_grün": []
    }

    # Reihenfolge der Fehlerprüfung: Zuerst alle Knoten der Entitäten, dann Attribute, dann Relationships 
    # Fehler Reihenfolge: Richtige Knoten, Extra Knoten, Fehlende Knoten, Falscher Name und Falscher Typ 
    
    ########## RICHTIGE KNOTEN ##############################     
    for node, data in muster_graph.nodes(data=True): 
            for studentNode, studentData in studenten_graph.nodes(data=True):
                print()
                if data['type'] == 'Entität' and studentData['type'] == 'Entität' and node == studentNode: ##### Beginnen mit Fehlerprüfung für Entiäten    
                    ############## Richtige Knoten prüfen
                    # if studentData['label'] in data['label']:
                    musterLabelListe = data['label'] if isinstance(data['label'], list) else [data['label']]
                    # studentLabelListe = studentData['label'] if isinstance(studentData['label'], list) else [studentData['label']]
                    if any(label == studentData['label'] for label in musterLabelListe):

                        musterLabels = [
                            muster_graph.nodes[n]['label'] if isinstance(muster_graph.nodes[n]['label'], list)
                            else [muster_graph.nodes[n]['label']]
                            for n in list(muster_graph.neighbors(node)) + list(muster_graph.predecessors(node))
                        ]
                        musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                        studentenNachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(studentNode)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(studentNode)]
                        )                    

                        # if any(muster == studentenNachbarn for muster in musterNachbarn):
                        if any(set(muster) == set(studentenNachbarn) for muster in musterNachbarn):


                            fehler["richtige_Knoten"].append(studentNode)
                            fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                        # if not any(muster == studentenNachbarn for muster in musterNachbarn): 
                        #     ############ SPÄTER ENTFERNEN WENN Nachbarn fehlen / zusätzlich sind? 
                        #     fehler['falsche_Nachbarn'].append(studentNode)
                        #     fehler_visualisierung['falsche_Nachbarn_blau'].append(f"   style {studentNode} fill:#d9eaf7,stroke:#045a8d,stroke-width:2px")

                elif data['type'] == 'Entität' and studentData['type'] == 'Entität' and node != studentNode:
                    # if studentNode not in fehler['richtige_Knoten']:
                        # if studentData['label'] not in data['label']: # wenn mögliche Lösung nicht in den Varianten der Musterlösung ist
                        musterLabelListe = data['label'] if isinstance(data['label'], list) else [data['label']]
                        # studentLabelListe = studentData['label'] if isinstance(studentData['label'], list) else [studentData['label']]
                        if not any(label == studentData['label'] for label in musterLabelListe):                          
                            musterLabels = [
                                muster_graph.nodes[n]['label'] if isinstance(muster_graph.nodes[n]['label'], list)
                                else [muster_graph.nodes[n]['label']]
                                for n in list(muster_graph.neighbors(node)) + list(muster_graph.predecessors(node))
                            ]
                            musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                            studentenNachbarn = sorted(
                                [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(studentNode)] +
                                [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(studentNode)]
                            )        
                            print(f"MusterNACHBARN: {musterNachbarn}")            
                            nicht_gefunden = set(map(str, studentenNachbarn)) - set(map(str, musterNachbarn))

                            # if any(muster == studentenNachbarn for muster in musterNachbarn):
                            #     print(studentNode, studentData) 
                            #     fehler["richtige_Knoten"].append(studentNode)
                            #     fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                            if len(nicht_gefunden) <= 2:  # Maximal ein/zwei/drei Nachbar unterscheidet sich (zwei damit mehr Fehler erkannt werden?)
                                fehler["falscher_Name_Knoten"].append(
                                    f"Muster: {node}, {data} Studentische Lösung: {studentNode}"
                                )
                                fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                    f"   style {studentNode} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                                )
                            for liste in musterNachbarn:
                                for nachbar in liste:
                                    if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(studentNode, nachbar): 
                                        muster_kard = muster_graph.get_edge_data(node, nachbar)
                                        studenten_kard = studenten_graph.get_edge_data(studentNode, nachbar)
                                        # if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                        if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and not any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            # ##################### TESTEN #####################    
                                            print(f"V1 {studentNode, nachbar}")                                
                                            fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            print(f"V2 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                            print(f"V3 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")  

                elif data['type'] == 'Relationship' and studentData['type'] == 'Relationship' and node == studentNode: 
                    # if studentData['label'] in data['label']:
                    # if studentData['label'] in data['label']:
                    musterLabelListe = data['label'] if isinstance(data['label'], list) else [data['label']]
                    # studentLabelListe = studentData['label'] if isinstance(studentData['label'], list) else [studentData['label']]
                    if any(label == studentData['label'] for label in musterLabelListe):
                        musterLabels = [
                            muster_graph.nodes[n]['label'] if isinstance(muster_graph.nodes[n]['label'], list)
                            else [muster_graph.nodes[n]['label']]
                            for n in list(muster_graph.neighbors(node)) + list(muster_graph.predecessors(node))
                        ]
                        musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                        studentenNachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(studentNode)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(studentNode)]
                        )                    
                        # if any(muster == studentenNachbarn for muster in musterNachbarn):
                        if any(set(muster) == set(studentenNachbarn) for muster in musterNachbarn):

                            fehler["richtige_Knoten"].append(studentNode)
                            fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                
                elif data['type'] == 'Relationship' and studentData['type'] == 'Relationship' and node != studentNode:
                    if studentNode not in fehler['richtige_Knoten']:
                        # if studentData['label'] not in data['label']: # wenn mögliche Lösung nicht in den Varianten der Musterlösung ist
                        musterLabelListe = data['label'] if isinstance(data['label'], list) else [data['label']]
                        # studentLabelListe = studentData['label'] if isinstance(studentData['label'], list) else [studentData['label']]
                        if not any(label == studentData['label'] for label in musterLabelListe):
                            musterLabels = [
                                muster_graph.nodes[n]['label'] if isinstance(muster_graph.nodes[n]['label'], list)
                                else [muster_graph.nodes[n]['label']]
                                for n in list(muster_graph.neighbors(node)) + list(muster_graph.predecessors(node))
                            ]
                            musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                            studentenNachbarn = sorted(
                                [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(studentNode)] +
                                [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(studentNode)]
                            )                    
                            nicht_gefunden = set(map(str, studentenNachbarn)) - set(map(str, musterNachbarn))

                            # # if any(muster == studentenNachbarn for muster in musterNachbarn):
                            # if any(set(muster) == set(studentenNachbarn) for muster in musterNachbarn):
                            #     print(studentNode, studentData) 
                            #     fehler["richtige_Knoten"].append(studentNode)
                            #     fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                            if len(nicht_gefunden) <= 3:  # Maximal ein/zwei/drei Nachbar unterscheidet sich (zwei damit mehr Fehler erkannt werden?)
                                fehler["falscher_Name_Knoten"].append(
                                    f"Muster: {node}, {data} Studentische Lösung: {studentNode}"
                                )
                                fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                    f"   style {studentNode} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                                )
                            # print(f"Musternachbarn: {musterNachbarn}")
                            for liste in musterNachbarn:
                                
                                for nachbar in liste:
                                    if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(studentNode, nachbar): 
                                        muster_kard = muster_graph.get_edge_data(node, nachbar)
                                        studenten_kard = studenten_graph.get_edge_data(studentNode, nachbar)
                                        # if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                        if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and not any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            # ##################### TESTEN #####################    
                                            print(f"V1 {studentNode, nachbar} und {node, nachbar}")                                
                                            fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            print(f"V2 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                            print(f"V3 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")  



                elif data['type'] == 'Attribut' and studentData['type'] == 'Attribut' or data['type'] == 'zusammengesetztes Attribut' and studentData['type'] == 'zusammengesetztes Attribut' or data['type'] == 'Primärschlüssel-Attribut' and studentData['type'] == 'Primärschlüssel-Attribut' or data['type'] == 'mehrwertiges Attribut' and studentData['type'] == 'mehrwertiges Attribut' and node == studentNode: 
                    # if studentData['label'] in data['label']:
                    musterLabelListe = data['label'] if isinstance(data['label'], list) else [data['label']]
                    # studentLabelListe = studentData['label'] if isinstance(studentData['label'], list) else [studentData['label']]
                    if any(label == studentData['label'] for label in musterLabelListe):
                        musterLabels = [
                            muster_graph.nodes[n]['label'] if isinstance(muster_graph.nodes[n]['label'], list)
                            else [muster_graph.nodes[n]['label']]
                            for n in list(muster_graph.neighbors(node)) + list(muster_graph.predecessors(node))
                        ]
                        musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                        studentenNachbarn = sorted(
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(studentNode)] +
                            [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(studentNode)]
                        )                    
                        # if any(muster == studentenNachbarn for muster in musterNachbarn):
                        if any(set(muster) == set(studentenNachbarn) for muster in musterNachbarn):

                            fehler["richtige_Knoten"].append(studentNode)
                            fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                
                elif data['type'] == 'Attribut' and studentData['type'] == 'Attribut' or data['type'] == 'zusammengesetztes Attribut' and studentData['type'] == 'zusammengesetztes Attribut' or data['type'] == 'Primärschlüssel-Attribut' and studentData['type'] == 'Primärschlüssel-Attribut' or data['type'] == 'mehrwertiges Attribut' and studentData['type'] == 'mehrwertiges Attribut' and node != studentNode:
                    if studentNode not in fehler['richtige_Knoten']:
                        # if studentData['label'] not in data['label']: # wenn mögliche Lösung nicht in den Varianten der Musterlösung ist
                        musterLabelListe = data['label'] if isinstance(data['label'], list) else [data['label']]
                        # studentLabelListe = studentData['label'] if isinstance(studentData['label'], list) else [studentData['label']]
                        if not any(label == studentData['label'] for label in musterLabelListe):
                            musterLabels = [
                                muster_graph.nodes[n]['label'] if isinstance(muster_graph.nodes[n]['label'], list)
                                else [muster_graph.nodes[n]['label']]
                                for n in list(muster_graph.neighbors(node)) + list(muster_graph.predecessors(node))
                            ]
                            musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                            studentenNachbarn = sorted(
                                [studenten_graph.nodes[n]['label'] for n in studenten_graph.neighbors(studentNode)] +
                                [studenten_graph.nodes[n]['label'] for n in studenten_graph.predecessors(studentNode)]
                            )                    
                            nicht_gefunden = set(map(str, studentenNachbarn)) - set(map(str, musterNachbarn))

                            # if any(muster == studentenNachbarn for muster in musterNachbarn):
                            #     print(studentNode, studentData) 
                            #     fehler["richtige_Knoten"].append(studentNode)
                            #     fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
                            if len(nicht_gefunden) <= 3:  # Maximal ein/zwei/drei Nachbar unterscheidet sich (zwei damit mehr Fehler erkannt werden?)
                                fehler["falscher_Name_Knoten"].append(
                                    f"Muster: {node}, {data} Studentische Lösung: {studentNode}"
                                )
                                fehler_visualisierung["falscher_Name_Knoten_rot"].append(
                                    f"   style {studentNode} fill:#F4CCCC,stroke:#F4CCCC,color:#CC0000,stroke-width:2px,font-weight:bold;"
                                )
                            for liste in musterNachbarn:
                                for nachbar in liste:
                                    if muster_graph.has_edge(node, nachbar) and studenten_graph.has_edge(studentNode, nachbar): 
                                        muster_kard = muster_graph.get_edge_data(node, nachbar)
                                        studenten_kard = studenten_graph.get_edge_data(studentNode, nachbar)
                                        # if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                        if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and not any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            # ##################### TESTEN #####################    
                                            print(f"V1 {studentNode, nachbar}")                                
                                            fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            print(f"V2 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                            print(f"V3 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")  
                                    
                                    elif muster_graph.has_edge(nachbar, node) and studenten_graph.has_edge(nachbar, studentNode):
                                        muster_kard = muster_graph.get_edge_data(nachbar, node)
                                        studenten_kard = studenten_graph.get_edge_data(nachbar, studentNode)
                                        # if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and muster_kard.get("Kardinalität") != studenten_kard.get("Kardinalität"): 
                                        if muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and not any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            # ##################### TESTEN #####################    
                                            print(f"V1 {studentNode, nachbar}")                                
                                            fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studenten_kard.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is not None and studenten_kard.get("Kardinalität") is not None and any(k in studenten_kard.get("Kardinalität") for k in muster_kard.get("Kardinalität")): 
                                            print(f"V2 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")
                                        elif muster_kard.get('Beziehung') == studenten_kard.get('Beziehung') and muster_kard.get("Kardinalität") is None and studenten_kard.get("Kardinalität") is None: 
                                            print(f"V3 {studentNode, nachbar}")
                                            fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studenten_kard.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")  
                                    
                
                # elif studentNode not in 

            # else: 
            #     print(node, data)
            #     print(studentNode, studentData)

            ########## STROKE für mehrwertige Attribute weiterhin grün,sodass man die doppelten Umrandungen sieht
            # elif data['type'] == 'schwache Entität' and studentData['type'] == 'schwache Entität' and node == studentNode: 
            #     if studentData['label'] in data['label']:
            #         fehler["richtige_Knoten"].append(studentNode)
            #         fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
            # elif data['type'] == 'IS-A-Element' and studentData['type'] == 'IS-A-Element' and node == studentNode: 
            #     if studentData['label'] in data['label']:
            #         fehler["richtige_Knoten"].append(studentNode)
            #         fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#d4edda,stroke-width:2px")
    
    ######################## Falsche Elemente identifizieren
            


    feedback = visualisieren(fehler_visualisierung, studentische_loesung)
    return feedback

# Visualieren des Feedbakcs (Hinzufügen zu der studentischen Lösung)
def visualisieren(fehler, studentische_loesung):
    for x in fehler:
        for y in  fehler[x]:
            if y not in studentische_loesung: 
                studentische_loesung = studentische_loesung + f"\n {y}"
        
    return studentische_loesung

ergebnis = compare_graphs(muster_graph, studenten_graph)
# print(ergebnis)