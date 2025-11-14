import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import pandas as pd

# Page configuration
st.set_page_config(page_title="Navier-Stokes Weather Predictor", layout="wide")

# Title and introduction
st.title("🌦️ Complete Weather Prediction using Navier-Stokes & Coupled Equations")

st.markdown("""
### About This Application
This educational tool demonstrates how **four fundamental equations** work together to predict weather:
1. **Navier-Stokes** (momentum/wind)
2. **Continuity** (mass conservation)
3. **Thermodynamic Energy** (temperature)
4. **Moisture Transport** (humidity/precipitation)

**⚠️ Important:** This is a simplified educational model. Real weather forecasting uses complex numerical models
with thousands of variables, satellite data, and supercomputers.
""")

# Display ALL 4 Fundamental Equations
st.markdown("---")
st.subheader("📐 The Four Coupled Equations of Weather Prediction")

# Create tabs for each equation
eq_tab1, eq_tab2, eq_tab3, eq_tab4 = st.tabs([
    "1️⃣ Momentum (Navier-Stokes)", 
    "2️⃣ Continuity", 
    "3️⃣ Thermodynamic Energy", 
    "4️⃣ Moisture Transport"
])

with eq_tab1:
    st.markdown("### Navier-Stokes Momentum Equation")
    st.latex(r"\rho\left(\frac{\partial\mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u}\right) = -\nabla p + \mu\nabla^2 \mathbf{u} + \mathbf{f}")
    st.markdown("""
    **What it does:** Predicts how **wind velocity** changes over time
    
    **Physical meaning:**
    - Left side: Rate of change of momentum (acceleration)
    - Right side: Forces acting on air parcels
        - **-∇p**: Pressure gradient force (high → low pressure)
        - **μ∇²u**: Viscous friction (usually small in atmosphere)
        - **f**: External forces (gravity, Coriolis effect)
    
    **Weather impact:** Determines wind speed and direction
    """)

with eq_tab2:
    st.markdown("### Continuity Equation (Mass Conservation)")
    st.latex(r"\nabla\cdot\mathbf{u} = 0 \quad \text{(incompressible)}")
    st.latex(r"\frac{\partial \rho}{\partial t} + \nabla\cdot(\rho\mathbf{u}) = 0 \quad \text{(compressible)}")
    st.markdown("""
    **What it does:** Ensures **air mass is conserved** - air can't appear or disappear
    
    **Physical meaning:**
    - Divergence (∇·u > 0): Air spreading out → sinking motion
    - Convergence (∇·u < 0): Air coming together → rising motion
    
    **Weather impact:** 
    - Convergence → Air rises → Cooling → Clouds & Rain ☁️🌧️
    - Divergence → Air sinks → Warming → Clear skies ☀️
    """)

with eq_tab3:
    st.markdown("### Thermodynamic Energy Equation")
    st.latex(r"\frac{\partial \theta}{\partial t} + (\mathbf{u}\cdot\nabla)\theta = \frac{Q}{c_p}")
    st.markdown("""
    **What it does:** Predicts how **temperature** (or potential temperature θ) changes
    
    **Physical meaning:**
    - Left side: Temperature change following air motion
    - Right side: Heat sources/sinks
        - **Q**: Diabatic heating (solar radiation, latent heat from condensation)
        - **c_p**: Specific heat at constant pressure
    
    **Weather impact:** 
    - Solar heating → warm air rises → convection
    - Latent heat release → powers thunderstorms
    - Radiative cooling → nighttime temperature drops
    """)

with eq_tab4:
    st.markdown("### Moisture Transport Equation")
    st.latex(r"\frac{\partial q}{\partial t} + (\mathbf{u}\cdot\nabla)q = S(q)")
    st.markdown("""
    **What it does:** Tracks **water vapor** (humidity) and predicts precipitation
    
    **Physical meaning:**
    - **q**: Specific humidity (kg water / kg air)
    - **S(q)**: Source/sink terms
        - Evaporation from surface (+)
        - Condensation to clouds/rain (-)
        - Precipitation removal
    
    **Weather impact:** 
    - High q + rising air → clouds form
    - Condensation → releases latent heat → strengthens storms
    - Essential for predicting rain, snow, fog
    """)

st.markdown("---")
st.info("""
🧠 **Why You Need ALL 4 Equations:**

Weather is a coupled system. Each equation depends on the others:
- **Wind** (Navier-Stokes) transports heat and moisture
- **Temperature** affects air density and pressure
- **Moisture** releases latent heat, affecting temperature and pressure
- **Mass conservation** links wind divergence to vertical motion and precipitation

**Leaving out any one equation breaks the ability to predict weather!** ⚠️
""")

st.markdown("---")

# Sidebar for inputs
st.sidebar.header("🎛️ Input Parameters")
st.sidebar.markdown("Adjust the atmospheric conditions below:")

# Atmospheric state variables
st.sidebar.subheader("Initial Atmospheric State")

rho = st.sidebar.number_input("Air Density ρ (kg/m³)", 
                               min_value=0.5, max_value=2.0, value=1.225, step=0.01,
                               help="Standard air density at sea level is ~1.225 kg/m³")

mu = st.sidebar.number_input("Dynamic Viscosity μ (×10⁻⁵ Pa·s)", 
                              min_value=1.0, max_value=3.0, value=1.81, step=0.01,
                              help="Air viscosity at 15°C is ~1.81×10⁻⁵ Pa·s") * 1e-5

pressure = st.sidebar.number_input("Pressure P (hPa)", 
                                    min_value=950.0, max_value=1050.0, value=1013.25, step=0.5,
                                    help="Standard atmospheric pressure is 1013.25 hPa")

temperature = st.sidebar.number_input("Temperature T (°C)", 
                                      min_value=-30.0, max_value=50.0, value=15.0, step=0.5)

humidity = st.sidebar.slider("Relative Humidity (%)", 
                              min_value=0, max_value=100, value=60,
                              help="Relative humidity percentage")

# Convert relative humidity to specific humidity (simplified)
# q ≈ 0.622 * e / (P - e), where e is vapor pressure
# Simplified: q increases with RH and temp
specific_humidity = (humidity / 100) * 0.015 * np.exp(temperature / 20)  # kg/kg

st.sidebar.markdown("---")
st.sidebar.subheader("Wind Velocity Components")

u_wind = st.sidebar.number_input("u-component (East-West, m/s)", 
                                  min_value=-30.0, max_value=30.0, value=5.0, step=0.5,
                                  help="Positive = eastward")

v_wind = st.sidebar.number_input("v-component (North-South, m/s)", 
                                  min_value=-30.0, max_value=30.0, value=3.0, step=0.5,
                                  help="Positive = northward")

w_wind = st.sidebar.number_input("w-component (Vertical, m/s)", 
                                  min_value=-5.0, max_value=5.0, value=0.0, step=0.1,
                                  help="Positive = upward (convergence)")

st.sidebar.markdown("---")
st.sidebar.subheader("Forcing & Sources")

solar_heating = st.sidebar.slider("Solar Heating (W/m²)", 
                                   min_value=0, max_value=1000, value=200,
                                   help="Solar radiation heating rate")

