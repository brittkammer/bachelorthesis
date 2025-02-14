import re 
import networkx as nx 

def parse_mermaid_text(mermaid_text):
    #regex_muster_knoten = r"(\w+)---(\w+)\(\[(?:(?:`?<ins>(.*?)<\/ins>`?)|([^\]]*?))\]\)|\((\w+)---(\w+)\(\(\((.*?)\)\)\)" 
    regex_muster_knoten = [
        r"(\w+)---(\w+)\(\[\"`?<ins>(.*?)<\/ins>`?\"\]\)$",  # Mit <ins>-Tags - Primärschlüssel
        r"(\w+)---(\w+)\(\[(\w+)\]\)$",                      # Ohne Tags - normales Attribut
        r"(\w+)---(\w+)\(\(\((.*?)\)\)\)$"                   # Verschachtelte Klammern - mehrwertiges Attribut
    ]

    regex_muster_kanten = [
        r"(\w+)\{(\w+)\}--\((\d,\*|\d,\d|\*?,\d)\)---(\w+)$", # Relationship{}--()---Entiät
        r"(\w+)--\((\d,\*|\d,\d|\*?,\d)\)---(\w+)\{(\w+)\}$", # Entität--()---Relationship{}
        r"(\w+)\{(\w+)\}---(\w+)\(\[(\w+)\]\)$"                  # Relationship{}---Attribut([])
    ]
    regex_zusammengesetztes_atrribut = r"(\w+)\(\[([^\[\]]+)\]\)---(\w+)\(\[([^\[\]]+)\]\)$" # für Attribute die Atrribute enthalten
    regex_schwache_entitaeten = [
        r"(\w+)\[\[(\w+)\]\]---(\w+)$", # SchwacheEntität[[]]---Entität
        r"(\w+)---(\w+)\[\[(\w+)\]\]$", # Entität---SchwacheEntität[[]]
        r"(\w+)\[\[(\w+)\]\]---(\w+)\(\[(\w+)\]\)$", # SchwacheEntität[[]]---Attribut
        r"(\w+)\[\[(\w+)\]\]---(\w+)\(\[\"`?<ins>(.*?)<\/ins>`?\"\]\)$", # SchwacheEntität[[]]---Primärschlüssel-Attribut
        r"(\w+)\[\[(\w+)\]\]---(\w+)\(\(\((.*?)\)\)\)$", # SchwacheEntität[[]]---mehrwertige Attribut
        r"(\w+)\[\[(\w+)\]\]--\((\d,\*|\d,\d|\*?,\d)\)---(\w+)\{(\w+)\}$", # SchwacheEntität[[]]---Relationship{}
        r"(\w+)\{(\w+)\}--\((\d,\*|\d,\d|\*?,\d)\)---(\w+)\[\[(\w+)\]\]$" # Relationship{}---SchwacheEntität[[]]
    ] # 
    regex_is_a = [
        r"(\w+)---IS\-A\{\{IS\-A}}---(\w+)$", # Entität(Subtyp)---IS-A{{}}---Entität(Supertyp)
        r"(\w+)---IS\-A\{\{IS\-A}}$" # Entität(Subtyp)---IS-A{{}}
    ] 

    graph = nx.DiGraph()
    lines = mermaid_text.split("\n")
    global counter_kanten 
    counter_kanten = 0
    for line in lines: 
        matches = re.findall(regex_is_a[0], line)
        for entitaetSubtyp, entitaetSupertyp in matches:
            graph.add_node(entitaetSubtyp, type="Entität(Subtyp)", label=entitaetSubtyp)
            graph.add_node(entitaetSupertyp, type="Entität(Supertyp)", label=entitaetSupertyp)
            graph.add_edge(entitaetSubtyp, entitaetSupertyp, Beziehung="IS-A-Beziehung", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_is_a[1], line)
        for entitaet in matches:
            graph.add_node(entitaet, type="Entität(Subtyp)", label=entitaet)
            graph.add_edges_from(entitaetSubtyp, entitaetSupertyp, Beziehung="IS-A-Beziehung", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
##################### Entitäten und Attribute ###########################
        for muster in regex_muster_knoten:
            matches = re.findall(muster, line)
            for entitaet, attribut_id, attribut_name in matches:
                if not graph.has_node(entitaet):
                    graph.add_node(entitaet, type="Entität", label=entitaet)
                if muster == regex_muster_knoten[0]:
                    graph.add_node(attribut_id, type="Primärschlüssel-Attribut", label=attribut_name)
                    graph.add_edge(entitaet, attribut_id, Beziehung="hat Primärschlüssel-Attribut", Nummer=counter_kanten)
                    counter_kanten = counter_kanten + 1
                elif muster == regex_muster_knoten[1]: 
                    graph.add_node(attribut_id, type="Attribut", label=attribut_name)
                    graph.add_edge(entitaet, attribut_id, Beziehung="hat Attribut", Nummer=counter_kanten)
                    counter_kanten = counter_kanten + 1
                elif muster == regex_muster_knoten[2]: 
                    graph.add_node(attribut_id, type="mehrwertiges Attribut", label=attribut_name)
                    graph.add_edge(entitaet, attribut_id, Beziehung="hat mehrwertiges Attribut", Nummer=counter_kanten)
                    counter_kanten = counter_kanten + 1
############ Schwache Entitäten ###################
        matches = re.findall(regex_schwache_entitaeten[0], line)
        for schwacheEntitaetID, schwacheEntitaet, entitaet in matches: 
            print(f"TEST1 {matches}")
            graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaet)
            graph.add_edge(schwacheEntitaetID, entitaet, Beziehung="hat schwache Entität", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[1], line)
        for entitaet, schwacheEntitaetID, schwacheEntitaet in matches: 
            print(f"TEST2 {matches}")

            graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaet)
            graph.add_edge(entitaet, schwacheEntitaetID, Beziehung="hat schwache Entität", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[2], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches: 
            print(f"TEST3 {matches}")
            
            graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaet)
            graph.add_node(attribut_id, type="Attribut", label=attribut_name)
            graph.add_edge(schwacheEntitaetID, attribut_id, Beziehung="hat Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[3], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches:
            print(f"TEST4 {matches}")
            
            graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaet)
            graph.add_node(attribut_id, type="Primärschlüssel-Attribut", label=attribut_name)
            graph.add_edge(schwacheEntitaetID, entitaet, Beziehung="hat Primärschlüssel-Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[4], line)
        for schwacheEntitaetID, schwacheEntitaet, attribut_id, attribut_name in matches: 
            print(f"TEST5 {matches}")
            
            graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaet)
            graph.add_node(attribut_id, type="mehrwertiges Attribut", label=attribut_name)
            graph.add_edge(schwacheEntitaetID, entitaet, Beziehung="hat mehrwertiges Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[5], line)
        for schwacheEntitaetID, schwacheEntitaet,cardinalitaet, relationship, relationship_name in matches: 
            print(f"TEST6 {matches}")
            
            graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaet)
            if not graph.has_node(relationship):
                graph.add_node(relationship, type="Relationship", label=relationship_name)
            graph.add_edge(schwacheEntitaetID, relationship, Beziehung="schwache Entität-Relationship", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_schwache_entitaeten[6], line)
        for relationship, relationship_name,cardinalitaet, schwacheEntitaetID, schwacheEntitaet in matches: 
            print(f"TEST7 {matches}")
            
            if not graph.has_node(relationship):
                graph.add_node(relationship, type="Relationship", label=relationship_name)
            graph.add_node(schwacheEntitaetID, type="Schwache Entität", label=schwacheEntitaet)
            graph.add_edge(relationship, schwacheEntitaetID , Beziehung="Relationship-schwache Entität", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
################### Zusammengesetztes Attribut ################
        matches = re.findall(regex_zusammengesetztes_atrribut, line)
        for attribut_zusammengesetzt_id, attribut_zusammengesetzt_name, attribut_id, attribut_name in matches: # überschreiben des Typs des zusammengesetzten Attributes, Label bleibt gleich
            graph.add_node(attribut_zusammengesetzt_id, type="zusammengesetztes Attribut", label=attribut_zusammengesetzt_name)
            graph.add_node(attribut_id, type="Attribut", label=attribut_name)
            graph.add_edge(attribut_zusammengesetzt_id, attribut_id, Beziehung="hat Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1

################## Relationships #######################
        matches = re.findall(regex_muster_kanten[0], line) 
        for relationship,relationship_name, cardinalitaet, entitaet in matches: 
            graph.add_node(relationship, type="Relationship", label=relationship_name),
            graph.add_edge(relationship, entitaet,Beziehung="Relationship-Entität", Kardinalität=cardinalitaet, Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_muster_kanten[1], line)
        for entitaet, cardinalitaet, relationship, relationship_name in matches: 
            graph.add_node(relationship, type="Relationship", label=relationship),
            graph.add_edge(entitaet, relationship, Beziehung="Entität-Relationship", Kardinalität=cardinalitaet, Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1
        matches = re.findall(regex_muster_kanten[2], line)
        for relationship, relationship_name, attribut_id, attribut_name in matches: 
            graph.add_node(attribut_id, type="Attribut", label=attribut_name)
            graph.add_edge(relationship, attribut_id, Beziehung="Relationship-Attribut", Nummer=counter_kanten)
            counter_kanten = counter_kanten + 1

    return graph 



################## DEBUGGING ###################
mermaid_text =  """mermaid
flowchart 
    subgraph SG1 [ ]
        Land---L1(["`<ins>KFZ</ins>`"])
    end
    subgraph SG5 [ ]
        Land--(1,*)---liegt{liegt}
        Provinz[[Provinz]]--(1,1)---liegt{liegt}
    end
    subgraph SG2 [ ]
        Stadt[[Stadt]]---S1(["`<ins>Name</ins>`"])
        Stadt[[Stadt]]---S2([Einwohnerzahl])
        Stadt[[Stadt]]---S3([Lage])
        S3([Lage])---S4([Breitengrad])
        S3([Lage])---S5([Längengrad])
    end
    subgraph SG4 [ ]
        Land--(1,1)---ist_HS{ist_HS}
        ist_HS{ist_HS}--(0,1)---Stadt[[Stadt]]
    end
    subgraph SG3 [ ]
        Provinz[[Provinz]]---P1(["`<ins>Name</ins>`"])
        Provinz[[Provinz]]---P2([Einwohnerzahl])
        Provinz[[Provinz]]---P3([Fläche])
    end

    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG4 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG5 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    linkStyle default marker-end:none
"""

# graph = parse_mermaid_text(mermaid_text)
# print("Knoten:")
# for node, data in graph.nodes(data=True):
#     print(node, data)

# print("\nKanten:")
# for u, v, data in graph.edges(data=True):
#     print(u, v, data)
# print(graph)