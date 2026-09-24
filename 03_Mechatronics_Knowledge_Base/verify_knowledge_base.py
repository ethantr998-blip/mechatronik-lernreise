#!/usr/bin/env python3
"""
Automated Test & Verification Suite for Mechatronics & Robotics Knowledge Base
=============================================================================
Validates:
1. Central Master Matrix (`00_Master_Matrix.md`)
2. Subsystem Knowledge Packages (`01` through `06`)
3. Reference Simulation Scripts (`labs/lab01_kinematics.py` through `labs/lab06_vision_feature.py`)

Standard Library Only: sys, os, re, subprocess, time, pathlib, argparse.
Zero external package dependencies.
"""

import sys
import os
import re
import subprocess
import time
from pathlib import Path
import argparse
from typing import Dict, List, Tuple, Optional, Any


# Terminal formatting with graceful non-TTY fallback
class TerminalColor:
    USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

    GREEN = "\033[92m" if USE_COLOR else ""
    RED = "\033[91m" if USE_COLOR else ""
    YELLOW = "\033[93m" if USE_COLOR else ""
    CYAN = "\033[96m" if USE_COLOR else ""
    BLUE = "\033[94m" if USE_COLOR else ""
    BOLD = "\033[1m" if USE_COLOR else ""
    RESET = "\033[0m" if USE_COLOR else ""


# Expected knowledge packages and simulation scripts
SUBSYSTEM_PACKAGES = [
    {
        "id": "01",
        "file": "01_Kinematics_Dynamics_Actuation.md",
        "name": "Kinematics, Dynamics & Actuation",
        "lab": "labs/lab01_kinematics.py",
        "dihk": ["LF1", "LF2", "LF7"],
    },
    {
        "id": "02",
        "file": "02_Power_Electronics_Signal_Conditioning.md",
        "name": "Power Electronics & Signal Conditioning",
        "lab": "labs/lab02_signal_filter.py",
        "dihk": ["LF3", "LF4", "LF8"],
    },
    {
        "id": "03",
        "file": "03_Embedded_Systems_Firmware.md",
        "name": "Embedded Systems & Firmware Architecture",
        "lab": "labs/lab03_can_rtos_sim.py",
        "dihk": ["LF5", "LF7", "LF9"],
    },
    {
        "id": "04",
        "file": "04_Control_Theory_Estimation.md",
        "name": "Modern Control Theory & State Estimation",
        "lab": "labs/lab04_kalman_lqr.py",
        "dihk": ["LF8", "LF11"],
    },
    {
        "id": "05",
        "file": "05_Autonomous_Robotics_ROS2_SLAM.md",
        "name": "Autonomous Robotics, ROS 2 & SLAM",
        "lab": "labs/lab05_astar_rrt.py",
        "dihk": ["LF10", "LF12"],
    },
    {
        "id": "06",
        "file": "06_Computer_Vision_Robot_Learning.md",
        "name": "Computer Vision & Robot Learning",
        "lab": "labs/lab06_vision_feature.py",
        "dihk": ["LF6", "LF10", "LF13"],
    },
]

MASTER_MATRIX_FILE = "00_Master_Matrix.md"

ALL_DIHK_LERNFELDER = [f"LF{i}" for i in range(1, 14)]


class VerificationResult:
    def __init__(self, target_name: str, target_type: str):
        self.target_name = target_name
        self.target_type = target_type
        self.status = "PENDING"  # PASS, FAIL, PENDING
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metrics: Dict[str, Any] = {}
        self.duration_ms: float = 0.0

    @property
    def passed(self) -> bool:
        return self.status == "PASS"

    @property
    def failed(self) -> bool:
        return self.status == "FAIL"

    @property
    def pending(self) -> bool:
        return self.status == "PENDING"


def count_substantive_lines(content: str) -> int:
    """Counts non-empty, substantive lines of text."""
    lines = content.splitlines()
    return sum(1 for line in lines if line.strip())


