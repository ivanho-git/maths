
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="🌦️ Weather Simulation (Div, Curl, Gradient)", layout="centered")

st.title("🌦️ Animated Weather Simulation")
st.subheader("Understand Gradient, Divergence, and Curl using Motion Fields")

st.markdown("""
Select a simulation below to visualize how air moves according to:
- **Gradient** → air flows from high to low pressure
- **Divergence** → air spreads or converges
- **Curl** → air rotates (like cyclones)
""")

# --- Sidebar Controls ---
mode = st.sidebar.radio(
    "Choose Simulation Type:",
    ["Gradient (Pressure Field)", "Divergence (Air Outflow/Inflow)", "Curl (Cyclonic Motion)"]
)

frames = 25
n = 25
x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)
X, Y = np.meshgrid(x, y)

def compute_field(t):
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

# Create animation frames
fig_frames = []
for t in np.linspace(0, 2 * np.pi, frames):
    U, V = compute_field(t)
    fig_frames.append(
        go.Frame(
            data=[go.Streamtube(
                x=X.flatten(),
                y=Y.flatten(),
                z=np.zeros_like(X).flatten(),
                u=U.flatten(),
                v=V.flatten(),
                w=np.zeros_like(U).flatten(),
                sizeref=0.5,
                colorscale="Viridis",
                showscale=False,
                opacity=0.7
            )],
            name=f"t={t:.2f}"
        )
    )

fig = go.Figure(
    data=fig_frames[0].data,
    layout=go.Layout(
        scene=dict(
            xaxis=dict(range=[-2, 2]),
            yaxis=dict(range=[-2, 2]),
            zaxis=dict(range=[-1, 1]),
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        title=mode,
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="▶️ Play", method="animate", args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}])]
        )]
    ),
    frames=fig_frames
)
