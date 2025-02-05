from parse_into_graph import parse_mermaid_text
from solution_parser import parse_solution
import networkx as nx 
from itertools import product


##################### PREPARING ######################
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
        B3([Größe])---B4([ae])
        B3([Größe])---B5([Breite])
        B3([Größe])---B6([Hoehe])
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
        Produzent---P3(((Certificate)))
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
        bauen{bauen}--(2,2)---Bauteil
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

#################### MATCHER #########################

# print(dict(muster_graph.nodes(data=True)))

####################### FEHLERÜBERSICHT #################
global fehler 
fehler = {
# Fehler bei Knoten
    "richtige_Knoten": [],
    "falsche_Nachbarn": [],
    "fehlende_Knoten": [],
    "extra_Knoten": [],
    "falscher_Typ_Knoten": [], #typabweichung
    "falscher_Name_Knoten":[], # label
    "helper-liste-falscher-Name": [], # liste mit falschen Namen und "richtigem" Namen / ID
    "falscher_Knoten": [], # weder label, type noch Nachbarn stimmen
    "NichteinhaltungERM-Regeln": [],
# Fehler bei Kanten
    "fehlende_Kanten": [],
    "extra_Kanten": [],
    "falsche_Kanten": [] # Kardinalität, Beziehung?

}

fehler_visualisierung= {
    "richtige_Knoten": [],
    "falsche_Nachbarn_gelb": [],
    "fehlende_Knoten_Info": [],
    "extra_Knoten_gelb": [],
    "falscher_Typ_Knoten_rot": [],
    "falscher_Name_Knoten_rot": [],
    "falscher_Knoten_rot": [],
    "NichteinhaltungERM-Regeln_Info": [],
# Kanten
    "fehlende_Kanten_Info": [],
    "extra_Kanten_gelb": [],
    "falsche_Kanten_rot": [],
    "richtige_Kanten_grün": []
    
}
###################### FEHLER TEMPLATES #############################

# richtigeKnotenGRÜN = f"   style {studentNode} fill:#d4edda,stroke:#5a8f66,stroke-width:2px"
# faslcheNachbarnGELB = f"   style {studentNode} fill:#FFD966,stroke:#FFD966,stroke-width:2px"
# fehlendeKnotenINFO = 
# extraKnotenBLAU = 
# falscherNameKnotenROT = f"   style {studentNode} color:#CC0000,stroke-width:2px,font-weight:bold"
# falscherTypKnotenROT = 
# falscherKnotenROT = f"   style {studentNode} fill:#F4CCCC,stroke:#CC0000,color:#CC0000,stroke-width:2px,font-weight:bold"

######################

def compare_graphs(musterGraph, studentenGraph, studentische_loesung):
    for studentNode, studentData in studentenGraph.nodes(data=True):
            if studentNode in fehler['richtige_Knoten']:
                continue
            if studentData['type'] == 'Entität':
                # ERM MODELLIERUNGS REGELN PRÜFEN 
                entitätenPrüfen(musterGraph, studentenGraph, studentNode, studentData)
                kardinalitätPrüfen(musterGraph, studentenGraph, studentNode, studentData)
            elif studentData['type'] == 'Relationship':
                relationshipsPrüfen(musterGraph, studentenGraph, studentNode, studentData)
                kardinalitätPrüfen(musterGraph, studentenGraph, studentNode, studentData)
            elif 'Attribut' in studentData['type']:
                attributePrüfen(musterGraph, studentenGraph, studentNode, studentData)

    if musterGraph.number_of_nodes() > studentenGraph.number_of_nodes(): 
        studentische_loesung = studentische_loesung + f"\n   fehlerFehlendeKnoten[Fehler: Es fehlen noch Enitäten, Attribute oder Relationships!] \n    style fehlerFehlendeKnoten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;"
    
    elif musterGraph.number_of_nodes() < studentenGraph.number_of_nodes():
        studentische_loesung = studentische_loesung + f"\n   fehlerExtraKnoten[Fehler: Es sind zusätzliche Enitäten, Attribute oder Relationships in deiner Lösung enthalten, die nicht im Muster sind!] \n    style fehlerFehlendeKnoten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p,font-weight:bold;"

    feedback = visualisieren(fehler_visualisierung, studentische_loesung)
    return feedback

