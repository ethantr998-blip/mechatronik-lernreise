#!/usr/bin/env python3
"""
================================================================================
LAB 03: FREERTOS PREEMPTIVE SCHEDULER & CAN 2.0B BUS ARBITRATION SIMULATION
================================================================================
Reference Simulation for Subsystem 03: Embedded Systems & Firmware Architecture
Course Benchmarks: ETH Zürich 227-0124-00L, UC Berkeley EE192, Georgia Tech ECE 4550
Industrial & DIHK Standards: ISO 11898-1/2, FreeRTOS Kernel V10, DIHK LF5/LF9

Pure Python 3 Implementation (Standard Library Only: time, math, dataclasses, typing, heapq)
Zero External Dependencies (No NumPy/SciPy required).
Target Execution Time: < 50 ms on macOS CPU.
================================================================================
"""

import time
import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set


# ==============================================================================
# PART 1: FREERTOS PREEMPTIVE PRIORITY SCHEDULER SIMULATION
# ==============================================================================

@dataclass
class TaskTCB:
    """
    Task Control Block (TCB - Taskkontrollblock) per FreeRTOS architecture.
    Higher integer priority = higher scheduling priority.
    """
    name: str
    priority: int               # FreeRTOS Priority (3 = highest, 1 = lowest)
    period_ms: int              # Task period in milliseconds
    wcet_ms: int                # Worst-Case Execution Time (WCET) in ms
    deadline_ms: int            # Relative deadline in ms (implicit deadline D_i = T_i)
    remaining_wcet_ms: int = 0  # Remaining computation budget in current period
    next_release_ms: int = 0    # Absolute time for next release
    instances_completed: int = 0
    deadlines_missed: int = 0
    response_times_ms: List[int] = field(default_factory=list)


def simulate_freertos_scheduler(sim_duration_ms: int = 100) -> Dict[str, object]:
    """
    Simulates a FreeRTOS preemptive priority-based scheduler over discrete 1 ms SysTick ticks.
    Validates Rate Monotonic Scheduling (RMS) utilization bounds (Liu & Layland, 1973).
    """
    tasks = [
        TaskTCB(name="vControlTask", priority=3, period_ms=10, wcet_ms=2, deadline_ms=10),
        TaskTCB(name="vSensorProcessingTask", priority=2, period_ms=20, wcet_ms=4, deadline_ms=20),
        TaskTCB(name="vTelemetryLoggingTask", priority=1, period_ms=50, wcet_ms=8, deadline_ms=50),
    ]

    current_task: Optional[TaskTCB] = None
    context_switches = 0
    timeline: List[str] = []

    for t in range(sim_duration_ms):
        # 1. Release periodic tasks at period boundaries
        for task in tasks:
            if t == task.next_release_ms:
                if task.remaining_wcet_ms > 0:
                    task.deadlines_missed += 1
                task.remaining_wcet_ms = task.wcet_ms
                task.next_release_ms += task.period_ms

        # 2. Preemptive priority dispatching: select highest priority ready task
        ready_tasks = [task for task in tasks if task.remaining_wcet_ms > 0]
        highest_prio_task: Optional[TaskTCB] = None
        if ready_tasks:
            highest_prio_task = max(ready_tasks, key=lambda x: x.priority)

        # 3. Context Switch detection (vTaskSwitchContext / PendSV trigger)
        if highest_prio_task != current_task:
            context_switches += 1
            current_task = highest_prio_task

        # 4. Advance execution by 1 ms SysTick tick
        if current_task is not None:
            current_task.remaining_wcet_ms -= 1
            timeline.append(current_task.name)
            if current_task.remaining_wcet_ms == 0:
                current_task.instances_completed += 1
                # Calculate task response time: completion_time - release_time
                release_time = current_task.next_release_ms - current_task.period_ms
                resp_time = (t + 1) - release_time
                current_task.response_times_ms.append(resp_time)
        else:
            timeline.append("prvIdleTask")

    # Analytical schedulability bounds:
    # Liu & Layland RMS bound: U <= n * (2^(1/n) - 1)
    n = len(tasks)
    ll_bound = n * (2.0 ** (1.0 / n) - 1.0)
    actual_u = sum(task.wcet_ms / task.period_ms for task in tasks)
    
    # Bini et al. Hyperbolic bound: prod(U_i + 1) <= 2
    hyperbolic_prod = 1.0
    for task in tasks:
        hyperbolic_prod *= (task.wcet_ms / task.period_ms + 1.0)

    return {
        "tasks": tasks,
        "context_switches": context_switches,
        "actual_utilization": actual_u,
        "ll_bound": ll_bound,
        "schedulable_by_rms": actual_u <= ll_bound,
        "hyperbolic_bound_pass": hyperbolic_prod <= 2.0,
        "idle_ticks": timeline.count("prvIdleTask"),
        "total_ticks": sim_duration_ms,
    }


