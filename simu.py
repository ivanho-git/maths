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

# --- Create Tabs ---
tab1, tab2 = st.tabs(["🌪️ Vector Field Simulation", "🌊 Navier-Stokes Theory"])

# ==========================================
# TAB 1: Vector Field Simulation (Original)
# ==========================================
with tab1:
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
            # Create clear radial divergence/convergence pattern
            # Pulsating flow: expands outward then contracts inward
            pulse = np.sin(t) * 0.8 + 0.2  # Oscillates between 0.2 and 1.0
            
            # Radial distance from center
            R = np.sqrt(X**2 + Y**2) + 0.1
            
            # Radial outward/inward flow
            # pulse > 0.5: Divergence (flowing OUT)
            # pulse < 0.5: Convergence (flowing IN)
            U = magnitude * (X / R) * pulse * 2.0
            V = magnitude * (Y / R) * pulse * 2.0
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
        fig, ax = plt.subplots(figsize=(7,7))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_title(field_mode, fontsize=14, fontweight='bold', pad=20)
        ax.set_aspect('equal')
        ax.set_xlabel('X', fontsize=10)
        ax.set_ylabel('Y', fontsize=10)

        U, V, divergence, curl = compute_field(0)
        
        # Adjust quiver appearance based on field mode
        if field_mode == "Divergence (Air Outflow/Inflow)":
            quiver = ax.quiver(X, Y, U, V, color='darkblue', pivot='mid', scale=12, width=0.008, alpha=0.8)
        else:
            quiver = ax.quiver(X, Y, U, V, color='dodgerblue', pivot='mid', scale=15, width=0.007)

        if show_heatmap:
            if field_mode == "Divergence (Air Outflow/Inflow)":
                # For divergence, show the actual divergence field
                div_img = ax.imshow(divergence, extent=[-2,2,-2,2], origin='lower', 
                                   cmap='RdBu_r', alpha=0.6, vmin=-2, vmax=2)
                cbar = plt.colorbar(div_img, ax=ax, fraction=0.046, pad=0.04)
                cbar.set_label('Divergence (∇·V)', rotation=270, labelpad=20, fontsize=10)
                # Add a central marker to show the center point
                ax.plot(0, 0, 'ko', markersize=8, label='Center')
            else:
                div_img = ax.imshow(divergence, extent=[-2,2,-2,2], origin='lower', 
                                   cmap='RdBu', alpha=0.5)
                plt.colorbar(div_img, ax=ax, fraction=0.046, pad=0.04, label='Divergence')

        # Add text annotation for divergence mode
        if field_mode == "Divergence (Air Outflow/Inflow)":
            text_annotation = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                                     fontsize=11, verticalalignment='top',
                                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            # Initialize rain drops (for divergence mode only)
            num_raindrops = 80
            raindrop_x = np.random.uniform(-2, 2, num_raindrops)
            raindrop_y = np.random.uniform(0.5, 2, num_raindrops)
            raindrop_velocities = np.random.uniform(0.08, 0.15, num_raindrops)
            rain_scatter = ax.scatter(raindrop_x, raindrop_y, c='blue', s=30, alpha=0, marker='|', linewidths=3)
            
            # Initialize clouds (gray circles)
            num_clouds = 12
            cloud_circles = []
            for i in range(num_clouds):
                cx = np.random.uniform(-1.8, 1.8)
                cy = np.random.uniform(1.3, 1.9)
                radius = np.random.uniform(0.15, 0.3)
                cloud = plt.Circle((cx, cy), radius, color='gray', alpha=0, zorder=10)
                ax.add_patch(cloud)
                cloud_circles.append(cloud)

        def update(frame):
            t = frame * 0.15
            U, V, divergence, curl = compute_field(t)
            quiver.set_UVC(U, V)
            
            if show_heatmap:
                div_img.set_data(divergence)
            
            # Update annotation for divergence
            if field_mode == "Divergence (Air Outflow/Inflow)":
                pulse = np.sin(t) * 0.8 + 0.2
                
                if pulse > 0.5:
                    # DIVERGENCE - Clear skies
                    state = "DIVERGENCE\n(Air Spreading OUT)\n☀️ Clear Skies"
                    color = 'lightyellow'
                    
                    # Hide rain and clouds
                    rain_scatter.set_alpha(0)
                    for cloud in cloud_circles:
                        cloud.set_alpha(0)
                else:
                    # CONVERGENCE - Rain and clouds
                    state = "CONVERGENCE\n(Air Coming IN)\n🌧️ Rain & Clouds"
                    color = 'lightblue'
                    
                    # Show clouds
                    for cloud in cloud_circles:
                        cloud.set_alpha(0.7)
                    
                    # Animate rain falling
                    nonlocal raindrop_y, raindrop_x
                    raindrop_y -= raindrop_velocities
                    
                    # Reset raindrops that fall below bottom
                    reset_mask = raindrop_y < -2
                    raindrop_y[reset_mask] = np.random.uniform(1.5, 2.0, np.sum(reset_mask))
                    raindrop_x[reset_mask] = np.random.uniform(-2, 2, np.sum(reset_mask))
                    
                    # Update rain positions
                    rain_scatter.set_offsets(np.c_[raindrop_x, raindrop_y])
                    rain_scatter.set_alpha(0.6)
                
                text_annotation.set_text(state)
                text_annotation.set_bbox(dict(boxstyle='round', facecolor=color, alpha=0.9))
            
            return quiver,

        ani = animation.FuncAnimation(fig, update, frames=80, interval=80, blit=False)
        
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
            ani.save(tmpfile.name, writer=PillowWriter(fps=25))
            tmpfile.seek(0)
            gif_bytes = tmpfile.read()

        st.image(gif_bytes, caption=f"{field_mode} (2D Animated Field)", use_container_width=True)
        
        # Add explanation below for divergence
        if field_mode == "Divergence (Air Outflow/Inflow)":
            st.info("""
            🌬️ **Understanding the Animation:**
            - **☀️ DIVERGENCE (Clear Skies)** = Air spreading outward → High pressure → Sinking air → No clouds/rain
            - **🌧️ CONVERGENCE (Rain & Clouds)** = Air coming together → Low pressure → Rising air → Clouds form → Rain falls!
            - **RED regions** = Positive Divergence → Air escaping (like air leaving a balloon)
            - **BLUE regions** = Negative Divergence (Convergence) → Air gathering (like water down a drain)
            
            **In Real Weather:**
            - Convergence at surface → air is forced to rise → cools → water vapor condenses → clouds & precipitation ☁️🌧️
            - Divergence at surface → air sinks → warms → evaporates moisture → clear skies ☀️
            """)

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
        for t in np.linspace(0, 2*np.pi, 30):
            if field_mode == "Gradient (Pressure Field)":
                Phi = np.exp(-X3**2 - Y3**2 - Z3**2)
                U = -2 * X3 * Phi * magnitude
                V = -2 * Y3 * Phi * magnitude
                W = -2 * Z3 * Phi * magnitude
                colorscale = "Viridis"
            elif field_mode == "Divergence (Air Outflow/Inflow)":
                # Create clear divergence (outflow) and convergence (inflow) pattern
                # Pulsating radial field that shows expansion and contraction
                pulse = np.sin(t) * 0.8 + 0.2  # Oscillates between 0.2 and 1.0
                
                # Radial distance from center
                R = np.sqrt(X3**2 + Y3**2 + Z3**2) + 0.1
                
                # Radial outward/inward flow
                # When pulse > 0.5: Divergence (air flowing OUT from center)
                # When pulse < 0.5: Convergence (air flowing IN to center)
                U = magnitude * (X3 / R) * pulse * 1.5
                V = magnitude * (Y3 / R) * pulse * 1.5
                W = magnitude * (Z3 / R) * pulse * 1.5
                
                # Color based on divergence strength (red=outflow, blue=inflow)
                colorscale = "RdBu_r"
            else:  # Curl
                U = -Y3 * np.cos(t)
                V = X3 * np.sin(t)
                W = np.sin(np.sqrt(X3**2 + Y3**2)) * 0.5
                colorscale = "Viridis"
            
            # Compute vector magnitudes for coloring
            magnitude_field = np.sqrt(U**2 + V**2 + W**2)
            
            frames.append(go.Frame(data=[go.Cone(
                x=X3.flatten(), y=Y3.flatten(), z=Z3.flatten(),
                u=U.flatten(), v=V.flatten(), w=W.flatten(),
                colorscale=colorscale, 
                sizemode="absolute", 
                sizeref=0.5 if field_mode != "Divergence (Air Outflow/Inflow)" else 0.6,
                showscale=True if field_mode == "Divergence (Air Outflow/Inflow)" else False,
                colorbar=dict(title="Flow<br>Strength") if field_mode == "Divergence (Air Outflow/Inflow)" else None,
                cmin=0,
                cmax=magnitude * 2
            )], name=f"t={t:.2f}"))

        # Add title based on field mode
        if field_mode == "Divergence (Air Outflow/Inflow)":
            title_text = "3D Divergence: Watch air EXPAND (red) and CONTRACT (blue)"
        elif field_mode == "Gradient (Pressure Field)":
            title_text = "3D Pressure Gradient: Air flows from high to low pressure"
        else:
            title_text = "3D Curl: Rotational/Vortex motion"

        fig3 = go.Figure(
            data=frames[0].data,
            layout=go.Layout(
                title=dict(text=title_text, x=0.5, xanchor='center'),
                scene=dict(
                    xaxis=dict(range=[-2,2], title="X"), 
                    yaxis=dict(range=[-2,2], title="Y"), 
                    zaxis=dict(range=[-2,2], title="Z"), 
                    aspectmode="cube",
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.3)
                    )
                ),
                updatemenus=[dict(
                    type="buttons",
                    showactive=False,
                    y=1.15,
                    x=0.85,
                    buttons=[dict(label="▶️ Play",
                                  method="animate",
                                  args=[None, {"frame": {"duration":100, "redraw": True}, 
                                               "fromcurrent": True, 
                                               "mode": "immediate"}])])]
            ),
            frames=frames
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Add explanation below the 3D plot
        if field_mode == "Divergence (Air Outflow/Inflow)":
            st.info("""
            🌬️ **What you're seeing:**
            - **Arrows pointing OUTWARD** (expansion) = **Positive Divergence** → Air spreading out (associated with HIGH pressure, sinking air)
            - **Arrows pointing INWARD** (contraction) = **Negative Divergence** (Convergence) → Air coming together (associated with LOW pressure, rising air, clouds)
            - The animation pulses to show both states clearly
            
            **In weather:** Convergence at surface → air rises → clouds & rain form ☁️🌧️
            """)

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

