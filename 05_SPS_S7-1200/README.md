# 🧰 S7-1200 PLC Trainer (Bàn tập PLC)

**Phục vụ:** LF 7, LF 8, LF 9 · **Trọng tâm:** nền tảng lập trình PLC
**Thiết bị đối chiếu:** CPU 1214C DC/DC/DC · Ngôn ngữ LAD (ladder diagram) theo IEC 61131-3
**Ngôn ngữ trang:** tiếng Anh + tiếng Việt

Mở [`plc-trainer.html`](./plc-trainer.html) bằng trình duyệt: một file duy nhất, chạy trên điện thoại và máy tính, không cần cài TIA Portal. Tiến độ và chương trình của từng bài được lưu trong trình duyệt.

## Cách học một bài
1. **Bài học:** đọc lý thuyết, đề bài và *tag table* (bảng biến).
2. **LAD:** tự viết chương trình trong OB1. Khi CPU ở RUN, dòng tín hiệu hiện như TIA Portal lúc bật *Monitoring*: xanh lá liền là có dòng, xanh dương nét đứt là không.
3. **Bàn tập:** bấm nút, gạt công tắc, xem quá trình chạy và *signal trace* 10 s gần nhất. Trên điện thoại, thẻ LAD có thanh điều khiển ở cạnh dưới.
4. **Check:** máy chấm chạy chương trình trên một CPU ảo riêng qua nhiều tình huống thử. Bí thì dùng *Gợi ý*; *Solution* chỉ nên xem sau cùng (bài giải bằng lời giải mẫu được đánh dấu ◐ thay vì ✓).

## 10 bài theo lộ trình
| # | Chủ đề | Lệnh trong TIA Portal (English) | Học được gì |
|:---:|:---|:---|:---|
| 1 | Assignment | Normally open contact, Assignment | Chu kỳ quét, process image, địa chỉ %I/%Q |
| 2 | AND / OR | Contacts in series and parallel | Bảng chân trị, LAD ↔ FBD |
| 3 | NC / NOT | Normally closed contact | Ký hiệu hỏi *trạng thái tín hiệu*, không phải loại nút |
| 4 | Latching | Normally open contact, Assignment | Tự giữ, OFF thắng, an toàn khi đứt dây |
| 5 | SR / Tank | SR, Set output, Reset output | Bộ nhớ, SR ↔ RS, điều khiển hai điểm có trễ |
| 6 | Edge | Scan operand for positive signal edge | Sườn tín hiệu, bẫy đặt/xóa trong cùng chu kỳ |
| 7 | Timers | TON, TOF, TP | Khác nhau giữa ba loại timer, instance DB |
| 8 | Counters | CTU, CTD, CTUD | CV, PV, QU/QD, đếm sườn |
| 9 | Reversing | NC contact, latching | Khóa chéo, tránh ngắn mạch, đổi chiều qua OFF |
| 10 | Traffic light | TON, Set/Reset output | Trình tự theo thời gian, điều kiện an toàn |
| ∞ | Free practice | tất cả | Bàn tập 8 vào / 8 ra để tự đặt bài |

## Làm lại trong TIA Portal
Sau khi đạt một bài ở đây, hãy làm lại đúng bài đó trên máy ở trường. Các bước (Add new device → CPU 1214C, PLC tags, Main [OB1], Compile, Download to device hoặc S7-PLCSIM, Monitoring) có trong thẻ **Hướng dẫn** của trang, kèm cách chuyển giao diện TIA Portal sang tiếng Anh. TIA Portal chỉ chạy trên Windows.

> Trang mô phỏng phục vụ học tập, không phải phần mềm của Siemens. Một vài điểm được đơn giản hóa (bit nhớ sườn tự quản lý, bộ đếm và timer gọi tắt là C0…C3, T0…T7), điều này được nói rõ trong từng bài.

## Kiểm thử
Trang có sẵn `window.S7UK` để kiểm thử trong console trình duyệt, ví dụ:

```js
const L = S7UK.LESSONS[4];                // Lesson 5
S7UK.grade(L, L.sample())                 // lời giải mẫu phải đạt mọi tiêu chí
```
