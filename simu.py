import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Streamlit page config ---
st.set_page_config(page_title="🌦️ Weather Flow Simulation", layout="centered")
st.title("🌦️ Animated Weather Simulation (Div, Curl, Gradient)")
st.write("""
Visualize **Gradient**, **Divergence**, and **Curl** as vector fields.
This animation shows how air might move in different weather patterns:
- **Gradient** → air flows from high to low pressure  
- **Divergence** → air spreads or converges  
- **Curl** → air rotates (like a cyclone)
""")

# --- Sidebar controls ---
mode = st.sidebar.radio(
    "Choose Simulation Type:",
    ["Gradient (Pressure Field)", "Divergence (Air Outflow/Inflow)", "Curl (Cyclonic Motion)"]
)

# --- Grid setup ---
n = 20
x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)
X, Y = np.meshgrid(x, y)

# --- Function to compute the field ---
def compute_field(t):
    if mode == "Gradient (Pressure Field)":
        P = np.exp(-X**2 - Y**2)
        dPx, dPy = np.gradient(P)
        U, V = -dPx, -dPy
    elif mode == "Divergence (Air Outflow/Inflow)":
        U = X * np.cos(t) - Y * np.sin(t)
        V = Y * np.cos(t) + X * np.sin(t)
    else:  # Curl (Cyclonic Motion)
        U = -Y * np.cos(t)
        V = X * np.sin(t)
    return U, V

# --- Create figure ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title(mode, fontsize=14)
ax.set_aspect('equal')
ax.axis('off')

# Initial field
U, V = compute_field(0)
quiver = ax.quiver(X, Y, U, V, color='dodgerblue', pivot='mid', scale=15, width=0.007)

# --- Animation update ---
def update(frame):
    U, V = compute_field(frame * 0.2)
    quiver.set_UVC(U, V)
    return quiver,

ani = animation.FuncAnimation(fig, update, frames=60, interval=100, blit=False)

# --- Display animation in Streamlit ---
from matplotlib.animation import PillowWriter
import io

buf = io.BytesIO()
ani.save(buf, format='gif', writer=PillowWriter(fps=20))
st.image(buf.getvalue(), caption=f"{mode} Simulation", use_container_width=True)

st.markdown("---")
st.markdown("🧭 *Animated vector field illustrating air flow using vector calculus concepts.*")
