import networkx as nx 
from itertools import product


####################### FEHLERÜBERSICHT ######################
####################### FEHLER TEMPLATES #####################

# richtigeKnotenGRÜN = f"   style {studentNode} fill:#d4edda,stroke:#5a8f66,stroke-width:2px"
# falscheNachbarnGELB = f"   style {studentNode} fill:#FFD966,stroke:#FFD966,stroke-width:2px"
# fehlendeKnotenINFO = 
# falscherNameKnotenROT = f"   style {studentNode} color:#CC0000,stroke-width:2px,font-weight:bold"
# falscherTypKnotenROT = 
# falscherKnotenROT = f"   style {studentNode} fill:#F4CCCC,stroke:#CC0000,color:#CC0000,stroke-width:2px,font-weight:bold"

############################# MATCHER ########################

def compare_graphs(musterGraph, studentenGraph, studentische_loesung):

################### Dictionary zum Debuggen  #################
    fehler = {
        "richtige_Knoten": [],
        "falsche_Nachbarn": [],
        "fehlende_Knoten": [],
        "extra_Knoten": [],
        "falscher_Typ_Knoten": [], 
        "falscher_Name_Knoten":[], 
        "helper-liste-falscher-Name": [], 
        "falscher_Knoten": [], 
        "NichteinhaltungERM-Regeln": [],
        "fehlende_Kanten": [],
        "extra_Kanten": [],
        "falsche_Kanten": [] 
    }
################### Dictionary zum Visualisieren  ############
    fehler_visualisierung= {
        "richtige_Knoten": [],
        "falsche_Nachbarn_gelb": [],
        "fehlende_Knoten_Info": [],
        "extra_Knoten_gelb": [],
        "falscher_Typ_Knoten_rot": [],
        "falscher_Name_Knoten_rot": [],
        "falscher_Knoten_rot": [],
        "NichteinhaltungERM-Regeln_Info": [],
        "fehlende_Kanten_Info": [],
        "extra_Kanten_gelb": [],
        "falsche_Kanten_rot": [],
        "richtige_Kanten_grün": []
    }
    for studentNode, studentData in studentenGraph.nodes(data=True):
            if studentNode in fehler['richtige_Knoten']:
                continue
            if studentData['type'] == 'Entität':
                # ERM-Modellierungsregeln und Knoten prüfen
                entitätenPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler, fehler_visualisierung)
                # Kardinalitäten prüfen
                kardinalitätPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler_visualisierung)
            elif studentData['type'] == 'Entität(Supertyp)':
                entitätenPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler, fehler_visualisierung)
                kardinalitätPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler_visualisierung)
            elif studentData['type'] == 'Entität(Subtyp)': 
                entitätenPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler, fehler_visualisierung)
                kardinalitätPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler_visualisierung)
            elif studentData['type'] == 'Relationship':
                relationshipsPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler, fehler_visualisierung)
                kardinalitätPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler_visualisierung)
            elif 'Attribut' in studentData['type']:
                attributePrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler, fehler_visualisierung)
                # Attribute haben keine Kardinalitäten, daher keine Überprüfung dieser
            elif studentData['type'] == "Schwache Entität": 
                entitätenPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler, fehler_visualisierung)
                kardinalitätPrüfen(musterGraph, studentenGraph, studentNode, studentData, fehler_visualisierung)

    if musterGraph.number_of_nodes() > studentenGraph.number_of_nodes(): 
        studentische_loesung = studentische_loesung + f"\n   fehlerFehlendeKnoten[Fehler: Es fehlen noch Enitäten, Attribute oder Relationships!] \n    style fehlerFehlendeKnoten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;"
    
    elif musterGraph.number_of_nodes() < studentenGraph.number_of_nodes():
        studentische_loesung = studentische_loesung + f"\n   fehlerExtraKnoten[Fehler: Es sind zusätzliche Enitäten, Attribute oder Relationships in deiner Lösung enthalten, die nicht im Muster sind!] \n    style fehlerFehlendeKnoten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;"

    feedback = visualisieren(fehler_visualisierung, studentische_loesung)
    return feedback

def elementPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung): 
    fehlerdict = {
        "richtige_Knoten": [],
        "falsche_Nachbarn": [],
        "falscher_Name_Knoten": [],
        "falscher_Typ_Knoten": [],
        "falscher_Knoten": []
    }
    for musterNode, musterData in MGraph.nodes(data=True):
    # keine Unterscheidung ob node == studentNode, da genau die gleichen Prüfungen gemacht werden
        if musterData['type'] == studentData['type']: 
            musterLabelListe = musterData['label'] if isinstance(musterData['label'], list) else [musterData['label']]
            if any(label == studentData['label'] for label in musterLabelListe):
                ### Wenn Prüfung True, dann stimmen type und label mit Musterlösung
                nachbarVergleich = nachbarnPrüfen(MGraph, musterNode, SGraph, studentNode)
                ## bei nachbarVergleich leer == alle Nachbarn richtig
                if nachbarVergleich: 
                    fehlerdict["richtige_Knoten"].append(studentNode)
                else: 
                    fehlerdict["falsche_Nachbarn"].append(studentNode)
            elif not any(label == studentData['label'] for label in musterLabelListe):
                nachbarVergleich = nachbarnPrüfen(MGraph, musterNode, SGraph, studentNode)
                if nachbarVergleich: 
                    fehlerdict["falscher_Name_Knoten"].append(studentNode)
                    fehler['helper-liste-falscher-Name'].append(f"{studentNode} gemeint: {musterNode}")
                else: 
                    fehlerdict["falscher_Knoten"].append(studentNode)
        elif musterData['type'] != studentData['type']: 
            musterLabelListe = musterData['label'] if isinstance(musterData['label'], list) else [musterData['label']]
            if any(label == studentData['label'] for label in musterLabelListe):
                ### Wenn Prüfung True, dann stimmen type und label mit Musterlösung
                nachbarVergleich = nachbarnPrüfen(MGraph, musterNode, SGraph, studentNode)
                ## bei nachbarVergleich leer == alle Nachbarn richtig
                if nachbarVergleich: 
                    fehlerdict['falscher_Typ_Knoten'].append(studentNode)
                else: 
                    fehlerdict['falscher_Knoten'].append(studentNode)
    if fehlerdict["richtige_Knoten"]: 
        fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} color:#000000,fill:#d4edda,stroke:#5a8f66,stroke-width:2px")
        return
    elif fehlerdict["falsche_Nachbarn"]:
        fehler_visualisierung["falsche_Nachbarn_gelb"].append(f"   style {studentNode} color:#000000,fill:#FFD966,stroke:#FFD966,stroke-width:2px")
        return
    elif fehlerdict["falscher_Name_Knoten"]: 
        fehler_visualisierung["falscher_Name_Knoten_rot"].append(f"   style {studentNode} color:#CC0000,stroke-width:2px,font-weight:bold")
        return
    elif fehlerdict['falscher_Typ_Knoten']: 
        fehler_visualisierung['falscher_Typ_Knoten_rot'].append(f"   style {studentNode} color:#000000,stroke:#CC0000,stroke-width:3px")
    elif fehlerdict["falscher_Knoten"]: 
        fehler_visualisierung["falscher_Knoten_rot"].append(f"   style {studentNode} fill:#F4CCCC,stroke:#CC0000,color:#000000,stroke-width:2px,font-weight:bold")
        return

