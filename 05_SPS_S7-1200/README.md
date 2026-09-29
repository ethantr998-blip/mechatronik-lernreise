# 🧰 SPS-Übungskoffer S7-1200 (Bàn tập PLC)

**Phục vụ:** LF 7, LF 8, LF 9 · **Trọng tâm:** nền tảng lập trình PLC cho AP1, chuẩn bị cho AP2
**Thiết bị đối chiếu:** CPU 1214C DC/DC/DC · Ngôn ngữ KOP (LAD) theo IEC 61131-3

Mở [`uebungskoffer.html`](./uebungskoffer.html) bằng trình duyệt: một file duy nhất, chạy trên điện thoại và máy tính, không cần cài TIA Portal. Tiến độ và chương trình của từng bài được lưu trong trình duyệt.

## Cách học một bài
1. **Bài học:** đọc lý thuyết, đề bài (Đức + Việt) và *Variablentabelle*.
2. **KOP:** tự viết chương trình trong OB1. Khi CPU ở RUN, dòng tín hiệu hiện như TIA Portal lúc *Beobachten*: xanh lá liền là có dòng, xanh dương nét đứt là không.
3. **Bàn tập:** bấm nút, gạt công tắc, xem quá trình chạy và *Zeitdiagramm* 10 s gần nhất. Trên điện thoại, thẻ KOP có thanh điều khiển ở cạnh dưới.
4. **Prüfen:** máy chấm chạy chương trình trên một CPU ảo riêng qua nhiều tình huống thử. Bí thì dùng *Gợi ý*; *Lösung* chỉ nên xem sau cùng (bài giải bằng lời giải mẫu được đánh dấu ◐ thay vì ✓).

## 10 bài theo lộ trình
| # | Thema | Lệnh TIA Portal | Học được gì |
|:---:|:---|:---|:---|
| 1 | Zuweisung | Schließer, Zuweisung | Chu kỳ quét, PAE/PAA, địa chỉ %I/%Q |
| 2 | UND / ODER | Reihen- und Parallelschaltung | Bảng chân trị, KOP ↔ FUP |
| 3 | Öffner / NICHT | Öffner | Ký hiệu hỏi *trạng thái tín hiệu*, không phải loại nút |
| 4 | Selbsthaltung | Schließer, Zuweisung | Tự giữ, AUS thắng, *Drahtbruchsicherheit* |
| 5 | SR / Behälter | SR, (S), (R) | Bộ nhớ, SR ↔ RS, *Zweipunktregelung* có trễ |
| 6 | Flanke | ┤P├ | Sườn tín hiệu, bẫy đặt/xóa trong cùng chu kỳ |
| 7 | Zeiten | TON, TOF, TP | Khác nhau giữa ba loại timer, *Instanz-DB* |
| 8 | Zähler | CTU, CTD, CTUD | CV, PV, QU/QD, đếm sườn |
| 9 | Wendeschütz | Öffner, Selbsthaltung | Khóa chéo, tránh ngắn mạch, đổi chiều qua AUS |
| 10 | Ampel | TON, (S), (R) | Trình tự theo thời gian, điều kiện an toàn |
| ∞ | Freies Üben | tất cả | Bàn tập 8 vào / 8 ra để tự đặt bài |

## Làm lại trong TIA Portal
Sau khi đạt một bài ở đây, hãy làm lại đúng bài đó trên máy ở trường. Các bước (tạo CPU 1214C, *PLC-Variablen*, OB1, *Übersetzen*, *Laden in Gerät* hoặc S7-PLCSIM, *Beobachten*) có trong thẻ **Hướng dẫn** của trang. TIA Portal chỉ chạy trên Windows.

> Trang mô phỏng phục vụ học tập, không phải phần mềm của Siemens. Một vài điểm được đơn giản hóa (bit nhớ sườn tự quản lý, bộ đếm và timer gọi tắt là C0…C3, T0…T7), điều này được nói rõ trong từng bài.

## Kiểm thử
Trang có sẵn `window.S7UK` để kiểm thử trong console trình duyệt, ví dụ:

```js
const L = S7UK.LESSONS[4];                // Lektion 5
S7UK.grade(L, L.sample())                 // lời giải mẫu phải đạt mọi tiêu chí
```