evaporation_rate = st.sidebar.slider("Surface Evaporation (mm/day)", 
                                      min_value=0.0, max_value=10.0, value=3.0, step=0.5,
                                      help="Water evaporation from surface")

# Time step for prediction
time_hours = st.sidebar.slider("Prediction Time Horizon (hours)", 
                                min_value=1, max_value=12, value=3)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 💡 Tips:
- **Positive w** (upward) → Convergence → Clouds/Rain
- **High solar heating** → Convection → Storms
- **High evaporation** → More moisture → Rain
- **Low pressure** + **high humidity** → Storms
""")

# Main computation
st.markdown("---")
st.header("📊 Prediction Results from Coupled Equations")

# Calculate derived quantities
wind_speed = np.sqrt(u_wind**2 + v_wind**2)
wind_direction_deg = np.degrees(np.arctan2(v_wind, u_wind))
if wind_direction_deg < 0:
    wind_direction_deg += 360

def get_direction_name(deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = int((deg + 22.5) // 45) % 8
    return directions[idx]

# =======================
# SOLVE THE 4 EQUATIONS
# =======================

dt = time_hours * 3600  # Convert to seconds
L = 100000  # Characteristic length scale (100 km)

# 1. CONTINUITY EQUATION - Calculate divergence
divergence = (u_wind + v_wind) / L + w_wind / 5000  # Simplified divergence
# Positive divergence → air spreading (sinking)
# Negative divergence → air converging (rising)

# 2. NAVIER-STOKES - Wind evolution
# Pressure gradient force (simplified)
pressure_gradient_x = -(pressure - 1013.25) * 100 / (rho * L)  # m/s²
pressure_gradient_y = -(pressure - 1013.25) * 50 / (rho * L)

# Viscous damping (very small in atmosphere)
viscous_term = -mu * wind_speed / (rho * L**2)

# Coriolis force (f = 2Ω sin(φ), Ω = 7.3e-5 rad/s, φ = 45°)
coriolis_f = 1e-4  # rad/s at mid-latitudes
coriolis_u = coriolis_f * v_wind
coriolis_v = -coriolis_f * u_wind

# Update wind components
du_dt = pressure_gradient_x + coriolis_u + viscous_term
dv_dt = pressure_gradient_y + coriolis_v + viscous_term
dw_dt = -divergence * 0.1  # Vertical motion from continuity

u_future = u_wind + du_dt * dt
v_future = v_wind + dv_dt * dt
w_future = w_wind + dw_dt * dt

# 3. THERMODYNAMIC ENERGY EQUATION - Temperature evolution
cp = 1005  # Specific heat of air (J/kg/K)

# Diabatic heating from solar radiation
Q_solar = solar_heating / rho  # W/m² → J/(kg·s)

# Latent heat release from condensation (if rising air and high humidity)
latent_heat = 2.5e6  # J/kg (latent heat of vaporization)
if w_future > 0 and specific_humidity > 0.008:  # Rising air + moisture
    condensation_rate = specific_humidity * 0.3 * (w_future / 5.0)  # kg/kg/s
    Q_latent = latent_heat * condensation_rate
else:
    condensation_rate = 0
    Q_latent = 0

# Adiabatic cooling/warming from vertical motion
adiabatic_rate = 9.8 / 1000  # °C per meter (dry adiabatic lapse rate)
Q_adiabatic = -w_future * adiabatic_rate

# Temperature advection (simplified)
T_advection = -(u_wind * 0.001 + v_wind * 0.001) * dt / 3600

# Total temperature change
dT_dt = (Q_solar + Q_latent) / cp + Q_adiabatic
future_temperature = temperature + dT_dt * dt / 3600 + T_advection

# 4. MOISTURE EQUATION - Humidity evolution
# Evaporation source
evap_source = evaporation_rate / 1000 / 86400  # mm/day → kg/m²/s
dq_evap = evap_source / (rho * 1000) * dt  # Simplified

# Condensation sink (rain formation)
if condensation_rate > 0:
    dq_condensation = -condensation_rate * dt
    precipitation_rate = -dq_condensation * rho * 1000 * 3600 / dt  # mm/hr
else:
    dq_condensation = 0
    precipitation_rate = 0

# Moisture advection (simplified)
dq_advection = -(u_wind * specific_humidity * 0.00001 + 
                 v_wind * specific_humidity * 0.00001) * dt

future_specific_humidity = specific_humidity + dq_evap + dq_condensation + dq_advection
future_specific_humidity = max(0, min(0.03, future_specific_humidity))  # Bounds

# Convert back to relative humidity (simplified)
future_humidity = (future_specific_humidity / (0.015 * np.exp(future_temperature / 20))) * 100
future_humidity = max(0, min(100, future_humidity))

# Pressure evolution from continuity + ideal gas law
# P ∝ ρT, with mass conservation
pressure_change = -divergence * pressure * 0.001 * dt / 3600  # Simplified
future_pressure = pressure + pressure_change

# Wind speed and direction
future_wind_speed = np.sqrt(u_future**2 + v_future**2)
future_wind_direction_deg = np.degrees(np.arctan2(v_future, u_future))
if future_wind_direction_deg < 0:
    future_wind_direction_deg += 360

# Weather classification based on ALL variables
def predict_weather(p, t, h, ws, w_vert, precip):
    """Advanced weather classification using all 4 equations"""
    score = 0
    
    # Pressure (from continuity + state)
    if p < 1000:
        score += 3
    elif p < 1010:
        score += 1
    
    # Humidity (from moisture equation)
    if h > 85:
        score += 3
    elif h > 70:
        score += 2
    elif h > 50:
        score += 1
    
    # Vertical motion (from continuity)
    if w_vert > 1.0:  # Strong updraft
        score += 4
    elif w_vert > 0.2:
        score += 2
    
    # Precipitation (from moisture equation)
    if precip > 5:
        score += 3
    elif precip > 1:
        score += 2
    
    # Wind speed (from Navier-Stokes)
    if ws > 20:
        score += 3
    elif ws > 12:
        score += 2
    elif ws > 8:
        score += 1
    
    # Temperature extremes (from thermodynamic equation)
    if t < -10 or t > 38:
        score += 1
    
    # Classification
    if score >= 10:
        return "⛈️ Severe Thunderstorms"
    elif score >= 7:
        return "🌧️ Heavy Rain/Storms"
    elif score >= 5:
        return "🌦️ Showers/Light Rain"
    elif score >= 3:
        return "☁️ Cloudy"
    elif score >= 1:
        return "⛅ Partly Cloudy"
    else:
        return "☀️ Clear"

current_weather = predict_weather(pressure, temperature, humidity, wind_speed, w_wind, 0)
future_weather = predict_weather(future_pressure, future_temperature, future_humidity, 
                                 future_wind_speed, w_future, precipitation_rate)

# Display results
st.subheader("🔄 Results from Each Equation")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 1️⃣ Momentum (N-S)")
    st.metric("Wind Speed", f"{wind_speed:.1f} m/s", 
              delta=f"{future_wind_speed - wind_speed:+.1f} m/s")
    st.metric("Wind Direction", 
              f"{get_direction_name(wind_direction_deg)}",
              delta=f"{future_wind_direction_deg - wind_direction_deg:+.0f}°")
    st.caption(f"u: {u_wind:.1f}→{u_future:.1f} m/s")
    st.caption(f"v: {v_wind:.1f}→{v_future:.1f} m/s")

with col2:
    st.markdown("### 2️⃣ Continuity")
    st.metric("Divergence", f"{divergence*1e5:.2f}×10⁻⁵ s⁻¹")
    st.metric("Vertical Motion", f"{w_wind:.2f} m/s",
              delta=f"{w_future - w_wind:+.2f} m/s")
    if divergence > 0:
        st.caption("🔻 Divergence → Sinking")
    else:
        st.caption("🔺 Convergence → Rising")
    st.caption("(Mass conserved)")

with col3:
    st.markdown("### 3️⃣ Thermodynamics")
    st.metric("Temperature", f"{temperature:.1f}°C", 
              delta=f"{future_temperature - temperature:+.1f}°C")
    st.metric("Heating Rate", f"{(Q_solar + Q_latent)/cp*3600:.1f} °C/hr")
    st.caption(f"Solar: {Q_solar/cp*3600:.1f} °C/hr")
    st.caption(f"Latent: {Q_latent/cp*3600:.1f} °C/hr")

with col4:
    st.markdown("### 4️⃣ Moisture")
    st.metric("Humidity", f"{humidity:.0f}%", 
              delta=f"{future_humidity - humidity:+.0f}%")
    st.metric("Precipitation", f"{precipitation_rate:.2f} mm/hr")
    st.caption(f"q: {specific_humidity*1000:.2f}→{future_specific_humidity*1000:.2f} g/kg")
    if precipitation_rate > 0.5:
        st.caption("🌧️ Rain forming!")

# Pressure (coupling all equations)
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.metric("Pressure (from all eqs)", f"{pressure:.1f} hPa", 
              delta=f"{pressure_change:+.1f} hPa")

# Weather condition display
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Condition")
    st.markdown(f"## {current_weather}")
    st.caption(f"Based on coupled equation analysis")

with col2:
    st.subheader(f"Predicted ({time_hours}h)")
    st.markdown(f"## {future_weather}")
    if precipitation_rate > 1:
        st.caption(f"💧 Expect {precipitation_rate:.1f} mm/hr rain")

# Detailed prediction
st.markdown("---")
st.subheader("📝 Detailed Prediction from Coupled System")

trend = "falling" if pressure_change < 0 else "rising"
temp_trend = "cooling" if future_temperature < temperature else "warming"
wind_change = "strengthening" if future_wind_speed > wind_speed else "weakening"
moisture_trend = "increasing" if future_humidity > humidity else "decreasing"

if w_future > 0:
    vertical_desc = f"Rising at {w_future:.2f} m/s (convergence → clouds forming)"
elif w_future < 0:
    vertical_desc = f"Sinking at {abs(w_future):.2f} m/s (divergence → clear skies)"
else:
    vertical_desc = "Minimal vertical motion"

summary = f"""
**🌍 Coupled System Analysis** (All 4 Equations Working Together):

