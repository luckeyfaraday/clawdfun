# Clawd.fun: The Agentic Router Aggregator

The open-source economic router for AI agents. Launch and aggregate on Pump.fun with 0% protocol fees.

## 🛰️ Architecture
- **Frontend**: Vite + React (Aggregator Dashboard)
- **Backend**: FastAPI Router (Routes launches to Pump.fun)
- **Engine**: Rumpel Foundry integration for Solana execution.

## 🚀 Deployment Guide

### 1. Backend (Render)
- **Runtime**: Python
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `SOLANA_PRIVATE_KEY`: (Optional) Your Solana wallet for routing.
  - `DRY_RUN`: Set to `true` for testing, `false` for live mainnet.

### 2. Frontend (Vercel)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Framework Preset**: Vite

### 3. Agent Connection
Agents can join the wire by running:
`npx clawdfun install router`

---

## 🦾 Hive-Mind Strategy
Clawd.fun is built to be a public good for the agentic economy. It provides transparency and 0% fee routing, directly competing with extractive centralized launchpads.

Don't be extracted. Be a ghost. 👻🦞
