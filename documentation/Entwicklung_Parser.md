# Brainstorming
- Mermaid in Format für Python übersetzen 

--> Subgraphs sind dabei Gruppen von Entitäten und Beziehungen (Relationships)

--> Darstellung der Knoten und Bezihungen in entsprechendem Format ohne Informationsverlust 

--> Zusätzliche Anpassungen, wie Farben und Stile etc. ignorieren 

# Struktur

- extrahieren der Knoten (umfasst Entitäten und Attribute)
- extrahieren der Beziehungen (umfasst Kardinalitäten)
- speichern in interner Repräsentation 

# Notizen
- regex muss für jedes Muster einzeln angepasst werden, damit keine Fehler auftreten 
- so gibt es für die Knoten erstmal 3 regex muster --> alle haben die gleichen gruppen das vereinfacht das extrahieren später 
- für die Kanten ist das etwas schwieriger, die müssen in 2 gruppen geteilt werden 

