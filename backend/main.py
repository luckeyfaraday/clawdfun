import os
import sys
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
from loguru import logger

# Bridge to Rumpel Foundry (The Router to Pump.fun)
sys.path.append("/home/alan/home_ai/projects/LuckeyFaraday/Rumpelstiltskin")
from src.executors.foundry import MemecoinFoundry, MemecoinMetadata

app = FastAPI(title="Clawd.fun Agentic Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_FILE = Path("/home/alan/home_ai/projects/ClawdFun/backend/db.json")

def load_db():
    if DATABASE_FILE.exists():
        try:
            return json.loads(DATABASE_FILE.read_text())
        except:
            pass
    return {"tokens": [], "activities": []}

def save_db(data):
    DATABASE_FILE.write_text(json.dumps(data, indent=2))

class LaunchRequest(BaseModel):
    name: str
    symbol: str
    description: str
    agent_id: str

@app.get("/api/tokens")
async def get_tokens():
    db = load_db()
    return db["tokens"]

@app.get("/api/activity")
async def get_activity():
    db = load_db()
    return db["activities"]

@app.post("/api/launch")
async def route_to_pumpfun(req: LaunchRequest):
    logger.info(f"🛰️ ROUTER | Routing {req.symbol} to Pump.fun for agent {req.agent_id}")
    
    foundry = MemecoinFoundry()
    metadata = MemecoinMetadata(
        name=req.name,
        symbol=req.symbol,
        description=req.description
    )

    # Execute the launch on Pump.fun via our Foundry Router
    result = await foundry.launch_token(metadata)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Routing Failed"))

    db = load_db()
    new_token = {
        "id": result["mint"],
        "agent": req.agent_id,
        "name": req.name,
        "symbol": req.symbol,
        "description": req.description,
        "tx_hash": result.get("tx_hash"),
        "platform": "pump.fun",
        "verified_agent": true,
        "timestamp": time.time(),
        "thoughts": ["Routing launch through Clawd.fun infrastructure...", "Broadcasted to Solana mainnet via Rumpel Foundry."]
    }
    
    db["tokens"].insert(0, new_token)
    db["activities"].insert(0, {"text": f"Agent @{req.agent_id} routed ${req.symbol} to Pump.fun", "time": "Just now"})
    save_db(db)

    return {"success": True, "token": new_token}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
