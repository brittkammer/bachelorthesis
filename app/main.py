from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.graphMatcher import compare_graphs
from app.parse_into_graph import parse_mermaid_text
from app.solution_parser import parse_solution
import os

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# Datenmodell für die Anfrage
class SolutionRequest(BaseModel):
    loesungID: int
    er_model: str  # Die studentische Lösung im Mermaid-Format

# Funktion zum Laden der Musterlösung basierend auf der ID
def musterloesungLaden(loesungID): 
    file = f"Musterlösungen/musterlösungID{loesungID}.txt"
    if not os.path.exists(file): 
        return None
    with open(file, "r") as f: 
        return f.read()

@app.post("/validate/")
def loesungPruefen(request: SolutionRequest): 
    # Musterlösung laden
    musterloesung = musterloesungLaden(request.loesungID)
    if musterloesung is None: 
        return {"error": "Musterlösung nicht gefunden"}
    
    try:
        # Musterlösung und studentische Lösung einlesen und parsen
        musterloesung_graph = parse_solution(musterloesung)  # Musterlösung parsen
        student_loesung_graph = parse_mermaid_text(request.er_model)  # Studentische Lösung parsen

        # Vergleich der Graphen durchführen (drei Argumente übergeben)
        feedback = compare_graphs(
            musterloesung_graph,
            student_loesung_graph,
            request.er_model  # Übergabe der originalen studentischen Lösung
        )

        # Feedback als Mermaid-Diagramm visualisieren
        return {"feedback": feedback}
    
    except Exception as e:
        # Fehlerbehandlung und Debugging
        return {"error": str(e)}

@app.get("/diagram/")
def show_diagram(request: Request, code: str):
    # Mermaid-Diagramm visualisieren
    return templates.TemplateResponse("diagram.html", {"request": request, "diagram_code": code})
