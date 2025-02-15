import re 
import networkx as nx 

def parse_solution(mermaid_text):
    regex_muster_knoten = [
    r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\[\"`?<ins>([a-zA-ZäöüÄÖÜß0-9_|\-.]+)<\/ins>`?\"\]\)$",  # Mit <ins>-Tags - Primärschlüssel
    r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\)$",                      # Ohne Tags - normales Attribut
    r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\(\(([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\)\)\)$"                   # Verschachtelte Klammern - mehrwertiges Attribut
    ]
    regex_muster_kanten = [
    r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)$", # Relationship{}--()---Entität
    r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}$", # Entität--()---Relationship{}
    r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\)$"                  # Relationship{}---Attribut([])
    ]
    regex_zusammengesetztes_atrribut = r"(\w+)\(\[([^\[\]]+(?:\|[^\[\]]+)*)\]\)---(\w+)\(\[([^\[\]]+(?:\|[^\[\]]+)*)\]\)$" # für Attribute die Atrribute enthalten
    regex_schwache_entitaeten = [
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]---([a-zA-ZäöüÄÖÜß0-9_]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\)$", # SchwacheEntität[[]]---Attribut
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]---([a-zA-ZäöüÄÖÜß0-9_]+)\(\[\"`?<ins>([a-zA-ZäöüÄÖÜß0-9_|\-.]+)<\/ins>`?\"\]\)$", # SchwacheEntität[[]]---Primärschlüssel-Attribut
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]---([a-zA-ZäöüÄÖÜß0-9_]+)\(\(\(([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\)\)\)$", # SchwacheEntität[[]]---mehrwertiges Attribut
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}$", # SchwacheEntität[[]]---Relationship{}
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]$" # Relationship{}---SchwacheEntität
    ] # schwache Enitäten 
    regex_is_a = [
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---IS\-A\{\{IS\-A\}\}---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)$", # Subtyp---IS-A{{}}---Supertyp
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---IS\-A\{\{IS\-A\}\}$" # Subtyp---IS-A{{}}
    ]  

    graph = nx.DiGraph()
    lines = mermaid_text.split("\n")
    global counter_kanten 
    global syntaxFehlerListe
    syntaxFehlerListe = []
    counter_kanten = 0
    for line in lines: 
        # Hinzufügen der Knoten
        ## Zeilen mit IS-A Beziehung hinzufügen
        matches = re.findall(regex_is_a[0], line)
        for entitaetSubtyp, entitaetSupertyp in matches: 
            entitaetSubtypListe = entitaetSubtyp.split("|")
            entitaetSupertypListe = entitaetSupertyp.split("|")
            graph.add_node(entitaetSubtypListe[0], type="Entität(Subtyp)", label=entitaetSubtypListe)
            graph.add_node(entitaetSupertypListe[0], type="Entität(Supertyp)", label=entitaetSupertypListe)
            graph.add_edge(entitaetSubtypListe[0], entitaetSupertypListe[0], Beziehung="IS-A-Beziehung", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_is_a[1], line)
        for entitaetSubtyp in matches: 
            print(f"TESTESSSS {matches}")
            entitaetSubtypListe = entitaetSubtyp.split("|")
            graph.add_node(entitaetSubtypListe[0], type="Entität(Subtyp)", label=entitaetSubtypListe)
            graph.add_edge(entitaetSubtypListe[0], entitaetSupertypListe[0], Beziehung="IS-A-Beziehung", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        for muster in regex_muster_knoten:
            ### Zeilen mit Attributen hinzufügen
            matches = re.findall(muster, line)
            for entitaet, attribut_id, attribut_name in matches:
                entitaetListe = entitaet.split("|")
                if not graph.has_node(entitaetListe[0]):
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
        for relationship, relationship_name, cardinalitaet, entitaet in matches: 
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
        for relationship, relationship_name, attribut_id, attribut_name in matches: 
            attributListe = attribut_name.split("|")
            graph.add_node(attribut_id, type="Attribut", label=attributListe)
            graph.add_edge(relationship, attribut_id, Beziehung="Relationship-Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
    #### Zeilen mit schwachen Entitäten hinzufügen
        # matches = re.findall(regex_schwache_entitaeten[0], line)
        # for schwacheEntitaetID, schwacheEntitaet, entitaet in matches:
        #     schwacheEntitaetListe = schwacheEntitaet.split("|")
        #     entitaetListe = entitaet.split("|")
        #     graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaetListe)
        #     graph.add_edge(schwacheEntitaetID, entitaetListe[0], Beziehung="hat schwache Entität", Nummer=counter_kanten) 
        #     counter_kanten = counter_kanten + 1
        # matches = re.findall(regex_schwache_entitaeten[1], line)
        # for entitaet, schwacheEntitaetID, schwacheEntitaet in matches:
        #     schwacheEntitaetListe = schwacheEntitaet.split("|")
        #     entitaetListe = entitaet.split("|")
        #     graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaetListe)
        #     graph.add_edge(entitaetListe[0], schwacheEntitaetID, Beziehung="hat schwache Entität", Nummer=counter_kanten)
        #     counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[0], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            attributListe = attribut_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaetListe)
            graph.add_node(attribut_id, type="Attribut", label=schwacheEntitaetListe)
            graph.add_edge(schwacheEntitaetID, attribut_id, Beziehung="hat Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[1], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            attributListe = attribut_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaetListe)
            graph.add_node(attribut_id, type="Primärschlüssel-Attribut", label=schwacheEntitaetListe)
            graph.add_edge(schwacheEntitaetID, attribut_id, Beziehung="hat Primärschlüssel-Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[2], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            attributListe = attribut_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaetListe)
            graph.add_node(attribut_id, type="mehrwertiges Attribut", label=schwacheEntitaetListe)
            graph.add_edge(schwacheEntitaetID, attribut_id, Beziehung="hat mehrwertiges Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[3], line)
        for schwacheEntitaetID, schwacheEntitaet, cardinalitaet, relationship, relationship_name in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            relationshipListe = relationship_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaetListe)
            graph.add_node(relationship, type="Relationship", label=relationshipListe)
            graph.add_edge(schwacheEntitaetID, relationship, Beziehung="Schwache Entität-Relationship", Kardinalität=cardinalitaetListe, Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[4], line)
        for relationship, relationship_name, cardinalitaet,  schwacheEntitaetID, schwacheEntitaet in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            relationshipListe = relationship_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaetListe)
            graph.add_node(relationship, type="Relationship", label=relationshipListe)
            graph.add_edge(relationship,schwacheEntitaetID, Beziehung="Relationship-Schwache Entität", Kardinalität=cardinalitaetListe, Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1

    return graph

################## DEBUGGING ###################
 
mermaid_text =  """mermaid
flowchart 
    subgraph SG1 [ ]
        Land---A1(["`<ins>KFZ</ins>`"])
    end
    subgraph SG5 [ ]
        Land--(1,*)---liegt_in{liegt_in|liegt}
        Provinz[[Provinz]]--(1,1)---liegt_in{liegt_in|liegt}
    end
    subgraph SG2 [ ]
        Stadt[[Stadt]]---F1(["`<ins>Name</ins>`"])
        Stadt[[Stadt]]---F2([EWZ|Einwohnerzahl])
        Stadt[[Stadt]]---F3([Lage])
        F3([Lage])---F4([BG|Breitengrad])
        F3([Lage])---F5([LG|Längengrad])
    end
    subgraph SG4 [ ]
        Land--(1,1)---ist_HS{ist_HS}
        ist_HS{ist_HS}--(0,1)---Stadt[[Stadt]]
    end
    subgraph SG3 [ ]
        Provinz[[Provinz]]---P1(["`<ins>Name</ins>`"])
        Provinz[[Provinz]]---P2([EWZ|Einwohnerzahl])
        Provinz[[Provinz]]---P3([Fläche])
    end
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG4 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG5 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    linkStyle default marker-end:none
"""


# graph = parse_solution(mermaid_text)
# print("Knoten:")
# for node, data in graph.nodes(data=True):
#     print(node, data)

# print("\nKanten:")
# for u, v, data in graph.edges(data=True):
#     print(u, v, data)
# print(graph)