# ==============================================================================
# PART 2: CAN 2.0B BUS ARBITRATION & BIT-STUFFING SIMULATION
# ==============================================================================

@dataclass
class CANFrame:
    """
    CAN 2.0A/B Frame Data Structure per ISO 11898-1.
    """
    node_id: str
    can_id: int          # 11-bit standard ID (0x000 - 0x7FF)
    data: List[int]      # Data bytes (0 to 8 bytes)
    rtr: int = 0         # Remote Transmission Request (0 = Data Frame, 1 = Remote Frame)
    ide: int = 0         # Identifier Extension Flag (0 = 11-bit standard, 1 = 29-bit extended)


def build_can_bitstream(frame: CANFrame) -> List[int]:
    """
    Encodes standard CAN 2.0A frame header into raw bitstream:
    SOF (1b dominant 0) + ID (11b) + RTR (1b) + IDE (1b) + r0 (1b) + DLC (4b) + Data (8*len).
    """
    bits = [0]  # Start of Frame (SOF) is always dominant 0
    # 11-bit CAN Identifier (MSB first)
    for i in range(10, -1, -1):
        bits.append((frame.can_id >> i) & 1)
    bits.append(frame.rtr)  # RTR: 0 for data frame
    bits.append(frame.ide)  # IDE: 0 for standard format
    bits.append(0)          # r0: reserved bit (dominant 0)
    dlc = len(frame.data)
    for i in range(3, -1, -1):
        bits.append((dlc >> i) & 1)
    # Payload bytes
    for byte in frame.data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def apply_bit_stuffing(bits: List[int]) -> List[int]:
    """
    Applies standard ISO 11898-1 bit-stuffing rule:
    Whenever 5 consecutive identical bits occur in the stream, insert 1 complementary stuff bit.
    """
    stuffed: List[int] = []
    consecutive = 1
    last_bit = bits[0]
    stuffed.append(last_bit)
    for b in bits[1:]:
        if b == last_bit:
            consecutive += 1
            stuffed.append(b)
            if consecutive == 5:
                stuffed.append(1 - b)  # Insert inverted stuff bit
                consecutive = 1
                last_bit = 1 - b
        else:
            consecutive = 1
            last_bit = b
            stuffed.append(b)
    return stuffed


def simulate_can_arbitration(frames: List[CANFrame], bit_rate_kbps: int = 500) -> Dict[str, object]:
    """
    Simulates non-destructive bitwise arbitration (CSMA/CD + AMP) on the physical bus.
    Wired-AND behavior: dominant '0' overwrites recessive '1'.
    Any node transmitting recessive '1' while sensing dominant '0' immediately loses arbitration.
    """
    t_bit_us = 1000.0 / bit_rate_kbps

    # Encode raw frames and apply bit-stuffing
    stuffed_streams: Dict[str, List[int]] = {}
    for f in frames:
        raw_bits = build_can_bitstream(f)
        stuffed_streams[f.node_id] = apply_bit_stuffing(raw_bits)

    max_len = max(len(s) for s in stuffed_streams.values())
    active_nodes: Set[str] = set(f.node_id for f in frames)
    arbitration_winner: Optional[str] = None
    arbitration_bit_loss: Dict[str, int] = {}

    # Step bit-by-bit through arbitration segment
    for bit_idx in range(max_len):
        current_bits: Dict[str, int] = {}
        for nid in active_nodes:
            if bit_idx < len(stuffed_streams[nid]):
                current_bits[nid] = stuffed_streams[nid][bit_idx]
            else:
                current_bits[nid] = 1  # Bus idle (recessive)

        # Physical bus wired-AND: 0 (dominant) wins over 1 (recessive)
        bus_state = 0 if any(b == 0 for b in current_bits.values()) else 1

        # Check for arbitration loss
        losing_nodes = []
        for nid, b in current_bits.items():
            if b == 1 and bus_state == 0:
                losing_nodes.append(nid)
                arbitration_bit_loss[nid] = bit_idx

        for nid in losing_nodes:
            active_nodes.remove(nid)

        if len(active_nodes) == 1:
            arbitration_winner = list(active_nodes)[0]
            break

    winner_frame_len = len(stuffed_streams[arbitration_winner]) if arbitration_winner else 0
    # Fixed-form tail bits without bit-stuffing:
    # CRC Delimiter (1b) + ACK Slot (1b) + ACK Delimiter (1b) + End of Frame (7b) + Intermission (3b) = 13 bits
    # Plus CRC sequence (15b) = 28 bits
    total_frame_bits = winner_frame_len + 28
    transmission_duration_us = total_frame_bits * t_bit_us

    return {
        "winner_node": arbitration_winner,
        "arbitration_bit_loss": arbitration_bit_loss,
        "stuffed_lengths": {k: len(v) for k, v in stuffed_streams.items()},
        "total_bits_winner": total_frame_bits,
        "transmission_duration_us": transmission_duration_us,
        "bit_rate_kbps": bit_rate_kbps,
        "bit_time_us": t_bit_us,
    }


