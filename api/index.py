from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import os
from .quantity_shade import parse_quantity, shade_for

app = FastAPI(docs_url=None, redoc_url=None)

# Vercel will inject this environment variable securely
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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
        # Clamping shade to max 1.0 (Fixing the bug you found in code review)
        shade = min(shade, 1.0)
        return {"tag": "measured", "shade": shade, "rule": 1}

    # Rule 3: LLM Aisle Classification
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=20,
            system="You are a grocery classifier. Categorize the given item into exactly one of these five aisles: produce, dairy, bakery, frozen, household. Return ONLY the single word of the aisle, nothing else in lowercase.",
            messages=[{"role": "user", "content": item}]
        )
        aisle = response.content[0].text.strip().lower()
        
        valid_aisles = {"produce", "dairy", "bakery", "frozen", "household"}
        if aisle not in valid_aisles:
            aisle = "household" 

        return {"tag": aisle, "shade": None, "rule": 3}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="LLM Classification failed")