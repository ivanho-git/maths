import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import matplotlib.animation as animation
import tempfile
import plotly.graph_objects as go

# --- Streamlit page config ---
st.set_page_config(page_title="🌦️ Weather Simulation Lab", layout="wide")
st.title("🌦️ Weather Simulation Lab — Gradient, Divergence & Curl")

st.markdown("""
Explore **Numerical Weather Prediction (NWP)** interactively.
See how **gradient, divergence, and curl** explain winds, storms, and cyclones.
""")

# --- Sidebar controls ---
view_mode = st.sidebar.radio("Select View Mode:", ["2D Animation", "3D Animation", "Particle Animation"])
field_mode = st.sidebar.radio("Select Vector Field:", 
                              ["Gradient (Pressure Field)", "Divergence (Air Outflow/Inflow)", "Curl (Cyclonic Motion)"])
show_heatmap = st.sidebar.checkbox("Show Heatmap (2D only)", value=True)
magnitude = st.sidebar.slider("Field Magnitude", 0.1, 5.0, 1.0)

# --- Grid setup ---
n = 20
x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)
X, Y = np.meshgrid(x, y)

# --- Function to compute vector fields ---
def compute_field(t=0):
    if field_mode == "Gradient (Pressure Field)":
        P = np.exp(-X**2 - Y**2)
        dPx, dPy = np.gradient(P)
        U, V = -magnitude*dPx, -magnitude*dPy
    elif field_mode == "Divergence (Air Outflow/Inflow)":
        U = magnitude * (X * np.cos(t) - Y * np.sin(t))
        V = magnitude * (Y * np.cos(t) + X * np.sin(t))
    else:  # Curl
        U = -magnitude * Y * np.cos(t)
        V = magnitude * X * np.sin(t)
    divergence = np.gradient(U, axis=1) + np.gradient(V, axis=0)
    curl = np.gradient(V, axis=1) - np.gradient(U, axis=0)
    return U, V, divergence, curl

# -------------------------------
# 2D Animation (Matplotlib quiver)
# -------------------------------
if view_mode == "2D Animation":
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title(field_mode, fontsize=14)
    ax.set_aspect('equal')
    ax.axis('off')

    U, V, divergence, curl = compute_field(0)
    quiver = ax.quiver(X, Y, U, V, color='dodgerblue', pivot='mid', scale=15, width=0.007)

    if show_heatmap:
        div_img = ax.imshow(divergence, extent=[-2,2,-2,2], origin='lower', cmap='RdBu', alpha=0.5)
        plt.colorbar(div_img, ax=ax, fraction=0.046, pad=0.04, label='Divergence')

    def update(frame):
        U, V, divergence, curl = compute_field(frame * 0.2)
        quiver.set_UVC(U, V)
        if show_heatmap:
            div_img.set_data(divergence)
        return quiver,

    ani = animation.FuncAnimation(fig, update, frames=60, interval=100, blit=False)
    
    with tempfile.NamedTemporaryFile(suffix=".gif") as tmpfile:
        ani.save(tmpfile.name, writer=PillowWriter(fps=20))
        tmpfile.seek(0)
        gif_bytes = tmpfile.read()

    st.image(gif_bytes, caption=f"{field_mode} (2D Animated Field)", use_container_width=True)

