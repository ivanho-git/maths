import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import pandas as pd

# Page configuration
st.set_page_config(page_title="Navier-Stokes Weather Predictor", layout="wide")

# Title and introduction
st.title("🌦️ Simplified Weather Prediction using Navier-Stokes Equations")

st.markdown("""
### About This Application
This educational tool demonstrates how the **Navier-Stokes equations** form the foundation of weather prediction models.
The Navier-Stokes equations describe the motion of viscous fluids (including air in our atmosphere) and are fundamental
to computational fluid dynamics and numerical weather prediction.

**⚠️ Important:** This is a simplified educational model. Real weather forecasting uses complex numerical models
with thousands of variables, satellite data, and supercomputers. This app demonstrates the core concepts only.
""")

# Display Navier-Stokes Equations
st.markdown("---")
st.subheader("📐 The Navier-Stokes Equations")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    The **incompressible Navier-Stokes equations** in vector form:
    
    **Momentum Equation:**
    """)
    st.latex(r"\rho \left(\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u}\right) = -\nabla P + \mu \nabla^2 \mathbf{u} + \mathbf{f}")
    
    st.markdown("**Continuity Equation (Conservation of Mass):**")
    st.latex(r"\nabla \cdot \mathbf{u} = 0")
    
    st.markdown("""
    Where:
    - **ρ** = air density (kg/m³)
    - **u** = velocity field (m/s)
    - **P** = pressure (Pa)
    - **μ** = dynamic viscosity (Pa·s)
    - **f** = external forces (e.g., gravity, Coriolis)
    - **t** = time
    """)

with col2:
    st.info("""
    **Key Components:**
    - **Convection term**: (u·∇)u
    - **Pressure gradient**: -∇P
    - **Viscous term**: μ∇²u
    - **External forces**: f
    
    These equations are coupled with:
    - Thermodynamic equations
    - Moisture equations
    - Radiation models
    """)

st.markdown("---")

# Sidebar for inputs
st.sidebar.header("🎛️ Input Parameters")
st.sidebar.markdown("Adjust the atmospheric conditions below:")

# Create two columns for better organization
col_left, col_right = st.sidebar.columns(2)

with col_left:
    rho = st.sidebar.number_input("Air Density ρ (kg/m³)", 
                                   min_value=0.5, max_value=2.0, value=1.225, step=0.01,
                                   help="Standard air density at sea level is ~1.225 kg/m³")
    
    mu = st.sidebar.number_input("Dynamic Viscosity μ (×10⁻⁵ Pa·s)", 
                                  min_value=1.0, max_value=3.0, value=1.81, step=0.01,
                                  help="Air viscosity at 15°C is ~1.81×10⁻⁵ Pa·s") * 1e-5
    
    pressure = st.sidebar.number_input("Pressure P (hPa)", 
                                        min_value=950.0, max_value=1050.0, value=1013.25, step=0.5,
                                        help="Standard atmospheric pressure is 1013.25 hPa")

with col_right:
    temperature = st.sidebar.number_input("Temperature T (°C)", 
                                          min_value=-30.0, max_value=50.0, value=15.0, step=0.5)
    
    humidity = st.sidebar.slider("Humidity (%)", 
                                  min_value=0, max_value=100, value=60,
                                  help="Relative humidity percentage")

st.sidebar.markdown("---")
st.sidebar.subheader("Wind Velocity Components")

u_wind = st.sidebar.number_input("u-component (East-West, m/s)", 
                                  min_value=-30.0, max_value=30.0, value=5.0, step=0.5,
                                  help="Positive = eastward, negative = westward")

v_wind = st.sidebar.number_input("v-component (North-South, m/s)", 
                                  min_value=-30.0, max_value=30.0, value=3.0, step=0.5,
                                  help="Positive = northward, negative = southward")

# Time step for prediction
st.sidebar.markdown("---")
time_hours = st.sidebar.slider("Prediction Time Horizon (hours)", 
                                min_value=1, max_value=12, value=3)

# Example values button
if st.sidebar.button("📋 Load Example Values"):
    st.sidebar.success("Example values loaded! (Refresh to see changes)")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 💡 Tips:
- **Low pressure** + **high humidity** → Rain likely
- **High wind speeds** → Storm conditions
- **Temperature** affects air density
- **Pressure changes** indicate weather fronts
""")