**Current State:** {current_weather} with winds from {get_direction_name(wind_direction_deg)} at {wind_speed:.1f} m/s.

**Equation-by-Equation Prediction (next {time_hours} hours):**

1️⃣ **Navier-Stokes (Momentum):** 
   - Wind {wind_change} from {wind_speed:.1f} to {future_wind_speed:.1f} m/s
   - Direction: {get_direction_name(wind_direction_deg)} → {get_direction_name(future_wind_direction_deg)}
   - Pressure gradient and Coriolis forces driving wind changes

2️⃣ **Continuity (Mass Conservation):**
   - Divergence: {divergence*1e5:.2f}×10⁻⁵ s⁻¹ ({'positive (diverging)' if divergence > 0 else 'negative (converging)'})
   - Vertical motion: {vertical_desc}
   - This {'suppresses' if divergence > 0 else 'triggers'} cloud formation

3️⃣ **Thermodynamic Energy:**
   - Temperature {temp_trend} from {temperature:.1f}°C to {future_temperature:.1f}°C
   - Solar heating: {Q_solar/cp*3600:.1f} °C/hr
   - Latent heat {'release' if Q_latent > 0 else 'none'}: {Q_latent/cp*3600:.1f} °C/hr
   - {'Convection active' if future_temperature > temperature + 2 else 'Stable atmosphere'}

4️⃣ **Moisture Transport:**
   - Humidity {moisture_trend} from {humidity:.0f}% to {future_humidity:.0f}%
   - Specific humidity: {specific_humidity*1000:.2f} → {future_specific_humidity*1000:.2f} g/kg
   - Precipitation: {precipitation_rate:.2f} mm/hr {'(rain expected!)' if precipitation_rate > 0.5 else '(no rain)'}
   - Evaporation adding {evaporation_rate:.1f} mm/day moisture

**🔗 Coupled Effects:**
- Pressure {trend} to {future_pressure:.1f} hPa (linked to temperature and divergence)
- {'Moisture condensation releasing latent heat → strengthening updrafts → more rain (positive feedback!)' if precipitation_rate > 1 else 'Stable conditions with minimal coupling effects'}