def extract_sections(content: str) -> Dict[str, str]:
    """Splits markdown package content into the 4 mandatory parts."""
    sections = {}
    lines = content.splitlines()
    current_section = "PREAMBLE"
    current_lines: List[str] = []

    # Patterns matching mandatory top-level section headings (level 1 or 2)
    p1_pat = re.compile(r"^#{1,2}\s+(?:(?:Phần|Part)?\s*1[\.\:\s]+)?.*?(?:Syllabus Breakdown|Đề cương chuẩn hóa)", re.IGNORECASE)
    p2_pat = re.compile(r"^#{1,2}\s+(?:(?:Phần|Part)?\s*2[\.\:\s]+)?.*?(?:Academic Reading List|Danh mục tài liệu)", re.IGNORECASE)
    p3_pat = re.compile(r"^#{1,2}\s+(?:(?:Phần|Part)?\s*3[\.\:\s]+)?.*?(?:Practical Labs|Bài tập thực hành)", re.IGNORECASE)
    p4_pat = re.compile(r"^#{1,2}\s+(?:(?:Phần|Part)?\s*4[\.\:\s]+)?.*?(?:Exact Search Queries|Từ khóa tìm kiếm|Bilingual Terminology|Thuật ngữ)", re.IGNORECASE)

    for line in lines:
        if p1_pat.search(line) and current_section not in ("PART1", "PART2", "PART3", "PART4"):
            sections[current_section] = "\n".join(current_lines)
            current_section = "PART1"
            current_lines = [line]
        elif p2_pat.search(line) and current_section not in ("PART2", "PART3", "PART4"):
            sections[current_section] = "\n".join(current_lines)
            current_section = "PART2"
            current_lines = [line]
        elif p3_pat.search(line) and current_section not in ("PART3", "PART4"):
            sections[current_section] = "\n".join(current_lines)
            current_section = "PART3"
            current_lines = [line]
        elif p4_pat.search(line) and current_section != "PART4":
            sections[current_section] = "\n".join(current_lines)
            current_section = "PART4"
            current_lines = [line]
        else:
            current_lines.append(line)

    sections[current_section] = "\n".join(current_lines)
    return sections


