import re 
import networkx as nx 

def parse_solution(mermaid_text):
    regex_muster_knoten = [
    r"([a-zA-ZäöüÄÖÜß0-9_|]+)---([a-zA-ZäöüÄÖÜß0-9_]+)\(\[\"`?<ins>([a-zA-ZäöüÄÖÜß0-9_|]+)<\/ins>`?\"\]\)",  # Mit <ins>-Tags - Primärschlüssel
    r"([a-zA-ZäöüÄÖÜß0-9_|]+)---([a-zA-ZäöüÄÖÜß0-9_]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|]+)\]\)",                      # Ohne Tags - normales Attribut
    r"([a-zA-ZäöüÄÖÜß0-9_|]+)---([a-zA-ZäöüÄÖÜß0-9_]+)\(\(\(([a-zA-ZäöüÄÖÜß0-9_|]+)\)\)\)"                   # Verschachtelte Klammern - mehrwertiges Attribut
    ]
    regex_muster_kanten = [
    r"([a-zA-ZäöüÄÖÜß0-9_|]+)\{([a-zA-ZäöüÄÖÜß0-9_|]+)\}--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|]+)", # Relationship{}--()---Entität
    r"([a-zA-ZäöüÄÖÜß0-9_|]+)--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_]+)\{([a-zA-ZäöüÄÖÜß0-9_|]+)\}", # Entität--()---Relationship{}
    r"([a-zA-ZäöüÄÖÜß0-9_|]+)\{([a-zA-ZäöüÄÖÜß0-9_|]+)\}---([a-zA-ZäöüÄÖÜß0-9_]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|]+)\]\)"                  # Relationship{}---Attribut([])
    ]
    regex_zusammengesetztes_atrribut = r"(\w+)\(\[([^\[\]]+(?:\|[^\[\]]+)*)\]\)---(\w+)\(\[([^\[\]]+(?:\|[^\[\]]+)*)\]\)" # für Attribute die Atrribute enthalten
    regex_schwache_entitaeten = [
        r"" # SchwacheEntität[[]]---Entität
        r"" # Entität---SchwacheEntität[[]]
        r"" # SchwacheEntität[[]]---Attribut
        r"" # SchwacheEntität[[]]---Relationship{}
    ] # schwache Enitäten 
    regex_is_a = [
        r""
    ] # Darstellungselement Is-A 

    graph = nx.DiGraph()
    lines = mermaid_text.split("\n")
    global counter_kanten 
    global syntaxFehlerListe
    syntaxFehlerListe = []
    counter_kanten = 0
    for line in lines: 
        # Hinzufügen der Knoten
        for muster in regex_muster_knoten:

            ### Zeilen mit Attributen hinzufügen
            matches = re.findall(muster, line)
            for entitaet, attribut_id, attribut_name in matches:
                entitaetListe = entitaet.split("|")
                graph.add_node(entitaetListe[0], type="Entität", label=entitaetListe)
                if muster == regex_muster_knoten[0]:
                    attribut_liste = attribut_name.split("|")
                    graph.add_node(attribut_id, type="Primärschlüssel-Attribut", label=attribut_liste)
                    graph.add_edge(entitaetListe[0], attribut_id, Beziehung="hat Primärschlüssel-Attribut", Nummer=counter_kanten)
                    counter_kanten = counter_kanten + 1
                elif muster == regex_muster_knoten[1]: 
                    attribut_liste = attribut_name.split("|")
                    graph.add_node(attribut_id, type="Attribut", label=attribut_liste)
                    graph.add_edge(entitaetListe[0], attribut_id, Beziehung="hat Attribut", Nummer=counter_kanten)
                    counter_kanten = counter_kanten + 1
                elif muster == regex_muster_knoten[2]: 
                    attribut_liste = attribut_name.split("|")
                    graph.add_node(attribut_id, type="mehrwertiges Attribut", label=attribut_liste)
                    graph.add_edge(entitaetListe[0], attribut_id, Beziehung="hat mehrwertiges Attribut", Nummer=counter_kanten)
                    counter_kanten = counter_kanten + 1

        # Zeile mit zusammmengesetzten Attribut hinzufügen
        matches = re.findall(regex_zusammengesetztes_atrribut, line)
        for attribut_zusammengesetzt_id, attribut_zusammengesetzt_name, attribut_id, attribut_name in matches: # überschreiben des Typs des zusammengesetzten Attributes, Label bleibt gleich
            attributZusammengesetztListe = attribut_zusammengesetzt_name.split("|")
            attributListe = attribut_name.split("|")
            graph.add_node(attribut_zusammengesetzt_id, type="zusammengesetztes Attribut", label=attributZusammengesetztListe)
            graph.add_node(attribut_id, type="Attribut", label=attributListe)
            graph.add_edge(attribut_zusammengesetzt_id, attribut_id, Beziehung="hat Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
            # print(counter_kanten)

        # Zeilen mit Ralationships hinzufügen
        matches = re.findall(regex_muster_kanten[0], line) 
        for relationship,relation_name, cardinalitaet, entitaet in matches: 
            relationshipListe = relationship_name.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            entitaetListe = entitaet.split("|")
            graph.add_node(relationship, type="Relationship", label=relationshipListe),
            graph.add_edge(relationship, entitaetListe[0],Beziehung="Relationship-Entität", Kardinalität=cardinalitaetListe, Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        
        matches = re.findall(regex_muster_kanten[1], line)
        for entitaet, cardinalitaet, relationship, relationship_name in matches: 
            entitaetListe = entitaet.split("|")
            relationshipListe = relationship_name.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            graph.add_node(relationship, type="Relationship", label=relationshipListe),
            graph.add_edge(entitaetListe[0], relationship, Beziehung="Entität-Relationship", Kardinalität=cardinalitaetListe, Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_muster_kanten[2], line)
        for relationship, relation_name, attribut_id, attribut_name in matches: 
            attributListe = attribut_name.split("|")
            graph.add_node(attribut_id, type="Attribut", label=attributListe)
            graph.add_edge(relationship, attribut_id, Beziehung="Relationship-Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        

    ########### RETURN um syntaxFehlerListe erweitern
    return graph

    
mermaid_text =  """mermaid
flowchart
    subgraph SG1 [ ]
        Produzent|Test---P1(["`<ins>ProdId|Test</ins>`"])
        Produzent|Test---P3(((Zertifikate|Test)))
    end
    subgraph SG2 [ ]
        Bauteil|Test---B1(["`<ins>Name|name|test|</ins>`"])
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe|Test])
        Bauteil---B7([Farbe])
        B3([Größe|Test])---B4([Länge|Test])
        B3([Größe|Test])---B5([Breite|Test])
        B3([Größe|Test])---B6([Höhe|Test])
    end
    subgraph SG3 [ ]
        Produzent|Test--(1,*|1,2)---bauen{bauen|herstellen}
        bauen{bauen|herstellen}--(1,1)---Bauteil 
        bauen{bauen|herstellen}---H1([Jahr|Test])
        Bauteil--(2,3)---bestehen_aus{bestehen_aus|Test}
        bestehen_aus{bestehen_aus|Test}--(0,*)---Bauteil
    end    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
"""


# graph = parse_solution(mermaid_text)
# print("Knoten:")
# for node, data in graph.nodes(data=True):
#     print(node, data)

# print("\nKanten:")
# for u, v, data in graph.edges(data=True):
#     print(u, v, data)
# print(graph)