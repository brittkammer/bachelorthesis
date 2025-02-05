# Grenzen

## Grenzen des Matchers
    * Probeleme bei Identifizierung richtiger/falscher Kanten, wenn beide Knoten die daran hängen falsch sind (aber nur teilweise, komisches Phänomen)
    * Wenn ein Knoten mal richtig und mal falsch geschrieben ist --> wird als 2 verschiedene Knoten identifiziert und daher dann einmal als richtig und einmal als zusätzlich dargestellt
    * Kanten bei zusätzlichen Knoten werden oft schwarz statt gelb dargestellt

    * Beim Vergelich werden keine verschiedenen Beziehungen / Varianten für Beziehungen verglichen
## Grenzen bei Parser der Musterlösungen: 
        Bauteil---B1(["`<ins>Name|name|test|</ins>`"])
    - Wird wie in dem Beispiel oben ein letztes | hinzugefügt so wird danach auch das Leere Element "" der Liste mit AttributNamen hinzugefügt
    - keine Umlaute und Sonderzeichen bei Eingabe in mermaid