def verify_markdown_package(file_path: Path, pkg_info: Dict[str, Any]) -> VerificationResult:
    """Performs rigorous static analysis on an individual subsystem package."""
    res = VerificationResult(pkg_info["file"], "Markdown Package")
    start_t = time.perf_counter()

    if not file_path.exists():
        res.status = "FAIL"
        res.errors.append(f"File not found: {file_path}")
        res.duration_ms = (time.perf_counter() - start_t) * 1000.0
        return res

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        res.status = "FAIL"
        res.errors.append(f"Failed to read file: {e}")
        res.duration_ms = (time.perf_counter() - start_t) * 1000.0
        return res

    # 1. Non-empty & Line Count >= 250
    substantive_lines = count_substantive_lines(content)
    res.metrics["substantive_lines"] = substantive_lines
    if substantive_lines < 250:
        res.errors.append(f"Substantive lines count {substantive_lines} < 250 minimum required threshold.")

    sections = extract_sections(content)

    # 2. Part 1: Syllabus Breakdown
    if "PART1" not in sections:
        res.errors.append("Missing Part 1 heading: 'Syllabus Breakdown' or 'Đề cương chuẩn hóa'.")
    else:
        part1_text = sections["PART1"]
        # Module count >= 10
        # Matches headings like: ### Module 01: ..., ### Chương 1: ..., ### Tuần 1: ...
        module_matches = re.findall(
            r"^#{2,4}\s*(?:Module|Chương|Tuần)\s*(\d+)[:\s\.]",
            part1_text,
            re.MULTILINE | re.IGNORECASE,
        )
        if not module_matches:
            # Fallback check across bold items or lists
            module_matches = re.findall(
                r"(?:^|\n)\s*(?:#{2,4}|\d+\.|\*|-)\s+\*?\*?(?:Module|Chương|Tuần)\s*(\d+)[:\s\.]",
                part1_text,
                re.IGNORECASE,
            )
        unique_modules = set(module_matches)
        module_count = max(len(module_matches), len(unique_modules))
        res.metrics["modules"] = module_count
        if module_count < 10:
            res.errors.append(f"Part 1 contains {module_count} modules; expected >= 10.")

        # University course citations: MIT, Stanford, ETH, UC Berkeley, TUM, or Georgia Tech
        univ_pattern = re.compile(
            r"\b(MIT|Stanford|ETH(?:\s+Z[uü]rich)?|UC\s+Berkeley|Berkeley|TUM|TU\s+M[uü]nchen|Georgia\s+Tech)\b",
            re.IGNORECASE,
        )
        found_univs = set(univ_pattern.findall(content))
        res.metrics["university_citations"] = sorted(list(found_univs))
        if not found_univs:
            res.errors.append("Part 1 lacks explicit university citations (expected MIT, Stanford, ETH, UC Berkeley, TUM, or Georgia Tech).")

        # LaTeX Equation Blocks: $$...$$ or \begin{equation}...\end{equation}
        latex_blocks = re.findall(r"\$\$([\s\S]*?)\$\$", content)
        alt_latex = re.findall(r"\\begin\{equation\*?\}[\s\S]*?\\end\{equation\*?\}", content)
        total_latex = len(latex_blocks) + len(alt_latex)
        res.metrics["latex_blocks"] = total_latex
        if total_latex < 3:
            res.errors.append(f"Found {total_latex} LaTeX equation blocks ($$...$$); expected >= 3.")

    # 3. Part 2: Academic Reading List
    if "PART2" not in sections:
        res.errors.append("Missing Part 2 heading: 'Academic Reading List' or 'Danh mục tài liệu học thuật'.")
    else:
        part2_text = sections["PART2"]
        # Look for referenced books/papers with author and year (19xx or 20xx)
        ref_items = []
        for line in part2_text.splitlines():
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("|"):
                continue
            # Check if line is a list item containing a 4-digit year (19xx or 20xx)
            if re.match(r"^(?:\d+\.|\*|-)\s+", s) and re.search(r"\b(19\d{2}|20\d{2})\b", s):
                ref_items.append(s)

        res.metrics["reading_list_items"] = len(ref_items)
        if len(ref_items) < 5:
            res.errors.append(f"Part 2 contains {len(ref_items)} academic citations; expected >= 5.")

    # 4. Part 3: Practical Labs
    if "PART3" not in sections:
        res.errors.append("Missing Part 3 heading: 'Practical Labs' or 'Bài tập thực hành'.")
    else:
        part3_text = sections["PART3"]
        lab_items = re.findall(
            r"(?:^|\n)\s*(?:#{2,4}|\d+\.|\*|-)\s+\*?\*?(?:Lab|Bài tập(?:\s+thực hành)?|Project)\s*(\d+)[:\s\.]",
            part3_text,
            re.IGNORECASE,
        )
        if not lab_items:
            lab_items = re.findall(r"(?:Lab|Bài tập(?:\s+thực hành)?)\s*0?(\d+)", part3_text, re.IGNORECASE)
        unique_labs = set(lab_items)
        lab_count = max(len(lab_items), len(unique_labs))
        res.metrics["practical_labs"] = lab_count
        if lab_count < 3:
            res.errors.append(f"Part 3 contains {lab_count} lab assignments; expected >= 3.")

    # 5. Part 4: Exact Search Queries & Bilingual Terminology Table
    if "PART4" not in sections:
        res.errors.append("Missing Part 4 heading: 'Exact Search Queries & Bilingual Terminology' or 'Từ khóa tìm kiếm & Thuật ngữ'.")
    else:
        part4_text = sections["PART4"]
        # Search Queries: Count list items in Part 4 that are not table rows
        query_candidates = []
        for line in part4_text.splitlines():
            s = line.strip()
            if not s or s.startswith("|") or s.startswith("#"):
                continue
            # Match numbered items: e.g. "1. query", "12. query"
            m_num = re.match(r"^\d+\.\s+(.+)$", s)
            if m_num:
                query_candidates.append(m_num.group(1).strip())
                continue
            # Match bullet item if containing search operators or quotes
            m_bullet = re.match(r"^[-*]\s+(.+)$", s)
            if m_bullet and (any(k in s.lower() for k in ["site:", "filetype:", "pdf", "github", "topic"]) or '"' in s or '`' in s):
                query_candidates.append(m_bullet.group(1).strip())

        res.metrics["search_queries"] = len(query_candidates)
        if len(query_candidates) < 12:
            res.errors.append(f"Part 4 contains {len(query_candidates)} search queries; expected >= 12.")

        # Bilingual Terminology Table: Markdown table rows >= 15
        table_rows = []
        for line in part4_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                # Ignore table header dividers like |---|---|
                if re.match(r"^\|[\s\-:|]+\|$", stripped):
                    continue
                # Split columns
                cols = [c.strip() for c in stripped.split("|")[1:-1]]
                if len(cols) >= 3 and not ("English" in cols[0] and ("German" in cols[1] or "Fachbegriff" in cols[1])):
                    table_rows.append(cols)

        res.metrics["terminology_rows"] = len(table_rows)
        if len(table_rows) < 15:
            res.errors.append(f"Part 4 terminology table has {len(table_rows)} rows; expected >= 15.")

    res.duration_ms = (time.perf_counter() - start_t) * 1000.0
    res.status = "PASS" if not res.errors else "FAIL"
    return res


