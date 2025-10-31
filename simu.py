import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

st.title("🌪️ Vector Field Simulation — Gradient, Divergence & Curl in Weather Systems")

# Select simulation type
field_type = st.selectbox("Select Vector Field Type", ["Gradient", "Divergence", "Curl"])

# Create grid
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x, y)

# Define fields
if field_type == "Gradient":
    Z = np.exp(-(X**2 + Y**2))
    U, V = np.gradient(Z)
    title = "Gradient Field (like temperature gradient → heat flow)"
elif field_type == "Divergence":
    U = X
    V = Y
    title = "Divergence Field (like high to low pressure air flow)"
else:
    U = -Y
    V = X
    title = "Curl Field (like cyclones/rotating wind systems)"

# Streamlit info
st.markdown(f"**{title}**")
st.markdown("""
- **Gradient:** shows direction of fastest increase (e.g., temperature → heat flow).  
- **Divergence:** shows expansion (high → low pressure, air outflow).  
- **Curl:** shows rotation (vortices, cyclones).  
""")

# Create animation
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title(title)
ax.set_facecolor("black")

# Initialize arrows
quiver = ax.quiver(X, Y, U, V, color="cyan", scale=25, width=0.008)

def animate(frame):
    """Rotate or pulse the vectors for visible motion."""
    if field_type == "Curl":
        angle = frame * 0.1
        u = np.cos(angle) * U - np.sin(angle) * V
        v = np.sin(angle) * U + np.cos(angle) * V
    else:
        scale = 1 + 0.3 * np.sin(frame * 0.1)
        u = U * scale
        v = V * scale

    quiver.set_UVC(u, v)
    return quiver,

ani = animation.FuncAnimation(fig, animate, frames=100, interval=80, blit=False)

# Streamlit display
st.pyplot(fig)