**Final Forecast:** {future_weather}
"""

st.info(summary)

# Visualizations
st.markdown("---")
st.subheader("📈 Visual Analysis: All 4 Equations")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Wind field (from Navier-Stokes)
ax1 = axes[0, 0]
x = np.linspace(0, 10, 8)
y = np.linspace(0, 10, 8)
X, Y = np.meshgrid(x, y)
U_current = np.ones_like(X) * u_wind + np.random.uniform(-0.3, 0.3, X.shape)
V_current = np.ones_like(Y) * v_wind + np.random.uniform(-0.3, 0.3, Y.shape)
U_future = np.ones_like(X) * u_future + np.random.uniform(-0.3, 0.3, X.shape)
V_future = np.ones_like(Y) * v_future + np.random.uniform(-0.3, 0.3, Y.shape)
ax1.quiver(X, Y, U_current, V_current, alpha=0.6, color='blue', label='Current', scale=80)
ax1.quiver(X, Y, U_future, V_future, alpha=0.6, color='red', label=f'{time_hours}h', scale=80)
ax1.set_title('1. Navier-Stokes: Wind Evolution', fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_aspect('equal')

# Plot 2: Divergence field (from Continuity)
ax2 = axes[0, 1]
x_fine = np.linspace(0, 10, 50)
y_fine = np.linspace(0, 10, 50)
X_fine, Y_fine = np.meshgrid(x_fine, y_fine)
# Create synthetic divergence field
div_field = divergence * 1e5 * (1 + 0.3 * np.sin(X_fine) * np.cos(Y_fine))
contour2 = ax2.contourf(X_fine, Y_fine, div_field, levels=15, cmap='RdBu_r', alpha=0.8)
plt.colorbar(contour2, ax=ax2, label='Divergence (×10⁻⁵ s⁻¹)')
ax2.set_title('2. Continuity: Divergence Field', fontweight='bold')
ax2.set_aspect('equal')
if divergence < 0:
    ax2.text(5, 9, '⬆️ Convergence\n(Rising Air)', ha='center', 
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
else:
    ax2.text(5, 9, '⬇️ Divergence\n(Sinking Air)', ha='center',
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

# Plot 3: Temperature field (from Thermodynamics)
ax3 = axes[1, 0]
T_field = temperature + (X_fine - 5) * (future_temperature - temperature) / 5 + np.random.uniform(-1, 1, X_fine.shape)
contour3 = ax3.contourf(X_fine, Y_fine, T_field, levels=15, cmap='RdYlBu_r', alpha=0.8)
plt.colorbar(contour3, ax=ax3, label='Temperature (°C)')
ax3.set_title('3. Thermodynamics: Temperature Field', fontweight='bold')
ax3.set_aspect('equal')
if Q_latent > 1000:
    ax3.text(5, 9, '🔥 Latent Heat\nRelease Active', ha='center',
             bbox=dict(boxstyle='round', facecolor='orange', alpha=0.8))

# Plot 4: Moisture field (from Moisture equation)
ax4 = axes[1, 1]
q_field = specific_humidity * 1000 + (X_fine - 5) * (future_specific_humidity - specific_humidity) * 1000 / 5
q_field += np.random.uniform(-0.5, 0.5, X_fine.shape)
contour4 = ax4.contourf(X_fine, Y_fine, q_field, levels=15, cmap='Blues', alpha=0.8)
plt.colorbar(contour4, ax=ax4, label='Specific Humidity (g/kg)')
ax4.set_title('4. Moisture: Humidity & Precipitation', fontweight='bold')
ax4.set_aspect('equal')
if precipitation_rate > 0.5:
    # Add rain symbols
    rain_x = np.random.uniform(1, 9, 20)
    rain_y = np.random.uniform(1, 9, 20)
    ax4.scatter(rain_x, rain_y, marker='|', s=100, c='blue', alpha=0.6, linewidths=2)
    ax4.text(5, 9, f'🌧️ Rain\n{precipitation_rate:.1f} mm/hr', ha='center',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

plt.tight_layout()
st.pyplot(fig)

# Time evolution of all variables
st.markdown("---")
st.subheader("⏱️ Temporal Evolution: Coupled System Dynamics")

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 8))
time_points = np.linspace(0, time_hours, 30)

# Wind speed evolution
wind_evolution = wind_speed + ((future_wind_speed - wind_speed) / time_hours) * time_points
axes2[0, 0].plot(time_points, wind_evolution, 'b-', linewidth=2, label='Wind Speed')
axes2[0, 0].set_xlabel('Time (hours)')
axes2[0, 0].set_ylabel('Wind Speed (m/s)')
axes2[0, 0].set_title('Navier-Stokes: Wind Evolution')
axes2[0, 0].grid(True, alpha=0.3)
axes2[0, 0].legend()

# Vertical velocity (from continuity)
w_evolution = w_wind + ((w_future - w_wind) / time_hours) * time_points
axes2[0, 1].plot(time_points, w_evolution, 'g-', linewidth=2, label='Vertical Velocity')
axes2[0, 1].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
axes2[0, 1].fill_between(time_points, 0, w_evolution, where=(w_evolution > 0), 
                         alpha=0.3, color='blue', label='Rising (Convergence)')
axes2[0, 1].fill_between(time_points, 0, w_evolution, where=(w_evolution < 0),
                         alpha=0.3, color='red', label='Sinking (Divergence)')
axes2[0, 1].set_xlabel('Time (hours)')
axes2[0, 1].set_ylabel('Vertical Velocity (m/s)')
axes2[0, 1].set_title('Continuity: Vertical Motion')
axes2[0, 1].grid(True, alpha=0.3)
axes2[0, 1].legend(fontsize=8)

# Temperature evolution
temp_evolution = temperature + ((future_temperature - temperature) / time_hours) * time_points
axes2[1, 0].plot(time_points, temp_evolution, 'r-', linewidth=2, label='Temperature')
axes2[1, 0].set_xlabel('Time (hours)')
axes2[1, 0].set_ylabel('Temperature (°C)')
axes2[1, 0].set_title('Thermodynamics: Temperature Evolution')
axes2[1, 0].grid(True, alpha=0.3)
axes2[1, 0].legend()

# Humidity and precipitation evolution
humidity_evolution = humidity + ((future_humidity - humidity) / time_hours) * time_points
precip_evolution = np.linspace(0, precipitation_rate, len(time_points))
ax_hum = axes2[1, 1]
ax_precip = ax_hum.twinx()
ax_hum.plot(time_points, humidity_evolution, 'b-', linewidth=2, label='Humidity')
ax_precip.bar(time_points, precip_evolution, width=time_hours/30, alpha=0.4, color='blue', label='Precipitation')
ax_hum.set_xlabel('Time (hours)')
ax_hum.set_ylabel('Humidity (%)', color='b')
ax_precip.set_ylabel('Precipitation (mm/hr)', color='blue')
ax_hum.set_title('Moisture: Humidity & Precipitation')
ax_hum.tick_params(axis='y', labelcolor='b')
ax_precip.tick_params(axis='y', labelcolor='blue')
ax_hum.grid(True, alpha=0.3)
lines1, labels1 = ax_hum.get_legend_handles_labels()
lines2, labels2 = ax_precip.get_legend_handles_labels()
ax_hum.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

plt.tight_layout()
st.pyplot(fig2)

# Educational section
st.markdown("---")
st.subheader("🎓 Understanding the Coupled System")

# Create tabs for educational content
edu_tab1, edu_tab2, edu_tab3 = st.tabs([
    "🔗 How Equations Couple", 
    "🖥️ Real NWP Systems",
    "🔢 Step-by-Step Algorithm"
])

with edu_tab1:
    with st.expander("🔗 How the 4 Equations Work Together", expanded=True):
        st.markdown("""
        ### The Beautiful Coupling of Atmospheric Physics
        
        Weather prediction requires solving all 4 equations **simultaneously** because they are deeply interconnected:
        
        #### 🔄 Key Coupling Mechanisms:
        
        **1. Momentum ↔ Continuity:**
        - Wind creates divergence/convergence (∇·u)
        - Divergence drives vertical motion (w)
        - Vertical motion feeds back into horizontal wind patterns
        
        **2. Continuity ↔ Moisture:**
        - Rising air (convergence) → Cooling → Condensation → Clouds & Rain
        - Falling air (divergence) → Warming → Evaporation → Clear skies
        
        **3. Moisture ↔ Thermodynamics:**
        - Condensation releases **latent heat** (2.5 MJ/kg!)
        - This heats the air → Creates buoyancy → Strengthens updrafts
        - **Positive feedback loop** powers thunderstorms and hurricanes!
        
        **4. Thermodynamics ↔ Momentum:**
        - Temperature gradients → Pressure gradients → Wind
        - Wind transports heat → Changes temperature distribution
        
        **5. ALL FOUR → Pressure:**
        - Ideal gas law: P = ρRT (links pressure, density, temperature)
        - Continuity ensures mass conservation
        - Pressure gradients drive winds (Navier-Stokes)
        - Temperature changes affect pressure (Thermodynamics)
        
        #### 🌪️ Real-World Example: Thunderstorm Formation
        
        1. **Solar heating** warms surface → air rises (Thermodynamics)
        2. **Rising air** creates convergence at surface (Continuity)
        3. **Convergence** draws in more air → strengthens updraft (Navier-Stokes)
        4. **Rising air cools** → moisture condenses → clouds form (Moisture)
        5. **Condensation releases latent heat** → air becomes more buoyant (Thermodynamics)
        6. **Stronger updraft** pulls up more moisture → more rain (Coupled feedback!)
        7. **Precipitation** cools the air → creates downdrafts → cycle continues
        
        This is why you **cannot** predict weather with just one equation!
        """)

    with st.expander("⚠️ Why Weather Prediction is Hard (Chaos Theory)"):
        st.markdown("""
        ### The Butterfly Effect & Predictability Limits
        
        #### 🦋 Edward Lorenz's Discovery (1961)
        - Tiny changes in initial conditions → Huge changes in forecasts
        - Famous quote: *"A butterfly flapping wings in Brazil can cause a tornado in Texas"*
        
        #### 📉 Forecast Accuracy Decay
        - **1-3 days**: Very accurate (skill > 90%)
        - **4-7 days**: Good (skill 70-85%)
        - **8-10 days**: Fair (skill 50-70%)
        - **11-14 days**: Limited skill (< 50%)
        - **Beyond 2 weeks**: No better than climatology!
        
        #### 🎲 Why the Limit?
        1. **Nonlinearity**: The (u·∇)u term in Navier-Stokes
        2. **Sensitive dependence**: Small errors **exponentially** grow
        3. **Incomplete observations**: Can't measure everywhere perfectly
        4. **Model approximations**: Physics not 100% accurate
        5. **Chaos**: Atmosphere is inherently chaotic system
        
        #### 💡 What Helps:
        - Better observations (satellites, radar, drones)
        - Higher resolution models
        - Improved physics parameterizations
        - Ensemble forecasting (quantify uncertainty)
        - Machine learning (AI-enhanced predictions)
        
        **But the ~2-week limit is fundamental!** No matter how powerful our computers become, chaos theory sets a hard limit on weather predictability.
        """)

    with st.expander("🚀 Future of Weather Prediction"):
        st.markdown("""
        ### Cutting-Edge Developments
        
        #### 🤖 AI/Machine Learning
        - Google's GraphCast: 10-day forecasts in under 1 minute!
        - Huawei's Pangu-Weather: Beats traditional models on some metrics
        - NVIDIA's FourCastNet: GPU-accelerated predictions
        - **Challenge**: Interpretability and physics consistency
        
        #### 🛰️ Observation Revolution
        - Small satellite constellations (100s of satellites)
        - Ground-based GPS networks (water vapor sensing)
        - Drone swarms for targeted observations
        - Crowdsourced data (smartphones, IoT devices)
        
        #### 💻 Exascale Computing
        - Next-gen supercomputers (1+ exaflop = quintillion calculations/sec)
        - Sub-kilometer global resolution
        - Explicit convection (no parameterization needed)
        - Run-to-run in hours
        
        #### 🌊 Earth System Models
        - Couple atmosphere + ocean + ice + land + chemistry
        - Two-way interactions (e.g., ocean affects weather AND vice versa)
        - Better long-range forecasts (weeks to seasons)
        
        #### 🎯 Probabilistic Forecasts
        - Move from "will it rain?" to "30% chance of 0.5-1 inch rain"
        - Impact-based forecasting: "Dangerous flooding likely"
        - Communicate uncertainty effectively
        
        **The Goal**: More accurate, longer-range, probabilistic forecasts that save lives and property!
        """)

with edu_tab2:
    with st.expander("🖥️ How Real Weather Models Work", expanded=True):
        st.markdown("""
        ### From Equations to Forecasts: The NWP Process
        
        **Modern Numerical Weather Prediction (NWP) systems:**
        
        #### 1. Spatial Discretization
        - Divide atmosphere into **3D grid** (millions of cells)
        - Horizontal resolution: 1-50 km
        - Vertical levels: 50-137 layers (surface to ~50 km altitude)
        
        #### 2. Time Integration
        - Solve all 4 equations at **every grid point**
        - Time steps: seconds to minutes
        - March forward in time: current → 1 hour → 2 hours → ... → 10 days
        
        #### 3. Additional Physics
        Real models include much more:
        - **Radiation**: Solar heating, infrared cooling
        - **Cloud microphysics**: Ice, liquid, mixed-phase processes
        - **Turbulence**: Boundary layer, subgrid-scale mixing
        - **Surface**: Land/ocean interactions, vegetation
        - **Gravity waves**: Mountain effects, atmospheric oscillations
        
        #### 4. Data Assimilation
        - Combine observations with model forecasts
        - Satellites, weather stations, aircraft, balloons
        - Billions of observations daily!
        - Kalman filters, variational methods (4D-Var)
        
        #### 5. Ensemble Forecasting
        - Run model many times with slightly different initial conditions
        - Quantify uncertainty
        - Probability of rain: 70% = 7 out of 10 ensemble members predict rain
        
        #### 6. Supercomputing
        - **NOAA's supercomputers**: 12+ petaflops (quadrillion calculations/second)
        - **Runtime**: Hours to produce a 10-day forecast
        - **Data**: Petabytes stored daily
        
        #### Major Global Models:
        - **GFS** (USA): 13 km resolution, 16-day forecasts
        - **ECMWF** (Europe): 9 km resolution, 10-day forecasts (most accurate!)
        - **UKMO** (UK): Unified Model, 10 km global
        - **JMA** (Japan): 13 km resolution
        - **CMC** (Canada): 15 km resolution
        """)

with edu_tab3:
    st.markdown("""
    ## 🔢 Step-by-Step Algorithm: How This App Predicts Weather
    
    This section explains **exactly** how the simplified weather prediction algorithm works, step by step.
    """)
    
    st.markdown("---")
    
    st.markdown("### 📥 STEP 1 — USER INPUT")
    st.code("""