# ==========================================
# TAB 2: Navier-Stokes Theory
# ==========================================
with tab2:
    st.header("🌊 Navier-Stokes Equations in Weather Prediction")
    
    st.markdown("""
    The **Navier-Stokes equations** are the fundamental governing equations of fluid dynamics and form the 
    mathematical foundation of all modern weather prediction models. These equations describe how the velocity, 
    pressure, temperature, and density of a moving fluid are related.
    """)
    
    # Main Navier-Stokes Equations
    st.subheader("📐 The Navier-Stokes Equations")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("**Momentum Equation (Newton's Second Law for Fluids):**")
        st.latex(r"\rho \left(\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u}\right) = -\nabla P + \mu \nabla^2 \mathbf{u} + \mathbf{f}")
        
        st.markdown("**Continuity Equation (Mass Conservation):**")
        st.latex(r"\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{u}) = 0")
        
        st.markdown("**For incompressible flows:**")
        st.latex(r"\nabla \cdot \mathbf{u} = 0")
    
    with col2:
        st.info("""
        **Variables:**
        - **ρ**: Air density (kg/m³)
        - **u**: Velocity field (m/s)
        - **P**: Pressure (Pa)
        - **μ**: Dynamic viscosity
        - **f**: Body forces (gravity, Coriolis)
        - **t**: Time
        """)
    
    st.markdown("---")
    
    # Physical Interpretation
    st.subheader("🔍 Physical Interpretation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1️⃣ Acceleration Term")
        st.latex(r"\frac{\partial \mathbf{u}}{\partial t}")
        st.markdown("**Local acceleration** - How fast the wind is changing at a fixed point.")
    
    with col2:
        st.markdown("### 2️⃣ Advection Term")
        st.latex(r"(\mathbf{u} \cdot \nabla)\mathbf{u}")
        st.markdown("**Convective acceleration** - Wind carrying its own momentum.")
    
    with col3:
        st.markdown("### 3️⃣ Pressure Gradient")
        st.latex(r"-\nabla P")
        st.markdown("**Pressure force** - Drives air from high to low pressure.")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("### 4️⃣ Viscous Term")
        st.latex(r"\mu \nabla^2 \mathbf{u}")
        st.markdown("**Friction/diffusion** - Air resistance and turbulent mixing.")
    
    with col5:
        st.markdown("### 5️⃣ Body Forces")
        st.latex(r"\mathbf{f}")
        st.markdown("**External forces** - Gravity, Coriolis effect (Earth's rotation).")
    
    with col6:
        st.markdown("### 6️⃣ Continuity")
        st.latex(r"\nabla \cdot \mathbf{u} = 0")
        st.markdown("**Mass conservation** - Air is neither created nor destroyed.")
    
    st.markdown("---")
    
    # Connection to Weather
    st.subheader("🌍 How Navier-Stokes Predicts Weather")
    
    st.markdown("""
    Modern weather forecasting models solve the Navier-Stokes equations coupled with additional equations for:
    
    1. **Thermodynamics** (Energy/Temperature evolution)
       - First Law of Thermodynamics
       - Diabatic heating (solar radiation, latent heat)
    
    2. **Moisture Transport** (Humidity and precipitation)
       - Water vapor advection
       - Cloud microphysics
       - Phase changes (evaporation, condensation, precipitation)
    
    3. **Equation of State** (Relating pressure, temperature, and density)
       - Ideal gas law: P = ρRT
    
    4. **Turbulence Models** (Subgrid-scale processes)
       - Parameterization of unresolved eddies
       - Boundary layer physics
    """)
    
    # Real-world applications
    st.subheader("🖥️ Numerical Weather Prediction (NWP) Systems")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Major Global Weather Models:**
        - **GFS** (NOAA, USA) - Global Forecast System
        - **ECMWF** (Europe) - European Centre for Medium-Range Weather Forecasts
        - **UKMO** (UK) - UK Met Office Unified Model
        - **JMA** (Japan) - Japan Meteorological Agency
        - **CMC** (Canada) - Canadian Meteorological Centre
        """)
    
    with col2:
        st.markdown("""
        **Computational Requirements:**
        - Grid resolution: 10-50 km globally, 1-3 km regionally
        - Time steps: seconds to minutes
        - Vertical levels: 50-137 atmospheric layers
        - Compute time: Hours on supercomputers
        - Data assimilation: Billions of observations daily
        """)
    
    st.markdown("---")
    
    # Challenges
    st.subheader("⚠️ The Challenge: Why Weather Prediction is Hard")
    
    st.warning("""
    **Fundamental Difficulties:**
    
    1. **Nonlinearity**: The (u·∇)u term makes the equations highly nonlinear, leading to chaos and sensitivity to initial conditions
    2. **Multiscale Physics**: Weather involves processes from molecular scales (micrometers) to planetary scales (thousands of km)
    3. **Turbulence**: One of the biggest unsolved problems in physics - no exact analytical solution exists
    4. **Computational Cost**: Solving Navier-Stokes on a global grid requires petaflops of computing power
    5. **Initial Condition Uncertainty**: Small errors in current conditions grow exponentially (butterfly effect)
    6. **Incomplete Physics**: Many processes must be approximated (clouds, radiation, surface interactions)
    """)
    
    st.markdown("---")
    
    # Numerical Methods
    st.subheader("🔢 Solving the Equations: Numerical Methods")
    
    st.markdown("""
    Since analytical solutions don't exist for realistic atmospheric flows, meteorologists use:
    
    **Discretization Methods:**
    - **Finite Differences**: Approximate derivatives on a grid
    - **Finite Elements**: Solve on irregular meshes
    - **Spectral Methods**: Decompose fields into wave components
    
    **Time Integration:**
    - **Explicit schemes**: Euler, Runge-Kutta (stable but slow)
    - **Implicit schemes**: Backward Euler (faster but requires solving large systems)
    - **Semi-implicit**: Hybrid approaches for efficiency
    
    **Data Assimilation:**
    - Combine observations with model forecasts
    - Kalman filtering, variational methods (3D-Var, 4D-Var)
    - Ensemble methods for uncertainty quantification
    """)
    
    st.markdown("---")
    
    # Interactive Predictor Button
    st.subheader("🚀 Try Weather Prediction with Navier-Stokes!")
    
    st.markdown("""
    Ready to see Navier-Stokes in action? Our interactive weather predictor lets you:
    - Adjust atmospheric parameters (density, viscosity, pressure, temperature)
    - Visualize wind fields and pressure gradients
    - See simplified weather predictions based on NS equations
    - Explore the physics behind each prediction
    """)
    
    # Create centered button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🌦️ Predict Weather with Navier-Stokes"):
            st.markdown("""
            <meta http-equiv="refresh" content="0; url=https://navierstokes.streamlit.app/" />
            """, unsafe_allow_html=True)
            st.success("🔄 Redirecting to Weather Predictor...")
            st.markdown("[Click here if not redirected automatically](https://navierstokes.streamlit.app/)")
    
    st.markdown("---")
    
    # Fun Facts
    with st.expander("🎓 Fun Facts About Navier-Stokes"):
        st.markdown("""
        1. **Million Dollar Problem**: Proving the existence and smoothness of Navier-Stokes solutions in 3D is one of the 
           seven Millennium Prize Problems. Solve it and win $1,000,000 from the Clay Mathematics Institute!
        
        2. **Named After Two Mathematicians**: 
           - Claude-Louis Navier (French, 1785-1836)
           - George Gabriel Stokes (Irish, 1819-1903)
        
        3. **Universal Application**: The same equations govern:
           - Weather and climate
           - Ocean currents
           - Blood flow in arteries
           - Airflow around aircraft
           - Turbulence in coffee stirring
        
        4. **Predictability Limit**: Due to chaos, weather forecasts are generally reliable only up to 7-10 days, 
           no matter how powerful our computers become!
        
        5. **Supercomputer Power**: NOAA's weather supercomputers can perform over 12 quadrillion calculations per second!
        """)
    
    # References
    with st.expander("📚 Further Reading"):
        st.markdown("""
        **Books:**
        - *Atmospheric Modeling, Data Assimilation and Predictability* by Eugenia Kalnay
        - *Numerical Weather and Climate Prediction* by Thomas T. Warner
        - *An Introduction to Fluid Dynamics* by G.K. Batchelor
        
        **Online Resources:**
        - [NOAA's Numerical Weather Prediction](https://www.weather.gov/media/notification/pdfs/scn20-97_nws_supercomputer_aac.pdf)
        - [ECMWF Documentation](https://www.ecmwf.int/en/forecasts/documentation-and-support)
        - [Clay Mathematics Institute - Navier-Stokes Problem](https://www.claymath.org/millennium-problems/navier-stokes-equation)
        
        **Academic Papers:**
        - Lynch, P. (2008). "The origins of computer weather prediction and climate modeling"
        - Bauer, P., Thorpe, A., & Brunet, G. (2015). "The quiet revolution of numerical weather prediction"
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🌍 Weather Simulation Lab | Daksh Agarwal | Ibhan Mukherjee | Uddipan Kalita | Udayan Nath </p>
    <p>Built By Engineers For The Love Of Mathematics Not Just For Credits</p>
</div>
""", unsafe_allow_html=True)