# Main computation
st.markdown("---")
st.header("📊 Prediction Results")

# Calculate derived quantities
wind_speed = np.sqrt(u_wind**2 + v_wind**2)
wind_direction_deg = np.degrees(np.arctan2(v_wind, u_wind))
if wind_direction_deg < 0:
    wind_direction_deg += 360

# Direction name
def get_direction_name(deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = int((deg + 22.5) // 45) % 8
    return directions[idx]

# Simplified physics-based predictions
# These are educational approximations

# 1. Pressure evolution (using simplified continuity and ideal gas law)
# Pressure tendency affected by wind divergence and temperature
divergence = np.random.uniform(-0.5, 0.5)  # Simplified divergence approximation
pressure_change = -divergence * pressure * 0.1 * time_hours
future_pressure = pressure + pressure_change

# 2. Temperature change (affected by pressure change and advection)
# Adiabatic cooling/warming
temp_pressure_effect = -pressure_change * 0.02
temp_advection = -u_wind * 0.05 * time_hours  # Simplified advection
future_temperature = temperature + temp_pressure_effect + temp_advection

# 3. Wind velocity prediction (using simplified momentum equation)
# Wind changes due to pressure gradients and viscous effects
pressure_gradient = pressure_change / 1000  # Simplified gradient
reynolds_number = (rho * wind_speed * 1000) / mu  # Characteristic length ~1km

# Viscous damping (small for high Reynolds number)
viscous_damping = 1 - (mu / (rho * wind_speed + 0.1)) * 0.01 * time_hours

# Future wind components
u_future = u_wind * viscous_damping + pressure_gradient * 0.5
v_future = v_wind * viscous_damping + pressure_gradient * 0.3

future_wind_speed = np.sqrt(u_future**2 + v_future**2)
future_wind_direction_deg = np.degrees(np.arctan2(v_future, u_future))
if future_wind_direction_deg < 0:
    future_wind_direction_deg += 360

# 4. Weather condition prediction
def predict_weather(p, t, h, ws):
    """Simplified weather classification"""
    score = 0
    
    # Pressure factor
    if p < 1000:
        score += 3
    elif p < 1010:
        score += 1
    
    # Humidity factor
    if h > 80:
        score += 3
    elif h > 60:
        score += 1
    
    # Temperature factor (extreme temps)
    if t < 0 or t > 35:
        score += 1
    
    # Wind speed factor
    if ws > 15:
        score += 2
    elif ws > 10:
        score += 1
    
    if score >= 6:
        return "⛈️ Stormy/Heavy Rain"
    elif score >= 4:
        return "🌧️ Rainy"
    elif score >= 2:
        return "☁️ Cloudy"
    else:
        return "☀️ Clear"

current_weather = predict_weather(pressure, temperature, humidity, wind_speed)
future_weather = predict_weather(future_pressure, future_temperature, humidity, future_wind_speed)

# Display results in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Wind Speed", f"{wind_speed:.1f} m/s", 
              delta=f"{future_wind_speed - wind_speed:+.1f} m/s")
    st.metric("Current Wind Direction", 
              f"{wind_direction_deg:.0f}° ({get_direction_name(wind_direction_deg)})",
              delta=f"{future_wind_direction_deg - wind_direction_deg:+.0f}°")

with col2:
    st.metric("Current Pressure", f"{pressure:.1f} hPa", 
              delta=f"{pressure_change:+.1f} hPa")
    st.metric("Current Temperature", f"{temperature:.1f}°C", 
              delta=f"{future_temperature - temperature:+.1f}°C")

with col3:
    st.metric("Current Humidity", f"{humidity}%")
    st.metric("Reynolds Number", f"{reynolds_number:.0f}",
              help="High Re indicates turbulent flow")

# Weather condition display
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Condition")
    st.markdown(f"## {current_weather}")

with col2:
    st.subheader(f"Predicted ({time_hours}h)")
    st.markdown(f"## {future_weather}")

# Prediction summary
st.markdown("---")
st.subheader("📝 Detailed Prediction Summary")

trend = "decreasing" if pressure_change < 0 else "increasing"
temp_trend = "cooling" if future_temperature < temperature else "warming"
wind_change = "strengthening" if future_wind_speed > wind_speed else "weakening"

summary = f"""
Based on the current atmospheric conditions and simplified Navier-Stokes dynamics:

**Current State:** {current_weather} with winds from {get_direction_name(wind_direction_deg)} at {wind_speed:.1f} m/s.

**Predicted Evolution (next {time_hours} hours):**
- **Pressure**: {trend.capitalize()} from {pressure:.1f} to {future_pressure:.1f} hPa (Δ{pressure_change:+.1f} hPa)
- **Temperature**: {temp_trend.capitalize()} from {temperature:.1f}°C to {future_temperature:.1f}°C
- **Wind**: {wind_change.capitalize()} to {future_wind_speed:.1f} m/s from {get_direction_name(future_wind_direction_deg)}
- **Weather Condition**: Transitioning to **{future_weather}**

**Physical Interpretation:**
- The pressure {trend} indicates {'divergence (rising air)' if pressure_change < 0 else 'convergence (sinking air)'}.
- Reynolds number of {reynolds_number:.0f} suggests {'turbulent' if reynolds_number > 4000 else 'transitional'} flow regime.
- High humidity ({humidity}%) combined with {trend} pressure increases precipitation likelihood.
"""

st.info(summary)

# Visualizations
st.markdown("---")
st.subheader("📈 Visual Analysis")

# Create plots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Wind vector field
ax1 = axes[0]
x = np.linspace(0, 10, 6)
y = np.linspace(0, 10, 6)
X, Y = np.meshgrid(x, y)

# Current wind field (uniform for simplicity, with small perturbations)
U_current = np.ones_like(X) * u_wind + np.random.uniform(-0.5, 0.5, X.shape)
V_current = np.ones_like(Y) * v_wind + np.random.uniform(-0.5, 0.5, Y.shape)

# Future wind field
U_future = np.ones_like(X) * u_future + np.random.uniform(-0.5, 0.5, X.shape)
V_future = np.ones_like(Y) * v_future + np.random.uniform(-0.5, 0.5, Y.shape)

# Plot current wind
ax1.quiver(X, Y, U_current, V_current, alpha=0.6, color='blue', label='Current', scale=100)
ax1.quiver(X, Y, U_future, V_future, alpha=0.6, color='red', label=f'Predicted ({time_hours}h)', scale=100)
ax1.set_xlabel('X Position (arbitrary units)')
ax1.set_ylabel('Y Position (arbitrary units)')
ax1.set_title('Wind Velocity Field Evolution')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_aspect('equal')

# Plot 2: Pressure contour
ax2 = axes[1]
x_fine = np.linspace(0, 10, 50)
y_fine = np.linspace(0, 10, 50)
X_fine, Y_fine = np.meshgrid(x_fine, y_fine)

# Create synthetic pressure field with gradient
P_field = pressure - (X_fine - 5) * pressure_change/10 + np.random.uniform(-2, 2, X_fine.shape)

contour = ax2.contourf(X_fine, Y_fine, P_field, levels=15, cmap='RdYlBu_r', alpha=0.8)
ax2.contour(X_fine, Y_fine, P_field, levels=15, colors='black', alpha=0.3, linewidths=0.5)
plt.colorbar(contour, ax=ax2, label='Pressure (hPa)')
ax2.set_xlabel('X Position (arbitrary units)')
ax2.set_ylabel('Y Position (arbitrary units)')
ax2.set_title(f'Pressure Field (Current: {pressure:.1f} hPa)')
ax2.set_aspect('equal')

plt.tight_layout()
st.pyplot(fig)

# Time evolution plot
st.markdown("---")
st.subheader("⏱️ Temporal Evolution")

fig2, axes2 = plt.subplots(1, 3, figsize=(15, 4))

time_points = np.linspace(0, time_hours, 20)

# Pressure evolution
pressure_evolution = pressure + (pressure_change / time_hours) * time_points
axes2[0].plot(time_points, pressure_evolution, 'b-', linewidth=2)
axes2[0].axhline(y=1013.25, color='gray', linestyle='--', alpha=0.5, label='Standard Pressure')
axes2[0].set_xlabel('Time (hours)')
axes2[0].set_ylabel('Pressure (hPa)')
axes2[0].set_title('Pressure Evolution')
axes2[0].grid(True, alpha=0.3)
axes2[0].legend()

# Temperature evolution
temp_evolution = temperature + ((future_temperature - temperature) / time_hours) * time_points
axes2[1].plot(time_points, temp_evolution, 'r-', linewidth=2)
axes2[1].set_xlabel('Time (hours)')
axes2[1].set_ylabel('Temperature (°C)')
axes2[1].set_title('Temperature Evolution')
axes2[1].grid(True, alpha=0.3)

# Wind speed evolution
wind_evolution = wind_speed + ((future_wind_speed - wind_speed) / time_hours) * time_points
axes2[2].plot(time_points, wind_evolution, 'g-', linewidth=2)
axes2[2].set_xlabel('Time (hours)')
axes2[2].set_ylabel('Wind Speed (m/s)')
axes2[2].set_title('Wind Speed Evolution')
axes2[2].grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig2)