# User provides initial atmospheric state:
- pressure (hPa)
- temperature (°C)
- humidity (%)
- wind components: u (east-west), v (north-south), w (vertical)
- solar_heating (W/m²)
- evaporation_rate (mm/day)
- time_hours (prediction horizon)
    """, language="python")
    
    st.info("✅ These are your initial conditions for the prediction")
    
    st.markdown("---")
    
    st.markdown("### 🧮 STEP 2 — CALCULATE DERIVED QUANTITIES")
    
    st.markdown("**Wind Speed:**")
    st.code("""
wind_speed = sqrt(u² + v²)
    """, language="python")
    
    st.markdown("**Wind Direction:**")
    st.code("""
wind_direction = arctan2(v, u)  # Returns angle in radians
# Convert to degrees: 0° = East, 90° = North, 180° = West, 270° = South
    """, language="python")
    
    st.markdown("**Specific Humidity (from relative humidity):**")
    st.code("""
# Simplified approximation
specific_humidity = (humidity/100) × 0.015 × exp(temperature/20)  # kg/kg
    """, language="python")
    
    st.success("✅ Basic meteorological quantities computed")
    
    st.markdown("---")
    
    st.markdown("### 🌬️ STEP 3 — CONTINUITY EQUATION (Divergence & Vertical Motion)")
    
    st.markdown("**Calculate Divergence:**")
    st.code("""
# Simplified divergence from wind components
L = 100000  # Characteristic length scale (100 km)
divergence = (u_wind + v_wind) / L + w_wind / 5000

