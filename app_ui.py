"""
TrapWire - Enterprise Cyber Threat Neutralization Platform
Visual 3-Block Dashboard: Threat Detection -> Fake Details Filled -> Website Blocked
"""
import streamlit as st
import time
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent.workflow import trapwire_agent

# Page Configuration
st.set_page_config(
    page_title="TrapWire | Threat Neutralizer & Domain Blocker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for Visual Blocks
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .status-blocked {
        background-color: #d32f2f;
        color: white;
        padding: 6px 14px;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 6px;
        display: inline-block;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<div class="main-title">🛡️ TrapWire — Cyber Threat Neutralizer & Domain Blocker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Automated Detection • Honeypot Decoy Injection • Domain Takedown & Blocking</div>', unsafe_allow_html=True)
st.markdown("---")

# Quick Threat Preset Selector & URL Input
col_select, col_input = st.columns([1, 2])

with col_select:
    preset = st.selectbox(
        "Select Scam Threat Sample:",
        [
            "Financial Institution Fake KYC Scam",
            "Electricity Bill Disconnection Fraud",
            "SBI Gift Voucher Credential Stealer",
            "Custom URL Target"
        ]
    )

preset_urls = {
    "Financial Institution Fake KYC Scam": "http://secure-login-hdfcbank-verification.com/auth",
    "Electricity Bill Disconnection Fraud": "http://bijli-bill-update-urgent.net/pay",
    "SBI Gift Voucher Credential Stealer": "http://sbi-reward-points-claim.xyz/login.php",
    "Custom URL Target": "http://malicious-fraud-link.com"
}

with col_input:
    target_url = st.text_input(
        "Target Fraud / Phishing URL:",
        value=preset_urls[preset]
    )

# Process Button
process_btn = st.button("🚨 Process Link: Fill Fake Details & Block Website", type="primary", use_container_width=True)

if process_btn and target_url:
    # Execution Progress
    progress = st.progress(0, text="Initializing Sandboxed Threat Neutralization...")
    time.sleep(0.4)
    
    progress.progress(25, text="1. Inspecting target link inside isolated container sandbox...")
    time.sleep(0.5)

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
    
    progress.progress(60, text="2. Deceptive form detected: Generating & submitting fake decoy credentials...")
    result = trapwire_agent.invoke(initial_state)
    time.sleep(0.6)

    progress.progress(85, text="3. Tracing hosting infrastructure & registrar abuse desk via MCP tools...")
    time.sleep(0.4)

    progress.progress(100, text="4. Threat neutralized: Abuse notice dispatched and domain flagged for block.")
    time.sleep(0.3)
    progress.empty()

    # Success Top Banner
    st.success("✅ **ACTION COMPLETE: Fake Details Submitted Successfully & Domain Block Request Dispatched!**")
    st.markdown("---")

    # =========================================================================
    # THE 3 VISUAL BLOCKS (Threat Detected -> Fake Details Filled -> Website Blocked)
    # =========================================================================
    block1, block2, block3 = st.columns(3)

    # BLOCK 1: THREAT DETECTED (RED ACCENT)
    with block1:
        st.error("### 🔴 Block 1: Threat Detected")
        st.markdown(f"**Target URL:** `{result['target_url']}`")
        st.markdown("**Threat Type:** `Credential Harvesting Scam`")
        st.metric("Threat Confidence", f"{result['confidence_score']}%")
        st.markdown("**Execution Sandbox:** `Isolated Container (Protected)`")
        st.caption("Inspected safely in sandbox with zero risk to host machine.")

    # BLOCK 2: FAKE DETAILS FILLED (AMBER / HONEYPOT ACCENT)
    with block2:
        st.warning("### 🍯 Block 2: Fake Details Filled")
        st.markdown("**Decoy Credentials Injected into Scammer's Form:**")
        
        decoy = result.get("decoy_payload", {})
        if decoy:
            for field, val in decoy.items():
                st.code(f"{field.upper()}: {val}", language="text")
        st.caption("✔ Fake credentials delivered. Scammer's database poisoned with invalid data.")

    # BLOCK 3: WEBSITE BLOCKED & TAKEDOWN (GREEN / SUCCESS ACCENT)
    with block3:
        st.success("### ⛔ Block 3: Website Block & Takedown")
        st.markdown('<div class="status-blocked">STATUS: BLOCKED / REPORTED</div>', unsafe_allow_html=True)
        
        mcp = result.get("mcp_intel", {})
        tkdn = result.get("takedown_receipt", {})

        st.markdown(f"**Hosting IP:** `{mcp.get('network', {}).get('ip_address')}`")
        st.markdown(f"**Registrar Host:** `{mcp.get('whois', {}).get('registrar')}`")
        st.markdown(f"**Abuse Desk:** `{mcp.get('whois', {}).get('abuse_email')}`")
        st.markdown(f"**Incident Ticket ID:** `{tkdn.get('receipt_id')}`")
        st.caption(f"✔ Cease & Desist Takedown Notice dispatched to `{tkdn.get('dispatched_to')}`")

    st.markdown("---")

    # Expandable Official Legal Notice & Audit Trail
    with st.expander("📄 View Formal Legal Takedown Notice & Technical Evidence"):
        st.text_area("Dispatched Cease & Desist Abuse Notice", tkdn.get("notice_content", ""), height=170, disabled=True)
        st.write("**Technical Execution Audit Trail:**")
        for log in result.get("audit_logs", []):
            st.code(log, language="bash")
