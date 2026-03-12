"""
Travel Planning Agent — Streamlit Demo
Run: streamlit run app.py
"""

import streamlit as st
from orchestrator import run_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Travel Planning Agent",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Styles ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { max-width: 760px; padding-top: 2rem; }
  h1 { font-size: 2rem !important; }
  .agent-badge {
    display: inline-block; padding: 2px 10px; border-radius: 4px;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em;
    text-transform: uppercase; margin-right: 6px;
  }
  .badge-green  { background: #d1fae5; color: #065f46; }
  .badge-amber  { background: #fef3c7; color: #92400e; }
  .badge-purple { background: #ede9fe; color: #5b21b6; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("✈️ Travel Planning Agent")
st.caption("A multi-agent AI system · Hotel Search + Flight Search + Budget Optimizer with Retry Loop")
st.divider()

# ── Example prompts ──────────────────────────────────────────────────────────
EXAMPLES = [
    "Plan a 10-day trip to Japan in April under $3,000 for 2 people, focused on food and culture.",
    "I want a 7-day trip to Italy for 1 person, budget $2,000, interested in history and art.",
    "Plan a 5-day Thailand trip for 2 people under $1,500, beach and food focus.",
]

st.markdown("**Try an example or type your own:**")
cols = st.columns(3)
for i, ex in enumerate(EXAMPLES):
    if cols[i].button(f"Example {i+1}", key=f"ex{i}", use_container_width=True):
        st.session_state["user_input"] = ex

# ── Input ────────────────────────────────────────────────────────────────────
user_input = st.text_area(
    "Your travel request",
    value=st.session_state.get("user_input", ""),
    placeholder="e.g. Plan a 10-day trip to Japan in April under $3,000 for 2 people...",
    height=80,
    label_visibility="collapsed",
)

run = st.button("🗺️ Plan my trip", type="primary", use_container_width=True)

# ── Pipeline execution ────────────────────────────────────────────────────────
if run and user_input.strip():
    with st.spinner("Running agents..."):

        # Show live agent status
        status = st.empty()
        status.markdown("**🤖 Agent pipeline running...**")

        import time
        steps = [
            ("Trip Planner Agent", "Parsing intent and extracting constraints..."),
            ("Hotel Search Agent", "Searching accommodation options..."),
            ("Flight Search Agent", "Searching flight routes..."),
            ("Budget Optimizer", "Scoring combinations and checking budget..."),
        ]
        progress = st.progress(0)
        for idx, (agent, msg) in enumerate(steps):
            status.markdown(f"**{agent}** — {msg}")
            progress.progress((idx + 1) / len(steps))
            time.sleep(0.5)

        result = run_pipeline(user_input)
        status.empty()
        progress.empty()

    # ── Constraints parsed ──────────────────────────────────────────────────
    c = result["constraints"]
    st.subheader("📋 Parsed Constraints")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Destination", c.get("destination", "—"))
    col2.metric("Duration", f"{c.get('duration_days', '—')} days")
    col3.metric("Budget", f"${c.get('budget_usd', '—'):,}")
    col4.metric("Travelers", c.get("travelers", "—"))
    if c.get("interests"):
        st.caption("Interests detected: " + ", ".join(c["interests"]))

    st.divider()

    # ── Retry loop info ─────────────────────────────────────────────────────
    retries = result.get("retries_needed", 0)
    budget_met = result.get("budget_met", False)

    if retries == 0 and budget_met:
        st.markdown('<span class="agent-badge badge-green">✓ Budget met on first pass</span>', unsafe_allow_html=True)
    elif retries > 0 and budget_met:
        st.markdown(f'<span class="agent-badge badge-amber">↺ Budget met after {retries} retry cycle(s)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="agent-badge badge-purple">⚠ Best-effort plan — budget could not be fully met</span>', unsafe_allow_html=True)

    # Show retry history in expander
    if result.get("retry_history"):
        with st.expander("🔁 View retry loop details", expanded=(retries > 0)):
            for h in result["retry_history"]:
                st.markdown(f"""
**Cycle {h['cycle']}** — Hotel ceiling: **${h['hotel_ceiling']}/night** · Flight ceiling: **${h['flight_ceiling_per_person']}/person** · Budget carriers: {'Yes' if h['allow_budget_carriers'] else 'No'}
→ Found {h['hotels_found']} hotels, {h['flights_found']} flights, scored {h['combinations_scored']} combinations.
""")

    # ── Recommendation ──────────────────────────────────────────────────────
    if result["success"]:
        rec = result["recommendation"]
        st.subheader("🏆 Top Recommendation")

        col_h, col_f = st.columns(2)

        with col_h:
            st.markdown("#### 🏨 Hotel")
            st.markdown(f"**{rec['hotel']['name']}**")
            st.caption(f"{rec['hotel']['location']} · {'⭐' * rec['hotel']['stars']} · {rec['hotel']['rating']}/5")
            st.metric("Total Hotel Cost", f"${rec['hotel']['total_hotel_cost']:,.0f}",
                      f"${rec['hotel']['price_per_night']}/night")
            for h in rec["hotel"]["highlights"]:
                st.markdown(f"• {h}")

        with col_f:
            st.markdown("#### ✈️ Flight")
            st.markdown(f"**{rec['flight']['airline']}**")
            st.caption(f"{rec['flight']['route']} · {rec['flight']['stops']} stop(s) · Departs {rec['flight']['departure_date']}")
            st.metric("Total Flight Cost", f"${rec['flight']['total_flight_cost']:,.0f}",
                      f"${rec['flight']['price_per_person']}/person")
            for h in rec["flight"]["highlights"]:
                st.markdown(f"• {h}")

        st.divider()

        # Budget summary
        col_t, col_r = st.columns(2)
        col_t.metric("Total Trip Cost", f"${rec['total_cost']:,.0f}", f"Budget: ${rec['budget']:,}")
        remaining = rec["remaining_budget"]
        col_r.metric(
            "Remaining Budget",
            f"${abs(remaining):,.0f}",
            "under budget ✓" if remaining >= 0 else "over budget ✗",
            delta_color="normal" if remaining >= 0 else "inverse",
        )

        # ── Itinerary ───────────────────────────────────────────────────────
        st.subheader("📅 Day-by-Day Itinerary")
        itinerary = result.get("itinerary", [])
        for item in itinerary:
            st.markdown(f"**Day {item['day']}** — {item['activity']}")

    else:
        st.error(result.get("message", "Something went wrong. Please try again."))

elif run and not user_input.strip():
    st.warning("Please enter a travel request first.")

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption("Built by [@amaan-x8](https://github.com/amaan-x8) · [View on GitHub](https://github.com/amaan-x8/travel-planning-agent) · PM Portfolio Project")