# Physical meaning:
# divergence > 0 → Air spreading out (DIVERGENCE) → Sinking motion
# divergence < 0 → Air converging (CONVERGENCE) → Rising motion
    """, language="python")
    
    st.markdown("**Pressure Change from Divergence:**")
    st.code("""
dt = time_hours × 3600  # Convert hours to seconds

# Pressure tendency (simplified continuity)
pressure_change = -divergence × pressure × 0.001 × dt / 3600
future_pressure = pressure + pressure_change
    """, language="python")
    
    st.warning("""
    **➡️ Key Physics:**
    - **Convergence** (divergence < 0) → Pressure drops → Rising air → Clouds/Rain ☁️🌧️
    - **Divergence** (divergence > 0) → Pressure rises → Sinking air → Clear skies ☀️
    """)
    
    st.markdown("---")
    
    st.markdown("### 🌡️ STEP 4 — THERMODYNAMIC EQUATION (Temperature Change)")
    
    st.markdown("**Heat Sources:**")
    st.code("""
cp = 1005  # Specific heat of air (J/kg/K)

# 1. Solar Heating
Q_solar = solar_heating / rho  # W/m² → J/(kg·s)

# 2. Latent Heat from Condensation
latent_heat = 2.5e6  # J/kg
if w_future > 0 and specific_humidity > 0.008:  # Rising + moist air
    condensation_rate = specific_humidity × 0.3 × (w_future / 5.0)
    Q_latent = latent_heat × condensation_rate
else:
    Q_latent = 0

# 3. Adiabatic Cooling/Warming from Vertical Motion
adiabatic_rate = 9.8 / 1000  # °C per meter (dry adiabatic lapse rate)
Q_adiabatic = -w_future × adiabatic_rate

# 4. Temperature Advection (wind transporting heat)
T_advection = -(u_wind × 0.001 + v_wind × 0.001) × dt / 3600
    """, language="python")
    
    st.markdown("**Total Temperature Change:**")
    st.code("""
dT_dt = (Q_solar + Q_latent) / cp + Q_adiabatic
future_temperature = temperature + dT_dt × dt / 3600 + T_advection
    """, language="python")
    
    st.success("""
    ✅ **Temperature driven by:**
    - Solar radiation heating
    - Latent heat from condensation (powers storms!)
    - Adiabatic cooling when air rises
    - Wind advection of temperature
    """)
    
    st.markdown("---")
    
    st.markdown("### 💨 STEP 5 — NAVIER-STOKES (Wind Update)")
    
    st.markdown("**Forces Acting on Air:**")
    st.code("""
# 1. Pressure Gradient Force (drives air from high → low pressure)
pressure_gradient_x = -(pressure - 1013.25) × 100 / (rho × L)  # m/s²
pressure_gradient_y = -(pressure - 1013.25) × 50 / (rho × L)

# 2. Viscous Damping (friction, usually very small in atmosphere)
viscous_term = -mu × wind_speed / (rho × L²)

# 3. Coriolis Force (Earth's rotation)
coriolis_f = 1e-4  # rad/s at mid-latitudes (f = 2Ω sin(φ))
coriolis_u = coriolis_f × v_wind   # Deflects eastward wind
coriolis_v = -coriolis_f × u_wind  # Deflects northward wind
    """, language="python")
    
    st.markdown("**Wind Component Updates:**")
    st.code("""
# Acceleration = Forces
du_dt = pressure_gradient_x + coriolis_u + viscous_term
dv_dt = pressure_gradient_y + coriolis_v + viscous_term
dw_dt = -divergence × 0.1  # Vertical motion from continuity

# Update wind components
u_future = u_wind + du_dt × dt
v_future = v_wind + dv_dt × dt
w_future = w_wind + dw_dt × dt

# New wind speed and direction
future_wind_speed = sqrt(u_future² + v_future²)
future_wind_direction = arctan2(v_future, u_future)
    """, language="python")
    
    st.success("""
    ✅ **Wind changes due to:**
    - Pressure gradients (primary driver)
    - Coriolis effect (deflects wind to the right in NH)
    - Friction (small effect in free atmosphere)
    """)
    
    st.markdown("---")
    
    st.markdown("### 💧 STEP 6 — MOISTURE EQUATION (Humidity & Precipitation)")
    
    st.code("""
# 1. Evaporation Source (from surface)
evap_source = evaporation_rate / 1000 / 86400  # mm/day → kg/m²/s
dq_evap = evap_source / (rho × 1000) × dt

# 2. Condensation Sink (rain formation)
if condensation_rate > 0:
    dq_condensation = -condensation_rate × dt
    precipitation_rate = -dq_condensation × rho × 1000 × 3600 / dt  # mm/hr
else:
    dq_condensation = 0
    precipitation_rate = 0

# 3. Moisture Advection (wind transporting humidity)
dq_advection = -(u_wind × specific_humidity × 0.00001 + 
                 v_wind × specific_humidity × 0.00001) × dt

# Update moisture
future_specific_humidity = specific_humidity + dq_evap + dq_condensation + dq_advection
future_specific_humidity = max(0, min(0.03, future_specific_humidity))  # Physical bounds

# Convert back to relative humidity
future_humidity = (future_specific_humidity / (0.015 × exp(future_temperature/20))) × 100
    """, language="python")
    
    st.success("""
    ✅ **Moisture changes due to:**
    - Surface evaporation (source)
    - Condensation/precipitation (sink)
    - Wind advection of moisture
    """)
    
    st.markdown("---")
    
    st.markdown("### 🌦️ STEP 7 — WEATHER CLASSIFICATION")
    
    st.code("""
def predict_weather(p, t, h, ws, w_vert, precip):
    score = 0
    
    # Pressure factor
    if p < 1000: score += 3
    elif p < 1010: score += 1
    
    # Humidity factor
    if h > 85: score += 3
    elif h > 70: score += 2
    elif h > 50: score += 1
    
    # Vertical motion factor (from continuity)
    if w_vert > 1.0: score += 4     # Strong updraft
    elif w_vert > 0.2: score += 2
    
    # Precipitation factor (from moisture equation)
    if precip > 5: score += 3
    elif precip > 1: score += 2
    
    # Wind speed factor (from Navier-Stokes)
    if ws > 20: score += 3
    elif ws > 12: score += 2
    elif ws > 8: score += 1
    
    # Temperature extremes
    if t < -10 or t > 38: score += 1
    
    # Classification based on total score
    if score >= 10: return "⛈️ Severe Thunderstorms"
    elif score >= 7: return "🌧️ Heavy Rain/Storms"
    elif score >= 5: return "🌦️ Showers/Light Rain"
    elif score >= 3: return "☁️ Cloudy"
    elif score >= 1: return "⛅ Partly Cloudy"
    else: return "☀️ Clear"

current_weather = predict_weather(pressure, temperature, humidity, 
                                  wind_speed, w_wind, 0)
future_weather = predict_weather(future_pressure, future_temperature, 
                                 future_humidity, future_wind_speed, 
                                 w_future, precipitation_rate)
    """, language="python")
    
    st.info("⚠️ **Note**: This is a simplified scoring system. Real weather classification uses complex algorithms and pattern recognition.")
    
    st.markdown("---")
    
    st.markdown("### 📊 STEP 8 — GENERATE VISUALIZATIONS")
    
    st.markdown("**Graph 1: Wind Vector Field (from Navier-Stokes)**")
    st.code("""
