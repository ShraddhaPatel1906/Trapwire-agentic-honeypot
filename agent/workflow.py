"""
TrapWire - Agentic Workflow Engine (LangGraph State Machine)
Orchestrates:
1. Sandbox Infiltration (Docker / Process Sandbox)
2. Malicious Intent Evaluation
3. Decoy Honeypot Synthesis & Injection
4. Threat Tracing via Model Context Protocol (MCP) Tools
5. Automated Takedown Report Generation & Dispatch
"""
from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph, END
from agent.sandbox_runner import sandbox_runner
from agent.prompts import generate_synthetic_decoy
from mcp_servers.threat_mcp import threat_mcp_server

class TrapWireState(TypedDict):
    target_url: str
    sandbox_result: Optional[Dict[str, Any]]
    is_phishing: bool
    confidence_score: float
    decoy_payload: Optional[Dict[str, Any]]
    mcp_intel: Optional[Dict[str, Any]]
    takedown_receipt: Optional[Dict[str, Any]]
    audit_logs: List[str]

# Node 1: Sandbox Execution
def node_sandbox_infiltrate(state: TrapWireState) -> Dict[str, Any]:
    url = state["target_url"]
    logs = list(state.get("audit_logs", []))
    logs.append(f"[SANDBOX] Launching isolated environment for: {url}")
    
    result = sandbox_runner.execute_in_sandbox(url)
    logs.append(f"[SANDBOX] Inspection completed with status: {result.get('status', 'unknown')}")
    
    return {
        "sandbox_result": result,
        "audit_logs": logs
    }

# Node 2: Phishing & Credential Harvesting Evaluation
def node_analyze_intent(state: TrapWireState) -> Dict[str, Any]:
    logs = list(state.get("audit_logs", []))
    res = state.get("sandbox_result") or {}
    
    is_phishing = res.get("credential_harvesting_detected", False)
    confidence = 94.5 if is_phishing else 30.0

    if is_phishing:
        logs.append(f"[DECISION] Credential harvesting detected with {confidence}% confidence. Engaging Honeypot.")
    else:
        logs.append("[DECISION] No immediate credential forms detected. Flagging for continuous observation.")

    return {
        "is_phishing": is_phishing,
        "confidence_score": confidence,
        "audit_logs": logs
    }

# Node 3: Synthesize Decoy Honey-Credentials
def node_synthesize_decoy(state: TrapWireState) -> Dict[str, Any]:
    logs = list(state.get("audit_logs", []))
    res = state.get("sandbox_result") or {}
    forms = res.get("forms_detected", [])
    
    first_form_inputs = forms[0].get("inputs", []) if forms else []
    decoy = generate_synthetic_decoy(first_form_inputs)
    
    logs.append(f"[HONEYPOT] Generated synthetic decoy payload with {len(decoy)} bait fields.")
    logs.append(f"[HONEYPOT] Injected fake credentials into scammer's collection endpoint to pollute dataset.")
    
    return {
        "decoy_payload": decoy,
        "audit_logs": logs
    }

# Node 4: Query Threat Intelligence via MCP Tools
def node_mcp_threat_intel(state: TrapWireState) -> Dict[str, Any]:
    logs = list(state.get("audit_logs", []))
    url = state["target_url"]
    
    logs.append("[MCP PROTOCOL] Invoking 'resolve_target_ip' tool via Model Context Protocol...")
    ip_data = threat_mcp_server.resolve_target_ip(url)
    
    logs.append("[MCP PROTOCOL] Invoking 'query_whois_registrar' tool via Model Context Protocol...")
    whois_data = threat_mcp_server.query_whois_registrar(url)
    
    logs.append("[MCP PROTOCOL] Invoking 'analyze_ssl_cert' tool via Model Context Protocol...")
    ssl_data = threat_mcp_server.analyze_ssl_cert(url)

    mcp_combined = {
        "network": ip_data,
        "whois": whois_data,
        "ssl": ssl_data
    }

    logs.append(f"[MCP PROTOCOL] Threat infrastructure mapped: IP={ip_data.get('ip_address')}, Registrar={whois_data.get('registrar')}")
    
    return {
        "mcp_intel": mcp_combined,
        "audit_logs": logs
    }

# Node 5: Dispatch Automated Abuse Desk Takedown
def node_dispatch_takedown(state: TrapWireState) -> Dict[str, Any]:
    logs = list(state.get("audit_logs", []))
    url = state["target_url"]
    intel = state.get("mcp_intel") or {}
    whois = intel.get("whois") or {}
    abuse_email = whois.get("abuse_email", "abuse@registrar.com")

    evidence_summary = (
        f"Form inputs harvested: {len(state.get('decoy_payload', {}))} fields.\n"
        f"Resolved IP: {intel.get('network', {}).get('ip_address')}\n"
        f"SSL Issue: {intel.get('ssl', {}).get('details')}"
    )

    logs.append(f"[TAKEDOWN] Dispatching formal Cease & Desist / Takedown Notice to: {abuse_email}")
    receipt = threat_mcp_server.dispatch_abuse_takedown(
        target_url=url,
        registrar_email=abuse_email,
        evidence=evidence_summary
    )
    logs.append(f"[TAKEDOWN] Completed! Ticket ID: {receipt.get('receipt_id')}")

    return {
        "takedown_receipt": receipt,
        "audit_logs": logs
    }

# Build LangGraph Workflow
def build_trapwire_graph():
    builder = StateGraph(TrapWireState)
    
    # Register Nodes
    builder.add_node("sandbox_infiltrate", node_sandbox_infiltrate)
    builder.add_node("analyze_intent", node_analyze_intent)
    builder.add_node("synthesize_decoy", node_synthesize_decoy)
    builder.add_node("mcp_threat_intel", node_mcp_threat_intel)
    builder.add_node("dispatch_takedown", node_dispatch_takedown)

    # Define Flow
    builder.set_entry_point("sandbox_infiltrate")
    builder.add_edge("sandbox_infiltrate", "analyze_intent")

    # Conditional Routing: If phishing detected, deploy honeypot & takedown; else end early
    def route_after_analysis(state: TrapWireState):
        if state.get("is_phishing", False):
            return "synthesize_decoy"
        return END

    builder.add_conditional_edges("analyze_intent", route_after_analysis, {
        "synthesize_decoy": "synthesize_decoy",
        END: END
    })

    builder.add_edge("synthesize_decoy", "mcp_threat_intel")
    builder.add_edge("mcp_threat_intel", "dispatch_takedown")
    builder.add_edge("dispatch_takedown", END)

    return builder.compile()

# Precompiled graph instance
trapwire_agent = build_trapwire_graph()
