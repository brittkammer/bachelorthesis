from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.parse_into_graph import parse_mermaid_text
from app.solution_parser import parse_solution
from app.graphMatcher import compare_graphs
import os

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

class SolutionRequest(BaseModel):
    loesungID: int
    er_model: str

def musterloesungLaden(loesungID): 
    file = f"Musterlösungen/musterlösungID{loesungID}.txt"
    if not os.path.exists(file): 
        return None
    with open(file, "r") as f: 
        return f.read()

@app.post("/validate/")
def loesungPruefen(request: SolutionRequest): 
    musterloesung = musterloesungLaden(request.loesungID)
    if musterloesung is None: 
        return {"error": "Musterlösung nicht gefunden"}
    
    else: 
        print(f"Geladene Musterlösung: \n{musterloesung}")

        feedback = compare_graphs(parse_solution(musterloesung), parse_mermaid_text(request.er_model))

        return {"feedback": feedback}

@app.get("/diagram/")
def show_diagram(request: Request, code: str):
    return templates.TemplateResponse("diagram.html", {"request": request, "diagram_code": code})