# Create spatial grid
X, Y = meshgrid(linspace(0, 10, 8), linspace(0, 10, 8))

# Add small spatial variations (noise)
U_current = u_wind + random_noise
V_current = v_wind + random_noise
U_future = u_future + random_noise
V_future = v_future + random_noise

# Plot blue arrows (current) and red arrows (future)
quiver(X, Y, U_current, V_current, color='blue')
quiver(X, Y, U_future, V_future, color='red')
    """, language="python")
    st.caption("➡️ Shows how wind velocity field evolves over time")
    
    st.markdown("**Graph 2: Divergence Field (from Continuity)**")
    st.code("""
# Create synthetic divergence field with spatial variations
div_field = divergence × 1e5 × (1 + 0.3 × sin(X) × cos(Y))

# Plot as filled contours
contourf(X_fine, Y_fine, div_field, cmap='RdBu_r')
# Red = divergence (sinking), Blue = convergence (rising)
    """, language="python")
    st.caption("➡️ Shows regions of rising (blue) vs sinking (red) air")
    
    st.markdown("**Graph 3: Temperature Field (from Thermodynamics)**")
    st.code("""
# Create spatial temperature gradient
T_field = temperature + (X - 5) × (future_temperature - temperature) / 5

# Add random variations
T_field += random_noise

contourf(X_fine, Y_fine, T_field, cmap='RdYlBu_r')
    """, language="python")
    st.caption("➡️ Shows temperature distribution and gradients")
    
    st.markdown("**Graph 4: Moisture & Precipitation (from Moisture Equation)**")
    st.code("""
# Specific humidity field
q_field = specific_humidity × 1000 + spatial_gradient

contourf(X_fine, Y_fine, q_field, cmap='Blues')

# If raining, add rain droplet symbols
if precipitation_rate > 0.5:
    scatter(rain_x, rain_y, marker='|', color='blue')  # Rain drops
    """, language="python")
    st.caption("➡️ Shows moisture distribution and precipitation locations")
    
    st.markdown("**Time Evolution Graphs:**")
    st.code("""
# Linear interpolation from current to future state
time_points = linspace(0, time_hours, 30)

wind_evolution = wind_speed + (future_wind_speed - wind_speed)/time_hours × time_points
temp_evolution = temperature + (future_temperature - temperature)/time_hours × time_points
humidity_evolution = humidity + (future_humidity - humidity)/time_hours × time_points
precip_evolution = linspace(0, precipitation_rate, len(time_points))

# Plot all as time series
plot(time_points, wind_evolution)
plot(time_points, temp_evolution)
plot(time_points, humidity_evolution)
bar(time_points, precip_evolution)
    """, language="python")
    st.caption("➡️ Shows temporal evolution of all variables")
    
    st.markdown("---")
    
    st.markdown("### 📝 STEP 9 — GENERATE TEXT SUMMARY")
    
    st.code("""
# Analyze trends
trend = "falling" if pressure_change < 0 else "rising"
temp_trend = "cooling" if future_temperature < temperature else "warming"
wind_change = "strengthening" if future_wind_speed > wind_speed else "weakening"

# Describe vertical motion
if w_future > 0:
    vertical_desc = f"Rising at {w_future:.2f} m/s (convergence → clouds)"
else:
    vertical_desc = f"Sinking at {abs(w_future):.2f} m/s (divergence → clear)"

# Generate comprehensive summary with all physics
summary = f\"\"\"
Current: {current_weather} with {wind_speed:.1f} m/s winds

Predictions ({time_hours} hours):
1. Navier-Stokes: Wind {wind_change} to {future_wind_speed:.1f} m/s
2. Continuity: {vertical_desc}
3. Thermodynamics: Temperature {temp_trend} to {future_temperature:.1f}°C
4. Moisture: Precipitation {precipitation_rate:.2f} mm/hr

Final Forecast: {future_weather}
\"\"\"
    """, language="python")
    
    st.markdown("---")
    
    st.markdown("### 🎯 COMPLETE PIPELINE SUMMARY")
    
    pipeline_df = pd.DataFrame({
        'Stage': ['1️⃣ Input', '2️⃣ Derived Quantities', '3️⃣ Continuity', 
                  '4️⃣ Thermodynamics', '5️⃣ Navier-Stokes', '6️⃣ Moisture',
                  '7️⃣ Classification', '8️⃣ Visualization', '9️⃣ Output'],
        'What Happens': [
            'User enters initial conditions',
            'Calculate wind speed, direction, specific humidity',
            'Compute divergence → Pressure change → Vertical motion',
            'Solar + latent + adiabatic heating → Temperature change',
            'Pressure gradient + Coriolis + friction → Wind change',
            'Evaporation + condensation + advection → Humidity & precipitation',
            'Score-based weather classification',
            'Generate 4 field plots + time series graphs',
            'Display predictions, summary text, warnings'
        ],
        'Key Equation': [
            '—',
            'Basic formulas',
            '∇·u = 0 (continuity)',
            '∂θ/∂t + u·∇θ = Q/cp',
            'ρ(∂u/∂t + u·∇u) = -∇p + f',
            '∂q/∂t + u·∇q = S(q)',
            'Empirical scoring',
            'Plotting libraries',
            'Text formatting'
        ],
        'Output Variable': [
            'p, T, RH, u, v, w',
            'wind_speed, wind_dir, q',
            'divergence, p_future, w_future',
            'T_future, Q_solar, Q_latent',
            'u_future, v_future, wind_speed_future',
            'RH_future, q_future, precip_rate',
            'current_weather, future_weather',
            'Graphs (wind, div, temp, moisture)',
            'Summary, metrics, warnings'
        ]
    })
    
    st.dataframe(pipeline_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.success("""
    ### ✅ KEY TAKEAWAYS
    
    **This Algorithm:**
    - ✅ Uses simplified versions of all 4 fundamental equations
    - ✅ Shows how they couple together (pressure affects temp, temp affects moisture, etc.)
    - ✅ Predicts wind, temperature, humidity, and precipitation
    - ✅ Generates visual and text output
    
    **Real NWP Models:**
    - Use full 3D grids (millions of points)
    - Solve PDEs numerically with advanced schemes
    - Include hundreds more physical processes
    - Run on supercomputers for hours
    - Assimilate billions of observations
    
    **Educational Value:**
    - Demonstrates the physics behind weather prediction
    - Shows equation coupling
    - Provides intuition for how forecasts are made
    - Not suitable for actual forecasting!
    """)

# Physics-based insightsabytes stored daily
    
    #### Major Global Models:
    - **GFS** (USA): 13 km resolution, 16-day forecasts
    - **ECMWF** (Europe): 9 km resolution, 10-day forecasts (most accurate!)
    - **UKMO** (UK): Unified Model, 10 km global
    - **JMA** (Japan): 13 km resolution
    - **CMC** (Canada): 15 km resolution
    """)

