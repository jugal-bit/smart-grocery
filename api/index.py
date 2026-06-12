from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from .quantity_shade import parse_quantity, shade_for

app = FastAPI(docs_url=None, redoc_url=None)

# Configure Gemini with the key from Vercel
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

class GroceryItem(BaseModel):
    item: str

@app.post("/api/classify")
async def classify_item(payload: GroceryItem):
    item = payload.item.strip().lower()
    
    # Rule 2: Staples (Wins over everything)
    staples = {"salt", "sugar", "flour", "rice", "oil"}
    if any(staple in item for staple in staples):
        return {"tag": "staple", "shade": None, "rule": 2}

    # Rule 1: Quantity and Unit
    parsed = parse_quantity(item)
    if parsed is not None:
        shade = shade_for(item)
        shade = min(shade, 1.0)
        return {"tag": "measured", "shade": shade, "rule": 1}

    # Rule 3: LLM Aisle Classification using Gemini

   # Rule 3: LLM Aisle Classification using Gemini
    try:
        system_prompt = "You are a grocery classifier. Categorize the given item into exactly one of these five aisles: produce, dairy, bakery, frozen, household. Return ONLY the single word of the aisle, nothing else in lowercase."
        
        response = model.generate_content(f"{system_prompt}\n\nItem: {item}")
        aisle = response.text.strip().lower()
        
        valid_aisles = {"produce", "dairy", "bakery", "frozen", "household"}
        if aisle not in valid_aisles:
            aisle = "household" 

        return {"tag": aisle, "shade": None, "rule": 3}
        
    except Exception as e:
        # TRICK: Return the error as a 200 OK response so React prints it on the screen!
        error_msg = str(e)[:25] # Cut it to 25 characters so it fits in the badge
        return {"tag": f"API ERR: {error_msg}", "shade": None, "rule": 3}