def verify_master_matrix(file_path: Path) -> VerificationResult:
    """Validates 00_Master_Matrix.md for cross-cutting coverage."""
    res = VerificationResult(MASTER_MATRIX_FILE, "Central Master Matrix")
    start_t = time.perf_counter()

    if not file_path.exists():
        res.status = "FAIL"
        res.errors.append(f"File not found: {file_path}")
        res.duration_ms = (time.perf_counter() - start_t) * 1000.0
        return res

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        res.status = "FAIL"
        res.errors.append(f"Failed to read file: {e}")
        res.duration_ms = (time.perf_counter() - start_t) * 1000.0
        return res

    substantive_lines = count_substantive_lines(content)
    res.metrics["substantive_lines"] = substantive_lines
    if substantive_lines < 100:
        res.warnings.append(f"Master Matrix has {substantive_lines} substantive lines (recommended >= 100).")

    # 1. Presence and cross-mapping of all 6 subsystems
    missing_subsystems = []
    for pkg in SUBSYSTEM_PACKAGES:
        sub_id = pkg["id"]
        has_file = pkg["file"] in content
        core_name = pkg["name"].split(",")[0].split("&")[0].strip()
        pat = re.compile(rf"(?:Subsystem|Phân hệ|\b)\s*0?{sub_id}\b.*?(?:{re.escape(core_name)})", re.IGNORECASE)
        has_entry = bool(pat.search(content))
        if not (has_file or has_entry):
            missing_subsystems.append(f"Subsystem {sub_id} ({pkg['name']})")

    res.metrics["missing_subsystems"] = missing_subsystems
    if missing_subsystems:
        res.errors.append(f"Master Matrix missing coverage of: {', '.join(missing_subsystems)}")

    # 2. Coverage of German DIHK Lernfelder LF1 through LF13
    found_lfs = set(re.findall(r"\bLF\s*([1-9]|1[0-3])\b", content, re.IGNORECASE))
    all_lf_nums = {str(i) for i in range(1, 14)}
    missing_lfs = sorted(list(all_lf_nums - found_lfs), key=lambda x: int(x))
    res.metrics["dihk_lernfelder_covered"] = len(found_lfs)
    if missing_lfs:
        res.errors.append(f"Master Matrix missing DIHK Lernfelder: {', '.join([f'LF{x}' for x in missing_lfs])}")

    # 3. Cross-cutting dataflow architecture & Lab catalog
    dataflow_detected = bool(
        re.search(r"(?:dataflow|architecture|architektur|luồng dữ liệu|dependency graph)", content, re.IGNORECASE)
        and ("-->" in content or "->" in content or "==>" in content or "graph" in content or "flow" in content)
    )
    res.metrics["dataflow_architecture"] = dataflow_detected
    if not dataflow_detected:
        res.errors.append("Master Matrix lacks cross-cutting dataflow architecture diagram/graph.")

    # Lab catalog check (references to lab01 through lab06)
    missing_labs = []
    for i in range(1, 7):
        lab_id = f"lab0{i}"
        if lab_id not in content:
            missing_labs.append(lab_id)
    res.metrics["missing_lab_catalog"] = missing_labs
    if missing_labs:
        res.errors.append(f"Master Matrix lab catalog missing references to: {', '.join(missing_labs)}")

    res.duration_ms = (time.perf_counter() - start_t) * 1000.0
    res.status = "PASS" if not res.errors else "FAIL"
    return res


