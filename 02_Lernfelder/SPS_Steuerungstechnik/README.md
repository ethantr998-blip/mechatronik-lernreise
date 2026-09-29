# 🖥️ Lập trình PLC (SPS — Speicherprogrammierbare Steuerung)

**Phục vụ:** LF 7, LF 8, LF 9 · **Trọng tâm:** AP1 & AP2 — lập trình và vận hành bộ điều khiển
**Tiêu chuẩn:** Ngôn ngữ lập trình PLC theo IEC 61131-3 · Phần cứng mục tiêu: Siemens LOGO!, S7-1200/1500

👉 Luyện tập tương tác từng bước: [SPS-Übungskoffer S7-1200](../../05_SPS_S7-1200/README.md) (10 bài KOP có chấm tự động).

---

## 🎯 1. Mục tiêu
* Hiểu chu kỳ quét của PLC (*Zyklus*): đọc ảnh vào (*Prozessabbild der Eingänge*) → xử lý chương trình → ghi ảnh ra.
* Nối tiếp kiến thức [Kỹ thuật số](../../Kỹ%20thuật%20số/README.md): cổng logic → hàm AND/OR trong PLC, Flip-Flop → khối SR/RS, bộ đếm → CTU/CTD.
* Lập trình các khối cơ bản: tiếp điểm, cuộn dây, tự giữ, timer (TON/TOF/TP), counter.
* Đấu nối cảm biến 3 dây PNP/NPN vào ngõ vào số 24 V DC.
* Trên TIA Portal: tạo project, cấu hình phần cứng, viết chương trình, nạp và giám sát online.

## 🧾 2. Ngôn ngữ lập trình (IEC 61131-3)
| Tên tiếng Đức (Siemens) | Tên quốc tế | Ghi chú |
|:---|:---|:---|
| **KOP** — Kontaktplan | LAD — Ladder Diagram | Giống sơ đồ mạch rơ-le |
| **FUP** — Funktionsplan | FBD — Function Block Diagram | Giống sơ đồ cổng logic |
| **SCL** — Structured Control Language | ST — Structured Text | Dạng văn bản, giống Pascal |
| **GRAPH** — Ablaufsprache | SFC — Sequential Function Chart | Điều khiển tuần tự theo bước |

## 💻 3. Công cụ trên MacBook (Intel, RAM 8GB)
* **LOGO! Soft Comfort** (Siemens) — có bản chạy trên macOS, nhẹ, phù hợp làm quen logic PLC.
* **TIA Portal** — chỉ chạy trên Windows → dùng Boot Camp (xem checklist trong [Pruefungsstruktur](../../00_DIHK/Pruefungsstruktur.md)); với RAM 8GB nên tránh chạy trong máy ảo.

## 📖 4. Thuật ngữ (Fachbegriffe)
| Tiếng Việt | Tiếng Đức (*Deutsch*) | Tiếng Anh (*English*) |
|:---|:---|:---|
| Ngõ vào / ngõ ra | **der Eingang / der Ausgang** | input / output |
| Tiếp điểm thường mở | **der Schließer** | normally open contact (NO) |
| Tiếp điểm thường đóng | **der Öffner** | normally closed contact (NC) |
| Bộ định thời | **das Zeitglied / der Timer** | timer |
| Chu kỳ quét | **der Zyklus** | scan cycle |
| Khối chức năng | **der Funktionsbaustein** | function block |

## 🛠️ 5. Nhật ký bài tập
| Ngày | Bài tập | Ngôn ngữ (KOP/FUP/SCL) | File project | Ghi chú lỗi → [Fehlerlog](../../00_DIHK/Fehlerlog.md) |
|:---|:---|:---|:---|:---|
| | | | | |
