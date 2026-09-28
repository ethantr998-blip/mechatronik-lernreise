# 🔍 Vận hành, Tìm lỗi & Bảo trì (Inbetriebnahme, Fehlersuche & Instandhaltung)

**Phục vụ:** LF 3, LF 11, LF 12 · **Trọng tâm:** AP2 — *Fehlersuche* trên hệ thống thực
**Tiêu chuẩn:** DIN VDE 0105-100 (vận hành thiết bị điện) · DIN 31051 (khái niệm bảo trì)

---

## ⚡ 1. Năm quy tắc an toàn (Die fünf Sicherheitsregeln — DIN VDE 0105-100)
Thuộc lòng **đúng thứ tự** — giám khảo AHK hỏi rất thường xuyên:
1. **Freischalten** — cắt điện hoàn toàn.
2. **Gegen Wiedereinschalten sichern** — khóa, treo biển chống đóng điện lại.
3. **Spannungsfreiheit feststellen (allpolig)** — kiểm tra không còn điện trên tất cả các cực.
4. **Erden und Kurzschließen** — nối đất và ngắn mạch.
5. **Benachbarte, unter Spannung stehende Teile abdecken oder abschranken** — che chắn phần tử lân cận còn mang điện.

## 🧰 2. Bốn nhóm công việc bảo trì (DIN 31051)
| Tiếng Đức | Nghĩa | Ví dụ |
|:---|:---|:---|
| **Wartung** | Bảo dưỡng (giữ nguyên trạng thái tốt) | Tra dầu, xả nước cụm lọc khí |
| **Inspektion** | Kiểm tra (xác định trạng thái hiện tại) | Đo điện trở cách điện, nghe tiếng ồn ổ bi |
| **Instandsetzung** | Sửa chữa (khôi phục chức năng) | Thay cảm biến hỏng |
| **Verbesserung** | Cải tiến (tăng độ tin cậy) | Thay loại van bền hơn |

## 🧭 3. Quy trình tìm lỗi có hệ thống
1. Hỏi & quan sát triệu chứng (*Fehlerbeschreibung*) — không tháo lắp vội.
2. Đọc sơ đồ, khoanh vùng khối nghi ngờ (cảm biến → PLC → cơ cấu chấp hành).
3. Đo kiểm từng điểm (tuân thủ 5 quy tắc an toàn khi làm việc trên phần mạch điện).
4. Xác định nguyên nhân gốc (*Fehlerursache*), sửa, rồi **chạy thử lại toàn bộ chức năng**.
5. Ghi biên bản (*Protokoll*) — và ghi vào [Fehlerlog](../../00_DIHK/Fehlerlog.md) nếu là lỗi của chính mình.

## 📖 4. Thuật ngữ (Fachbegriffe)
| Tiếng Việt | Tiếng Đức (*Deutsch*) | Tiếng Anh (*English*) |
|:---|:---|:---|
| Đưa vào vận hành | **die Inbetriebnahme** | commissioning |
| Tìm lỗi | **die Fehlersuche** | troubleshooting |
| Nguyên nhân lỗi | **die Fehlerursache** | root cause |
| Biên bản | **das Protokoll** | report / log |
| Bảo trì | **die Instandhaltung** | maintenance |
