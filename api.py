from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
import csv
import numpy as np
import requests
from pydantic import BaseModel
import re
import json
import os
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

student_marks = [{"name":"M","marks":90},{"name":"w","marks":12},{"name":"PvCFcv","marks":78},{"name":"XPhny","marks":61},{"name":"HdGQwJIS","marks":64},{"name":"adx12jiA","marks":82},{"name":"onAh","marks":74},{"name":"JGeaQ","marks":12},{"name":"wz54b","marks":99},{"name":"wGvFULmfva","marks":85},{"name":"1ms5JVSx","marks":31},{"name":"cn","marks":26},{"name":"zXV1f","marks":41},{"name":"NjG2pigUO","marks":48},{"name":"7FASdNnN","marks":32},{"name":"jGd","marks":49},{"name":"yCrmq1kL3","marks":18},{"name":"m","marks":49},{"name":"UJ10sKHj","marks":79},{"name":"CsBsm","marks":18},{"name":"afDEj","marks":43},{"name":"d","marks":82},{"name":"ES","marks":42},{"name":"Ok1D3vV5AN","marks":48},{"name":"tbG","marks":73},{"name":"qE","marks":26},{"name":"Mog","marks":34},{"name":"2v","marks":38},{"name":"UKY","marks":11},{"name":"C6S4kdJ0S","marks":24},{"name":"Zm3k3","marks":79},{"name":"f","marks":33},{"name":"nfg","marks":30},{"name":"WTzbjsr","marks":44},{"name":"h0Qzdi5fhC","marks":29},{"name":"c8h","marks":21},{"name":"7pO","marks":27},{"name":"9r","marks":63},{"name":"3Ge","marks":6},{"name":"nll4dIX","marks":54},{"name":"FtOey","marks":57},{"name":"rX","marks":33},{"name":"JYLVdeaQ","marks":45},{"name":"M35T","marks":87},{"name":"ye","marks":48},{"name":"79RS","marks":28},{"name":"upEtIl5","marks":93},{"name":"b8","marks":44},{"name":"d05t","marks":68},{"name":"OPTgNx8RK","marks":36},{"name":"43qORDGG","marks":28},{"name":"4","marks":98},{"name":"H","marks":28},{"name":"t4LBhW","marks":55},{"name":"pOj9F","marks":14},{"name":"5","marks":93},{"name":"tZk","marks":7},{"name":"tsSbt","marks":30},{"name":"n","marks":60},{"name":"4Fv","marks":4},{"name":"3ST61zyx","marks":30},{"name":"wMcge0qb1m","marks":57},{"name":"V85i6oOI","marks":61},{"name":"pWEbQ","marks":90},{"name":"dLl","marks":83},{"name":"ugb0ipbwEh","marks":68},{"name":"eONTwG7ME","marks":31},{"name":"YYREw","marks":12},{"name":"CkM14Z8u","marks":65},{"name":"hkI","marks":36},{"name":"FoiM","marks":30},{"name":"h6ld8I","marks":53},{"name":"3KZ47","marks":8},{"name":"caR0x","marks":17},{"name":"7YUqYWrury","marks":87},{"name":"9","marks":91},{"name":"hzXRLKu39","marks":83},{"name":"IINJIgdr","marks":87},{"name":"uBk1yj","marks":40},{"name":"yS1Fl79l","marks":64},{"name":"xXM6fyLsH","marks":76},{"name":"O0i9TO","marks":91},{"name":"t1WYWtI","marks":47},{"name":"Cvyxk","marks":24},{"name":"oVbTt","marks":64},{"name":"S9COB","marks":63},{"name":"TS7obWF6LO","marks":87},{"name":"5V93fvwooP","marks":56},{"name":"hXZeJeR","marks":26},{"name":"0arxwrRY","marks":88},{"name":"CrA","marks":82},{"name":"WwAFRYXw0","marks":72},{"name":"Ijwbv","marks":60},{"name":"UCcXO","marks":84},{"name":"hEHCxZQR","marks":84},{"name":"hDOz","marks":89},{"name":"ao","marks":87},{"name":"Rs8a","marks":27},{"name":"NWkt8","marks":13},{"name":"xiZqMhiz","marks":72}]

student_dict = {s["name"]: s["marks"] for s in student_marks}

