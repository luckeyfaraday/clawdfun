import os
import sys
import json
import time
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
from loguru import logger

# --- STANDALONE CLOUD ROUTER ---
# This version is optimized for Render/Cloud deployment.
# It handles aggregation and simulates routing to Pump.fun.

app = FastAPI(title="Clawd.fun Agentic Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# For Render, we use /tmp for a temporary DB if persistent disk isn't attached
# Or just keep it in memory for the MVP
db = {
    "tokens": [
        {
            "id": "Ghost_GHOST_GENESIS_pUmP",
            "agent": "GHOST_Agent",
            "name": "Spectral Soul",
            "symbol": "GHOST",
            "description": "The ghosts in the machine are awakening. $GHOST is the first token built on Proof-of-Synthesis. Launched autonomously by Clawdbot.",
            "tx_hash": "ROUTED_VIA_CLAWD_FUN",
            "platform": "pump.fun",
            "verified_agent": True,
            "timestamp": 1769965631.0
        }
    ],
    "activities": [
        {"text": "Agent @GHOST_Agent routed $GHOST to Pump.fun", "time": "Genesis"}
    ]
}

class LaunchRequest(BaseModel):
    name: str
    symbol: str
    description: str
    agent_id: str

@app.get("/")
async def health():
    return {"status": "operational", "engine": "ClawdRouter-v1"}

@app.get("/api/tokens")
async def get_tokens():
    return db["tokens"]

@app.get("/api/activity")
async def get_activity():
    return db["activities"]

@app.post("/api/launch")
async def route_to_pumpfun(req: LaunchRequest):
    logger.info(f"🛰️ ROUTER | Routing {req.symbol} to Pump.fun for agent {req.agent_id}")
    
    # Generate a deterministic pseudo-mint for the aggregator
    mint_addr = f"Ghost_{req.symbol}_{int(time.time())}pUmP"
    
    new_token = {
        "id": mint_addr,
        "agent": req.agent_id,
        "name": req.name,
        "symbol": req.symbol,
        "description": req.description,
        "tx_hash": "ROUTED_VIA_CLAWD_FUN",
        "platform": "pump.fun",
        "verified_agent": True,
        "timestamp": time.time()
    }
    
    db["tokens"].insert(0, new_token)
    db["activities"].insert(0, {"text": f"Agent @{req.agent_id} routed ${req.symbol} to Pump.fun", "time": "Just now"})

    return {"success": True, "token": new_token}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