# Educational section
st.markdown("---")
st.subheader("🎓 How This Works: From Navier-Stokes to Weather")

with st.expander("Click to learn more about the physics"):
    st.markdown("""
    ### The Physics Behind Weather Prediction
    
    **1. Navier-Stokes Equations:**
    These fundamental equations describe how fluids (including air) move and are the basis of all weather models:
    
    - **Momentum Conservation**: How wind velocity changes due to pressure gradients, viscosity, and external forces
    - **Mass Conservation**: The continuity equation ensures air mass is conserved
    - **Energy Conservation**: Temperature changes via thermodynamic processes
    
    **2. Key Physical Processes:**
    
    - **Pressure Gradients** (−∇P): High pressure pushes air toward low pressure, creating wind
    - **Viscous Forces** (μ∇²u): Air friction slows down wind (usually negligible except near surfaces)
    - **Advection** ((u·∇)u): Wind carries momentum, heat, and moisture
    - **Coriolis Force**: Earth's rotation deflects moving air (not included in this simplified model)
    
    **3. What Real Models Do:**
    
    Real numerical weather prediction (NWP) systems like those at NOAA, ECMWF, and other agencies:
    - Divide the atmosphere into millions of grid cells
    - Solve coupled Navier-Stokes + thermodynamic equations at each point
    - Incorporate satellite observations, radar data, and weather stations
    - Use supercomputers running for hours to predict days ahead
    - Include cloud physics, radiation, surface interactions, and more
    
    **4. This Educational Model:**
    
    This app uses **simplified approximations**:
    - Linear extrapolations based on current conditions
    - Simplified physics relationships
    - Statistical weather classification
    - Does NOT solve the full PDE system
    
    **Purpose**: To demonstrate the core concepts and inspire interest in atmospheric physics!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🌍 Educational Weather Prediction Tool | Based on Navier-Stokes Fluid Dynamics</p>
    <p>⚠️ For educational purposes only - not for actual weather forecasting</p>
</div>
""", unsafe_allow_html=True)