def elementPrüfen(MGraph, SGraph, studentNode, studentData): 
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
        fehler_visualisierung["richtige_Knoten"].append(f"   style {studentNode} fill:#d4edda,stroke:#5a8f66,stroke-width:2px")
        return
    elif fehlerdict["falsche_Nachbarn"]:
        fehler_visualisierung["falsche_Nachbarn_gelb"].append(f"   style {studentNode} fill:#FFD966,stroke:#FFD966,stroke-width:2px")
        return
    elif fehlerdict["falscher_Name_Knoten"]: 
        fehler_visualisierung["falscher_Name_Knoten_rot"].append(f"   style {studentNode} color:#CC0000,stroke-width:2px,font-weight:bold")
        return
    elif fehlerdict['falscher_Typ_Knoten']: 
        fehler_visualisierung['falscher_Typ_Knoten_rot'].append(f"   style {studentNode} stroke:#CC0000,stroke-width:3px")
    elif fehlerdict["falscher_Knoten"]: 
        fehler_visualisierung["falscher_Knoten_rot"].append(f"   style {studentNode} fill:#F4CCCC,stroke:#CC0000,color:#CC0000,stroke-width:2px,font-weight:bold")
        return

def kardinalitätPrüfen(MGraph, SGraph, studentNode, studentData): 
    fehlerdict = {
        "richtigeKanten": [],
        "falscheKanten": []
    }
    for musterNode, musterData in MGraph.nodes(data=True):
        if musterData['type'] =='Entität' and studentData['type'] == 'Entität' or musterData['type'] == 'Relationship' and studentData['type'] == 'Relationship':
                studentenNachbarn = sorted(list(SGraph.neighbors(studentNode))) + sorted(list(SGraph.predecessors(studentNode)))
                musterLabels = [
                MGraph.nodes[n]['label'] if isinstance(MGraph.nodes[n]['label'], list)
                        else [MGraph.nodes[n]['label']]
                        for n in list(MGraph.neighbors(musterNode)) + list(MGraph.predecessors(musterNode))
                    ]
                ### product um alle Möglichen Kombinationen von Nachbarn zu berechnen
                musterNachbarn = sorted([list(combo) for combo in product(*musterLabels)])
                for liste in musterNachbarn: 
                    for nachbar in liste: 
                        if MGraph.has_edge(musterNode, nachbar) and SGraph.has_edge(studentNode, nachbar):
                            musterEdgeData = MGraph.get_edge_data(musterNode, nachbar)
                            studentEdgeData = SGraph.get_edge_data(studentNode, nachbar)
                            # print(musterNode, nachbar, musterEdgeData)
                            # print(studentNode, nachbar, studentEdgeData)
                            if musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and not any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                fehlerdict['falscheKanten'].append( studentEdgeData.get('Nummer'))
                                # fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studentEdgeData.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                            elif musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                fehlerdict['richtigeKanten'].append(studentEdgeData.get('Nummer'))
                                # fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studentEdgeData.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")                            
                        elif MGraph.has_edge(nachbar, musterNode) and SGraph.has_edge(nachbar, studentNode):
                            musterEdgeData = MGraph.get_edge_data(nachbar, musterNode)
                            studentEdgeData = SGraph.get_edge_data(nachbar, studentNode)
                            if musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and not any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                fehlerdict['falscheKanten'].append(studentEdgeData.get('Nummer'))
                                # fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {studentEdgeData.get('Nummer')} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")
                            elif musterEdgeData.get('Kardinalität') is not None and studentEdgeData.get('Kardinalität') is not None and any(k in studentEdgeData.get("Kardinalität") for k in musterEdgeData.get("Kardinalität")):
                                fehlerdict['richtigeKanten'].append(studentEdgeData.get('Nummer'))
                                # fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {studentEdgeData.get('Nummer')} color:#2ca02c,stroke:#d4edda,stroke-width:2px;")  
                # for nachbarn in studentenNachbarn: 
            #     if SGraph.has_edge(studentNode)
    for number in fehlerdict['richtigeKanten']: 
        if number in fehlerdict['falscheKanten']: 
            fehlerdict['falscheKanten'].remove(number)
    if fehlerdict['richtigeKanten']: 
        for number in fehlerdict['richtigeKanten']: 
            if number not in fehler_visualisierung['richtige_Kanten_grün']:
                fehler_visualisierung["richtige_Kanten_grün"].append(f"   linkStyle {number} color:#2ca02c,stroke:#d4edda,stroke-width:4px;")
    if fehlerdict['falscheKanten']: 
        for number in fehlerdict['falscheKanten']: 
            if number not in fehler_visualisierung['falsche_Kanten_rot'] and number not in fehler_visualisierung['richtige_Kanten_grün']:
                fehler_visualisierung["falsche_Kanten_rot"].append(f"   linkStyle {number} stroke:#d62728,stroke-width:4px,color:#d62728,fill:none;")



