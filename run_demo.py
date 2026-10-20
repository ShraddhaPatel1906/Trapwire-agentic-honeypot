"""
TrapWire - Interactive CLI Demo Runner
Executes the full Agentic Honeypot + MCP + Sandboxed Execution Pipeline.
"""
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent.workflow import trapwire_agent

def print_banner():
    print("=" * 70)
    print("  TRAPWIRE — Autonomous Anti-Phishing Honeypot & Threat Neutralizer")
    print("  Stack: LangGraph Agentic AI | Model Context Protocol | Docker Sandbox")
    print("=" * 70)

def run_simulation(target_url: str):
    print_banner()
    print(f"\n[*] Target Suspicious URL: {target_url}\n")
    print("[*] Initializing Agentic State Machine...")
    time.sleep(1)

    initial_state = {
        "target_url": target_url,
        "sandbox_result": None,
        "is_phishing": False,
        "confidence_score": 0.0,
        "decoy_payload": None,
        "mcp_intel": None,
        "takedown_receipt": None,
        "audit_logs": []
    }

    # Execute LangGraph Pipeline
    final_state = trapwire_agent.invoke(initial_state)

    print("\n" + "-" * 70)
    print("                 LIVE AGENTIC AUDIT TRAIL LOGS")
    print("-" * 70)
    for log in final_state.get("audit_logs", []):
        print(f"  {log}")

    print("\n" + "=" * 70)
    print("                   INCIDENT RESOLUTION REPORT")
    print("=" * 70)
    print(f"  Target URL      : {final_state['target_url']}")
    print(f"  Phishing Verdict: {'MALICIOUS (High Threat)' if final_state['is_phishing'] else 'BENIGN'}")
    print(f"  Confidence Score: {final_state['confidence_score']}%")

    if final_state.get("decoy_payload"):
        print("\n  [+] Injected Honey-Decoy Bait (Dataset Poisoning):")
        for k, v in final_state["decoy_payload"].items():
            print(f"      - {k}: {v}")

    if final_state.get("mcp_intel"):
        mcp = final_state["mcp_intel"]
        print("\n  [+] Threat Infrastructure Discovered via MCP Protocol:")
        print(f"      - Hosting IP    : {mcp.get('network', {}).get('ip_address')}")
        print(f"      - Registrar     : {mcp.get('whois', {}).get('registrar')}")
        print(f"      - Abuse Desk    : {mcp.get('whois', {}).get('abuse_email')}")
        print(f"      - SSL Warning   : {mcp.get('ssl', {}).get('details')}")

    if final_state.get("takedown_receipt"):
        tkdn = final_state["takedown_receipt"]
        print("\n  [+] Automated Takedown Action:")
        print(f"      - Ticket ID     : {tkdn.get('receipt_id')}")
        print(f"      - Status        : {tkdn.get('status')}")
        print(f"      - Dispatched To : {tkdn.get('dispatched_to')}")

    print("\n" + "=" * 70)
    print("  [SUCCESS] Mission Accomplished. Threat Neutralized Autonomously.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    test_url = sys.argv[1] if len(sys.argv) > 1 else "http://secure-login-hdfcbank-verification.com/auth"
    run_simulation(test_url)