def kardinalitätPrüfen(MGraph, SGraph, studentNode, studentData, fehler_visualisierung): 
    fehlerdict = {
        "richtigeKanten": [],
        "falscheKanten": []
    }
    
    for musterNode, musterData in MGraph.nodes(data=True):
        if musterData['type'] =='Entität' and studentData['type'] == 'Entität' or musterData['type'] == 'Relationship' and studentData['type'] == 'Relationship' or musterData['type'] =='Entität(Supertyp)' and studentData['type'] == 'Entität(Supertyp)' or musterData['type'] =='Entität(Subtyp)' and studentData['type'] == 'Entität(Subtyp)' or studentData['type'] == 'Schwache Entität' and musterData['type'] == 'Schwache Entität':
            # for musterNode in musterData['label']:
                studentenNachbarn = sorted(list(SGraph.neighbors(studentNode))) + sorted(list(SGraph.predecessors(studentNode)))
                musterNachbarnID = sorted(list(MGraph.neighbors(musterNode))) + sorted(list(MGraph.predecessors(musterNode)))
                studentLabels = [
                SGraph.nodes[n]['label']
                        for n in list(SGraph.neighbors(studentNode)) + list(SGraph.predecessors(studentNode))
                    ]
                musterLabels = [
                MGraph.nodes[n]['label'] if isinstance(MGraph.nodes[n]['label'], list)
                        else [MGraph.nodes[n]['label']]
                        for n in list(MGraph.neighbors(musterNode)) + list(MGraph.predecessors(musterNode))
                    ]
                ### product um alle Möglichen Kombinationen von Nachbarn zu berechnen
                musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                for liste in musterNachbarn: 
                    if liste == studentLabels:
                        helperDict = { musterNachbarnID[i]: liste[i] for i in range(len(musterNachbarnID))
                        }    
                        helperCounter = 0
                        for nachbarID, nachbarName in helperDict.items(): 
                            if MGraph.has_edge(musterNode, nachbarID) and SGraph.has_edge(studentNode, studentenNachbarn[helperCounter]):
                                musterEdgeData = MGraph.get_edge_data(musterNode, nachbarID)
                                studentEdgeData = SGraph.get_edge_data(studentNode, studentenNachbarn[helperCounter])
                                if musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and not any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                    fehlerdict['falscheKanten'].append( studentEdgeData.get('Nummer'))
                                elif musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                    fehlerdict['richtigeKanten'].append(studentEdgeData.get('Nummer'))
                            elif MGraph.has_edge(nachbarID, musterNode) and SGraph.has_edge(studentenNachbarn[helperCounter], studentNode):
                                musterEdgeData = MGraph.get_edge_data(nachbarID, musterNode)
                                studentEdgeData = SGraph.get_edge_data(studentenNachbarn[helperCounter], studentNode)
                                if musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and not any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                    fehlerdict['falscheKanten'].append( studentEdgeData.get('Nummer'))
                                elif musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                    fehlerdict['richtigeKanten'].append(studentEdgeData.get('Nummer'))
                            helperCounter += 1
    if fehlerdict['richtigeKanten']: 
        for number in fehlerdict['richtigeKanten']:
            vorhandeneFehler =  [fehler.split()[1] for fehler in fehler_visualisierung["richtige_Kanten_grün"]]
            if str(number) not in vorhandeneFehler:
                fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {number} color:#2ca02c,stroke:#d4edda,stroke-width:4px;")
    if fehlerdict['falscheKanten']: 
        for number in fehlerdict['falscheKanten']: 
            vorhandeneFehlerRichtig = [fehler.split()[1] for fehler in fehler_visualisierung["richtige_Kanten_grün"]]
            vorhandeneFehlerFalsch = [fehler.split()[1] for fehler in fehler_visualisierung["falsche_Kanten_rot"]]
            if str(number) not in vorhandeneFehlerFalsch and str(number) not in vorhandeneFehlerRichtig:
                fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {number} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")

def entitätenPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung):
    # Übersicht der Nachbarn erstellen (hier sind labels egal da ich auf type prüfe)
    studentenNachbarn = sorted(list(SGraph.neighbors(studentNode))) + sorted(list(SGraph.predecessors(studentNode)))
    anzahlPrimärschlüssel = 0 # es darf nur ein Primärschlüssel geben
    booleanEntitäten = False # es darf keine andere Entität geben
    anzahlSupertypen = 0 # es darf nur einen Supertyp als Nachbarn geben
    for nachbar in studentenNachbarn: 
        if SGraph.nodes[nachbar]['type'] == 'Primärschlüssel-Attribut': 
            anzahlPrimärschlüssel += 1 
        if SGraph.nodes[nachbar]['type'] == 'Entität' or SGraph.nodes[nachbar]['type'] == 'Schwache Entität': # schwache Entitäten sind über ein Relationship gebunden
            booleanEntitäten = True
        if SGraph.nodes[studentNode]['type'] == "Entität(Subtyp)" and SGraph.nodes[nachbar]['type'] == 'Entität(Supertyp)':
            anzahlSupertypen += 1
    if anzahlPrimärschlüssel == 1 and booleanEntitäten == False and (anzahlSupertypen == 0 or anzahlSupertypen == 1): 
        elementPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung)
    else: 
        fehler["NichteinhaltungERM-Regeln"].append(studentNode)
        fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append(f"   style {studentNode} fill:#FFD966,stroke:#FFA500,stroke-width:2px") ########## HINZUFÜGEN


def relationshipsPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung):
    # Übersicht der Nachbarn 
    studentenNachbarn = sorted(list(SGraph.neighbors(studentNode))) + sorted(list(SGraph.predecessors(studentNode)))
    anzahlPrimärschlüssel = 0 # es darf keine primärschlüssel-attribute besitzen
    anzahlZusammengesetzteAttribute = 0 # es darf kein zusammengesetztes attribut besitzen
    booleanRelationships = False # es darf keine verbindung zu anderen relationships haben
    for nachbar in studentenNachbarn: 
        if SGraph.nodes[nachbar]['type'] == 'Primärschlüssel-Attribut': 
            anzahlPrimärschlüssel += 1 
        elif SGraph.nodes[nachbar]['type'] == 'zusammengesetztes Attribut':
            anzahlZusammengesetzteAttribute += 1
        elif SGraph.nodes[nachbar]['type'] == 'Relationship': 
            booleanRelationships = True
    if anzahlPrimärschlüssel == 0 and anzahlZusammengesetzteAttribute == 0 and booleanRelationships == False: 
        elementPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung)

    else: 
        fehler["NichteinhaltungERM-Regeln"].append(studentNode)
        fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append(f"   style {studentNode} fill:#FFD966,stroke:#FFA500,stroke-width:2px") ########## HINZUFÜGEN


def attributePrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung): 
    studentenNachbarn = sorted(list(SGraph.neighbors(studentNode))) + sorted(list(SGraph.predecessors(studentNode)))
    if studentData['type'] == 'Attribut' or studentData['type'] == 'mehrwertiges Attribut': 
        # Attribut kann nur an einem Element liegen (nicht an Attribut und auch nicht an mehrwertiges Attribut und auch nicht Primärschlüssel)
        for nachbar in studentenNachbarn: 
            if len(studentenNachbarn) == 1 and SGraph.nodes[nachbar]['type'] != 'Attribut' and SGraph.nodes[nachbar]['type'] != 'mehrwertiges Attribut' and SGraph.nodes[nachbar]['type'] != 'Primärschlüssel-Attribut': 
                elementPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung)

            else: 
                fehler["NichteinhaltungERM-Regeln"].append(studentNode)
                fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append(f"   style {studentNode} fill:#FFD966,stroke:#FFA500,stroke-width:2px") ########## HINZUFÜGEN
    elif studentData['type'] == 'Primärschlüssel-Attribut':
        # Attribut darf nur an einer Entität oder einer zusammengesetztes Attribut liegen und nur einen Nachbarn haben
        for nachbar in studentenNachbarn:  
            if SGraph.nodes[nachbar]['type'] == 'Entität' or SGraph.nodes[nachbar]['type'] == 'Schwache Entität' or SGraph.nodes[nachbar]['type'] == 'Entität(Supertyp)' or SGraph.nodes[nachbar]['type'] == 'Entität(Subtyp)' or SGraph.nodes[nachbar]['type'] == 'zusammengesetztes Attribut' and len(studentenNachbarn) == 1: 
                elementPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung)

            else: 
                fehler["NichteinhaltungERM-Regeln"].append(studentNode)
                fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append(f"   style {studentNode} fill:#FFD966,stroke:#FFA500,stroke-width:2px") ########## HINZUFÜGEN         
    elif studentData['type'] == 'zusammengesetztes Attribut':
        # Attribut kann mehrere Attribute enthalten
        anzahlMehrwertigeAttribute = 0
        anzahlZusammengesetztesAttribut = 0
        for nachbar in studentenNachbarn: 
            if SGraph.nodes[nachbar]['type'] == 'zusammengesetztes Attribut':
                anzahlMehrwertigeAttribute += 1
        if anzahlZusammengesetztesAttribut == 0: 
            elementPrüfen(MGraph, SGraph, studentNode, studentData, fehler, fehler_visualisierung)
        else: 
            fehler["NichteinhaltungERM-Regeln"].append(studentNode)
            fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append(f"   style {studentNode} fill:#FFD966,stroke:#FFA500,stroke-width:2px") ########## HINZUFÜGEN

