# Entwicklung Matcher

- matcher muss auch prüfen können ob knoten bereits falsch benannt wurden
--> die fallen aktuell durch fsd Muster/ die STruktur bei falsche Knoten durch, weil zu beginn gepürft wird ob der node im studentengraph enthalten ist 
wenn dies nicht der fall ist, wird das nicht weiter geprüft --> hierfür muss eine Lösung eingebaut werden

vielleicht das Konzept der Filterung der Fehler überarbeieten, sodass dort mehr mit elif und if gearbeitet wird und nicht jedes Fehlermuster einzeln neu durch schleifen geht --> Idee: Eine Schleife für Knoten und eine für Kanten, in der alle Fehlerfälle abgedeckt werden 

- dann ist mir aufgefallen, dass wie z.B. hier:         
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe])
        Bauteil---B7([Farbe])
    die Bezeichnungen B2, B3 und B4 festgelegt werden und diese auch als Name des Knoten festgelegt werden im Graphen 
    --> macht das überhaupt Sinn? 
    hier geht es ja nur darum dass mermaid untershciedliche IDs bekommt und die Visualisierung richtig vornehmen kann 
    wenn dort Mehrfachnennungen auftreten, dann werden die als das gleiche ELement betrachtet
    was wie bei Bauteil gewollt sein kann, aber eben auch nicht immer 
    wenn z.B. 2 verschiedene Entitäten beide Name als Attribut haben 

# 07.01.2025 
- Visualiserung der Fehler mit einem zweit dict, um für die debugging zwecke immer noch das erste verwenden zu können 
- Visualiserung soll wie folgt erfolgen: 
    Fehler wird erkannt und dem dict fehler_visualiserungen hinzugefügt
    Format in fehler_visualisierungen ist immer für style Knoten etc. / linkStyle Kante etc.
    dict fehler_visualisierungen der studentischen Lösung hinzufügen 
    (dabei werden für fehlenden Kanten/Knoten nur Hinweise ausgegeben) 
    --> andere Fehler wie falscher Typ / Name, extra Kante / Knoten werden farblich visualiert

- Aktuelles Problem: 
    - Wie kann ich die farblichen Anpassungen für die Kanten hinzufügen? 
    - linkStyle Kante etc... 
    --> benötigt die Nummer der Kante, d.h. die Zahl der Reihenfolge in der sie in mermaid.js hinzugefügt wird 
    --> Idee: Reihenfolge / Nummer als Attribut im Graph hinzufügen 
    --> so kann einfach das Attribut abgerufen werden und die Nummer dann für die Fehler Visualisierung verwendet werden

Um korrekte Visualisierungen als Output zu haben: 
    - tabulator entsprechend in der studentischen Lösung / Musterlösung hinzufügen
    --> muss automatisch passieren wenn studenten was eintippen
    --> sonst output der visualisierungen = fehler 