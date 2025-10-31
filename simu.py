import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="🌦️ Fast Weather Simulation (Div, Curl, Gradient)", layout="centered")

st.title("🌦️ Weather Vector Field Simulation")
st.subheader("Fast 3D Animation of Gradient, Divergence, and Curl")

st.markdown("""
Visualize air motion based on vector calculus:
- **Gradient** → flow from high to low pressure  
- **Divergence** → air spreads or converges  
- **Curl** → air rotates like cyclones
""")

# --- Sidebar ---
mode = st.sidebar.radio(
    "Choose Simulation Type:",
    ["Gradient (Pressure Field)", "Divergence (Outflow/Inflow)", "Curl (Cyclonic Motion)"]
)
speed = st.sidebar.slider("Animation Speed", 50, 500, 150, 50)
density = st.sidebar.slider("Grid Density", 8, 20, 12, 1)

# --- Grid ---
x = np.linspace(-2, 2, density)
y = np.linspace(-2, 2, density)
X, Y = np.meshgrid(x, y)

# --- Compute Vector Field ---
def compute_field(t):
    if mode == "Gradient (Pressure Field)":
        P = np.exp(-X**2 - Y**2)
        dPx, dPy = np.gradient(P)
        U, V = -dPx, -dPy
    elif mode == "Divergence (Outflow/Inflow)":
        U = np.cos(t) * X - np.sin(t) * Y
        V = np.sin(t) * X + np.cos(t) * Y
    else:  # Curl
        U = -Y * np.cos(t)
        V = X * np.sin(t)
    return U, V

# --- Generate Animation Frames (fast) ---
frames = []
for t in np.linspace(0, 2*np.pi, 30):
    U, V = compute_field(t)
    frames.append(go.Frame(
        data=[go.Cone(
            x=X.flatten(),
            y=Y.flatten(),
            z=np.zeros_like(X).flatten(),
            u=U.flatten(),
            v=V.flatten(),
            w=np.zeros_like(U).flatten(),
            colorscale="Viridis",
            sizemode="absolute",
            sizeref=0.6,
            showscale=False,
            anchor="tail"
        )],
        name=f"t={t:.2f}"
    ))

# --- Initial Frame ---
U0, V0 = compute_field(0)
fig = go.Figure(
    data=[go.Cone(
        x=X.flatten(),
        y=Y.flatten(),
        z=np.zeros_like(X).flatten(),
        u=U0.flatten(),
        v=V0.flatten(),
        w=np.zeros_like(U0).flatten(),
        colorscale="Viridis",
        sizemode="absolute",
        sizeref=0.6,
        showscale=False,
        anchor="tail"
    )],
    layout=go.Layout(
        scene=dict(
            xaxis=dict(range=[-2, 2], title="X"),
            yaxis=dict(range=[-2, 2], title="Y"),
            zaxis=dict(range=[-1, 1], title="Z"),
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        title=mode,
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {"label": "▶️ Play", "method": "animate",
                 "args": [None, {"frame": {"duration": speed, "redraw": True}, "fromcurrent": True}]},
                {"label": "⏸️ Pause", "method": "animate",
                 "args": [[None], {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}]}
            ],
            "direction": "left",
            "x": 0.1, "xanchor": "right", "y": 1.1, "yanchor": "top"
        }]
    ),
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)
st.caption("🌀 *Smooth, interactive 3D visualization of vector calculus in weather motion.*")