def entitätenPrüfen(MGraph, SGraph, studentNode, studentData):
    # Übersicht der Nachbarn erstellen (hier sind labels egal da ich auf type prüfe)
    studentenNachbarn = sorted(list(SGraph.neighbors(studentNode))) + sorted(list(SGraph.predecessors(studentNode)))
    anzahlPrimärschlüssel = 0 # es darf nur ein Primärschlüssel geben
    booleanEntitäten = False # es darf keine andere Entität geben
    for nachbar in studentenNachbarn: 
        if SGraph.nodes[nachbar]['type'] == 'Primärschlüssel-Attribut': 
            anzahlPrimärschlüssel += 1 
        if SGraph.nodes[nachbar]['type'] == 'Entität': 
            booleanEntitäten = True
    if anzahlPrimärschlüssel == 1 and booleanEntitäten == False: 
        # elementPrüfen(MGraph, musterNode, musterData, SGraph, studentNode, studentData)
        elementPrüfen(MGraph, SGraph, studentNode, studentData)
    else: 
        fehler["NichteinhaltungERM-Regeln"].append(studentNode)
        fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append('FEHLERMELDUNG') ########## HINZUFÜGEN


def relationshipsPrüfen(MGraph, SGraph, studentNode, studentData):
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
        # elementPrüfen(MGraph, musterNode, musterData, SGraph, studentNode, studentData)
        elementPrüfen(MGraph, SGraph, studentNode, studentData)

    else: 
        fehler["NichteinhaltungERM-Regeln"].append(studentNode)
        fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append('FEHLERMELDUNG') ########## HINZUFÜGEN


def attributePrüfen(MGraph, SGraph, studentNode, studentData): 
    studentenNachbarn = sorted(list(SGraph.neighbors(studentNode))) + sorted(list(SGraph.predecessors(studentNode)))
    if studentData['type'] == 'Attribut' or studentData['type'] == 'mehrwertiges Attribut': 
        # Attribut kann nur an einem Element liegen (nicht an Attribut und auch nicht an mehrwertiges Attribut und auch nicht Primärschlüssel)
        for nachbar in studentenNachbarn: 
            if len(studentenNachbarn) == 1 and SGraph.nodes[nachbar]['type'] != 'Attribut' and SGraph.nodes[nachbar]['type'] != 'mehrwertiges Attribut' and SGraph.nodes[nachbar]['type'] != 'Primärschlüssel-Attribut': 
                # elementPrüfen(MGraph, musterNode, musterData, SGraph, studentNode, studentData)
                elementPrüfen(MGraph, SGraph, studentNode, studentData)

            else: 
                fehler["NichteinhaltungERM-Regeln"].append(studentNode)
                fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append('FEHLERMELDUNG') ########## HINZUFÜGEN
    elif studentData['type'] == 'Primärschlüssel-Attribut':
        # Attribut darf nur an einer Entität oder einer zusammengesetztes Attribut liegen und nur einen Nachbarn haben
        for nachbar in studentenNachbarn:  
            if SGraph.nodes[nachbar]['type'] == 'Entität' or SGraph.nodes[nachbar]['type'] == 'zusammengesetztes Attribut' and len(studentenNachbarn) == 1: 
                # elementPrüfen(MGraph, musterNode, musterData, SGraph, studentNode, studentData)
                elementPrüfen(MGraph, SGraph, studentNode, studentData)

            else: 
                fehler["NichteinhaltungERM-Regeln"].append(studentNode)
                fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append('FEHLERMELDUNG') ########## HINZUFÜGEN         
    elif studentData['type'] == 'zusammengesetztes Attribut':
        # Attribut kann mehrere Attribute enthalten (aber nur normale?)
        # anzahlPrimärschlüssel = 0 # not needed 
        anzahlMehrwertigeAttribute = False
        anzahlZusammengesetztesAttribut = False
        for nachbar in studentenNachbarn: 
            # if SGraph.nodes[nachbar]['type'] == 'Primärschlüssel-Attribut':  # kann auch Primärschlüssel enthalten
            #     anzahlPrimärschlüssel += 1 
            if SGraph.nodes[nachbar]['type'] == 'zusammengesetztes Attribut':
                anzahlMehrwertigeAttribute += 1
            elif SGraph.nodes[nachbar]['type'] == 'mehrwertiges Attribut':    
                anzahlZusammengesetztesAttribut += 1
        # if anzahlPrimärschlüssel == 0 and anzahlMehrwertigeAttribute == 0 and anzahlZusammengesetztesAttribut == 0: 
        if anzahlMehrwertigeAttribute == 0 and anzahlZusammengesetztesAttribut == 0: 
            # elementPrüfen(MGraph, musterNode, musterData, SGraph, studentNode, studentData)
            elementPrüfen(MGraph, SGraph, studentNode, studentData)

        else: 
            fehler["NichteinhaltungERM-Regeln"].append(studentNode)
            fehler_visualisierung["NichteinhaltungERM-Regeln_Info"].append('FEHLERMELDUNG') ########## HINZUFÜGEN

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
        fehlendeElemente = set(map(str, liste)) - set(map(str, studentenNachbarn)) # Fehlen Elemente aus Muster un Studentenlösung
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

ergebnis = compare_graphs(muster_graph, studenten_graph, studentische_loesung)
print(ergebnis)