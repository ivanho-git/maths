import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import tempfile
import plotly.graph_objects as go

# --- Streamlit config ---
st.set_page_config(page_title="🌦️ Weather Simulation Lab", layout="wide")

st.title("🌦️ Weather Simulation Lab — Gradient, Divergence & Curl in NWP")
st.markdown("""
Explore **Numerical Weather Prediction (NWP)** simulations interactively.
These simulations show how **gradient, divergence, and curl** explain atmospheric phenomena like **winds, storms, and cyclones**.
""")

# --- Sidebar controls ---
view_mode = st.sidebar.radio("Select View Mode:", ["2D Animation", "3D Interactive"])
field_mode = st.sidebar.radio("Select Vector Field:", 
                              ["Gradient (Pressure Field)", "Divergence (Air Outflow/Inflow)", "Curl (Cyclonic Motion)"])

show_heatmap = st.sidebar.checkbox("Show Divergence/Convergence Heatmap (2D only)", value=True)

# --- Common grid ---
n = 20
x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)
X, Y = np.meshgrid(x, y)

# --- Compute vector field ---
def compute_field(t=0):
    if field_mode == "Gradient (Pressure Field)":
        P = np.exp(-X**2 - Y**2)
        dPx, dPy = np.gradient(P)
        U, V = -dPx, -dPy
        divergence = np.gradient(U, axis=1) + np.gradient(V, axis=0)
        curl = np.gradient(V, axis=1) - np.gradient(U, axis=0)
    elif field_mode == "Divergence (Air Outflow/Inflow)":
        U = X * np.cos(t) - Y * np.sin(t)
        V = Y * np.cos(t) + X * np.sin(t)
        divergence = np.gradient(U, axis=1) + np.gradient(V, axis=0)
        curl = np.gradient(V, axis=1) - np.gradient(U, axis=0)
    else:  # Curl / Vorticity
        U = -Y * np.cos(t)
        V = X * np.sin(t)
        divergence = np.gradient(U, axis=1) + np.gradient(V, axis=0)
        curl = np.gradient(V, axis=1) - np.gradient(U, axis=0)
    return U, V, divergence, curl

# =====================================================================
# 2D Animated Simulation
# =====================================================================
if view_mode == "2D Animation":
    fig, ax = plt.subplots(figsize=(6, 6))
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

# =====================================================================
# 3D Interactive Simulation
# =====================================================================
else:
    n3 = 10
    x3 = np.linspace(-2, 2, n3)
    y3 = np.linspace(-2, 2, n3)
    z3 = np.linspace(-2, 2, n3)
    X3, Y3, Z3 = np.meshgrid(x3, y3, z3)

    if field_mode == "Gradient (Pressure Field)":
        Phi = np.exp(-X3**2 - Y3**2 - Z3**2)
        U = -2 * X3 * Phi
        V = -2 * Y3 * Phi
        W = -2 * Z3 * Phi
    elif field_mode == "Divergence (Air Outflow/Inflow)":
        U = X3
        V = Y3
        W = Z3
    else:  # Curl / Vorticity
        U = -Y3
        V = X3
        W = np.sin(np.sqrt(X3**2 + Y3**2))

    fig3 = go.Figure(data=go.Cone(
        x=X3.flatten(), y=Y3.flatten(), z=Z3.flatten(),
        u=U.flatten(), v=V.flatten(), w=W.flatten(),
        colorscale="Viridis", sizemode="absolute", sizeref=0.5,
        showscale=False
    ))

    fig3.update_layout(
        scene=dict(
            xaxis=dict(title="X"), yaxis=dict(title="Y"), zaxis=dict(title="Z"),
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        title=f"{field_mode} (3D Field)"
    )
    st.plotly_chart(fig3, use_container_width=True)

# =====================================================================
# Theory, Equations, and Weather Explanation
# =====================================================================
st.markdown("---")
st.header("📘 Theory Behind the Simulation")

st.markdown("""
Numerical Weather Prediction (NWP) models use **gradient, divergence, and curl** to compute air motion:

- **Gradient (∇P)**: Drives air from high → low pressure (wind formation).  
- **Divergence (∇·V)**: Air spreading/converging; identifies cloud formation & rainfall.  
- **Curl (∇×V)**: Measures vorticity; forecasts cyclones, tornadoes, and rotational systems.
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
st.info("💡 Switch between 2D & 3D to connect mathematical concepts with real-world weather predictions.")