# -------------------------------
# Particle Animation (Plotly)
# -------------------------------
elif view_mode == "Particle Animation":
    num_particles = 200
    px = np.random.uniform(-2,2,num_particles)
    py = np.random.uniform(-2,2,num_particles)
    dt = 0.1
    n_frames = 60

    frames = []
    for f in range(n_frames):
        U, V, _, _ = compute_field(f*0.1)
        ix = np.clip(((px + 2)/4 * (n-1)).astype(int), 0, n-1)
        iy = np.clip(((py + 2)/4 * (n-1)).astype(int), 0, n-1)
        vx = U[iy, ix]
        vy = V[iy, ix]
        px += vx*dt
        py += vy*dt
        px = np.mod(px+2, 4)-2
        py = np.mod(py+2, 4)-2
        frames.append(go.Frame(data=[go.Scatter(x=px, y=py, mode='markers',
                                                marker=dict(color='blue', size=5))]))

    fig = go.Figure(
        data=[go.Scatter(x=px, y=py, mode='markers', marker=dict(color='blue', size=5))],
        layout=go.Layout(
            xaxis=dict(range=[-2,2]),
            yaxis=dict(range=[-2,2]),
            title=f"{field_mode} - Particle Animation",
            updatemenus=[dict(type="buttons",
                              buttons=[dict(label="▶️ Play",
                                            method="animate",
                                            args=[None, {"frame":{"duration":50,"redraw":True},
                                                         "fromcurrent":True}])])]
        ),
        frames=frames
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 3D Animation (Plotly Cone)
# -------------------------------
else:
    n3 = 8
    x3 = np.linspace(-2, 2, n3)
    y3 = np.linspace(-2, 2, n3)
    z3 = np.linspace(-2, 2, n3)
    X3, Y3, Z3 = np.meshgrid(x3, y3, z3)

    frames = []
    for t in np.linspace(0, 2*np.pi, 20):
        if field_mode == "Gradient (Pressure Field)":
            Phi = np.exp(-X3**2 - Y3**2 - Z3**2)
            U = -2 * X3 * Phi * magnitude
            V = -2 * Y3 * Phi * magnitude
            W = -2 * Z3 * Phi * magnitude
        elif field_mode == "Divergence (Air Outflow/Inflow)":
            U = X3 * np.cos(t) - Y3 * np.sin(t)
            V = Y3 * np.cos(t) + X3 * np.sin(t)
            W = Z3 * np.sin(t)
        else:
            U = -Y3 * np.cos(t)
            V = X3 * np.sin(t)
            W = np.sin(np.sqrt(X3**2 + Y3**2))
        frames.append(go.Frame(data=[go.Cone(
            x=X3.flatten(), y=Y3.flatten(), z=Z3.flatten(),
            u=U.flatten(), v=V.flatten(), w=W.flatten(),
            colorscale="Viridis", sizemode="absolute", sizeref=0.5, showscale=False
        )], name=f"t={t:.2f}"))

    fig3 = go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            scene=dict(xaxis=dict(range=[-2,2]), yaxis=dict(range=[-2,2]), zaxis=dict(range=[-2,2]), aspectmode="cube"),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                buttons=[dict(label="▶️ Play",
                              method="animate",
                              args=[None, {"frame": {"duration":100, "redraw": True}, "fromcurrent": True}])])]
        ),
        frames=frames
    )
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Theory & Math
# -------------------------------
st.markdown("---")
st.header("📘 Theory Behind the Simulation")
st.markdown("""
Numerical Weather Prediction (NWP) models use **gradient, divergence, and curl** to compute air motion:

- **Gradient (∇P):** Drives air from high → low pressure (wind formation)  
- **Divergence (∇·V):** Air spreading/converging; identifies cloud formation & rainfall  
- **Curl (∇×V):** Measures vorticity; forecasts cyclones, tornadoes, and rotational systems
""")

st.subheader("Mathematical Formulas in NWP")
if field_mode == "Gradient (Pressure Field)":
    st.latex(r"\vec{F} = -\frac{1}{\rho} \nabla P")
elif field_mode == "Divergence (Air Outflow/Inflow)":
    st.latex(r"\nabla \cdot \vec{V} = \frac{\partial U}{\partial x} + \frac{\partial V}{\partial y} + \frac{\partial W}{\partial z}")
else:
    st.latex(r"\nabla \times \vec{V} = \text{Curl}(\vec{V})")

st.markdown("""
These operators are calculated at **every grid point** in NWP simulations, which then predict:
- Wind patterns  
- Cloud formation & precipitation  
- Cyclones & storms  
- Overall weather system evolution
""")
st.info("💡 Switch between 2D, 3D, and Particle Animation to connect mathematical concepts with real-world weather predictions.")
