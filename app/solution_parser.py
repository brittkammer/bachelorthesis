import re
import networkx as nx


def parse_solution(mermaid_text):
    regex_muster_knoten = [
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\[\"`?<ins>([a-zA-ZäöüÄÖÜß0-9_|\-.]+)<\/ins>`?\"\]\)$",  # Mit <ins>-Tags - Primärschlüssel
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\)$",  # Ohne Tags - normales Attribut
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\(\(([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\)\)\)$",  # Verschachtelte Klammern - mehrwertiges Attribut
    ]
    regex_muster_kanten = [
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)$",  # Relationship{}--()---Entität
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}$",  # Entität--()---Relationship{}
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\)$",  # Relationship{}---Attribut([])
    ]
    regex_zusammengesetztes_atrribut = r"(\w+)\(\[([^\[\]]+(?:\|[^\[\]]+)*)\]\)---(\w+)\(\[([^\[\]]+(?:\|[^\[\]]+)*)\]\)$"  # für Attribute die Atrribute enthalten
    regex_schwache_entitaeten = [
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]---([a-zA-ZäöüÄÖÜß0-9_]+)\(\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\)$",  # SchwacheEntität[[]]---Attribut
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]---([a-zA-ZäöüÄÖÜß0-9_]+)\(\[\"`?<ins>([a-zA-ZäöüÄÖÜß0-9_|\-.]+)<\/ins>`?\"\]\)$",  # SchwacheEntität[[]]---Primärschlüssel-Attribut
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]---([a-zA-ZäöüÄÖÜß0-9_]+)\(\(\(([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\)\)\)$",  # SchwacheEntität[[]]---mehrwertiges Attribut
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}$",  # SchwacheEntität[[]]---Relationship{}
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\{([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\}--\(((?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*)(?:\|(?:\d+,\d+|\d+,\*|\*?,\d+|\d+|\*))*)\)---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\[\[([a-zA-ZäöüÄÖÜß0-9_|\-.]+)\]\]$",  # Relationship{}---SchwacheEntität
    ]  # schwache Enitäten
    regex_is_a = [
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---IS\-A\{\{IS\-A\}\}---([a-zA-ZäöüÄÖÜß0-9_|\-.]+)$",  # Subtyp---IS-A{{}}---Supertyp
        r"([a-zA-ZäöüÄÖÜß0-9_|\-.]+)---IS\-A\{\{IS\-A\}\}$",  # Subtyp---IS-A{{}}
    ]

    graph = nx.DiGraph()
    lines = mermaid_text.split("\n")
    global counter_kanten
    global syntaxFehlerListe
    syntaxFehlerListe = []
    counter_kanten = 0
    for line in lines:
        line.strip()
        ##################### IS-A Beziehungen ###########################
        matches = re.findall(regex_is_a[0], line)
        for entitaetSubtyp, entitaetSupertyp in matches:
            entitaetSubtypListe = entitaetSubtyp.split("|")
            entitaetSupertypListe = entitaetSupertyp.split("|")
            graph.add_node(
                entitaetSubtypListe[0],
                type="Entität(Subtyp)",
                label=entitaetSubtypListe,
            )
            graph.add_node(
                entitaetSupertypListe[0],
                type="Entität(Supertyp)",
                label=entitaetSupertypListe,
            )
            graph.add_edge(
                entitaetSubtypListe[0],
                entitaetSupertypListe[0],
                Beziehung="IS-A-Beziehung",
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_is_a[1], line)
        for entitaetSubtyp in matches:
            entitaetSubtypListe = entitaetSubtyp.split("|")
            graph.add_node(
                entitaetSubtypListe[0],
                type="Entität(Subtyp)",
                label=entitaetSubtypListe,
            )
            graph.add_edge(
                entitaetSubtypListe[0],
                entitaetSupertypListe[0],
                Beziehung="IS-A-Beziehung",
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
        for muster in regex_muster_knoten:
        ##################### Entitäten und Attribute ###########################
            matches = re.findall(muster, line)
            for entitaet, attribut_id, attribut_name in matches:
                entitaetListe = entitaet.split("|")
                if not graph.has_node(entitaetListe[0]):
                    graph.add_node(
                        entitaetListe[0], type="Entität", label=entitaetListe
                    )
                if muster == regex_muster_knoten[0]:
                    attribut_liste = attribut_name.split("|")
                    graph.add_node(
                        attribut_id,
                        type="Primärschlüssel-Attribut",
                        label=attribut_liste,
                    )
                    graph.add_edge(
                        entitaetListe[0],
                        attribut_id,
                        Beziehung="hat Primärschlüssel-Attribut",
                        Nummer=counter_kanten,
                    )
                    counter_kanten = counter_kanten + 1
                elif muster == regex_muster_knoten[1]:
                    attribut_liste = attribut_name.split("|")
                    graph.add_node(attribut_id, type="Attribut", label=attribut_liste)
                    graph.add_edge(
                        entitaetListe[0],
                        attribut_id,
                        Beziehung="hat Attribut",
                        Nummer=counter_kanten,
                    )
                    counter_kanten = counter_kanten + 1
                elif muster == regex_muster_knoten[2]:
                    attribut_liste = attribut_name.split("|")
                    graph.add_node(
                        attribut_id, type="mehrwertiges Attribut", label=attribut_liste
                    )
                    graph.add_edge(
                        entitaetListe[0],
                        attribut_id,
                        Beziehung="hat mehrwertiges Attribut",
                        Nummer=counter_kanten,
                    )
                    counter_kanten = counter_kanten + 1

        ##################### Zusammengesetzte Attribute ########################
        matches = re.findall(regex_zusammengesetztes_atrribut, line)
        for (
            attribut_zusammengesetzt_id,
            attribut_zusammengesetzt_name,
            attribut_id,
            attribut_name,
        ) in (
            matches
        ):  # überschreiben des Typs des zusammengesetzten Attributes, Label bleibt gleich
            attributZusammengesetztListe = attribut_zusammengesetzt_name.split("|")
            attributListe = attribut_name.split("|")
            graph.add_node(
                attribut_zusammengesetzt_id,
                type="zusammengesetztes Attribut",
                label=attributZusammengesetztListe,
            )
            graph.add_node(attribut_id, type="Attribut", label=attributListe)
            graph.add_edge(
                attribut_zusammengesetzt_id,
                attribut_id,
                Beziehung="hat Attribut",
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1

        ######################## Relationships ##################################
        matches = re.findall(regex_muster_kanten[0], line)
        for relationship, relationship_name, cardinalitaet, entitaet in matches:
            relationshipListe = relationship_name.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            entitaetListe = entitaet.split("|")
            if not graph.has_node(entitaetListe[0]):
                graph.add_node(
                    entitaet,
                    type="Entität",
                    label=entitaetListe,
                )
            graph.add_node(relationship, type="Relationship", label=relationshipListe),
            graph.add_edge(
                relationship,
                entitaetListe[0],
                Beziehung="Relationship-Entität",
                Kardinalität=cardinalitaetListe,
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1

        matches = re.findall(regex_muster_kanten[1], line)
        for entitaet, cardinalitaet, relationship, relationship_name in matches:
            entitaetListe = entitaet.split("|")
            relationshipListe = relationship_name.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            if not graph.has_node(entitaetListe[0]):
                graph.add_node(
                    entitaet,
                    type="Entität",
                    label=entitaetListe,
                )
            graph.add_node(relationship, type="Relationship", label=relationshipListe),
            graph.add_edge(
                entitaetListe[0],
                relationship,
                Beziehung="Entität-Relationship",
                Kardinalität=cardinalitaetListe,
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_muster_kanten[2], line)
        for relationship, relationship_name, attribut_id, attribut_name in matches:
            attributListe = attribut_name.split("|")
            graph.add_node(attribut_id, type="Attribut", label=attributListe)
            graph.add_edge(
                relationship,
                attribut_id,
                Beziehung="Relationship-Attribut",
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1

        ###################### Schwache Entitäten  ##############################
        matches = re.findall(regex_schwache_entitaeten[0], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            attributListe = attribut_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(
                    schwacheEntitaetID,
                    type="Schwache Entität",
                    label=schwacheEntitaetListe,
                )
            graph.add_node(attribut_id, type="Attribut", label=attributListe)
            graph.add_edge(
                schwacheEntitaetID,
                attribut_id,
                Beziehung="hat Attribut",
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[1], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            attributListe = attribut_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(
                    schwacheEntitaetID,
                    type="Schwache Entität",
                    label=schwacheEntitaetListe,
                )
            graph.add_node(
                attribut_id, type="Primärschlüssel-Attribut", label=attributListe
            )
            graph.add_edge(
                schwacheEntitaetID,
                attribut_id,
                Beziehung="hat Primärschlüssel-Attribut",
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[2], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            attributListe = attribut_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(
                    schwacheEntitaetID,
                    type="Schwache Entität",
                    label=schwacheEntitaetListe,
                )
            graph.add_node(
                attribut_id, type="mehrwertiges Attribut", label=attributListe
            )
            graph.add_edge(
                schwacheEntitaetID,
                attribut_id,
                Beziehung="hat mehrwertiges Attribut",
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[3], line)
        for (
            schwacheEntitaetID,
            schwacheEntitaet,
            cardinalitaet,
            relationship,
            relationship_name,
        ) in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            relationshipListe = relationship_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(
                    schwacheEntitaetID,
                    type="Schwache Entität",
                    label=schwacheEntitaetListe,
                )
            graph.add_node(relationship, type="Relationship", label=relationshipListe)
            graph.add_edge(
                schwacheEntitaetID,
                relationship,
                Beziehung="Schwache Entität-Relationship",
                Kardinalität=cardinalitaetListe,
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[4], line)
        for (
            relationship,
            relationship_name,
            cardinalitaet,
            schwacheEntitaetID,
            schwacheEntitaet,
        ) in matches:
            schwacheEntitaetListe = schwacheEntitaet.split("|")
            cardinalitaetListe = cardinalitaet.split("|")
            relationshipListe = relationship_name.split("|")
            if not graph.has_node(schwacheEntitaetListe[0]):
                graph.add_node(
                    schwacheEntitaetID,
                    type="Schwache Entität",
                    label=schwacheEntitaetListe,
                )
            graph.add_node(relationship, type="Relationship", label=relationshipListe)
            graph.add_edge(
                relationship,
                schwacheEntitaetID,
                Beziehung="Relationship-Schwache Entität",
                Kardinalität=cardinalitaetListe,
                Nummer=counter_kanten,
            )
            counter_kanten = counter_kanten + 1
    return graph

############################# DEBUGGING #########################################

mermaid_text = """mermaid
flowchart
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
# graph = parse_solution(mermaid_text)
# print("Knoten:")
# for node, data in graph.nodes(data=True):
#     print(node, data)

# print("\nKanten:")
# for u, v, data in graph.edges(data=True):
#     print(u, v, data)
# print(graph)