def nachbarnPrüfen(MGraph, musterNode, SGraph, studentNode): 
    musterLabels = [
    MGraph.nodes[n]['label'] if isinstance(MGraph.nodes[n]['label'], list)
            else [MGraph.nodes[n]['label']]
            for n in list(MGraph.neighbors(musterNode)) + list(MGraph.predecessors(musterNode))
        ]
    ### product um alle Möglichen Kombinationen von Nachbarn zu berechnen
    musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
    studentenNachbarn = sorted(
            [SGraph.nodes[n]['label'] for n in SGraph.neighbors(studentNode)] +
            [SGraph.nodes[n]['label'] for n in SGraph.predecessors(studentNode)]
        )
    for liste in musterNachbarn: 
        nachbarVergleich = set(map(str, studentenNachbarn)) - set(map(str, liste)) # sind alle Elemente aus Studentenlösung auch in Muster
        fehlendeElemente = set(map(str, liste)) - set(map(str, studentenNachbarn)) # Fehlen Elemente aus Muster in der Studentenlösung
    # Prüfen, ob die Listen leer sind
        if not nachbarVergleich and not fehlendeElemente:  
            return True
    return False
    
# Visualieren des Feedbakcs (Hinzufügen zu der studentischen Lösung)
def visualisieren(fehler, studentische_loesung):
    for x in fehler:
        for y in  fehler[x]:
            if y not in studentische_loesung: 
                studentische_loesung = studentische_loesung + f"\n {y}"
        
    return studentische_loesung

######################### DEBUGGING ##########################
# import parse_into_graph 
# import solution_parser

student = """
mermaid
flowchart
    subgraph SG1 [ ]
        Anbieter---P1(["`<ins>AnbieterID</ins>`"])
        Anbieter---P2([Name])
        Anbieter---P3(((Nachweise)))
    end
    subgraph SG2 [ ]
        Bauteil---B1(["`<ins>Modell</ins>`"])
        Bauteil---B2([Masse])
        Bauteil---B3([Maße])
        B3([Maße])---B4([Länge])
        B3([Maße])---B5([Breite])
        B3([Maße])---B6([Standhöhe])
    end
    subgraph SG3 [ ]
        Anbieter--(1,*)---produzieren{produzieren}
        Bauteil--(1,*)---produzieren{produzieren}
        produzieren{produzieren}---H1([Produktionsjahr])
        Bauteil--(1,*)---enthält{enthält}
        enthält{enthält}--(1,*)---Bauteil
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    linkStyle default marker-end:none
    """
muster = """flowchart
    subgraph SG1 [ ]
        Produzent|Anbieter---P1(["`<ins>ProdId|AnbieterID</ins>`"])
        Produzent|Anbieter---P2([Name|Bezeichnung])
        Produzent|Anbieter---P3(((Zertifikate|Bescheinigungen|Nachweise)))
    end
    subgraph SG2 [ ]
        Bauteil|Komponente---B1(["`<ins>Name|Modell|Typ</ins>`"])
        Bauteil|Komponente---B2([Gewicht|Masse])
        Bauteil|Komponente---B3([Größe|Maße|Abmessungen])
        B3([Größe|Maße|Abmessungen])---B4([Länge])
        B3([Größe|Maße|Abmessungen])---B5([Breite])
        B3([Größe|Maße|Abmessungen])---B6([Höhe|Standhöhe])
    end
    subgraph SG3 [ ]
        Produzent|Anbieter--(1,*)---herstellen{herstellen|produzieren|fertigen}
        Bauteil|Komponente--(1,1|1,*)---herstellen{herstellen|produzieren|fertigen}
        herstellen{herstellen|produzieren|fertigen}---H1([Jahr|Produktionsjahr|Fertigungsjahr])
        Bauteil|Komponente--(0,*|1,*)---bestehen_aus{bestehen_aus|enthält|setzt_sich_zusammen_aus}
        bestehen_aus{bestehen_aus|enthält|setzt_sich_zusammen_aus}--(0,*|1,*)---Bauteil|Komponente
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    linkStyle default marker-end:none
"""
# ergebnis = compare_graphs(solution_parser.parse_solution(muster), parse_into_graph.parse_mermaid_text(student), student)
# graph = parse_into_graph.parse_mermaid_text(student) 
# graph = solution_parser.parse_solution(muster)
# print(ergebnis)
# print("Knoten:")
# for node, data in graph.nodes(data=True):
#     print(node, data)

# print("\nKanten:")
# for u, v, data in graph.edges(data=True):
#     print(u, v, data)
# print(graph)