def verify_simulation_script(script_path: Path, pkg_info: Dict[str, Any], timeout_sec: float = 5.0) -> VerificationResult:
    """Executes a reference simulation script and checks for clean exit code and quantitative metrics."""
    res = VerificationResult(pkg_info["lab"], "Simulation Script")
    start_t = time.perf_counter()

    if not script_path.exists():
        res.status = "FAIL"
        res.errors.append(f"Script file not found: {script_path}")
        res.duration_ms = (time.perf_counter() - start_t) * 1000.0
        return res

    cmd = [sys.executable, str(script_path)]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        res.status = "FAIL"
        res.errors.append(f"Execution timed out after {timeout_sec} seconds.")
        res.duration_ms = (time.perf_counter() - start_t) * 1000.0
        return res
    except Exception as e:
        res.status = "FAIL"
        res.errors.append(f"Failed to spawn subprocess: {e}")
        res.duration_ms = (time.perf_counter() - start_t) * 1000.0
        return res

    exec_duration_ms = (time.perf_counter() - start_t) * 1000.0
    res.duration_ms = exec_duration_ms
    res.metrics["exec_duration_ms"] = round(exec_duration_ms, 2)
    res.metrics["exit_code"] = proc.returncode

    if proc.returncode != 0:
        res.errors.append(f"Process exited with non-zero code {proc.returncode}.")
        if proc.stderr:
            res.errors.append(f"Stderr: {proc.stderr.strip()[:300]}")
        res.status = "FAIL"
        return res

    stdout = proc.stdout.strip()
    if not stdout:
        res.errors.append("Standard output was empty; expected quantitative verification output.")
        res.status = "FAIL"
        return res

    # Check for quantitative performance/verification metrics in stdout
    metric_pat = re.compile(
        r"(?:[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?\s*(?:ms|s|rad|m|mm|deg|%|Hz|V|A|dB|steps?|nodes?|pts?|iterations?))"
        r"|(?:(?:error|residual|cost|time|rmse|snr|loss|margin|runtime|metric|convergence|iterations?|variance|bandwidth|tracking|deviation)\s*[:=]\s*[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)"
        r"|(?:\[(?:PASS|VERIFIED|OK|BENCHMARK)\])",
        re.IGNORECASE,
    )
    matches = metric_pat.findall(stdout)
    res.metrics["metric_matches_count"] = len(matches)

    if not matches and not any(char.isdigit() for char in stdout):
        res.errors.append("Standard output does not contain quantitative metrics or numeric benchmarks.")
        res.status = "FAIL"
        return res

    # Sample snippet of output
    first_line = stdout.splitlines()[0] if stdout.splitlines() else ""
    last_line = stdout.splitlines()[-1] if stdout.splitlines() else ""
    res.metrics["output_summary"] = f"{first_line} ... {last_line}"[:120]

    res.status = "PASS"
    return res


def print_banner(text: str, color: str = TerminalColor.BOLD):
    line = "=" * 78
    print(f"\n{color}{line}\n{text}\n{line}{TerminalColor.RESET}")


def format_status(status: str) -> str:
    if status == "PASS":
        return f"{TerminalColor.GREEN}[PASS]{TerminalColor.RESET}"
    elif status == "FAIL":
        return f"{TerminalColor.RED}[FAIL]{TerminalColor.RESET}"
    elif status == "PENDING":
        return f"{TerminalColor.YELLOW}[PENDING]{TerminalColor.RESET}"
    elif status == "WARN":
        return f"{TerminalColor.YELLOW}[WARN]{TerminalColor.RESET}"
    return f"[{status}]"


