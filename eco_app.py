import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Config & Theme
# -----------------------------
st.set_page_config(
    page_title="EcoGuide 🌱",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for fresh, card-based design
st.markdown("""
<style>
/* Gradient background */
.stApp {
    background: linear-gradient(145deg, #f0f9f0 0%, #d4e9d4 100%);
    font-family: 'Segoe UI', Roboto, sans-serif;
}

/* Main container styling */
.main .block-container {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(8px);
    border-radius: 2rem;
    padding: 2rem 2rem 2rem 2rem;
    box-shadow: 0 20px 40px rgba(0, 40, 0, 0.1);
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* Headers */
h1, h2, h3 {
    color: #1e4a1e;
    font-weight: 600;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.5);
    border-radius: 1rem;
    padding: 1rem 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 30, 0, 0.05);
    border: 1px solid rgba(100, 150, 100, 0.2);
    backdrop-filter: blur(4px);
}

/* Recommendation cards */
.reco-card {
    background: rgba(255, 255, 255, 0.7);
    border-radius: 1.5rem;
    padding: 1rem 1.5rem;
    margin: 0.5rem 0;
    border: 1px solid #bcd9b4;
    box-shadow: 0 4px 10px rgba(0, 30, 0, 0.1);
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}
.reco-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 20px rgba(30, 80, 30, 0.15);
    background: rgba(255, 255, 255, 0.9);
    border-color: #5f9e6b;
}
.reco-emoji {
    font-size: 2.5rem;
    background: #d9ead3;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.reco-text {
    flex: 1;
}
.reco-text p {
    margin: 0;
    font-size: 1.1rem;
}
.reco-reduction {
    font-weight: 700;
    color: #1d6b2c;
    background: #e2f0da;
    padding: 0.3rem 1rem;
    border-radius: 2rem;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar Inputs (with icons)
# -----------------------------
st.sidebar.markdown("## 🌿 Your Habits")
st.sidebar.markdown("---")

diet = st.sidebar.selectbox(
    "🥗 Diet Type",
    ["Meat", "Vegetarian", "Vegan"],
    help="Meat-based diets have the highest footprint."
)

daily_travel = st.sidebar.slider(
    "🚗 Daily Travel (km)", 0, 50, 10,
    help="Total kilometers you travel per day on average."
)

transport = st.sidebar.selectbox(
    "🚲 Transport Mode",
    ["Car", "Bike", "Walk"],
    help="Main way you get around."
)

electricity = st.sidebar.slider(
    "💡 Electricity Usage (kWh/day)", 0, 50, 15,
    help="Average daily kilowatt-hours consumed."
)

recycling = st.sidebar.selectbox(
    "♻️ Do You Recycle?",
    ["Yes", "No"],
    help="Recycling can reduce your waste-related emissions."
)

st.sidebar.markdown("---")
st.sidebar.caption("Adjust the sliders and see your impact live!")

# -----------------------------
# Carbon Emission Calculation
# -----------------------------
# Constants (kg CO₂ per unit)
co2_car_per_km = 0.21
co2_bike_per_km = 0.05
co2_walk_per_km = 0.0
co2_meat_per_week = 27
co2_veg_per_week = 10
co2_vegan_per_week = 5
co2_electricity_per_kwh = 0.5

# Transport CO₂ (weekly)
if transport == "Car":
    transport_co2 = daily_travel * co2_car_per_km * 7
elif transport == "Bike":
    transport_co2 = daily_travel * co2_bike_per_km * 7
else:
    transport_co2 = 0.0

# Diet CO₂ (weekly)
if diet == "Meat":
    diet_co2 = co2_meat_per_week
elif diet == "Vegetarian":
    diet_co2 = co2_veg_per_week
else:
    diet_co2 = co2_vegan_per_week

# Electricity CO₂ (weekly)
electricity_co2 = electricity * co2_electricity_per_kwh * 7

# Recycling factor (10% reduction if recycling)
recycle_factor = 0.9 if recycling == "Yes" else 1.0

# Total weekly CO₂
total_co2 = (transport_co2 + diet_co2 + electricity_co2) * recycle_factor

# -----------------------------
# Recommendations (with emoji icons)
# -----------------------------
recommendations = []

# Diet suggestions
if diet == "Meat":
    recommendations.append({
        "Action": "Switch to Vegetarian or Vegan Diet",
        "CO2 Reduction": 20,
        "Emoji": "🌾"
    })
elif diet == "Vegetarian":
    recommendations.append({
        "Action": "Try Vegan Meals Occasionally",
        "CO2 Reduction": 10,
        "Emoji": "🌱"
    })

# Transport suggestions
if transport == "Car":
    recommendations.append({
        "Action": "Use Bike or Walk for Short Trips",
        "CO2 Reduction": round(transport_co2 * 0.7, 1),
        "Emoji": "🚲"
    })
elif transport == "Bike":
    recommendations.append({
        "Action": "Walk Sometimes to Reduce Even More CO₂",
        "CO2 Reduction": round(transport_co2 * 0.3, 1),
        "Emoji": "🚶"
    })

# Electricity suggestions
if electricity > 20:
    recommendations.append({
        "Action": "Reduce Electricity Usage / Switch to Renewables",
        "CO2 Reduction": 15,
        "Emoji": "💡"
    })

# Recycling suggestions
if recycling == "No":
    recommendations.append({
        "Action": "Start Recycling to Reduce Waste CO₂",
        "CO2 Reduction": round(total_co2 * 0.1, 1),
        "Emoji": "♻️"
    })

# Convert to DataFrame for charts
rec_df = pd.DataFrame(recommendations)

# -----------------------------
# Main UI - Header & Metrics
# -----------------------------
st.title("🌱 EcoGuide – Your Personal Carbon Coach")
st.markdown("Track your weekly footprint and discover simple steps to **go greener**.")

# Top-level metric with progress bar
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total CO₂", f"{total_co2:.1f} kg/week")
with col2:
    st.metric("Diet", f"{diet_co2:.1f} kg")
with col3:
    st.metric("Transport", f"{transport_co2:.1f} kg")

# Progress bar (relative to 100 kg baseline)
st.progress(min(total_co2 / 100, 1.0))
st.caption(f"Your footprint is **{total_co2:.1f} kg CO₂/week** – typical is around 100 kg. Keep improving!")

# -----------------------------
# Breakdown Donut Chart
# -----------------------------
st.subheader("📊 Where your emissions come from")
breakdown = pd.DataFrame({
    "Category": ["Diet", "Transport", "Electricity"],
    "CO₂ (kg)": [diet_co2, transport_co2, electricity_co2]
})

fig_donut = px.pie(
    breakdown,
    values="CO₂ (kg)",
    names="Category",
    hole=0.5,
    color_discrete_sequence=["#7fb77f", "#5f9e6b", "#2d6a4f"],
    title="Weekly CO₂ Breakdown"
)
fig_donut.update_traces(textposition="inside", textinfo="percent+label")
fig_donut.update_layout(
    showlegend=False,
    margin=dict(t=40, b=0, l=0, r=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#1e4a1e")
)
st.plotly_chart(fig_donut, use_container_width=True)

# -----------------------------
# Recommendations as Cards
# -----------------------------
st.subheader("💚 Personalized tips for you")

if rec_df.empty:
    st.info("You're already doing great! Check back if you change your habits.")
else:
    for _, row in rec_df.iterrows():
        # Use custom HTML for card layout
        st.markdown(f"""
        <div class="reco-card">
            <div class="reco-emoji">{row['Emoji']}</div>
            <div class="reco-text">
                <p style="font-weight:600;">{row['Action']}</p>
            </div>
            <div class="reco-reduction">-{row['CO2 Reduction']:.1f} kg</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Interactive Reduction Chart
# -----------------------------
if not rec_df.empty:
    st.subheader("📉 Potential CO₂ reduction per action")
    fig_bar = px.bar(
        rec_df,
        x="Action",
        y="CO2 Reduction",
        color="CO2 Reduction",
        color_continuous_scale="Greens",
        labels={"CO2 Reduction": "kg CO₂ saved per week"},
        hover_data={"Action": True, "CO2 Reduction": ":.1f"}
    )
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="kg CO₂/week",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1e4a1e")
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("🌍 Every small step counts – start today and inspire others!")