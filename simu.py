import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="🌦️ Weather Simulation (Div, Curl, Gradient)", layout="wide")
st.title("🌦️ Vector Field Simulation: Gradient, Divergence & Curl")

st.markdown("""
Visualize how air behaves in weather-like conditions:
- **Gradient** → air moves from high to low pressure  
- **Divergence** → air spreads out or converges  
- **Curl** → air rotates (like cyclones)
""")

# --- Controls ---
mode = st.sidebar.selectbox(
    "Choose Simulation Type:",
    ["Gradient (Pressure Field)", "Divergence (Air Outflow/Inflow)", "Curl (Cyclonic Motion)"]
)
speed = st.sidebar.slider("Animation Speed", 0.05, 0.5, 0.2, 0.05)
density = st.sidebar.slider("Grid Density", 10, 30, 20, 2)

# --- Grid ---
x = np.linspace(-2, 2, density)
y = np.linspace(-2, 2, density)
X, Y = np.meshgrid(x, y)

# --- Compute Vector Field ---
def get_vectors(t):
    if mode == "Gradient (Pressure Field)":
        P = np.exp(-X**2 - Y**2)
        dPx, dPy = np.gradient(P)
        U, V = -dPx, -dPy
    elif mode == "Divergence (Air Outflow/Inflow)":
        U = X * np.cos(t) - Y * np.sin(t)
        V = Y * np.cos(t) + X * np.sin(t)
    else:  # Curl
        U = -Y * np.cos(t)
        V = X * np.sin(t)
    return U, V

# --- Animation Frames ---
frames = []
for t in np.linspace(0, 2*np.pi, 40):
    U, V = get_vectors(t)
    frames.append(go.Frame(
        data=[go.Scatter(
            x=X.flatten(),
            y=Y.flatten(),
            mode="markers",
            marker=dict(
                size=4,
                color=np.sqrt(U**2 + V**2).flatten(),
                colorscale="Viridis",
                showscale=False,
            ),
            hoverinfo='none'
        ),
        go.Cone(
            x=X.flatten(),
            y=Y.flatten(),
            z=np.zeros_like(X).flatten(),
            u=U.flatten(),
            v=V.flatten(),
            w=np.zeros_like(U).flatten(),
            sizemode="absolute",
            sizeref=0.3,
            showscale=False
        )]
    ))

# --- Figure ---
fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        xaxis=dict(range=[-2, 2], title="X"),
        yaxis=dict(range=[-2, 2], title="Y"),
        margin=dict(l=0, r=0, t=30, b=0),
        width=700,
        height=600,
        title=mode,
        updatemenus=[{
            "buttons": [
                {"label": "▶️ Play", "method": "animate",
                 "args": [None, {"frame": {"duration": int(1000*speed), "redraw": True}, "fromcurrent": True}]},
                {"label": "⏸️ Pause", "method": "animate", "args": [[None], {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}]}
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 10},
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 1.1,
            "yanchor": "top"
        }]
    ),
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)
st.caption("🌀 Visualize how vector calculus governs atmospheric motion — from pressure gradients to cyclones.")