def run_verification_suite(
    base_dir: Path,
    progressive: bool = False,
    markdown_only: bool = False,
    labs_only: bool = False,
    quiet: bool = False,
) -> Tuple[int, List[VerificationResult]]:
    """Runs the complete verification suite across all components."""
    results: List[VerificationResult] = []

    print_banner(
        f"MECHATRONICS & ROBOTICS KNOWLEDGE BASE VERIFICATION SUITE\n"
        f"Base Directory: {base_dir}\n"
        f"Mode: {'PROGRESSIVE (Tolerant of pending components)' if progressive else 'STRICT (All 13 components required)'}"
    )

    # 1. Central Master Matrix
    if not labs_only:
        matrix_path = base_dir / MASTER_MATRIX_FILE
        if not matrix_path.exists() and progressive:
            res = VerificationResult(MASTER_MATRIX_FILE, "Central Master Matrix")
            res.status = "PENDING"
            res.warnings.append("Component not yet created (pending milestone).")
            results.append(res)
        else:
            res = verify_master_matrix(matrix_path)
            results.append(res)

    # 2. Subsystem Markdown Packages
    if not labs_only:
        for pkg in SUBSYSTEM_PACKAGES:
            pkg_path = base_dir / pkg["file"]
            if not pkg_path.exists() and progressive:
                res = VerificationResult(pkg["file"], "Markdown Package")
                res.status = "PENDING"
                res.warnings.append("Component not yet created (pending milestone).")
                results.append(res)
            else:
                res = verify_markdown_package(pkg_path, pkg)
                results.append(res)

    # 3. Simulation Scripts
    if not markdown_only:
        for pkg in SUBSYSTEM_PACKAGES:
            script_path = base_dir / pkg["lab"]
            if not script_path.exists() and progressive:
                res = VerificationResult(pkg["lab"], "Simulation Script")
                res.status = "PENDING"
                res.warnings.append("Component not yet created (pending milestone).")
                results.append(res)
            else:
                res = verify_simulation_script(script_path, pkg)
                results.append(res)

    # Output detailed diagnostics per item
    if not quiet:
        for r in results:
            status_str = format_status(r.status)
            dur_str = f"({r.duration_ms:.1f}ms)" if r.duration_ms > 0 else ""
            print(f"{status_str} {r.target_type:<18} | {r.target_name:<42} {dur_str}")
            for err in r.errors:
                print(f"       {TerminalColor.RED}✖ Error:{TerminalColor.RESET} {err}")
            for warn in r.warnings:
                print(f"       {TerminalColor.YELLOW}⚠ Notice:{TerminalColor.RESET} {warn}")
            if r.status == "PASS" and r.metrics:
                metric_strs = []
                for k, v in r.metrics.items():
                    if k in ["substantive_lines", "modules", "latex_blocks", "reading_list_items", "terminology_rows", "search_queries", "exec_duration_ms"]:
                        metric_strs.append(f"{k}={v}")
                if metric_strs:
                    print(f"       {TerminalColor.CYAN}ℹ Metrics:{TerminalColor.RESET} {', '.join(metric_strs)}")

    # Summary table
    pass_count = sum(1 for r in results if r.passed)
    fail_count = sum(1 for r in results if r.failed)
    pending_count = sum(1 for r in results if r.pending)
    total_count = len(results)

    print_banner("VERIFICATION SUMMARY & AUDIT TRAIL")
    print(f"Total Components Evaluated: {total_count}")
    print(f"  {TerminalColor.GREEN}Passed:{TerminalColor.RESET}  {pass_count}")
    print(f"  {TerminalColor.RED}Failed:{TerminalColor.RESET}  {fail_count}")
    print(f"  {TerminalColor.YELLOW}Pending:{TerminalColor.RESET} {pending_count}")

    if fail_count > 0:
        print(f"\n{TerminalColor.RED}{TerminalColor.BOLD}STATUS: FAILED ({fail_count} components failed validation){TerminalColor.RESET}\n")
        return 1, results
    elif pending_count > 0 and not progressive:
        print(f"\n{TerminalColor.RED}{TerminalColor.BOLD}STATUS: FAILED ({pending_count} components missing in STRICT mode. Use --progressive for incremental runs){TerminalColor.RESET}\n")
        return 1, results
    else:
        print(f"\n{TerminalColor.GREEN}{TerminalColor.BOLD}STATUS: SUCCESS (All evaluated components passed validation){TerminalColor.RESET}\n")
        return 0, results


def main():
    parser = argparse.ArgumentParser(
        description="Automated Test & Verification Suite for Mechatronics & Robotics Knowledge Base"
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default=str(Path(__file__).resolve().parent),
        help="Base directory containing Markdown packages and labs/ (default: script parent dir)",
    )
    parser.add_argument(
        "--progressive",
        action="store_true",
        help="Progressive mode: validates existing files and reports pending milestones without failing the suite",
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Run static checks only on Markdown files",
    )
    parser.add_argument(
        "--labs-only",
        action="store_true",
        help="Run execution checks only on simulation scripts",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode: suppress per-item metric details, print summary only",
    )

    args = parser.parse_args()
    base_dir = Path(args.base_dir).resolve()

    exit_code, _ = run_verification_suite(
        base_dir=base_dir,
        progressive=args.progressive,
        markdown_only=args.markdown_only,
        labs_only=args.labs_only,
        quiet=args.quiet,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
