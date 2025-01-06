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