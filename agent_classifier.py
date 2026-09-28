#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
ZALO STUDY AGENT - BỘ PHÂN LOẠI TÀI LIỆU HỌC TẬP TỰ ĐỘNG
Dành cho: Sinh viên Kỹ thuật Cơ điện tử (Mechatronik) - Chuẩn CHLB Đức Lilama 2
Tối ưu hóa: macOS Native (Zero-dependencies, siêu nhẹ, không tốn RAM)
=============================================================================
"""

import os
import re
import sys
import time
import shutil
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

# Thư mục gốc chứa các môn học
WORKSPACE_DIR = Path(os.environ.get("STUDY_WORKSPACE_DIR", "/Users/trangiaphat/Documents/Inbox_HocTap"))
# Thư mục đệm hứng file từ Zalo
BUFFER_DIR = WORKSPACE_DIR / "_Zalo_Raw"

# Danh bạ môn học và các từ khóa đặc trưng (Domain Terminology)
SUBJECT_RULES = {
    "Kỹ thuật điện": {
        "de": "Elektrotechnik",
        "exact_titles": ["kỹ thuật điện", "ky thuat dien", "cơ sở kỹ thuật điện", "mh08", "direct current technology", "alternating current"],
        "keywords": [
            "định luật ohm", "kirchhoff", "mạch điện", "dòng điện", "điện áp", 
            "hiệu điện thế", "công suất điện", "xoay chiều", "một chiều", "direct current", 
            "alternating current", "dc circuit", "ac circuit", "điện trở", "cuộn cảm", 
            "tụ điện", "mạch cầu", "nguồn điện", "tổng trở", "hệ số công suất", "32121cd"
        ]
    },
    "Kỹ thuật số": {
        "de": "Digitaltechnik",
        "exact_titles": ["kỹ thuật số", "ky thuat so", "kts", "digitaltechnik"],
        "keywords": [
            "cổng logic", "logic gate", "bảng chân lý", "truth table", "bìa karnaugh", 
            "k-map", "nhị phân", "binary", "thập lục phân", "hexadecimal", "flip flop", 
            "flip-flop", "latch", "mã bcd", "thanh ghi", "register", "bộ đếm", "counter", 
            "mạch tuần tự", "mạch tổ hợp", "multiplexer", "mux", "demux", "đại số boole"
        ]
    },
    "Điện tử cơ bản": {
        "de": "Grundlagen der Elektronik",
        "exact_titles": ["điện tử cơ bản", "dien tu co ban", "dtcb", "vật liệu dẫn điện"],
        "keywords": [
            "bán dẫn", "semiconductor", "diode", "transistor", "bjt", "mosfet", 
            "chỉnh lưu", "khuếch đại", "op-amp", "opamp", "khuếch đại thuật toán", 
            "vật liệu dẫn điện", "linh kiện điện tử", "pn junction", "mối nối pn", 
            "zenner", "led", "phân cực"
        ]
    },
    "Cơ khí cơ bản": {
        "de": "Grundlagen der Mechanik",
        "exact_titles": ["cơ khí cơ bản", "co khi co ban", "ckcb", "gia công nguội"],
        "keywords": [
            "gia công nguội", "tiện", "phay", "bào", "mài", "hàn", "khoan", 
            "taro", "dũa", "thước cặp", "panme", "đo lường cơ khí", "dung sai", 
            "lắp ghép", "kim loại", "thép", "gang", "vật liệu cơ khí", "ren", "bulong"
        ]
    },
    "Giao tiếp kỹ thuật": {
        "de": "Technische Kommunikation",
        "exact_titles": ["giao tiếp kỹ thuật", "giao tiep ky thuat", "gtkt", "vẽ kỹ thuật", "ve ky thuat"],
        "keywords": [
            "vẽ kỹ thuật", "bản vẽ", "hình chiếu", "hình cắt", "mặt cắt", 
            "hình chiếu đứng", "hình chiếu bằng", "hình chiếu cạnh", "hình chiếu trục đo", 
            "tiêu chuẩn vẽ", "khổ giấy", "tỷ lệ vẽ", "autocad", "cad", "solidworks", "dung sai hình học"
        ]
    },
    "Tin học": {
        "de": "Informatik",
        "exact_titles": ["tin học", "tin hoc", "tin học văn phòng", "tin học đại cương"],
        "keywords": [
            "tin học", "tin học văn phòng", "microsoft word", "microsoft excel", 
            "powerpoint", "bảng tính", "hàm excel", "thuật toán", "algorithm", 
            "lập trình", "ngôn ngữ lập trình", "python", "ngôn ngữ c"
        ]
    },
    "Nhập môn CĐT": {
        "de": "Einführung in die Mechatronik",
        "exact_titles": ["nhập môn cơ điện tử", "nhap mon cdt", "nhập môn cđt", "mechatronics"],
        "keywords": [
            "nhập môn cơ điện tử", "tổng quan ngành cơ điện tử", "chuẩn đầu ra", 
            "chương trình đào tạo", "lilama 2", "nghề nghiệp cơ điện tử", "mechatronik"
        ]
    }
}

def normalize_text(text: str) -> str:
    """Chuẩn hóa Unicode sang dạng NFC và chữ thường để so khớp chính xác"""
    if not text:
        return ""
    return unicodedata.normalize('NFC', text).lower().replace("_", " ")

def contains_term(term: str, text: str) -> bool:
    """Khớp nguyên từ: 'hàn' không được khớp trong 'thực hành', 'led' không khớp 'called'."""
    return re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text) is not None

def extract_text_from_pdf(file_path: Path) -> str:
    """Trích xuất văn bản từ 2 trang đầu của PDF dùng Apple PDFKit (macOS Native)"""
    # Đường dẫn truyền qua argv, không chèn vào mã JXA (tên file chứa " sẽ phá vỡ script)
    script = '''
    function run(argv) {
        ObjC.import("PDFKit");
        var url = $.NSURL.fileURLWithPath(argv[0]);
        var doc = $.PDFDocument.alloc.initWithURL(url);
        var content = "";
        if (doc) {
            var count = Math.min(doc.pageCount, 3);
            for (var i = 0; i < count; i++) {
                var page = doc.pageAtIndex(i);
                if (page) {
                    content += " " + ObjC.unwrap(page.string);
                }
            }
        }
        return content;
    }
    '''
    try:
        res = subprocess.run(["osascript", "-l", "JavaScript", "-e", script, str(file_path.resolve())],
                             capture_output=True, text=True, timeout=10)
        return res.stdout
    except Exception as e:
        return ""

def extract_text_from_docx(file_path: Path) -> str:
    """Trích xuất văn bản từ file Word dùng lệnh textutil có sẵn trên macOS"""
    try:
        res = subprocess.run(["textutil", "-convert", "txt", str(file_path.resolve()), "-stdout"], 
                             capture_output=True, text=True, timeout=10)
        return res.stdout
    except Exception:
        return ""

def extract_text_from_pptx(file_path: Path) -> str:
    """Trích xuất chữ từ các slide PowerPoint bằng thư viện zipfile có sẵn trong Python"""
    texts = []
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            for sf in slide_files[:5]: # Đọc 5 slide đầu tiên
                xml_content = z.read(sf)
                tree = ET.fromstring(xml_content)
                for elem in tree.iter():
                    if elem.tag.endswith('}t') and elem.text:
                        texts.append(elem.text)
    except Exception:
        pass
    return " ".join(texts)

def extract_content(file_path: Path) -> str:
    """Bộ giải mã đa định dạng (Multi-format Content Extractor)"""
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc", ".rtf"]:
        return extract_text_from_docx(file_path)
    elif ext == ".pptx":
        return extract_text_from_pptx(file_path)
    elif ext in [".txt", ".md"]:
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""
    return ""

def score_subjects(file_name: str, content: str) -> dict:
    """Điểm khớp của từng môn học (Multi-tier Scoring Engine)"""
    norm_name = normalize_text(file_name)
    norm_content = normalize_text(content)[:4000]  # Chỉ phân tích 4000 ký tự đầu

    scores = {}
    for folder_name, rule in SUBJECT_RULES.items():
        score = 0

        # 1. Tên file chứa thẳng tên môn học
        if contains_term(normalize_text(folder_name), norm_name):
            score += 20

        # 2. Tiêu đề chuẩn trong tên file hoặc nội dung
        for title in rule["exact_titles"]:
            if contains_term(title, norm_name):
                score += 12
            elif contains_term(title, norm_content):
                score += 6

        # 3. Từ khóa chuyên môn
        for kw in rule["keywords"]:
            if contains_term(kw, norm_name):
                score += 5
            if contains_term(kw, norm_content):
                score += 2

        scores[folder_name] = score
    return scores

def classify_document(file_name: str, content: str) -> tuple:
    """Trả về: (Tên thư mục môn học, Thuật ngữ tiếng Đức, Điểm số khớp)"""
    scores = score_subjects(file_name, content)
    best_folder = max(scores, key=scores.get)
    if scores[best_folder] == 0:
        return None, "", 0
    return best_folder, SUBJECT_RULES[best_folder]["de"], scores[best_folder]

def send_macos_notification(title: str, message: str):
    """Gửi thông báo desktop macOS để người học biết file đã được phân loại xong"""
    # Truyền nội dung qua argv thay vì chèn vào AppleScript: tên file chứa " không thể chèn lệnh
    subprocess.run(["osascript",
                    "-e", "on run argv",
                    "-e", "display notification (item 2 of argv) with title (item 1 of argv)",
                    "-e", "end run",
                    title, message], capture_output=True)

def find_target_folder_path(target_folder_name: str) -> Path:
    """Tìm đúng đường dẫn thư mục môn học trong thư mục mẹ (bất kể chuẩn Unicode NFC/NFD)"""
    norm_target = unicodedata.normalize('NFC', target_folder_name)
    for child in WORKSPACE_DIR.iterdir():
        if child.is_dir() and unicodedata.normalize('NFC', child.name) == norm_target:
            return child
    target_path = WORKSPACE_DIR / norm_target
    target_path.mkdir(exist_ok=True)
    return target_path

def process_file(file_path: Path):
    """Xử lý phân loại và di chuyển 1 file"""
    # Bỏ qua các file ẩn hoặc file tạm đang trong tiến trình tải về của Zalo
    if file_path.name.startswith(".") or file_path.name.endswith(".download") or file_path.name.endswith(".tmp"):
        return

    # Chờ file hoàn tất ghi xuống đĩa (chống lỗi file đang tải dở)
    initial_size = -1
    for _ in range(5):
        try:
            current_size = file_path.stat().st_size
            if current_size == initial_size and current_size > 0:
                break
            initial_size = current_size
            time.sleep(0.5)
        except Exception:
            time.sleep(0.5)

    print(f"\n[⚡] Phát hiện file mới: {file_path.name}")
    print(" ↳ Đang trích xuất nội dung văn bản (Inspection)...")
    content = extract_content(file_path)
    
    folder, de_name, score = classify_document(file_path.name, content)
    
    if folder and score >= 4:
        target_dir = find_target_folder_path(folder)
        destination = target_dir / file_path.name
        
        # Nếu đã tồn tại file cùng tên, thêm hậu tố timestamp tránh ghi đè
        if destination.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            destination = target_dir / f"{stem}_{int(time.time())}{suffix}"

        shutil.move(str(file_path), str(destination))
        msg = f"Đã chuyển vào: '{folder}' ({de_name}) | Độ khớp: {score} điểm"
        print(f" [✓] {msg}")
        send_macos_notification("Zalo Study Agent", f"📁 Đã lưu vào môn: {folder}\nFile: {file_path.name}")
    else:
        print(f" [?] Chưa xác định được môn học chắc chắn (Điểm: {score}). Giữ nguyên tại thư mục chờ.")

def scan_once():
    """Quét và xử lý toàn bộ file hiện có trong _Zalo_Raw"""
    print(f"[*] Bắt đầu quét thư mục đệm: {BUFFER_DIR}")
    files = [f for f in BUFFER_DIR.iterdir() if f.is_file()]
    if not files:
        print("[-] Thư mục _Zalo_Raw hiện đang trống.")
        return
    for f in files:
        process_file(f)

def watch_loop():
    """Vòng lặp giám sát liên tục (Background Daemon Watcher)"""
    print("=" * 60)
    print("🚀 ZALO STUDY AGENT ĐANG CHẠY CHẾ ĐỘ GIÁM SÁT LIÊN TỤC (DAEMON)")
    print(f"📂 Thư mục lắng nghe: {BUFFER_DIR}")
    print("Nhấn Ctrl + C để dừng bất cứ lúc nào.")
    print("=" * 60)
    
    send_macos_notification("Zalo Study Agent", "Bộ lọc tài liệu tự động đã kích hoạt!")
    
    seen_files = set()
    while True:
        try:
            if BUFFER_DIR.exists():
                for item in BUFFER_DIR.iterdir():
                    if item.is_file() and item.name not in seen_files:
                        seen_files.add(item.name)
                        process_file(item)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n[!] Đã dừng giám sát.")
            break
        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch_loop()
    else:
        scan_once()
