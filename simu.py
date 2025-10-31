import plotly.graph_objects as go
import numpy as np
import streamlit as st

st.header("🌍 3D Animated Vector Field")

# Grid
n3 = 8  # keep small for smooth animation
x3 = np.linspace(-2, 2, n3)
y3 = np.linspace(-2, 2, n3)
z3 = np.linspace(-2, 2, n3)
X3, Y3, Z3 = np.meshgrid(x3, y3, z3)

# Create frames
frames = []
for t in np.linspace(0, 2*np.pi, 20):
    U = -Y3 * np.cos(t)  # curl
    V = X3 * np.sin(t)
    W = np.sin(np.sqrt(X3**2 + Y3**2))
    
    frames.append(go.Frame(data=[go.Cone(
        x=X3.flatten(), y=Y3.flatten(), z=Z3.flatten(),
        u=U.flatten(), v=V.flatten(), w=W.flatten(),
        colorscale="Viridis", sizemode="absolute", sizeref=0.5, showscale=False
    )], name=f"t={t:.2f}"))

# Initial plot
fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        scene=dict(xaxis=dict(range=[-2,2]),
                   yaxis=dict(range=[-2,2]),
                   zaxis=dict(range=[-2,2]),
                   aspectmode="cube"),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="▶️ Play",
                          method="animate",
                          args=[None, {"frame": {"duration":100, "redraw": True},
                                       "fromcurrent": True}])]
        )]
    ),
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)
