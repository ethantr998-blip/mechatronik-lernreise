# 🏭 Xưởng ảo Mechatronik (Virtuelle Werkstatt)

**Phục vụ:** LF 7, LF 11 · **Trọng tâm:** AP1 (lập trình PLC) & AP2 (*Fehlersuche*, *Fachgespräch*)

Mở [`sortierstation.html`](./sortierstation.html) bằng trình duyệt: một file duy nhất, không cần cài đặt, chạy được cả trên điện thoại.

## Trạm phân loại (Sortierstation)
Nhìn từ trên xuống: băng tải −M1, cảm biến quang −B1/−B3, cảm biến cảm ứng −B2 (nhận kim loại), xi lanh −1A1 với van 5/2 −1V1 và hai cảm biến vị trí −1B1/−1B2. Chi tiết kim loại (St) phải được đẩy vào thùng *Metall*, chi tiết nhựa (PA) chạy thẳng tới thùng *Kunststoff*.

## Ba chế độ
1. **Lập trình KOP:** tự viết chương trình Ladder, SPS chạy ngay với chu kỳ quét thật. Khi RUN, dòng tín hiệu hiển thị như TIA Portal online. Nút *Chấm bài tự động* chạy chương trình của bạn qua 6 tình huống: Start, đèn H1, Stop, phân loại, Not-Halt không tự chạy lại, đứt dây nút S0.
2. **Tìm lỗi AP2:** trạm bị cài ngẫu nhiên 1 trong 8 lỗi (cảm biến hỏng, đứt dây, cuộn van đứt, mất khí nén, aptomat nhảy…). Dùng đèn LED SPS, đồng hồ vạn năng ảo, làm đúng 3 quy tắc an toàn đầu tiên trước khi sửa, chạy thử rồi bàn giao.
3. **Fachgespräch:** giám khảo hỏi 3 câu bằng tiếng Đức, có giải thích tiếng Việt sau mỗi câu. Điểm theo thang IHK 100 điểm (Note 1–6).

## Chạy kiểm thử
Trang có sẵn `window.XuongAo` để kiểm thử logic trong console trình duyệt, ví dụ:

```js
XuongAo.gradeProgram(XuongAo.SAMPLE())   // lời giải mẫu phải đạt 6/6
```
