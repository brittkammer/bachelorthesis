# Was sind die Regeln bei der Erstellung von ERM? 

## Entitäten
    * sind immer ein Rechteck 
    * zwischen 2 Entitäten muss ein Relationship liegen, das heißt diese sind nicht direkt miteinander verbunden
    * kann durch Attriute (Primärschlüssel, zusammengesetztes Attribut, mehrwertiges Attribut) detailierter beschrieben werden
    * hat immer ein Primärschlüssel 

## Relationships 
    * liegen immer zwischen zwei Entiäten 
    * sind nie mit anderen Relationships verbunden 
    * können durch Attribute (kein Primärschlüssel-Attribut) genauer beschrieben werden 
    * rekursive Beziehung, dann nur mit einer Entität verbunden 

## Attribute 
    * beschreiben Entiäten / Relationships genauer 
    * nur ein zusammengesetztes Attribut kann mit anderen attributen verbunden sein

## Kardinalitäten / Beziehungstypen 
    * nach Chen gibt es nur 1:1, 1:N oder N:M Beziegungstypen 
    * nach Min-Max-Notation ist das anders 
    * können nur auf Kanten zwischen Entität und Relationship sein 