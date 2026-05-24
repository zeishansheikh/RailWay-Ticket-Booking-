# ============================================================
#  app.py  –  Train Ticket Reservation System
#  Run:  streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import datetime

from models import ReservationSystem

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Rail Express",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── General app background ─ */
.stApp {
    background-color: #DBD5CD;
    background-image: radial-gradient(rgba(184, 183, 176, 0.4) 1px, transparent 1px);
    background-size: 25px 25px;
}

/* ── Sidebar ─────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #4A4947 0%, #62445A 100%);
    border-right: 1px solid rgba(184, 183, 176, 0.3);
    box-shadow: 4px 0 15px rgba(0,0,0,0.2);
}
section[data-testid="stSidebar"] * {
    color: #DBD5CD !important;
}
section[data-testid="stSidebar"] h2 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 1.5rem;
    margin-bottom: 2rem;
    text-align: center;
}
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 500;
    padding: 0.5rem 0;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    transform: translateX(8px);
    color: #B1A29F !important;
}

/* ── Main background ─ */
.main .block-container {
    background: transparent;
    padding-top: 2rem;
}

/* ── Hero banner ──── */
.hero {
    background: linear-gradient(135deg, #62445A 0%, #62445A 60%, #B1A29F 100%);
    border-radius: 24px;
    padding: 4rem 3.5rem;
    color: #DBD5CD;
    margin-bottom: 3rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(101, 62, 50, 0.4), inset 0 2px 5px rgba(255,255,255,0.3);
    transform-style: preserve-3d;
    transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    text-align: center;
}
.hero:hover {
    transform: translateY(-8px) scale(1.01) perspective(1000px) rotateX(2deg);
    box-shadow: 0 25px 45px rgba(101, 62, 50, 0.5), inset 0 2px 5px rgba(255,255,255,0.4);
}
.hero::before {
    content: '';
    position: absolute;
    top: -100px; right: -100px;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 100%);
    box-shadow: inset 0 0 50px rgba(0,0,0,0.1);
    transform: translateZ(-10px);
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    letter-spacing: -1px;
    text-transform: uppercase;
    text-shadow: 3px 5px 15px rgba(0,0,0,0.3);
    transform: translateZ(20px);
}
.hero p { 
    margin: 0; 
    opacity: 0.95; 
    font-size: 1.2rem; 
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-shadow: 1px 2px 5px rgba(0,0,0,0.2);
    transform: translateZ(10px);
}

/* ── Cards ─────────── */
.card {
    background: linear-gradient(145deg, #ffffff, #DBD5CD);
    border-radius: 20px;
    padding: 2.2rem;
    box-shadow: 6px 6px 18px rgba(74, 73, 71, 0.05),
               -6px -6px 18px rgba(255, 255, 255, 0.9);
    margin-bottom: 2rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(184, 183, 176, 0.2);
    position: relative;
    z-index: 1;
}
.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 15px 15px 30px rgba(74, 73, 71, 0.1),
               -15px -15px 30px rgba(255, 255, 255, 1);
    z-index: 2;
}
.card h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    margin: 0 0 1.2rem 0;
    color: #62445A;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid rgba(184, 183, 176, 0.3);
    padding-bottom: 0.8rem;
}

