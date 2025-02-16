# Abschlussarbeit
# Entwicklung eines automatisierten Feedbacksystems von ER-Modellen

## Ziele: 
- Abgabedatum: 03.03.2025

## ToDo's ✅✅✅
### Parser 🚀
    - [] Musterlösungen mit mehreren Begriffen für denselben Knoten einbinden
    - [] weitere regex muster einbinden so dass möglich viele Arten von Eingaben abgefangen werden 
    - [] welche lines fallen nicht in die regexmuster? 
    - [] die dann zusätzlich an den matcher weitergeben, sodass hier eine liste mit denen erstellt wird und diese als Syntax Fehler ausgegeben werden.
### Matcher  🚀
    - [] Fehler (mehrere Knoten falsch betitelt, aber Typ, Kanten etc stimmt) erkennen 
        --> Überprüfung der Kanten jedoch erst später, sodass falsche Kanten trotzdem aussortiert werden
### Tests 🚀
    - [] Tests für Musterlösungen / studentische Lösungen, ob alle Fehler erkannt werden

### Webservice 🚀
    - [] erstellen eines Dockerfiles welches dann einen Webservice baut
    - [] Hinzufügen von Magic-Bibliothek 
    - [] vollständige Integration in Jupyter Notebook --> automatisiertes Feedback nach Abgabe
    - [] Wie kann die Musterlösung "geheim" gehalten / nicht einsehbar für Studenten bleiben?

### How to start Docker: 

    - docker build -t er_model_checker . 
    - docker run -p 8000:8000 er_model_checker

### Übersicht der Mermaid-Syntax 

| Darstellungselemente | Syntax | Beschreibung | Beispiel in Diagramm |
|----------------------|--------|--------------|----------------------|
| Entität(Subtyp) und Entität(Supertyp) | Subtyp---IS-A{{IS-A}}---Supertyp | Stellt eine IS-A Beziehung zwischen einem Subtyp und einem Supertyp von Entitäten dar. | `PKW---IS-A{{IS-A}}---Fahrzeug` |
| Entität(Subtyp) | `Subtyp---IS-A{{IS-A}}` | Stellt eine IS-A Beziehung mit einem Subtyp dar. Supertyp muss zuvor einmalig genannt werden. | `LKW---IS-A{{IS-A}}` |
| Entität | `Entität---AttribuID([Attributname])` | Stellt eine Entität mit Attribut dar.| `Kunde---K1([Name])` |
|         | `schwache_Entität[[schwache_Entität]]`---AttribuID(["`<ins>Attributname</ins>`"]) | `Kunde[[Kunde]]---K1([Name)]` |
| Primärschlüssel-Attribut | `Entität---AttributID(["<ins>Attributname</ins>"])` | Stellt eine Entität und ein Primärschlüssel-Attribut dar. | `Land---L1(["`<ins>KFZ</ins>`"])` |
|                          | `Entität[[Entität]]---AttributID(["<ins>Attributname</ins>"])` | Stellt eine schwache Entität und ein Primärschlüssel-Attribut dar. | `Provinz[[Provinz]]---P1(["`<ins>Name</ins>`"])` |
| mehrwertiges Attribut | `Entität---(((Attributname)))` | blbablabla | `Angestellter---A1(((Zertifikate)))` |
|                       | `schwache_Entität[[schwache_Entität]]---(((Attributname)))` | blablabla | `Angestellter---A1(((Zertifikate)))` |
| zusammengesetztes Attribut | `Entität---AttributID([Attributname])` | blabla | `Angestellte---A3([Anschrift])` |
|                            | `AttributID([Attributname])---AttributID([Attributname])` | blala | `A3([Anschrift])---A4([Stadt])` |
|                            |                                                           |       | `A3([Anschrift])---A4([Straße])` |
| Relationship | `Entität--(x,y)---Relationship{Relationship}` | Relationship und Entität mit einer Kardinalität(Min-Max-Notation). | `Land--(1,*)---liegt{liegt}` |
|              | `Relationship{Relationship}--(x,y)---Entität` |                                                                    | `ist_HS{ist_HS}--(1,1)---Land` |
|              | `schwache_Entität[[schwache_Entität]]--(x,y)---Relationship{Relationship}` |                                       | `Provinz[[Provinz]]--(1,1)---liegt{liegt}` |
|              | `Relationship{Relationship}--(x,y)---schwache_Entität[[schwache_Entität]]` |                                       | `ist_HS{ist_HS}--(0,1)---Stadt[[Stadt]]` |













