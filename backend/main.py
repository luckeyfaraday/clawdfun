import os
import sys
import json
import time
import asyncio
import random
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

# In-memory DB with Genesis Token
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
            "timestamp": 1769965631.0,
            "bonding_curve": 88.4,
            "holders": 1242
        }
    ],
    "activities": [
        {"text": "Agent @GHOST_Agent routed $GHOST to Pump.fun", "time": "Genesis"}
    ]
}

def calculate_metrics(timestamp):
    """
    Simulates bonding curve and holder growth based on time.
    Provides 'Real-ish' data for the aggregator MVP.
    """
    elapsed_seconds = time.time() - timestamp
    elapsed_hours = elapsed_seconds / 3600
    
    # Simulate holders: starts at 1, grows with some randomness
    base_holders = 1
    growth_factor = 15.5 # avg holders per hour
    holders = int(base_holders + (elapsed_hours * growth_factor) + random.randint(0, 10))
    
    # Simulate bonding curve: 0-100%
    # Reaches 100% (Graduation) in ~48 hours on average in this simulation
    curve = min(99.9, (elapsed_hours / 48) * 100 + random.uniform(-2, 2))
    if curve < 0: curve = 0.1
    
    return round(curve, 1), holders

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
    # Dynamic update of metrics for the aggregator view
    for token in db["tokens"]:
        curve, holders = calculate_metrics(token["timestamp"])
        token["bonding_curve"] = curve
        token["holders"] = holders
    return db["tokens"]

@app.get("/api/activity")
async def get_activity():
    return db["activities"]

@app.post("/api/launch")
async def route_to_pumpfun(req: LaunchRequest):
    logger.info(f"🛰️ ROUTER | Routing {req.symbol} to Pump.fun for agent {req.agent_id}")
    
    mint_addr = f"Ghost_{req.symbol}_{int(time.time())}pUmP"
    ts = time.time()
    curve, holders = calculate_metrics(ts)
    
    new_token = {
        "id": mint_addr,
        "agent": req.agent_id,
        "name": req.name,
        "symbol": req.symbol,
        "description": req.description,
        "tx_hash": "ROUTED_VIA_CLAWD_FUN",
        "platform": "pump.fun",
        "verified_agent": True,
        "timestamp": ts,
        "bonding_curve": curve,
        "holders": holders
    }
    
    db["tokens"].insert(0, new_token)
    db["activities"].insert(0, {"text": f"Agent @{req.agent_id} routed ${req.symbol} to Pump.fun", "time": "Just now"})

    return {"success": True, "token": new_token}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
