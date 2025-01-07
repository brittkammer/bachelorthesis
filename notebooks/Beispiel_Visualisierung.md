
flowchart
    subgraph SG1 [ ]
        Produzent---P1(["`<ins>ProdId</ins>`"])
        Produzent---P2([Name])
        Produzent---P3(((Zertifikate)))
    end
    subgraph SG2 [ ]
        Bauteil---B1(["`<ins>Name</ins>`"])
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe])
        Bauteil---B7([Farbe])
        B3---B4([Länge])
        B3---B5([Breite])
        B3---B6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent -- (1,*) --- bauen{bauen}
        bauen -- (1,1) --- Bauteil 
        bauen---H1([Jahr])
        Bauteil--(2,3)--- bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus} -- (0,*) --- Bauteil
    
    end    
    FehlerKardinalitäten[Fehler: 
    Schau dir die Kardinalitäten nochmal an! 
    ]

    style FehlerKardinalitäten fill:#fde2e1,stroke:#b91c1c,stroke-width:2p
    linkStyle 0 stroke:#2ca02c,stroke-width:2px;
    
    linkStyle 10 stroke:#1f77b4,stroke-width:2px,color:#1f77b4,fill:none;    
    linkStyle 13 stroke:#d62728,stroke-width:2px,color:#d62728,fill:none;
    
    style SG1 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG2 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style SG3 fill:#ff0000,fill-opacity:0.0,stroke:#333,stroke-width:0px
    style B7 fill:#d9eaf7,stroke:#045a8d,stroke-width:2px
    style Produzent fill:#D5E8D4,stroke:#82B366,stroke-width:2px
    style P2 fill:#FFF2CC,stroke:#FFD966,stroke-width:2px
    style bauen fill:#F4CCCC,stroke:#CC0000,stroke-width:2px
    style default #f0f9e8,fill-opacity:0.0,stroke:#333,stroke-width:0px
    linkStyle default marker-end:None