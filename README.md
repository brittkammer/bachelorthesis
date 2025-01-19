# Abschlussarbeit
# Entwicklung eines automatisierten Feedbacksystems von ER-Modellen

## Ziele: 
- Abgabedatum: 03.03.2025

## ToDo's 
### Parser 
    - [] Musterlösungen mit mehreren Begriffen für denselben Knoten einbinden
    - [] weitere regex muster einbinden so dass möglich viele Arten von Eingaben abgefangen werden 
    - [] welche lines fallen nicht in die regexmuster? 
    - [] die dann zusätzlich an den matcher weitergeben, sodass hier eine liste mit denen erstellt wird und diese als Syntax Fehler ausgegeben werden.
### Matcher  
    - [] Fehler (mehrere Knoten falsch betitelt, aber Typ, Kanten etc stimmt) erkennen 
        --> Überprüfung der Kanten jedoch erst später, sodass falsche Kanten trotzdem aussortiert werden
### Tests
    - [] Tests für Musterlösungen / studentische Lösungen, ob alle Fehler erkannt werden

### Webservice 
    - [] erstellen eines Dockerfiles welches dann einen Webservice baut
    - [] Hinzufügen von Magic-Bibliothek 
    - [] vollständige Integration in Jupyter Notebook --> automatisiertes Feedback nach Abgabe
    - [] Wie kann die Musterlösung "geheim" gehalten / nicht einsehbar für Stuenten bleiben?