/* ── Stat boxes ────── */
.stat-box {
    background: linear-gradient(145deg, #ffffff, #DBD5CD);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    box-shadow: 4px 4px 10px rgba(74, 73, 71, 0.05),
               -4px -4px 10px rgba(255, 255, 255, 0.9);
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(184, 183, 176, 0.2);
}
.stat-box:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 8px 8px 15px rgba(74, 73, 71, 0.1),
               -8px -8px 15px rgba(255, 255, 255, 1);
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #62445A;
    text-shadow: 1px 2px 4px rgba(153, 107, 92, 0.15);
    background: -webkit-linear-gradient(45deg, #62445A, #62445A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.stat-label {
    font-size: 0.75rem;
    color: #4A4947;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
}

/* ── Status badges ── */
.badge-confirmed  { background: linear-gradient(145deg, #62445A, #62445A); color: #fff; padding:6px 16px; border-radius:999px; font-size:.75rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; box-shadow: 2px 3px 8px rgba(101,62,50,0.3); display: inline-block; }
.badge-cancelled  { background: linear-gradient(145deg, #4A4947, #2d2c2b); color: #fff; padding:6px 16px; border-radius:999px; font-size:.75rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; box-shadow: 2px 3px 8px rgba(74,73,71,0.3); display: inline-block; }
.badge-waitlisted { background: linear-gradient(145deg, #B8B7B0, #B1A29F); color: #4A4947; padding:6px 16px; border-radius:999px; font-size:.75rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; box-shadow: 2px 3px 8px rgba(184,183,176,0.4); display: inline-block; }

/* ── Section title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #4A4947;
    margin-bottom: 1.5rem;
    margin-top: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #62445A;
    display: inline-block;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
}

/* ── Route pill ────── */
.route-pill {
    display: inline-block;
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border: 1px solid #B8B7B0;
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 0.8rem;
    color: #4A4947;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 6px 4px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05), inset 1px 1px 2px rgba(255,255,255,1);
    transition: transform 0.3s;
}
.route-pill:hover {
    transform: translateY(-3px);
    box-shadow: 4px 6px 12px rgba(0,0,0,0.08);
}

/* ── Streamlit overrides ── */
div[data-testid="stForm"] {
    background: linear-gradient(145deg, #ffffff, #DBD5CD);
    border-radius: 24px;
    padding: 3.5rem;
    box-shadow: 10px 10px 30px rgba(74, 73, 71, 0.05),
               -10px -10px 30px rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(184, 183, 176, 0.2) !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #62445A, #62445A);
    color: white !important;
    border: none;
    border-radius: 14px;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1rem;
    padding: 0.8rem 3rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 8px 20px rgba(101, 62, 50, 0.25), inset 0 2px 4px rgba(255,255,255,0.2);
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 2px;
}
div.stButton > button::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(to right, rgba(255,255,255,0), rgba(255,255,255,0.25), rgba(255,255,255,0));
    transform: skewX(-25deg);
    transition: all 0.6s ease;
}
div.stButton > button:hover::after {
    left: 150%;
}
div.stButton > button:hover { 
    transform: translateY(-5px) scale(1.03);
    box-shadow: 0 12px 25px rgba(101, 62, 50, 0.35), inset 0 2px 4px rgba(255,255,255,0.2);
}
div.stButton > button:active {
    transform: translateY(2px);
    box-shadow: 0 4px 10px rgba(101, 62, 50, 0.3);
}

div.stButton > button[kind="secondary"] {
    background: linear-gradient(145deg, #ffffff, #DBD5CD);
    color: #62445A !important;
    border: 2px solid #B1A29F;
    box-shadow: 4px 4px 15px rgba(74, 73, 71, 0.05),
               -4px -4px 15px rgba(255, 255, 255, 0.8);
}
div.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(145deg, #DBD5CD, #ffffff);
    border-color: #62445A;
}

/* ── Dark Luxury Cards & Expanders ── */
.card {
    background: linear-gradient(145deg, #62445A, #4a3243) !important;
    color: #DBD5CD !important;
    border: 1px solid rgba(219, 213, 205, 0.2) !important;
}
.card h3, .card span, .card div, .card strong {
    color: #DBD5CD !important;
}

div[data-testid="stExpander"] {
    background: linear-gradient(145deg, #62445A, #4a3243) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(219, 213, 205, 0.2) !important;
    margin-bottom: 1rem !important;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
}
div[data-testid="stExpander"] summary {
    background: transparent !important;
    color: #DBD5CD !important;
    padding: 1.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
}
div[data-testid="stExpander"] summary svg {
    fill: #DBD5CD !important;
    stroke: #DBD5CD !important;
}
div[data-testid="stExpanderDetails"] {
    background: rgba(0,0,0,0.1) !important;
    color: #DBD5CD !important;
    padding: 1.5rem !important;
    border-top: 1px solid rgba(219, 213, 205, 0.1) !important;
}
div[data-testid="stExpanderDetails"] * {
    color: #DBD5CD !important;
}

/* ── Fixing stat box to keep it dark to match theme ── */
.stat-box {
    background: linear-gradient(145deg, #62445A, #4a3243) !important;
    color: #DBD5CD !important;
    border: 1px solid rgba(219, 213, 205, 0.2) !important;
}
.stat-num {
    background: none !important;
    -webkit-text-fill-color: #DBD5CD !important;
    color: #DBD5CD !important;
    text-shadow: 2px 3px 6px rgba(0, 0, 0, 0.3) !important;
}
.stat-label {
    color: rgba(219, 213, 205, 0.8) !important;
}
.route-pill {
    background: rgba(0,0,0,0.2) !important;
    border: 1px solid rgba(219, 213, 205, 0.3) !important;
    color: #DBD5CD !important;
}
div[data-testid="stForm"] {
    background: linear-gradient(145deg, #62445A, #4a3243) !important;
    color: #DBD5CD !important;
    border: 1px solid rgba(219, 213, 205, 0.2) !important;
}
div[data-testid="stForm"] label, div[data-testid="stForm"] p, div[data-testid="stForm"] h3 {
    color: #DBD5CD !important;
}

/* Fix Inputs (Text, Number, Date) to be always visible */
div[data-testid="stTextInput"] input, 
div[data-testid="stNumberInput"] input,
div[data-baseweb="input"] input {
    background-color: #DBD5CD !important;
    color: #4A4947 !important;
    -webkit-text-fill-color: #4A4947 !important;
    border: 1px solid #4A4947 !important;
    border-radius: 6px !important;
}

/* Fix Dropdowns to be always visible */
div[data-baseweb="select"] > div {
    background-color: #DBD5CD !important;
    border-radius: 6px !important;
}
div[data-baseweb="select"] * {
    color: #4A4947 !important;
}

/* Ensure Form Submit Button is styled correctly like other buttons */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #62445A, #4a3243) !important;
    color: #DBD5CD !important;
    border: 1px solid rgba(219, 213, 205, 0.3) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.5rem !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(0,0,0,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
if "system" not in st.session_state:
    st.session_state.system = ReservationSystem()
if "last_msg" not in st.session_state:
    st.session_state.last_msg = None

rs: ReservationSystem = st.session_state.system

# ── Sidebar navigation ────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2>Rail Express</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["Dashboard",
         "Search Trains",
         "Book Ticket",
         "My Bookings",
         "Cancel Ticket",
         "Waiting List",
         "Undo Last Booking"],
        label_visibility="collapsed"
    )

# ── Helper ────────────────────────────────────────────────────
def status_badge(s):
    cls = {"Confirmed": "badge-confirmed",
           "Cancelled": "badge-cancelled",
           "Waitlisted": "badge-waitlisted"}.get(s, "")
    return f'<span class="{cls}">{s}</span>'

def show_msg():
    if st.session_state.last_msg:
        t, m = st.session_state.last_msg
        if t == "success": st.success(m)
        elif t == "error":   st.error(m)
        elif t == "info":    st.info(m)
        elif t == "warning": st.warning(m)
        st.session_state.last_msg = None

# ════════════════════════════════════════════════════════════
#  PAGES
# ════════════════════════════════════════════════════════════

# ── 1. DASHBOARD ─────────────────────────────────────────────
if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>Rail Express</h1>
        <p>Premium Ticket Reservation</p>
    </div>
    """, unsafe_allow_html=True)

    stats = rs.stats()
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, label, val in [
        (c1, "Total Bookings",  stats["total_bookings"]),
        (c2, "Confirmed",       stats["confirmed"]),
        (c3, "Cancelled",       stats["cancelled"]),
        (c4, "Waitlisted",      stats["waitlisted"]),
        (c5, "Revenue (Rs.)",   f"{stats['total_revenue']:,}"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-num">{val}</div>
                <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Available Trains</div>', unsafe_allow_html=True)

    for train in rs.get_all_trains():
        with st.expander(f"{train.name}  |  {train.departure} TO {train.arrival}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Train ID", train.train_id)
            c2.metric("Available Seats", f"{train.available_seats}/{train.total_seats}")
            c3.metric("Price/Seat", f"Rs. {train.price_per_seat}")
            route_pills = " ".join(
                f'<span class="route-pill">{s}</span>' for s in train.route.to_list()
            )
            st.markdown(f"<div style='margin-top:1.5rem'><strong>ROUTE:</strong><br><br>{route_pills}</div>", unsafe_allow_html=True)


# ── 2. SEARCH TRAINS ─────────────────────────────────────────
elif page == "Search Trains":
    st.markdown('<div class="section-title">Search Trains</div>', unsafe_allow_html=True)

    cities = sorted(set(
        [t.departure for t in rs.get_all_trains()] +
        [t.arrival   for t in rs.get_all_trains()]
    ))

    with st.form("search_form"):
        c1, c2 = st.columns(2)
        dep = c1.selectbox("From", cities)
        arr = c2.selectbox("To",   cities)
        submitted = st.form_submit_button("Search")

    if submitted:
        results = rs.search_trains(dep, arr)
        if results:
            st.success(f"Found {len(results)} train(s).")
            for t in results:
                st.markdown(f"""
                <div class="card">
                    <h3>{t.name} <span style='font-size:0.9rem;font-weight:500;color:#B1A29F;margin-left:10px;'>{t.train_id}</span></h3>
                    <div style='font-size:1.1rem; color:#4A4947; margin-bottom:1rem;'>
                        <strong>{t.departure}</strong> &nbsp;TO&nbsp; <strong>{t.arrival}</strong>
                    </div>
                    <div style='margin-bottom:1.5rem;'>
                        <span style='color:#62445A;font-weight:800;font-size:1.2rem;'>Rs. {t.price_per_seat}</span> <span style='font-size:0.8rem;color:#B8B7B0;text-transform:uppercase;'>per seat</span> 
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        <span style='color:#62445A;font-weight:600;'>{t.available_seats}/{t.total_seats} seats available</span>
                    </div>
                    <div>
                        <div style='font-size:0.8rem; color:#4A4947; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;'><strong>Route Path</strong></div>
                        {' '.join(f"<span class='route-pill'>{s}</span>" for s in t.route.to_list())}
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("No trains found for this route.")


# ── 3. BOOK TICKET ────────────────────────────────────────────
elif page == "Book Ticket":
    st.markdown('<div class="section-title">Book a Ticket</div>', unsafe_allow_html=True)
    show_msg()

    trains = rs.get_all_trains()
    train_options = {f"{t.name} ({t.train_id}) — {t.departure} TO {t.arrival}": t.train_id for t in trains}

    with st.form("book_form"):
        c1, c2 = st.columns(2)
        name     = c1.text_input("Passenger Name")
        pid      = c2.text_input("CNIC / Passport No.")
        selected = st.selectbox("Select Train", list(train_options.keys()))
        c3, c4, c5 = st.columns(3)
        seat_class = c3.selectbox("Seat Class", ["Economy", "Business", "First Class"])
        num_seats  = c4.number_input("Number of Seats", 1, 10, 1)
        journey    = c5.date_input("Journey Date", datetime.date.today() + datetime.timedelta(days=1))
        submit     = st.form_submit_button("Confirm Booking")

    if submit:
        if not name.strip() or not pid.strip():
            st.session_state.last_msg = ("error", "Please fill in all fields.")
        else:
            tid = train_options[selected]
            booking, msg = rs.book_ticket(name.strip(), pid.strip(), tid,
                                          seat_class, int(num_seats), journey)
            if booking:
                st.session_state.last_msg = (
                    "success" if booking.status == "Confirmed" else "warning", msg
                )
                # Show booking summary
                st.markdown(f"""
                <div class="card">
                    <h3>Booking Summary</h3>
                    <table style="width:100%; text-align:left; border-collapse:collapse; margin-top:1rem;">
                        <tr style="border-bottom:1px solid rgba(184,183,176,0.2);">
                            <td style="padding:0.8rem 0; color:#B1A29F; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">PNR</td>
                            <td style="padding:0.8rem 0; font-weight:800; color:#4A4947;">{booking.pnr}</td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(184,183,176,0.2);">
                            <td style="padding:0.8rem 0; color:#B1A29F; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">Passenger</td>
                            <td style="padding:0.8rem 0; font-weight:600; color:#62445A;">{booking.passenger_name}</td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(184,183,176,0.2);">
                            <td style="padding:0.8rem 0; color:#B1A29F; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">Train</td>
                            <td style="padding:0.8rem 0; color:#4A4947;">{booking.train.name} ({booking.train.departure} TO {booking.train.arrival})</td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(184,183,176,0.2);">
                            <td style="padding:0.8rem 0; color:#B1A29F; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">Date</td>
                            <td style="padding:0.8rem 0; color:#4A4947;">{booking.journey_date}</td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(184,183,176,0.2);">
                            <td style="padding:0.8rem 0; color:#B1A29F; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">Class & Seats</td>
                            <td style="padding:0.8rem 0; color:#4A4947;">{booking.seat_class} × {booking.num_seats}</td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(184,183,176,0.2);">
                            <td style="padding:0.8rem 0; color:#B1A29F; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">Total Fare</td>
                            <td style="padding:0.8rem 0; font-weight:800; color:#62445A;">Rs. {booking.total_fare:,}</td>
                        </tr>
                        <tr>
                            <td style="padding:1.2rem 0; color:#B1A29F; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">Status</td>
                            <td style="padding:1.2rem 0;">{status_badge(booking.status)}</td>
                        </tr>
                    </table>
                </div>""", unsafe_allow_html=True)
            else:
                st.session_state.last_msg = ("error", msg)
        st.rerun()

    show_msg()


# ── 4. MY BOOKINGS ────────────────────────────────────────────
elif page == "My Bookings":
    st.markdown('<div class="section-title">All Bookings</div>', unsafe_allow_html=True)

    sort_by = st.selectbox("Sort by", ["booking_time", "passenger_name", "journey_date", "fare"])
    bookings = rs.get_all_bookings(sort_by)

    if not bookings:
        st.info("No bookings yet.")
    else:
        rows = []
        for b in bookings:
            rows.append({
                "PNR": b.pnr,
                "Passenger": b.passenger_name,
                "Train": b.train.name,
                "Route": f"{b.train.departure} TO {b.train.arrival}",
                "Class": b.seat_class,
                "Seats": b.num_seats,
                "Date": b.journey_date,
                "Fare (Rs.)": b.total_fare,
                "Status": b.status,
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("**Detailed View**")
        for b in bookings:
            with st.expander(f"{b.pnr}  |  {b.passenger_name}  |  {b.status}"):
                c1, c2 = st.columns(2)
                c1.write(f"**Train:** {b.train.name}")
                c1.write(f"**Route:** {b.train.departure} TO {b.train.arrival}")
                c1.write(f"**Journey:** {b.journey_date}")
                c2.write(f"**Class:** {b.seat_class} × {b.num_seats}")
                c2.write(f"**Fare:** Rs. {b.total_fare:,}")
                c2.markdown(f"**Status:** {status_badge(b.status)}", unsafe_allow_html=True)


# ── 5. CANCEL TICKET ─────────────────────────────────────────
elif page == "Cancel Ticket":
    st.markdown('<div class="section-title">Cancel Ticket</div>', unsafe_allow_html=True)
    show_msg()

    with st.form("cancel_form"):
        pnr = st.text_input("Enter PNR Number")
        sub = st.form_submit_button("Cancel Booking")

    if sub:
        if not pnr.strip():
            st.session_state.last_msg = ("error", "Enter a PNR.")
        else:
            ok, msg = rs.cancel_ticket(pnr.strip().upper())
            st.session_state.last_msg = ("success" if ok else "error", msg)
        st.rerun()

    show_msg()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("**Quick PNR Lookup**")
    lookup = st.text_input("Search PNR", key="lookup")
    if lookup:
        b = rs.get_booking(lookup.strip().upper())
        if b:
            st.markdown(f"""
            <div class="card">
                <h3>{b.pnr}</h3>
                <div style="color:#4A4947; line-height:1.8;">
                    <strong>Passenger:</strong> {b.passenger_name}<br>
                    <strong>Train:</strong> {b.train.name} ({b.train.departure} TO {b.train.arrival})<br>
                    <strong>Date:</strong> {b.journey_date} &nbsp;|&nbsp; <strong>Fare:</strong> Rs. {b.total_fare:,}<br><br>
                    {status_badge(b.status)}
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("PNR not found.")


# ── 6. WAITING LIST ───────────────────────────────────────────
elif page == "Waiting List":
    st.markdown('<div class="section-title">Waiting List</div>', unsafe_allow_html=True)

    waiting = rs.get_waiting_list()
    if not waiting:
        st.info("No passengers on the waiting list.")
    else:
        st.markdown(f"**{len(waiting)} passenger(s) waiting**")
        for i, b in enumerate(waiting, 1):
            st.markdown(f"""
            <div class="card">
                <h3>#{i} — {b.passenger_name}</h3>
                <div style="color:#4A4947; line-height:1.8;">
                    <strong>PNR:</strong> {b.pnr}<br>
                    <strong>Train:</strong> {b.train.name} | {b.train.departure} TO {b.train.arrival}<br>
                    <strong>Date:</strong> {b.journey_date} | <strong>Seats:</strong> {b.num_seats} | <strong>Fare:</strong> Rs. {b.total_fare:,}
                </div>
            </div>""", unsafe_allow_html=True)


# ── 7. UNDO LAST BOOKING ──────────────────────────────────────
elif page == "Undo Last Booking":
    st.markdown('<div class="section-title">Undo Last Booking</div>', unsafe_allow_html=True)
    show_msg()

    stats = rs.stats()
    st.info(f"Booking history depth: **{stats['history_depth']}** entries available to undo.")

    if st.button("Undo Last Booking"):
        b, msg = rs.undo_last_booking()
        if b:
            st.session_state.last_msg = ("success", f"{msg} (PNR: {b.pnr})")
        else:
            st.session_state.last_msg = ("warning", msg)
        st.rerun()

    show_msg()
