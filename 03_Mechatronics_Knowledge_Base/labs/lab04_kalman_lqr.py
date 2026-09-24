#!/usr/bin/env python3
"""
================================================================================
LAB 04: INVERTED PENDULUM ON CART: LQR & DISCRETE KALMAN FILTER SIMULATION
================================================================================
Reference Simulation for Subsystem 04: Modern Control Theory & State Estimation
Course Benchmarks: MIT 2.14/6.302, ETH Zürich 151-0591-00L, 151-0566-00L
Industrial & DIHK Standards: DIN IEC 60050-351 / DIN 19226, DIHK LF8/LF11

Pure Python 3 Implementation (Standard Library Only: time, math, random, typing)
Zero External Dependencies (Pure-Python matrix operations & DARE Riccati solver).
Target Execution Time: < 150 ms on macOS CPU.
================================================================================
"""

import time
import math
import random
from typing import List, Tuple, Dict, Optional


# ==============================================================================
# MATRIX MATH UTILITIES (Pure Python Lightweight Linear Algebra)
# ==============================================================================

def mat_mul(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Matrix multiplication C = A * B."""
    n, m, p = len(A), len(A[0]), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def mat_vec(A: List[List[float]], x: List[float]) -> List[float]:
    """Matrix-vector multiplication y = A * x."""
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def transpose(A: List[List[float]]) -> List[List[float]]:
    """Matrix transpose A^T."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def mat_add(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Matrix addition C = A + B."""
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_sub(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Matrix subtraction C = A - B."""
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def inv_2x2(M: List[List[float]]) -> List[List[float]]:
    """Inverts a 2x2 matrix analytically."""
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    if abs(det) < 1e-14:
        raise ValueError("Singular 2x2 innovation covariance matrix in Kalman gain calculation.")
    inv_det = 1.0 / det
    return [
        [M[1][1] * inv_det, -M[0][1] * inv_det],
        [-M[1][0] * inv_det, M[0][0] * inv_det]
    ]


# ==============================================================================
# INVERTED PENDULUM ON CART DYNAMICS & STATE-SPACE MODEL
# ==============================================================================

class InvertedPendulumSystem:
    """
    Physical model of an inverted pendulum on a motor-driven cart:
    State vector: x = [p, p_dot, theta, theta_dot]^T
      p         : cart position (m)
      p_dot     : cart velocity (m/s)
      theta     : pendulum angle from upright vertical (rad)
      theta_dot : pendulum angular velocity (rad/s)
    Input u     : horizontal force applied to cart (N)
    """
    def __init__(self, M: float = 1.0, m: float = 0.1, b: float = 0.1,
                 l: float = 0.5, g: float = 9.81, dt: float = 0.01):
        self.M = M
        self.m = m
        self.b = b
        self.l = l
        self.g = g
        self.dt = dt

        # Moment of inertia about center of mass (rod of length 2l or point mass at l)
        # Standard benchmark: slender rod of length L = 2l has I = 1/3 * m * l^2
        self.I = (1.0 / 3.0) * m * (l ** 2)
        Mt = M + m
        Jt = self.I + m * (l ** 2)
        Delta = Mt * Jt - (m * l) ** 2

        # Continuous-Time Linearized State-Space Matrices (around theta = 0):
        # x_dot = A_c * x + B_c * u
        self.A_c = [
            [0.0, 1.0, 0.0, 0.0],
            [0.0, -Jt * b / Delta, (m**2 * g * l**2) / Delta, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, -m * l * b / Delta, (Mt * m * g * l) / Delta, 0.0]
        ]
        self.B_c = [
            [0.0],
            [Jt / Delta],
            [0.0],
            [m * l / Delta]
        ]
        # Measurement matrix: cart position p and pendulum angle theta
        self.C = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0]
        ]

        # Discrete-time discretization via forward Euler / Taylor series:
        # Ad = I + Ac * dt + 0.5 * (Ac * dt)^2
        # Bd = (I * dt + 0.5 * Ac * dt^2) * Bc
        I4 = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
        Ac_dt = [[self.A_c[i][j] * dt for j in range(4)] for i in range(4)]
        Ac2_dt2 = mat_mul(Ac_dt, Ac_dt)
        self.Ad = [[I4[i][j] + Ac_dt[i][j] + 0.5 * Ac2_dt2[i][j] for j in range(4)] for i in range(4)]
        
        B_term = [[I4[i][j] * dt + 0.5 * Ac_dt[i][j] * dt for j in range(4)] for i in range(4)]
        self.Bd = mat_mul(B_term, self.B_c)
        self.Cd = self.C

    def solve_dare_lqr(self, Q: List[List[float]], R: List[List[float]],
                       max_iter: int = 500, tol: float = 1e-8) -> Tuple[List[float], int]:
        """
        Solves the Discrete Algebraic Riccati Equation (DARE) via value iteration:
          P_{k+1} = Ad^T P_k Ad - (Ad^T P_k Bd) (R + Bd^T P_k Bd)^-1 (Bd^T P_k Ad) + Q
        Returns optimal state feedback gain vector K:
          K = (R + Bd^T P Bd)^-1 Bd^T P Ad
        """
        P = [row[:] for row in Q]
        Ad_T = transpose(self.Ad)
        Bd_T = transpose(self.Bd)
        iterations_converged = max_iter

        for it in range(max_iter):
            # Term 1: Ad^T P Ad
            term1 = mat_mul(mat_mul(Ad_T, P), self.Ad)
            # Term 2: (R + Bd^T P Bd)^-1
            scalar_denom = mat_mul(mat_mul(Bd_T, P), self.Bd)[0][0] + R[0][0]
            denom_inv = 1.0 / scalar_denom
            # Term 3: Ad^T P Bd (4x1)
            term3 = mat_mul(mat_mul(Ad_T, P), self.Bd)
            # Term 4: Bd^T P Ad (1x4)
            term4 = mat_mul(mat_mul(Bd_T, P), self.Ad)
            # Outer product correction: term3 * denom_inv * term4 (4x4)
            corr = [[term3[i][0] * denom_inv * term4[0][j] for j in range(4)] for i in range(4)]
            P_next = mat_add(mat_sub(term1, corr), Q)

            diff = sum(abs(P_next[i][j] - P[i][j]) for i in range(4) for j in range(4))
            P = P_next
            if diff < tol:
                iterations_converged = it + 1
                break

        # Optimal gain K
        denom = mat_mul(mat_mul(Bd_T, P), self.Bd)[0][0] + R[0][0]
        K = [(1.0 / denom) * mat_mul(mat_mul(Bd_T, P), self.Ad)[0][j] for j in range(4)]
        return K, iterations_converged


# ==============================================================================
# DISCRETE KALMAN FILTER (JOSEPH STABILIZED COVARIANCE FORM)
# ==============================================================================

class DiscreteKalmanFilter:
    """
    Linear Discrete-Time Kalman Filter (DKF) estimating state x_hat from noisy measurements z:
      Time Update (Predict):
        x_hat_{k|k-1} = Ad * x_hat_{k-1|k-1} + Bd * u_{k-1}
        P_{k|k-1}     = Ad * P_{k-1|k-1} * Ad^T + Q
      Measurement Update (Correct):
        y_k           = z_k - Cd * x_hat_{k|k-1}
        S_k           = Cd * P_{k|k-1} * Cd^T + R
        K_k           = P_{k|k-1} * Cd^T * S_k^-1
        x_hat_{k|k}   = x_hat_{k|k-1} + K_k * y_k
        P_{k|k}       = (I - K_k Cd) P_{k|k-1} (I - K_k Cd)^T + K_k R K_k^T  (Joseph Form)
    """
    def __init__(self, Ad: List[List[float]], Bd: List[List[float]], Cd: List[List[float]],
                 Q_cov: List[List[float]], R_cov: List[List[float]], x0: List[float]):
        self.Ad = Ad
        self.Bd = Bd
        self.Cd = Cd
        self.Q = Q_cov
        self.R = R_cov
        self.x_hat = x0[:]
        self.P = [row[:] for row in Q_cov]  # Initial state error covariance

    def predict(self, u: float):
        """A priori state and covariance prediction step."""
        Ax = mat_vec(self.Ad, self.x_hat)
        self.x_hat = [Ax[i] + self.Bd[i][0] * u for i in range(4)]
        Ad_T = transpose(self.Ad)
        self.P = mat_add(mat_mul(mat_mul(self.Ad, self.P), Ad_T), self.Q)

    def update(self, z: List[float]) -> List[float]:
        """A posteriori measurement innovation and Joseph stabilized correction."""
        z_pred = mat_vec(self.Cd, self.x_hat)
        y = [z[i] - z_pred[i] for i in range(2)]  # Innovation residual

        Cd_T = transpose(self.Cd)
        S = mat_add(mat_mul(mat_mul(self.Cd, self.P), Cd_T), self.R)
        S_inv = inv_2x2(S)

        # Kalman gain (4x2)
        P_Cd_T = mat_mul(self.P, Cd_T)
        K_gain = mat_mul(P_Cd_T, S_inv)

        # Correct state estimate
        Ky = mat_vec(K_gain, y)
        self.x_hat = [self.x_hat[i] + Ky[i] for i in range(4)]

        # Joseph stabilized covariance update
        I4 = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
        K_Cd = mat_mul(K_gain, self.Cd)
        IKC = mat_sub(I4, K_Cd)
        IKC_T = transpose(IKC)
        K_T = transpose(K_gain)

        term1 = mat_mul(mat_mul(IKC, self.P), IKC_T)
        term2 = mat_mul(mat_mul(K_gain, self.R), K_T)
        self.P = mat_add(term1, term2)
        return self.x_hat


# ==============================================================================
# CLOSED-LOOP CONTROL SIMULATION RUNNER
# ==============================================================================

def run_simulation(sim_seconds: float = 3.0) -> Dict[str, object]:
    """
    Executes closed-loop stabilization:
      Plant initialized at perturbation: cart position = 0.20 m, pendulum angle = 0.15 rad (~8.6 deg).
      LQR computes feedback control based on noisy Kalman Filter state estimates.
    """
    random.seed(42)  # Deterministic seed for reproducible verification
    dt = 0.01
    sys = InvertedPendulumSystem(M=1.0, m=0.1, b=0.1, l=0.5, g=9.81, dt=dt)

    # State weighting matrix Q: prioritize angle theta and position p
    Q_lqr = [
        [10.0, 0.0,   0.0,   0.0],
        [0.0,  1.0,   0.0,   0.0],
        [0.0,  0.0, 120.0,   0.0],
        [0.0,  0.0,   0.0,  10.0]
    ]
    # Control effort penalty R
    R_lqr = [[0.1]]

    K, riccati_iters = sys.solve_dare_lqr(Q_lqr, R_lqr)

    # Sensor noise characteristics (Gaussian):
    sigma_p = 0.01    # Cart position standard deviation: 10 mm
    sigma_th = 0.005  # Pendulum angle standard deviation: 0.28 deg

    Q_filter = [
        [1e-4, 0.0,  0.0,  0.0],
        [0.0,  1e-3, 0.0,  0.0],
        [0.0,  0.0,  1e-4, 0.0],
        [0.0,  0.0,  0.0,  1e-3]
    ]
    R_filter = [
        [sigma_p**2, 0.0],
        [0.0, sigma_th**2]
    ]

    # Initial perturbation
    x_true = [0.20, 0.0, 0.15, 0.0]
    kf = DiscreteKalmanFilter(sys.Ad, sys.Bd, sys.Cd, Q_filter, R_filter, x0=[0.0, 0.0, 0.0, 0.0])

    steps = int(sim_seconds / dt)
    history_true: List[List[float]] = []
    history_est: List[List[float]] = []
    u_history: List[float] = []

    for step in range(steps):
        # 1. Generate noisy measurements from physical plant
        z = [
            x_true[0] + random.gauss(0.0, sigma_p),
            x_true[2] + random.gauss(0.0, sigma_th)
        ]
        # 2. Measurement update of state estimator
        x_est = kf.update(z)

        # 3. LQR state feedback control law: u = -K * x_hat
        u = -sum(K[i] * x_est[i] for i in range(4))
        # Actuator physical saturation limits [-20 N, +20 N]
        u = max(-20.0, min(20.0, u))

        history_true.append(x_true[:])
        history_est.append(x_est[:])
        u_history.append(u)

        # 4. Filter time prediction
        kf.predict(u)

        # 5. Plant physical integration (discrete state-space)
        Ax = mat_vec(sys.Ad, x_true)
        x_true = [Ax[i] + sys.Bd[i][0] * u for i in range(4)]

    # Compute performance evaluation metrics
    final_p = history_true[-1][0]
    final_th = history_true[-1][2]
    final_p_dot = history_true[-1][1]
    final_th_dot = history_true[-1][3]

    rmse_p = math.sqrt(sum((history_true[k][0] - history_est[k][0])**2 for k in range(steps)) / steps)
    rmse_th = math.sqrt(sum((history_true[k][2] - history_est[k][2])**2 for k in range(steps)) / steps)

    # Settling time criterion: smallest time after which |theta| < 0.01 rad permanently
    settling_time_s = None
    for step in range(steps):
        if all(abs(history_true[k][2]) < 0.01 for k in range(step, steps)):
            settling_time_s = step * dt
            break

    stabilized = (abs(final_p) < 0.02) and (abs(final_th) < 0.005)

    return {
        "K_gain": K,
        "riccati_iterations": riccati_iters,
        "steps": steps,
        "final_position_m": final_p,
        "final_angle_rad": final_th,
        "final_cart_velocity_mps": final_p_dot,
        "final_angular_velocity_radps": final_th_dot,
        "rmse_position_m": rmse_p,
        "rmse_angle_rad": rmse_th,
        "settling_time_s": settling_time_s,
        "stabilized": stabilized,
        "max_control_force_N": max(abs(u) for u in u_history),
    }


# ==============================================================================
# MAIN BENCHMARK & VERIFICATION HARNESS
# ==============================================================================

def main():
    t_start = time.perf_counter()

    print("=" * 78)
    print("LAB 04: INVERTED PENDULUM LQR STABILIZATION & KALMAN FILTER BENCHMARK")
    print("=" * 78)

    res = run_simulation(sim_seconds=3.0)

    print("\n--- [1] Riccati Solver & Optimal LQR Design ---")
    print(f"Riccati DARE Convergence : {res['riccati_iterations']} iterations")
    print(f"LQR State Feedback Gain K : [{', '.join(f'{k:.3f}' for k in res['K_gain'])}]")
    print(f"Max Control Force Used    : {res['max_control_force_N']:.2f} N (Limit: 20.00 N)")

    print("\n--- [2] Discrete Kalman Filter Estimation Metrics ---")
    print(f"Kalman RMSE Position      : {res['rmse_position_m']*1000.0:.2f} mm")
    print(f"Kalman RMSE Angle         : {res['rmse_angle_rad']*180.0/math.pi:.3f} deg")

    print("\n--- [3] Closed-Loop Stabilization Performance ---")
    print(f"Total Simulation Steps    : {res['steps']} steps (dt = 0.01 s)")
    print(f"Pendulum Settling Time    : {res['settling_time_s']:.2f} s (|theta| < 0.01 rad)")
    print(f"Final Cart Position       : {res['final_position_m']:.4f} m (Target: < 0.02 m)")
    print(f"Final Pendulum Angle      : {res['final_angle_rad']:.5f} rad (Target: < 0.005 rad)")
    print(f"Final Cart Velocity       : {res['final_cart_velocity_mps']:.4f} m/s")
    print(f"Final Angular Velocity    : {res['final_angular_velocity_radps']:.5f} rad/s")
    print(f"System Stabilized (PASS)  : {res['stabilized']}")

    # Verification assertions
    assert res["stabilized"] is True, "Inverted pendulum failed to stabilize!"
    assert res["settling_time_s"] is not None and res["settling_time_s"] < 2.5, "Settling time exceeded threshold!"
    assert res["rmse_position_m"] < 0.02, "Kalman filter position tracking RMSE too high!"

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    print("\n" + "=" * 78)
    print(f"[PASS] Lab 04 Quantitative Verification Completed in {elapsed_ms:.2f} ms (Target < 150.0 ms)")
    print("=" * 78)


if __name__ == "__main__":
    main()