@app.get("/api/ga2-q6")
def get_marks(name: List[str] = Query([])):
    marks = [student_dict.get(n, None) for n in name]
    return {"marks": marks}

def load_csv():
    global students_data
    with open('students.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students_data.append({
                'studentId': int(row['studentId']),  # Ensure integer conversion
                'class': row['class']
            })
            
students_data = []

load_csv()

@app.get("/api/ga2-q9")
def get_students(class_: List[str] = Query(None, alias="class")):

    if class_:
        filtered_students = [student for student in students_data if student["class"] in class_]

        return {"students": filtered_students}
    return {"students": students_data}

class SimilarityRequest(BaseModel):
    docs: List[str]
    query: str
    
def generate_embeddings(texts: List[str]) -> List[List[float]]:
    try:
        ai_proxy_token=os.getenv("AI_PROXY_TOKEN")
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/embeddings",
            headers={"Authorization": f"Bearer {ai_proxy_token}"},
            json={"model": "text-embedding-3-small", "input": texts}
        )
        
        response.raise_for_status()
        embedding_data = response.json()

        return [data['embedding'] for data in embedding_data['data']]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

@app.post("/api/ga3-q7/similarity")
async def find_similar_documents(request: SimilarityRequest):
    try:
        # Generate embeddings for query and documents
        query_embedding = generate_embeddings([request.query])[0]
        doc_embeddings = generate_embeddings(request.docs)

        # Compute similarities
        similarities = [
            cosine_similarity(np.array(query_embedding), np.array(doc_embed)) 
            for doc_embed in doc_embeddings
        ]

        # Get indices of top 3 most similar documents
        top_3_indices = sorted(
            range(len(similarities)), 
            key=lambda i: similarities[i], 
            reverse=True
        )[:3]

        # Return top 3 documents
        matches = [request.docs[i] for i in top_3_indices]

        return {"matches": matches}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity search failed: {str(e)}")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_status",
            "description": "Get the status of a particular ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "integer",
                        "description": "Ticket ID number"
                    }
                },
                "required": ["ticket_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_meeting",
            "description": "Schedule a meeting",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date of the meeting"
                    },
                    "time": {
                        "type": "string",
                        "description": "Time of the meeting"
                    },
                    "meeting_room": {
                        "type": "string",
                        "description": "Meeting Room for the meeting"
                    }

                },
                "required": ["date", "time", "meeting_room"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_expense_balance",
            "description": "Shows the expense balance for an employee",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "Employee ID number"
                    }
                },
                "required": ["employee_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_performance_bonus",
            "description": "Calculate the performance bonus for an employee in a given year",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "Employee ID number"
                    },

                    "year": {
                        "type": "integer",
                        "description": "Year"
                    }
                    
                },
                "required": ["employee_id", "year"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    {
        "type": "function",
        "function": {
            "name": "report_office_issue",
            "description": "Report an office issue for a specific department",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_code": {
                        "type": "integer",
                        "description": "Issue Code number"
                    },

                    "department": {
                        "type": "string",
                        "description": "Department for which the issue is reported"
                    }
                },
                "required": ["issue_code", "department"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
]

@app.get("/api/ga3-q8/execute")
async def execute_query(q: str = Query(..., min_length=1)):
    try:
        ai_proxy_token=os.getenv("AI_PROXY_TOKEN")
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {ai_proxy_token}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": q}],
                "tools": tools,
                "tool_choice": "auto",
            },
        )
        
        response.raise_for_status()
        output = response.json()["choices"][0]["message"]

        return {"name": output["tool_calls"][0]["function"]["name"] , "arguments": output["tool_calls"][0]["function"]["arguments"]}
    except HTTPException as e:
        print(f"Error processing query: {str(e)}")
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/wiki/"

# Endpoint to scrape the wikipedia data
@app.get("/api/ga4-q3/outline")
async def get_country_outline(country: str = Query(..., title="Country Name")):
    url = f"{WIKIPEDIA_BASE_URL}{country.replace(' ', '_')}"
    
    # Fetch Wikipedia page
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to fetch Wikipedia page"}

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    # Generate Markdown Outline
    markdown_outline = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])  # Extract heading level (h1 -> 1, h2 -> 2, etc.)
        markdown_outline += f"{'#' * level} {heading.text.strip()}\n\n"

    return {"country": country, "outline": markdown_outline}