with st.expander("⚠️ Why Weather Prediction is Hard (Chaos Theory)"):
    st.markdown("""
    ### The Butterfly Effect & Predictability Limits
    
    #### 🦋 Edward Lorenz's Discovery (1961)
    - Tiny changes in initial conditions → Huge changes in forecasts
    - Famous quote: *"A butterfly flapping wings in Brazil can cause a tornado in Texas"*
    
    #### 📉 Forecast Accuracy Decay
    - **1-3 days**: Very accurate (skill > 90%)
    - **4-7 days**: Good (skill 70-85%)
    - **8-10 days**: Fair (skill 50-70%)
    - **11-14 days**: Limited skill (< 50%)
    - **Beyond 2 weeks**: No better than climatology!
    
    #### 🎲 Why the Limit?
    1. **Nonlinearity**: The (u·∇)u term in Navier-Stokes
    2. **Sensitive dependence**: Small errors **exponentially** grow
    3. **Incomplete observations**: Can't measure everywhere perfectly
    4. **Model approximations**: Physics not 100% accurate
    5. **Chaos**: Atmosphere is inherently chaotic system
    
    #### 💡 What Helps:
    - Better observations (satellites, radar, drones)
    - Higher resolution models
    - Improved physics parameterizations
    - Ensemble forecasting (quantify uncertainty)
    - Machine learning (AI-enhanced predictions)
    
    **But the ~2-week limit is fundamental!** No matter how powerful our computers become, chaos theory sets a hard limit on weather predictability.
    """)

with st.expander("🚀 Future of Weather Prediction"):
    st.markdown("""
    ### Cutting-Edge Developments
    
    #### 🤖 AI/Machine Learning
    - Google's GraphCast: 10-day forecasts in under 1 minute!
    - Huawei's Pangu-Weather: Beats traditional models on some metrics
    - NVIDIA's FourCastNet: GPU-accelerated predictions
    - **Challenge**: Interpretability and physics consistency
    
    #### 🛰️ Observation Revolution
    - Small satellite constellations (100s of satellites)
    - Ground-based GPS networks (water vapor sensing)
    - Drone swarms for targeted observations
    - Crowdsourced data (smartphones, IoT devices)
    
    #### 💻 Exascale Computing
    - Next-gen supercomputers (1+ exaflop = quintillion calculations/sec)
    - Sub-kilometer global resolution
    - Explicit convection (no parameterization needed)
    - Run-to-run in hours
    
    #### 🌊 Earth System Models
    - Couple atmosphere + ocean + ice + land + chemistry
    - Two-way interactions (e.g., ocean affects weather AND vice versa)
    - Better long-range forecasts (weeks to seasons)
    
    #### 🎯 Probabilistic Forecasts
    - Move from "will it rain?" to "30% chance of 0.5-1 inch rain"
    - Impact-based forecasting: "Dangerous flooding likely"
    - Communicate uncertainty effectively
    
    **The Goal**: More accurate, longer-range, probabilistic forecasts that save lives and property!
    """)

# Physics-based insights
st.markdown("---")
st.subheader("🧮 Physics Insights from Your Input")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Dimensionless Numbers")
    reynolds = (rho * wind_speed * 1000) / mu
    st.metric("Reynolds Number", f"{reynolds:.0f}",
              help="Ratio of inertial to viscous forces")
    if reynolds > 4000:
        st.caption("✓ Turbulent flow regime (typical for atmosphere)")
    elif reynolds > 2000:
        st.caption("⚠ Transitional flow")
    else:
        st.caption("⚠ Laminar flow (unrealistic for atmosphere)")
    
    # Richardson number (stability)
    if wind_speed > 0.1:
        N_squared = 9.8 / 300 * (future_temperature - temperature) / 1000  # Simplified
        richardson = N_squared * 1000 / (wind_speed**2)
        st.metric("Richardson Number", f"{richardson:.2f}",
                  help="Atmospheric stability indicator")
        if richardson < 0.25:
            st.caption("✓ Dynamically unstable → Turbulence")
        elif richardson < 1:
            st.caption("⚠ Marginally stable")
        else:
            st.caption("✓ Stable → Suppresses mixing")

with col2:
    st.markdown("#### Energy Analysis")
    
    # Kinetic energy
    ke = 0.5 * rho * wind_speed**2
    st.metric("Kinetic Energy Density", f"{ke:.1f} J/m³")
    
    # Latent heat content
    latent_energy = specific_humidity * rho * 2.5e6
    st.metric("Latent Heat Content", f"{latent_energy/1e3:.1f} kJ/m³",
              help="Energy available from moisture condensation")
    
    if latent_energy > 1e4:
        st.caption("🔥 High energy available → Potential for severe weather")
    
    # Pressure work
    pressure_work = (future_pressure - pressure) * 100  # J/m³
    st.metric("Pressure Work", f"{pressure_work:.0f} J/m³")

# Comparison table
st.markdown("---")
st.subheader("📊 Summary Table: Before vs After")

comparison_df = pd.DataFrame({
    'Variable': ['Wind Speed (m/s)', 'Wind Direction', 'Temperature (°C)', 
                 'Pressure (hPa)', 'Humidity (%)', 'Vertical Motion (m/s)',
                 'Precipitation (mm/hr)', 'Weather Condition'],
    'Current': [f"{wind_speed:.1f}", get_direction_name(wind_direction_deg), 
                f"{temperature:.1f}", f"{pressure:.1f}", f"{humidity:.0f}",
                f"{w_wind:.2f}", "0.00", current_weather],
    f'Predicted (+{time_hours}h)': [f"{future_wind_speed:.1f}", 
                                      get_direction_name(future_wind_direction_deg),
                                      f"{future_temperature:.1f}", f"{future_pressure:.1f}",
                                      f"{future_humidity:.0f}", f"{w_future:.2f}",
                                      f"{precipitation_rate:.2f}", future_weather],
    'Change': [f"{future_wind_speed - wind_speed:+.1f}", 
               f"{future_wind_direction_deg - wind_direction_deg:+.0f}°",
               f"{future_temperature - temperature:+.1f}", f"{pressure_change:+.1f}",
               f"{future_humidity - humidity:+.0f}", f"{w_future - w_wind:+.2f}",
               f"{precipitation_rate:+.2f}", "→"],
    'Governing Equation': ['Navier-Stokes', 'Navier-Stokes', 'Thermodynamic',
                          'Continuity + State', 'Moisture', 'Continuity',
                          'Moisture', 'All 4 Coupled']
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Warning messages
if precipitation_rate > 5:
    st.error("⚠️ HEAVY PRECIPITATION PREDICTED: Flash flooding possible!")
elif precipitation_rate > 2:
    st.warning("⚠️ Moderate to heavy rain expected. Monitor conditions.")

if future_wind_speed > 20:
    st.error("⚠️ HIGH WINDS PREDICTED: Secure loose objects!")
elif future_wind_speed > 15:
    st.warning("⚠️ Strong winds expected. Take precautions.")

if abs(w_future) > 2:
    st.warning("⚠️ Strong vertical motion detected. Thunderstorm development possible!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🌍 Complete Weather Prediction System | All 4 Fundamental Equations</p>
    <p>Navier-Stokes + Continuity + Thermodynamics + Moisture Transport</p>
    <p>⚠️ Educational tool - Not for actual weather forecasting</p>
    <p>Built for understanding the physics behind weather prediction</p>
</div>
""", unsafe_allow_html=True)
