import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import log2
from typing import Tuple

st.set_page_config(page_title="BB84 vs BB84-in-DFS Simulator", layout="wide")
st.title("🔐 BB84 vs BB84-in-DFS Simulator — show DFS improves security under collective noise")
st.markdown("""
This app simulates BB84 key distribution in two modes:
- **Standard**: single physical qubit per logical bit.
- **DFS**: encode logical qubit into a 2-qubit decoherence-free subspace that resists *collective dephasing*.

You can toggle noise types and an eavesdropper (intercept-resend).  
The app reports **QBER**, **sifted key size**, and a simple **secret-key fraction** estimate `R ≈ 1 - 2 H(Q)` (Shor–Preskill bound approximation).
""")

# -----------------------
# Utilities
# -----------------------
def H2(p: float) -> float:
    """Binary entropy (bits)."""
    p = max(0.0, min(1.0, p))
    if p == 0 or p == 1:
        return 0.0
    return -(p * log2(p) + (1 - p) * log2(1 - p))

def random_bases_and_bits(n: int) -> Tuple[np.ndarray, np.ndarray]:
    bits = np.random.randint(0, 2, size=n)
    bases = np.random.randint(0, 2, size=n)  # 0 = Z, 1 = X
    return bits, bases

# Pauli matrices (as numpy arrays) - not strictly needed for simplified simulation,
# but kept for clarity and potential extension.
I = np.array([[1,0],[0,1]], dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
H = 1/np.sqrt(2) * np.array([[1,1],[1,-1]], dtype=complex)

def measure_in_basis(state_bit: int, basis: int) -> int:
    """Ideal single-qubit measurement outcome for a qubit prepared as bit in basis."""
    # For simulation we already know how basis and bit map to outcomes:
    # If prepared in same basis, measurement returns the prepared bit.
    # If measured in different basis, outcome is random.
    return state_bit

# -----------------------
# Encoding / decoding
# -----------------------
def prepare_single_qubit(bit: int, basis: int) -> Tuple[int,int]:
    """Return (bit, basis) as prepared for single qubit simulation (placeholder)."""
    return (bit, basis)

def encode_dfs_logical(bit: int, basis: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Encode logical bit into 2 physical qubits using a simple DFS for collective dephasing.
    We'll use a common simple encoding for collective dephasing protection:
      |0_L> = |01>, |1_L> = |10>
    When using X-basis (Hadamard), encode the rotated logical states.
    For simulation we won't manipulate full density matrices — we'll track logical bit/basis
    and perform decoding rules and noise effects accordingly.
    """
    # Represent logical info as (logical_bit, logical_basis)
    return (bit, basis)

# -----------------------
# Noise models
# -----------------------
def apply_independent_depolarizing(qubits_bits: np.ndarray, p: float) -> np.ndarray:
    """
    For simplified bit-level simulation: depolarizing causes a random Pauli to be applied.
    On measurement this will flip the bit with some probability roughly p/2 (simplified).
    We'll model single-qubit flip probability as p_flip = 2/3 * p (approx), but simpler:
    treat p as probability of bit-flip error for demonstration.
    """
    flips = np.random.rand(*qubits_bits.shape) < p
    return qubits_bits ^ flips.astype(int)

def apply_collective_dephasing_single(bits: np.ndarray, phi_prob: float) -> np.ndarray:
    """
    Collective dephasing applies a shared phase (Z) to all qubits simultaneously with some prob.
    For computational-basis (Z-basis) states, Z does nothing to probability of 0/1 (no bit flip),
    but it affects X-basis superpositions (introduces phase error -> effectively causes bit errors
    when measuring in X basis).
    We'll model:
      - If measurement basis == Z: no effect (0 extra bit flip).
      - If measurement basis == X: phase error causes bit-flip with prob phi_prob.
    For the single-qubit mode we'll flip X-basis measurement outcomes with phi_prob.
    """
    # This function will be applied in measurement stage using bases array instead.
    return bits  # placeholder; actual effect handled in measurement logic

# -----------------------
# Eve (intercept-resend)
# -----------------------
def eve_intercept_resend_single(alice_bits, alice_bases, p_eve):
    """
    Eve intercept-resend for single-qubit BB84:
    For each qubit with probability p_eve, Eve measures in random basis and resends the result.
    If Eve measures in wrong basis relative to Alice, she introduces errors.
    We'll return Bob's incoming bits after Eve's action (before channel noise).
    """
    n = len(alice_bits)
    bob_in = alice_bits.copy()
    for i in range(n):
        if np.random.rand() < p_eve:
            eve_basis = np.random.randint(0,2)
            # Eve measures:
            if eve_basis == alice_bases[i]:
                measured = alice_bits[i]
            else:
                measured = np.random.randint(0,2)  # random if wrong basis
            # Eve resends a qubit prepared in (measured, eve_basis)
            # If Bob measures in a different basis will randomize later; for now we just set
            # the state as measured in Eve's basis. To keep simple, set transmitted bit = measured
            bob_in[i] = measured
    return bob_in

def eve_intercept_resend_dfs(alice_logical_bits, alice_logical_bases, p_eve):
    """
    Eve tries to intercept DFS encoded logical qubit.
    If Eve intercepts both physical qubits and measures them, she will likely disturb the DFS.
    In practice, intercepting DFS is harder in collective noise model; here we model Eve as
    measuring logical bit in a random logical basis (Z/X) with probability p_eve, causing errors.
    """
    n = len(alice_logical_bits)
    bob_logical = alice_logical_bits.copy()
    for i in range(n):
        if np.random.rand() < p_eve:
            eve_basis = np.random.randint(0,2)
            if eve_basis == alice_logical_bases[i]:
                measured = alice_logical_bits[i]
            else:
                measured = np.random.randint(0,2)
            bob_logical[i] = measured
    return bob_logical

# -----------------------
# Measurement logic
# -----------------------
def measure_single(bobs_in_bits, bob_bases, alice_bases, collective_phase_prob):
    """
    Simulate Bob's measurement for single-qubit mode, factoring in collective dephasing effect:
    if measuring in X and collective dephasing occurred, flip with probability collective_phase_prob.
    """
    n = len(bobs_in_bits)
    measured = bobs_in_bits.copy()
    # For indices where Bob measures in X basis but channel applied collective dephasing,
    # flip with probability collective_phase_prob.
    # To model collective dephasing, choose if a phase event happened globally:
    dephasing_happened = np.random.rand() < collective_phase_prob
    if dephasing_happened:
        # flip all X-basis measurement outcomes randomly with 50%? Simpler: flip with prob=0.5
        flips = (bob_bases == 1) & (np.random.rand(n) < 0.5)
        measured = measured ^ flips.astype(int)
    return measured, dephasing_happened

def measure_dfs(bob_logical_bits, bob_logical_bases, collective_phase_prob):
    """
    For DFS: because encoding is robust against *collective* phase, if the noise is purely collective
    dephasing, the logical state is preserved. If there are independent errors or Eve, logical bits may flip.
    We'll model collective dephasing as having *no effect* on DFS logical bits; independent noise still flips.
    """
    # If dephasing occurs, DFS protects: do nothing.
    dephasing_happened = np.random.rand() < collective_phase_prob
    return bob_logical_bits.copy(), dephasing_happened

# -----------------------
# Core simulation
# -----------------------
def simulate_bb84(n_bits: int,
                  mode: str,
                  channel_noise: str,
                  p_channel: float,
                  p_collective: float,
                  p_eve: float,
                  seed: int = None):
    """
    mode: 'standard' or 'dfs'
    channel_noise: 'depolarizing' or 'collective_dephasing'
    p_channel: strength of independent depolarizing (0..1)
    p_collective: probability that collective-phase event occurs (0..1) - relevant to collective dephasing
    p_eve: probability Eve intercepts each bit
    """
    if seed is not None:
        np.random.seed(seed)

    # --- Alice prepares ---
    alice_bits, alice_bases = random_bases_and_bits(n_bits)

    if mode == 'standard':
        # Eve acts
        bob_in = eve_intercept_resend_single(alice_bits.copy(), alice_bases, p_eve)

        # Channel noise: independent depolarizing flips bits with prob p_channel
        if channel_noise == 'depolarizing':
            bob_in = apply_independent_depolarizing(bob_in, p_channel)
            # No collective phase
            measured, deph_happened = measure_single(bob_in, alice_bases, alice_bases, 0.0)
        else:  # collective dephasing
            # independent depolarizing maybe small too
            bob_in = apply_independent_depolarizing(bob_in, p_channel)
            # measurement incorporates collective dephasing effect on X-basis
            bob_bases = np.random.randint(0,2,n_bits)  # Bob chooses measurement bases later; but for sim we choose now
            # For fairness we should choose Bob bases now (symmetric)
            bob_bases = np.random.randint(0,2,n_bits)
            measured, deph_happened = measure_single(bob_in, bob_bases, alice_bases, p_collective)
            # But later for sifting we will use the same bob_bases
            bob_bases_final = bob_bases
            return {
                'alice_bits': alice_bits,
                'alice_bases': alice_bases,
                'bob_bits': measured,
                'bob_bases': bob_bases_final,
                'dephasing_happened': deph_happened
            }
        # For depolarizing we still need Bob's bases
        bob_bases = np.random.randint(0,2,n_bits)
        return {
            'alice_bits': alice_bits,
            'alice_bases': alice_bases,
            'bob_bits': measured,
            'bob_bases': bob_bases,
            'dephasing_happened': False
        }

    else:  # DFS mode (logical qubits encoded)
        # Alice prepares logical bits and bases
        alice_log_bits = alice_bits.copy()
        alice_log_bases = alice_bases.copy()

        # Eve intercept-resend on logical level
        bob_logical_after_eve = eve_intercept_resend_dfs(alice_log_bits.copy(), alice_log_bases, p_eve)

        # Channel noise:
        if channel_noise == 'depolarizing':
            # independent physical noise -> some logical flips
            # model by flipping logical bit with prob p_channel (approx)
            flips = np.random.rand(n_bits) < p_channel
            bob_logical_after_eve = bob_logical_after_eve ^ flips.astype(int)
            measured, deph_happened = measure_dfs(bob_logical_after_eve, alice_log_bases, 0.0)
        else:
            # collective dephasing: DFS protects logical qubit -> no effect
            measured, deph_happened = measure_dfs(bob_logical_after_eve, alice_log_bases, p_collective)

        # Bob chooses bases
        bob_bases = np.random.randint(0,2,n_bits)
        return {
            'alice_bits': alice_log_bits,
            'alice_bases': alice_log_bases,
            'bob_bits': measured,
            'bob_bases': bob_bases,
            'dephasing_happened': deph_happened
        }

# -----------------------
# Post-processing: sifting, QBER, key rate
# -----------------------
def sift_and_estimate(sim_res):
    alice_bits = sim_res['alice_bits']
    alice_bases = sim_res['alice_bases']
    bob_bits = sim_res['bob_bits']
    bob_bases = sim_res['bob_bases']

    # Sift: keep indices where bases match
    matches = alice_bases == bob_bases
    sifted_alice = alice_bits[matches]
    sifted_bob = bob_bits[matches]
    sift_len = len(sifted_alice)
    if sift_len == 0:
        qber = 0.0
    else:
        qber = np.mean(sifted_alice != sifted_bob)
    # rough secret-key fraction R >= 1 - 2 H(Q)
    R = max(0.0, 1 - 2 * H2(qber))
    return {
        'sift_len': sift_len,
        'qber': qber,
        'R': R,
        'sifted_alice': sifted_alice,
        'sifted_bob': sifted_bob,
        'dephasing_happened': sim_res['dephasing_happened']
    }

# -----------------------
# Streamlit UI & run
# -----------------------
col1, col2 = st.columns([1,1])

with col1:
    st.header("Simulation parameters")
    N = st.slider("Number of raw qubits (Alice sends)", min_value=100, max_value=5000, value=1000, step=100)
    seed = st.number_input("Random seed (optional, 0 = random)", min_value=0, value=0, step=1)
    if seed == 0:
        seed_val = None
    else:
        seed_val = int(seed)

    mode = st.selectbox("Encoding mode", options=['standard', 'dfs'], index=0,
                        help="standard = single qubit; dfs = logical qubit encoded in 2 physical qubits (protects against collective dephasing)")
    channel_noise = st.selectbox("Channel noise type", options=['depolarizing', 'collective_dephasing'])
    p_channel = st.slider("Independent depolarizing strength (p)", min_value=0.0, max_value=0.5, value=0.02)
    p_collective = st.slider("Collective dephasing probability (prob event)", min_value=0.0, max_value=1.0, value=0.2)
    p_eve = st.slider("Eavesdropper probability (per qubit)", min_value=0.0, max_value=1.0, value=0.1)

    if st.button("Run simulation"):
        with st.spinner("Simulating BB84..."):
            sim = simulate_bb84(N, mode, channel_noise, p_channel, p_collective, p_eve, seed=seed_val)
            stats = sift_and_estimate(sim)

        st.success("Simulation finished")
        st.metric("Sifted key length", stats['sift_len'])
        st.metric("QBER (observed)", f"{stats['qber']*100:.2f} %")
        st.metric("Estimated secret-key fraction R", f"{stats['R']:.4f}")

        st.write("### Explanation")
        if mode == 'standard':
            st.write("- Single-qubit BB84. Collective dephasing causes phase errors that show up as bit flips when measuring in X basis.")
        else:
            st.write("- DFS encoding: logical qubit encoded so that *collective phase* acts trivially on the logical subspace, reducing errors caused by collective dephasing.")

        # show whether a collective dephasing event happened (statistic)
        st.write(f"Collective phase event occurred in this run? **{sim['dephasing_happened']}**")

        # show small sample of sifted key
        if stats['sift_len'] > 0:
            sample_n = min(50, stats['sift_len'])
            alice_sample = ''.join(map(str, stats['sifted_alice'][:sample_n]))
            bob_sample = ''.join(map(str, stats['sifted_bob'][:sample_n]))
            st.write("#### Sifted key sample (first {} bits)".format(sample_n))
            st.code(f"Alice: {alice_sample}\nBob:   {bob_sample}")

        # Visualizations
        fig, ax = plt.subplots(1,2, figsize=(10,4))
        # QBER bar
        ax[0].bar([0,1], [stats['qber']*100, p_eve*100], tick_label=['QBER (%)', 'Eve prob (%)'])
        ax[0].set_ylim(0, max(10, 100*max(stats['qber'], p_eve)))
        ax[0].set_title("QBER vs Eve activity")
        ax[0].grid(True, linestyle=':', alpha=0.5)

        # R vs Q curve (theoretical)
        q_vals = np.linspace(0,0.2,200)
        R_vals = np.maximum(0, 1 - 2 * np.array([H2(q) for q in q_vals]))
        ax[1].plot(q_vals*100, R_vals, label='R = 1 - 2 H(Q)')
        ax[1].scatter([stats['qber']*100], [stats['R']], color='red', label='This run')
        ax[1].set_xlabel("QBER (%)")
        ax[1].set_ylabel("R (secret fraction)")
        ax[1].legend()
        ax[1].grid(True, linestyle=':', alpha=0.5)
        st.pyplot(fig)

        # diagnostic text
        st.write("### Diagnostic / Notes")
        st.markdown("""
        - **DFS helps** primarily when channel noise is *collective dephasing* (same phase error on all physical qubits).
        - If noise is *independent depolarizing*, DFS may not help (it protects against correlated phase only).
        - Eve (intercept-resend) increases QBER; compare runs with p_eve=0 and p_eve>0 to see detection.
        - Secret key fraction R here is a simplified estimate (use more advanced formulas for production systems).
        """)

        st.balloons()
