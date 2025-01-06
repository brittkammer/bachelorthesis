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

- warum directed graphs in networkx? gerichtete Beziehungen?? 
- Ungerechnetete Graphen (Graph):
Problem: Beziehungen haben keine Richtung. Dies führt zu Informationsverlust.
Beispiel:
Eine ungerichtete Kante zwischen Produzent und herstellen könnte sowohl Produzent -- herstellen als auch herstellen -- Produzent bedeuten.
Die Kardinalitäten können in einem ungerichteten Graphen nicht korrekt modelliert werden.
Multigraphen:
Multigraphen (Graphen mit mehreren Kanten zwischen denselben Knoten) könnten verwendet werden, um Beziehungen darzustellen.
Nachteil:
Sie erhöhen die Komplexität unnötig.
Die meisten Beziehungen in ER-Diagrammen sind eindeutig (eine Beziehung zwischen zwei Entitäten). Daher sind Multigraphen oft überdimensioniert.

# verschiedene Verisonen von Entitäten und Attributen hinzufügen
- mir ist aufgefallen dass nur einfache Attribute und Entiäten im Parser enthalten waren 
- es fehlten zusammengesetzte Attribute, Primärschlüssel-Attribute und mehrwertige Attribute 
--> diese werden jetzt vom Parser korrekt erkannt und als Knoten mit entsprechenden Werten hinzugefügt
- schwache Enitäten müssen noch hinzugefügt werden
- Regex für Primärschlüssel-Attribut noch anpassen, sodass ins nicht im Wert ist
