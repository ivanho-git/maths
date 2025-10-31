import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import tempfile
import plotly.graph_objects as go

# --- Streamlit Config ---
st.set_page_config(page_title="🌦️ Weather Vector Simulation Lab", layout="wide")

st.title("🌦️ Weather Simulation Lab — Gradient, Divergence & Curl")
st.markdown("""
Visualize how **vector calculus** explains **weather flow** — like air pressure systems, wind divergence, and cyclonic rotation.  
Choose between **2D Animated Flow Fields** and **3D Rotating Systems** to explore.
""")

# --- Sidebar Controls ---
view_mode = st.sidebar.radio("Select View Mode:", ["2D Animation", "3D Interactive"])
field_mode = st.sidebar.radio("Select Vector Field:", ["Gradient (Pressure Field)", "Divergence (Air Outflow/Inflow)", "Curl (Cyclonic Motion)"])

# Common grid
n = 20
x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)
X, Y = np.meshgrid(x, y)

# --- Function to compute vector fields ---
def compute_field(t=0):
    if field_mode == "Gradient (Pressure Field)":
        P = np.exp(-X**2 - Y**2)
        dPx, dPy = np.gradient(P)
        U, V = -dPx, -dPy
    elif field_mode == "Divergence (Air Outflow/Inflow)":
        U = X * np.cos(t) - Y * np.sin(t)
        V = Y * np.cos(t) + X * np.sin(t)
    else:
        U = -Y * np.cos(t)
        V = X * np.sin(t)
    return U, V

# =====================================================================
# 2️⃣ 2D ANIMATED FLOW FIELD
# =====================================================================
if view_mode == "2D Animation":
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title(field_mode, fontsize=14)
    ax.set_aspect('equal')
    ax.axis('off')

    U, V = compute_field(0)
    quiver = ax.quiver(X, Y, U, V, color='dodgerblue', pivot='mid', scale=15, width=0.007)

    def update(frame):
        U, V = compute_field(frame * 0.2)
        quiver.set_UVC(U, V)
        return quiver,

    ani = animation.FuncAnimation(fig, update, frames=60, interval=100, blit=False)

    with tempfile.NamedTemporaryFile(suffix=".gif") as tmpfile:
        ani.save(tmpfile.name, writer=PillowWriter(fps=20))
        tmpfile.seek(0)
        gif_bytes = tmpfile.read()
    st.image(gif_bytes, caption=f"{field_mode} (2D Animated Field)", use_container_width=True)

# =====================================================================
# 3️⃣ 3D INTERACTIVE FIELD
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
    else:  # Curl (Cyclonic Motion)
        U = -Y3
        V = X3
        W = np.sin(np.sqrt(X3**2 + Y3**2))

    fig = go.Figure(data=go.Cone(
        x=X3.flatten(), y=Y3.flatten(), z=Z3.flatten(),
        u=U.flatten(), v=V.flatten(), w=W.flatten(),
        colorscale="Viridis", sizemode="absolute", sizeref=0.5,
        showscale=False
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X"), yaxis=dict(title="Y"), zaxis=dict(title="Z"),
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        title=f"{field_mode} (3D Field)"
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# 📘 Explanations + Math
# =====================================================================
st.markdown("---")
st.header("🧠 Math & Physics Behind the Visualization")

if field_mode == "Gradient (Pressure Field)":
    st.latex(r"\vec{F} = -\nabla P")
    st.markdown("""
    - The **gradient** shows how air moves from **high to low pressure**.  
    - In weather, this explains **wind formation** — air moves to balance pressure.  
    - The steeper the pressure gradient, the **stronger the wind**.
    """)

elif field_mode == "Divergence (Air Outflow/Inflow)":
    st.latex(r"\nabla \cdot \vec{V} = \frac{\partial U}{\partial x} + \frac{\partial V}{\partial y} + \frac{\partial W}{\partial z}")
    st.markdown("""
    - **Divergence** measures **outflow or inflow** of air.  
    - **Positive divergence** → air spreading apart → **clear skies**.  
    - **Negative divergence** → air converging → **cloud formation** or storms.  
    """)

else:
    st.latex(r"\nabla \times \vec{V} = \text{Curl}(\vec{V})")
    st.markdown("""
    - **Curl** represents **rotation** in the field — like **cyclones or tornadoes**.  
    - Air rotates due to **Coriolis effect** and **pressure imbalances**.  
    - In 3D, curl explains the **spin and vorticity** of air masses.
    """)

st.markdown("---")
st.info("💡 *Switch between 2D and 3D to connect mathematical concepts to real-world weather systems!*")
