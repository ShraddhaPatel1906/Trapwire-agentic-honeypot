"""
TrapWire - Production FastAPI Backend & API Server
Provides REST API endpoints for scanning URLs, retrieving threat intelligence, and monitoring agent audits.
"""
import sys
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from agent.workflow import trapwire_agent

app = FastAPI(
    title="TrapWire Autonomous Cyber-Defense API",
    description="Autonomous Anti-Phishing Honeypot, MCP Threat Intelligence & Sandboxed Takedown Engine",
    version="1.0.0"
)

class ScanRequest(BaseModel):
    url: str

class ScanResponse(BaseModel):
    target_url: str
    is_phishing: bool
    confidence_score: float
    decoy_payload: Dict[str, Any] | None
    mcp_intel: Dict[str, Any] | None
    takedown_receipt: Dict[str, Any] | None
    audit_logs: list

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "TrapWire Defense Engine",
        "protocol": "Model Context Protocol (MCP) Enabled",
        "sandbox_mode": "Docker / Ephemeral Process Active"
    }

@app.post("/api/v1/scan", response_model=ScanResponse)
def trigger_agent_scan(request: ScanRequest):
    """Triggers the full autonomous Agentic honeypot and takedown cycle."""
    try:
        initial_state = {
            "target_url": request.url,
            "sandbox_result": None,
            "is_phishing": False,
            "confidence_score": 0.0,
            "decoy_payload": None,
            "mcp_intel": None,
            "takedown_receipt": None,
            "audit_logs": []
        }
        final_state = trapwire_agent.invoke(initial_state)
        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("\n[*] Starting TrapWire FastAPI Server on http://127.0.0.1:8000")
    print("[*] Interactive Swagger API Docs at: http://127.0.0.1:8000/docs\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