# ==============================================================================
# MAIN VERIFICATION & BENCHMARK HARNESS
# ==============================================================================

def main():
    t_start = time.perf_counter()

    print("=" * 78)
    print("LAB 03: FREERTOS PREEMPTIVE SCHEDULER & CAN 2.0B ARBITRATION BENCHMARK")
    print("=" * 78)

    # 1. Run FreeRTOS Scheduler Simulation
    sim_ms = 100
    rtos = simulate_freertos_scheduler(sim_duration_ms=sim_ms)

    print("\n--- [1] FreeRTOS Preemptive Priority Scheduler Execution ---")
    print(f"Simulation Duration       : {rtos['total_ticks']} ms")
    print(f"Total Context Switches    : {rtos['context_switches']}")
    print(f"Idle Time                 : {rtos['idle_ticks']} ms ({rtos['idle_ticks']/rtos['total_ticks']*100:.1f}%)")
    print(f"Actual CPU Utilization U  : {rtos['actual_utilization']*100:.2f}%")
    print(f"Liu & Layland RMS Bound   : {rtos['ll_bound']*100:.2f}%")
    print(f"Schedulable by RMS Bound  : {rtos['schedulable_by_rms']}")
    print(f"Hyperbolic Bound Pass     : {rtos['hyperbolic_bound_pass']}")

    total_deadlines_missed = 0
    for task in rtos["tasks"]:
        avg_resp = (sum(task.response_times_ms) / len(task.response_times_ms)) if task.response_times_ms else 0.0
        max_resp = max(task.response_times_ms) if task.response_times_ms else 0.0
        total_deadlines_missed += task.deadlines_missed
        print(f"  Task: {task.name:<22} Prio={task.priority} Completed={task.instances_completed:<2} "
              f"Missed={task.deadlines_missed} AvgResp={avg_resp:.2f} ms MaxResp={max_resp:.2f} ms")

    # 2. Run CAN 2.0B Bus Arbitration Simulation
    frames = [
        CANFrame(node_id="Node_B_BrakeECU", can_id=0x050, data=[0x01, 0x02]),         # Priority Highest: 0x050
        CANFrame(node_id="Node_A_EngineECU", can_id=0x120, data=[0xAA, 0xBB, 0xCC]),   # Priority Medium : 0x120
        CANFrame(node_id="Node_C_BodyECU", can_id=0x750, data=[0xFF]),               # Priority Lowest : 0x750
    ]
    can = simulate_can_arbitration(frames, bit_rate_kbps=500)

    print("\n--- [2] CAN 2.0B Bus Arbitration & Bit-Stuffing Execution ---")
    print(f"Bus Nominal Bitrate       : {can['bit_rate_kbps']} kbps (Nominal bit time = {can['bit_time_us']:.2f} us)")
    print(f"Arbitration Winner Node   : {can['winner_node']} (Message ID: 0x050)")
    for nid, bit_loss in can["arbitration_bit_loss"].items():
        print(f"  Node {nid:<20} lost arbitration at bit index: {bit_loss}")
    for nid, slen in can["stuffed_lengths"].items():
        print(f"  Node {nid:<20} stuffed header + payload length: {slen} bits")
    print(f"Winning Frame Total Bits  : {can['total_bits_winner']} bits (including fixed tail & CRC)")
    print(f"Frame Transmission Delay  : {can['transmission_duration_us']:.2f} us")

    # 3. Validation Assertions
    assert rtos["actual_utilization"] <= rtos["ll_bound"], "RMS Utilization exceeded analytical bound!"
    assert total_deadlines_missed == 0, "Hard real-time deadlines were missed!"
    assert can["winner_node"] == "Node_B_BrakeECU", "Arbitration winner mismatch!"
    assert can["total_bits_winner"] > 0, "Invalid frame bit count!"

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    print("\n" + "=" * 78)
    print(f"[PASS] Lab 03 Quantitative Verification Completed in {elapsed_ms:.2f} ms (Target < 50.0 ms)")
    print("=" * 78)


if __name__ == "__main__":
    main()
