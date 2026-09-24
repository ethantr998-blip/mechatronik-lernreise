# 03. HỆ THỐNG NHÚNG & KIẾN TRÚC FIRMWARE THỜI GIAN THỰC (EMBEDDED SYSTEMS & REAL-TIME FIRMWARE ARCHITECTURE)

> **Tài liệu tri thức phân hệ 03 (Subsystem 03 Knowledge Package)**  
> **Các trường đại học tham chiếu:** ETH Zürich (227-0124-00L), UC Berkeley (EE192), Georgia Tech (ECE 4180 / ECE 4550), MIT (6.302 / 6.08), TU München (TUM)  
> **Tiêu chuẩn công nghiệp & CHLB Đức:** DIN EN ISO 11898 (CAN-Bus), DIN IEC 60050-351, MISRA-C:2012, IEC 61508, DIHK Lernfelder `LF5`, `LF7`, `LF9`  
> **Mã nguồn mô phỏng kiểm chứng:** `labs/lab03_can_rtos_sim.py` (FreeRTOS Preemptive Priority Scheduler & CAN 2.0B Bus Arbitration)  

---

## 1. Standardized Syllabus Breakdown (Đề cương chuẩn hóa)

Phân hệ Hệ thống nhúng và Kiến trúc Firmware đóng vai trò là "bộ não điều hành cấp thấp" (*Low-Level Embedded Brain*) của mọi cỗ máy cơ điện tử. Khác với lập trình ứng dụng trên máy tính thông thường, firmware trong cơ điện tử đòi hỏi tính tất định thời gian (*Temporal Determinism*), độ tin cậy tuyệt đối (*Zero-Defect Reliability*), và khả năng tương tác trực tiếp với thanh ghi phần cứng (*Hardware Registers*) dưới các điều kiện ràng buộc khắt khe về thời gian thực (*Hard Real-Time Deadlines*).

Chương trình đào tạo chuẩn hóa gồm 12 modules chuyên sâu được tổng hợp từ đề cương của **ETH Zürich** (227-0124-00L *Embedded Systems*), **UC Berkeley** (EE192 *Mechatronic Design*), **Georgia Tech** (ECE 4180 *Embedded Systems Design*), đối chiếu trực tiếp với các Trường học tập `LF5`, `LF7` và `LF9` theo chuẩn đào tạo nghề kép CHLB Đức (**DIHK / AHK**).

```
[KIẾN TRÚC PHÂN TẦNG FIRMWARE CƠ ĐIỆN TỬ]
┌────────────────────────────────────────────────────────────────────────┐
│ Ứng dụng điều khiển cấp cao: Quỹ đạo, Động học, LQR / PID Loops        │
├────────────────────────────────────────────────────────────────────────┤
│ Hệ điều hành thời gian thực (FreeRTOS Kernel): TCB, Sched, Queues, Mutex│
├────────────────────────────────────────────────────────────────────────┤
│ Lớp trừu tượng phần cứng (HAL / CMSIS Driver): NVIC, Timers, DMA, CAN  │
├────────────────────────────────────────────────────────────────────────┤
│ Vi điều khiển phần cứng (Silicon): ARM Cortex-M4/M7 Core, SRAM, Flash  │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Module 01: Kiến trúc máy tính & Vi điều khiển ARM Cortex-M (Computer Architecture & ARM Cortex-M)
- **Quy chiếu đại học & Tiêu chuẩn:** ETH Zürich 227-0124-00L (Lec 1-2), UC Berkeley EE192, DIHK `LF5` (*Auswählen und Integrieren von Hardware- und Softwarekomponenten*).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Kiến trúc Harvard sửa đổi (*Modified Harvard Architecture*): Tách biệt không gian bus lệnh (I-Code) và bus dữ liệu (D-Code, System Bus), cho phép nạp lệnh và truy xuất dữ liệu trong cùng một chu kỳ xung nhịp (*Single-Cycle Access*).
  - Đường ống xử lý 3 giai đoạn (*3-Stage Pipeline*): Nạp lệnh (Fetch), Giải mã (Decode), Thực thi (Execute). Hiện tượng rẽ nhánh (*Branching*) và xả đường ống (*Pipeline Flush*).
  - Tập lệnh Thumb-2: Kết hợp linh hoạt giữa các lệnh 16-bit tiết kiệm bộ nhớ và lệnh 32-bit hiệu năng cao, giảm kích thước mã thực thi từ 30% đến 40% so với mã ARM thuần túy.
  - Không gian địa chỉ 32-bit tuyến tính (4 GB): Phân vùng chuẩn gồm Code Flash (0x08000000), SRAM (0x20000000), Vùng ngoại vi Peripheral (0x40000000), và System Control Space (0xE0000000).
  - Khối bảo vệ bộ nhớ (MPU - *Speicherschutzeinheit*): Phân quyền truy cập các vùng nhớ đặc quyền (*Privileged Mode*) và người dùng (*Unprivileged Mode*), ngăn chặn việc ghi đè ngăn xếp (*Stack Overflow*) phá hủy bảng vector ngắt.
- **Mô hình toán học & Phương trình thiết kế:**
  Thời gian chu kỳ xung nhịp hệ thống $T_{\text{cycle}}$ và thời gian thực thi lệnh cơ sở $T_{\text{instr}}$:
  $$T_{\text{cycle}} = \frac{1}{f_{\text{CPU}}}, \quad T_{\text{instr}} = \text{CPI} \cdot T_{\text{cycle}} = \frac{\text{CPI}}{f_{\text{CPU}}}$$
  Trong đó $f_{\text{CPU}}$ là tần số xung nhịp lõi (ví dụ 168 MHz trên STM32F407), $\text{CPI}$ là số chu kỳ xung nhịp trên mỗi lệnh (*Cycles Per Instruction*).

---

### Module 02: Kỹ nghệ Firmware Bare-Metal & Giao tiếp ngoại vi (Bare-Metal Firmware Engineering & Peripheral Interfacing)
- **Quy chiếu đại học & Tiêu chuẩn:** Georgia Tech ECE 4180 (Lab 1-3), DIHK `LF9` (*Programmieren mechatronischer Systeme*).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Cơ chế I/O ánh xạ bộ nhớ (*Memory-Mapped I/O*): Mọi thanh ghi điều khiển, trạng thái và dữ liệu của ngoại vi đều được ánh xạ vào không gian địa chỉ vật lý.
  - Kỹ thuật truy cập thanh ghi thông qua con trỏ và từ khóa `volatile`: Ép trình biên dịch không tối ưu hóa ghi đè thanh ghi (`*(volatile uint32_t*)(PERIPH_BASE + OFFSET)`), đảm bảo thao tác ghi/đọc luôn được phản ánh trực tiếp ra bus vật lý.
  - Bộ điều khiển xung nhịp và khởi động lại (RCC - *Reset and Clock Control*): Cấu hình bộ dao động thạch anh ngoại (HSE), mạch khóa pha nhân tần (PLL - *Phase-Locked Loop*) để cung cấp xung nhịp ổn định cho AHB/APB buses.
  - Cấu hình chân vào/ra đa dụng (GPIO - *General Purpose Input/Output*): 4 chế độ đầu ra (Push-Pull, Open-Drain, Pull-Up, Pull-Down), tốc độ chuyển mạch I/O (Slew Rate), và chế độ chức năng thay thế (*Alternate Function* - AF) kết nối với Timer, UART, SPI, CAN.

---

### Module 03: Kiến trúc ngắt & Bộ điều khiển ngắt vector lồng nhau NVIC (Interrupt Architecture & Nested Vectored Interrupt Controller)
- **Quy chiếu đại học & Tiêu chuẩn:** ETH Zürich 227-0124-00L (Lec 4), UC Berkeley EE192, Yiu (2013) Ch. 7 & 8.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Bảng vector ngắt (*Vector Table*) và tái định vị thông qua thanh ghi VTOR (`SCB->VTOR`): Cho phép chuyển đổi linh hoạt giữa Bootloader và Application Firmware.
  - Phân cấp độ ưu tiên ngắt: Chia tách giữa độ ưu tiên chiếm quyền (*Preemption Priority*) và độ ưu tiên phụ (*Sub-priority*). Một ngắt có độ ưu tiên chiếm quyền cao hơn có thể ngắt quãng ngay lập tức một trình phục vụ ngắt (ISR - *Unterbrechungsroutine*) đang thực thi.
  - Các kỹ thuật tối ưu hóa phần cứng của NVIC trên ARM Cortex-M:
    - Nối đuôi ngắt (*Tail-Chaining*): Tiết kiệm 12 chu kỳ lưu/phục hồi ngăn xếp khi có một ngắt khác đang chờ xử lý, thời gian chuyển đổi giữa hai ngắt chỉ mất đúng 6 chu kỳ xung nhịp.
    - Ngắt đến muộn (*Late Arrival*): Tự động chuyển hướng phục vụ ngắt có ưu tiên cao hơn vừa xuất hiện trong quá trình đang lưu ngăn xếp của ngắt ưu tiên thấp.
    - Chiếm quyền khi phục hồi (*Pop-Preemption*).
- **Mô hình toán học & Phương trình thiết kế:**
  Thời gian lưu khung ngăn xếp tự động bằng phần cứng (*Hardware Stacking* - đẩy 8 thanh ghi R0-R3, R12, LR, PC, xPSR tương đương 32 bytes lên ngăn xếp):
  $$T_{\text{stack}} = \frac{12}{f_{\text{CPU}}}$$
  Tổng độ trễ ngắt xác định (*Total Interrupt Latency*) từ thời điểm chân phần cứng kích hoạt tín hiệu đến khi lệnh đầu tiên của ISR được thực thi:
  $$T_{\text{latency}} = T_{\text{jitter}} + T_{\text{stack}} + T_{\text{pipeline}} + T_{\text{ISR\_entry}}$$
  Với $T_{\text{jitter}} \in [0, T_{\text{cycle}}]$ là sai số trôi dạt do đồng pha xung nhịp, $T_{\text{pipeline}} \approx 3 \cdot T_{\text{cycle}}$ là độ trễ làm sạch đường ống.

---

### Module 04: Bộ định thời nâng cao, Điều chế độ rộng xung PWM phần cứng & DMA (Advanced Timers, Hardware PWM & Direct Memory Access)
- **Quy chiếu đại học & Tiêu chuẩn:** UC Berkeley EE192 (Lab 2), Georgia Tech ECE 4550, DIHK `LF5`.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Cấu trúc bộ định thời phần cứng: Bộ đếm xuôi/ngược (Up/Down Counter), Bộ tiền chia tần (*Prescaler* - PSC), Thanh ghi tự động nạp lại (*Auto-Reload Register* - ARR), Thanh ghi so sánh/bắt giữ (*Capture/Compare Register* - CCR).
  - Điều chế độ rộng xung trung tâm (*Center-Aligned PWM*): Giảm thiểu phổ phát xạ sóng hài bậc cao trong điều khiển van công suất cầu H so với PWM canh mép (*Edge-Aligned*).
  - Tạo khoảng thời gian chết (*Dead-Time Generation* - *Totzeit*): Ngăn chặn hiện tượng ngắn mạch đồng thời hai khóa bán dẫn trên cùng một nhánh cầu H (*Shoot-Through*).
  - Giải mã bộ mã hóa quay phần cứng (*Quadrature Encoder Interface* - QEI): Chế độ đếm x4 bằng cách bắt cả hai sườn lên và sườn xuống trên cả hai kênh lệch pha $90^\circ$ (Channel A & B).
  - Truy cập bộ nhớ trực tiếp (DMA - *Direkter Speicherzugriff*): Vận chuyển dữ liệu tự động giữa ngoại vi (ADC, SPI, UART) và SRAM dạng vòng tròn (*Circular Buffer* - *Ringpuffer*) mà không tiêu tốn chu kỳ xử lý của CPU.
- **Mô hình toán học & Phương trình thiết kế:**
  Tần số xung PWM $f_{\text{PWM}}$ và hệ số chu kỳ tải $D$ (*Duty Cycle*):
  $$f_{\text{PWM}} = \frac{f_{\text{TIM\_CLK}}}{(\text{PSC} + 1) \cdot (\text{ARR} + 1)}, \quad D = \frac{\text{CCR}}{\text{ARR} + 1}$$
  Khoảng thời gian chết an toàn $t_{\text{deadtime}}$ cần cài đặt dựa trên thời gian trễ đóng cắt của MOSFET/IGBT ($t_{\text{off}}, t_{\text{on}}$) và trễ truyền của Gate Driver ($t_{\text{prop}}$):
  $$t_{\text{deadtime}} \ge (t_{\text{off, max}} - t_{\text{on, min}}) + t_{\text{prop\_delay\_skew}} + t_{\text{margin}}$$

---

### Module 05: Kiến trúc nhân hệ điều hành thời gian thực FreeRTOS (Real-Time Operating System Kernel Architecture)
- **Quy chiếu đại học & Tiêu chuẩn:** ETH Zürich 227-0124-00L (Lec 6), Stanford CS237A, Barry (2016) Ch. 3, Kopetz (2011) Ch. 9.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Khái niệm về vi nhân thời gian thực (*Microkernel RTOS*): Quản lý luồng thực thi thông qua Khối điều khiển tác vụ (TCB - *Taskkontrollblock*).
  - Vòng đời và trạng thái của tác vụ: Đang chạy (*Running*), Sẵn sàng (*Ready*), Bị chặn chờ sự kiện (*Blocked*), Tạm ngưng (*Suspended*).
  - Kiến trúc con trỏ ngăn xếp kép trên ARM Cortex-M:
    - Con trỏ ngăn xếp chính (MSP - *Main Stack Pointer*): Dành riêng cho nhân hệ điều hành và tất cả các trình phục vụ ngắt ISR.
    - Con trỏ ngăn xếp tiến trình (PSP - *Process Stack Pointer*): Dành riêng cho không gian thực thi của từng tác vụ độc lập.
  - Cơ chế chuyển đổi ngữ cảnh (*Context Switch* - *Kontextwechsel*): Sử dụng ngắt phần mềm có độ ưu tiên thấp nhất `PendSV` (Pended Software Interrupt). Khi bộ định thời tick hệ thống `SysTick` kích hoạt bộ lập lịch, cờ `PendSV` được dựng lên để trì hoãn việc chuyển ngữ cảnh cho đến khi tất cả các ngắt phần cứng quan trọng hoàn tất.

---

### Module 06: Lý thuyết lập lịch thời gian thực & Phân tích tính khả thi (Real-Time Scheduling Theory & Schedulability Analysis)
- **Quy chiếu đại học & Tiêu chuẩn:** MIT 6.302 / 6.08, Liu & Layland (1973), Kopetz (2011) Ch. 9.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Lập lịch đơn điệu theo chu kỳ (RMS - *Rate Monotonic Scheduling*): Chiến lược gán độ ưu tiên tĩnh tỷ lệ nghịch với chu kỳ ($T_i < T_j \implies \text{Priority}_i > \text{Priority}_j$). Là thuật toán tối ưu trong lớp lập lịch ưu tiên tĩnh.
  - Lập lịch thời hạn sớm nhất (EDF - *Earliest Deadline First*): Thuật toán lập lịch động gán ưu tiên theo thời hạn thực thi gần nhất ($D_i$).
  - Phân tích thời điểm sự cố nguy kịch (*Critical Instant Analysis*): Thời điểm toàn bộ các tác vụ định kỳ đồng thời được kích hoạt giải phóng cùng lúc.
  - Phân tích thời gian đáp ứng chính xác (RTA - *Response Time Analysis*): Kiểm tra tính khả thi cho các hệ thống có thời hạn khác chu kỳ ($D_i \le T_i$).
- **Mô hình toán học & Phương trình thiết kế:**
  Ngưỡng giới hạn sử dụng CPU của Liu & Layland cho $n$ tác vụ định kỳ độc lập:
  $$U = \sum_{i=1}^n \frac{C_i}{T_i} \le n(2^{1/n} - 1), \quad \lim_{n \to \infty} U = \ln 2 \approx 0.69315$$
  Ngưỡng hyperbol Bini et al. (chặt chẽ hơn và giảm độ bảo thủ):
  $$\prod_{i=1}^n \left( \frac{C_i}{T_i} + 1 \right) \le 2$$
  Phương trình đệ quy phân tích thời gian đáp ứng trường hợp xấu nhất (RTA):
  $$R_i^{(k+1)} = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i^{(k)}}{T_j} \right\rceil C_j \le D_i$$
  Trong đó $C_i$ là thời gian thực thi xấu nhất (WCET), $T_i$ là chu kỳ tác vụ, $D_i$ là thời hạn chót (*Deadline*), và $hp(i)$ là tập hợp các tác vụ có độ ưu tiên cao hơn tác vụ $i$.

---

### Module 07: Giao tiếp liên tác vụ & Các cấu trúc đồng bộ hóa (Inter-Task Communication & Synchronization Primitives)
- **Quy chiếu đại học & Tiêu chuẩn:** Georgia Tech ECE 4180, Barry (2016) Ch. 4-5, DIHK `LF9`.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Hàng đợi tin nhắn (Message Queue - *Nachrichtenwarteschlangen*): Truyền dữ liệu an toàn đa luồng theo cơ chế sao chép giá trị (*Pass-by-Value*) hoặc sao chép con trỏ (*Pass-by-Reference*), tích hợp cơ chế tự động chuyển tác vụ sang trạng thái Blocked khi hàng đợi rỗng/đầy.
  - Cờ báo nhị phân (*Binary Semaphore*) và Cờ đếm (*Counting Semaphore*): Phục vụ đồng bộ hóa sự kiện giữa trình phục vụ ngắt ISR và tác vụ nền (*Deferred Interrupt Processing*).
  - Nhóm sự kiện (*Event Groups / Event Flags*): Cho phép một tác vụ chờ đợi đồng thời một tổ hợp nhiều sự kiện logic (AND/OR).
  - Thông báo trực tiếp tới tác vụ (*Direct-to-Task Notifications*): Bỏ qua việc cấp phát cấu trúc RAM trung gian của Queue, tăng tốc độ truyền tin lên 45% và giảm tiêu tốn bộ nhớ RAM.

---

### Module 08: Hiểm họa đồng thời & Các giao thức đảo ngược độ ưu tiên (Concurrency Hazards & Priority Inversion Protocols)
- **Quy chiếu đại học & Tiêu chuẩn:** MIT, TUM, Sha, Rajkumar & Sathaye (1990), Kopetz (2011) Ch. 9.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Điều kiện tương tranh (*Race Conditions*) và Tắc nghẽn tài nguyên (*Deadlocks* - *Verklemmung*).
  - Nghịch đảo độ ưu tiên không giới hạn (*Unbounded Priority Inversion* - *Unbegrenzte Prioritätsinversion*): Bài học kinh điển từ sự cố tàu thám hiểm Sao Hỏa Mars Pathfinder (1997). Khi tác vụ ưu tiên thấp giữ Mutex chia sẻ, tác vụ ưu tiên trung bình (không cần Mutex) chiếm quyền CPU, khiến tác vụ ưu tiên cao bị chặn vô thời hạn.
  - Giao thức kế thừa độ ưu tiên (PIP - *Priority Inheritance Protocol*): Nâng tạm thời độ ưu tiên của tác vụ đang giữ Mutex lên bằng độ ưu tiên của tác vụ cao nhất đang đợi Mutex đó.
  - Giao thức trần độ ưu tiên (PCP - *Priority Ceiling Protocol*): Gán cho mỗi Mutex một trần ưu tiên bằng tác vụ cao nhất từng dùng nó, loại bỏ hoàn toàn nguy cơ Deadlock và giới hạn thời gian chặn tối đa chỉ bằng 1 khối lệnh nguy cấp.
- **Mô hình toán học & Phương trình thiết kế:**
  Thời gian đáp ứng của tác vụ có tính đến thời gian chặn tối đa $B_i$ (*Blocking Term*) do nghịch đảo độ ưu tiên:
  $$R_i = C_i + B_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j \le D_i$$
  Với $B_i = \max_{k \in lp(i), m \in \text{Resources}(k)} \{ C_{k,m} \}$ là thời gian thực thi phần găng dài nhất của các tác vụ ưu tiên thấp hơn $lp(i)$.

---

### Module 09: Bus truyền thông nối tiếp nhúng: SPI, I2C, UART (Embedded Serial Buses)
- **Quy chiếu đại học & Tiêu chuẩn:** UC Berkeley EE192, Georgia Tech ECE 4180, DIHK `LF5`.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Chuẩn SPI (*Serial Peripheral Interface*): Truyền đồng bộ 4 dây (MOSI, MISO, SCK, CS), Full-Duplex, 4 chế độ xung nhịp phụ thuộc cực tính CPOL và pha CPHA, tốc độ lên tới 50+ Mbps.
  - Chuẩn I2C (*Inter-Integrated Circuit*): Truyền đồng bộ 2 dây (SDA, SCL), cấu hình cực má má hở (*Open-Drain*) kèm điện trở kéo lên (*Pull-Up Resistor*), phân xử trọng tài phân tán, địa chỉ 7-bit hoặc 10-bit, cơ chế kéo dài xung nhịp (*Clock Stretching*).
  - Giới hạn điện dung đường truyền của bus I2C: Giới hạn tiêu chuẩn $C_{\text{bus}} \le 400\text{ pF}$ đặt ra yêu cầu nghiêm ngặt khi lựa chọn điện trở kéo lên để đảm bảo thời gian sườn lên $t_r$.
- **Mô hình toán học & Phương trình thiết kế:**
  Dải giá trị cho phép của điện trở kéo lên bus I2C ($R_{p,\min}, R_{p,\max}$):
  $$R_{p,\min} = \frac{V_{DD} - V_{OL}}{I_{OL}}, \quad R_{p,\max} = \frac{t_r}{0.8473 \cdot C_{\text{bus}}}$$
  Trong đó $V_{OL}$ là điện áp mức thấp tối đa ngõ ra (thường 0.4V), $I_{OL}$ là dòng chìm tối đa (3 mA ở Standard Mode), $t_r$ là thời gian sườn tăng tối đa (1000 ns ở 100 kHz, 300 ns ở 400 kHz).

---

### Module 10: Bus trường công nghiệp: Controller Area Network CAN 2.0A/B & CAN-FD (Industrial Fieldbuses)
- **Quy chiếu đại học & Tiêu chuẩn:** ETH Zürich 227-0124-00L, TUM, Etschberger (2001) Ch. 2-4, ISO 11898-1/2, DIHK `LF5`, `LF7`, `LF9`.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Tín hiệu vi sai chống nhiễu công nghiệp (*Differential Signaling*): Cặp dây xoắn CAN_H và CAN_L. Trạng thái lặn (*Recessive* - Bit 1, $V_{\text{diff}} \approx 0\text{ V}$) và trạng thái trội (*Dominant* - Bit 0, $V_{\text{diff}} \ge 1.5\text{ V}$).
  - Trọng tài phân giải bus phi phá hủy (*Non-destructive Bitwise Arbitration* - CSMA/CD+AMP): Nhiều nút mạng cùng truyền đồng thời; nút phát bit lặn (1) mà cảm nhận đường truyền ở trạng thái trội (0) sẽ tự động rút lui nhường quyền ưu tiên mà không làm biến dạng khung dữ liệu của nút thắng. Mã định danh ID càng nhỏ thì mức độ ưu tiên càng cao.
  - Kỹ thuật chèn bit đồng bộ (*Bit-Stuffing* - *Bitstopfen*): Khi có 5 bit liên tiếp có cùng giá trị logic từ SOF đến CRC, phần cứng tự động chèn 1 bit đảo dấu để đảm bảo luôn có sườn tín hiệu cho mạch vòng khóa pha nội (DPLL) bám xung nhịp.
  - Cấu trúc khung chuẩn CAN 2.0A (11-bit ID) và mở rộng CAN 2.0B (29-bit ID): SOF, Arbitration Field, Control Field (DLC), Data Field (0–8 bytes), CRC Field (15-bit + Delimiter), ACK Slot, End of Frame (7-bit recessive).
- **Mô hình toán học & Phương trình thiết kế:**
  Định thời bit danh định ($t_{\text{bit}}$) thông qua các phân đoạn lượng tử thời gian ($t_q$ - *Zeitquant*):
  $$t_{\text{bit}} = t_{\text{Sync\_Seg}} + t_{\text{Prop\_Seg}} + t_{\text{Phase\_Seg1}} + t_{\text{Phase\_Seg2}} = N_{\text{TQ}} \cdot t_q, \quad t_q = \frac{\text{BRP}}{f_{\text{CAN\_CLK}}}$$
  Điều kiện kích thước phân đoạn lan truyền $t_{\text{Prop\_Seg}}$ đảm bảo bao trọn thời gian trễ vòng của cáp bus dài $L_{\text{bus}}$ và transceivers:
  $$t_{\text{Prop\_Seg}} \ge 2 \cdot (t_{\text{cable}} \cdot L_{\text{bus}} + t_{\text{tx\_transceiver}} + t_{\text{rx\_transceiver}})$$
  Số lượng bit tối đa của khung chuẩn CAN 2.0A có tính đến bit-stuffing xấu nhất:
  $$N_{\text{total\_bits}} \le 34 + 8 \cdot \text{DLC} + \left\lfloor \frac{34 + 8 \cdot \text{DLC} - 1}{4} \right\rfloor$$

---

### Module 11: Cô lập lỗi, Quản lý sự cố & Watchdog an toàn (Fault Confinement, Error Management & Safety Watchdogs)
- **Quy chiếu đại học & Tiêu chuẩn:** ISO 11898-1, Kopetz (2011) Ch. 6, Yiu (2013) Ch. 14, DIHK `LF9`.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Cơ chế đếm lỗi phần cứng CAN: Bộ đếm lỗi truyền (TEC - *Transmit Error Counter*) và nhận (REC - *Receive Error Counter*).
  - 3 trạng thái giới hạn lỗi của nút mạng:
    - *Error Active* ($\text{TEC}, \text{REC} \le 127$): Tham gia bus bình thường, phát cờ lỗi trội.
    - *Error Passive* ($\text{TEC} > 127$ hoặc $\text{REC} > 127$): Chỉ phát cờ lỗi lặn, phải chờ thêm 8 bit nhàn rỗi trước khi truyền lại.
    - *Bus-Off* ($\text{TEC} > 255$): Bị ngắt hoàn toàn khỏi bus vật lý để bảo vệ mạng khỏi bị tê liệt do nút hỏng.
  - Mạch giám sát thời gian độc lập (IWDG - *Independent Watchdog*) và có cửa sổ (WWDG - *Window Watchdog*): Bắt buộc firmware phải làm mới bộ đếm trong khoảng thời gian xác định; nếu phần mềm bị treo vào vòng lặp vô hạn, mạch Watchdog sẽ tự động kích hoạt Reset phần cứng toàn hệ thống.
  - Phân tích ngoại lệ lỗi nghiêm trọng (*HardFault Exception Handling*): Giải mã thanh ghi trạng thái lỗi khả cấu hình (CFSR, HFSR, MMFAR, BFAR) và giải nén ngăn xếp (*Stack Unwinding*) để truy vết địa chỉ lệnh gây ra lỗi.

---

### Module 12: Kỹ nghệ Firmware tiền định & Tuân thủ MISRA-C / IEC 61508 (Deterministic Firmware Engineering & MISRA-C Compliance)
- **Quy chiếu đại học & Tiêu chuẩn:** ETH Zürich, TUM, MISRA C:2012, IEC 61508 (Functional Safety SIL), DIHK `LF9`.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Cấp phát bộ nhớ tĩnh tuyệt đối (`configSUPPORT_STATIC_ALLOCATION`): Cấm hoàn toàn việc sử dụng cấp phát động `malloc()` / `free()` trong thời gian vận hành thực tế để triệt tiêu vĩnh viễn nguy cơ phân mảnh bộ nhớ (*Heap Fragmentation*).
  - Quy tắc an toàn MISRA-C:2012: Không sử dụng đệ quy (*No Recursion*), con trỏ hàm phải được kiểm tra hợp lệ, bắt buộc ép kiểu tường minh, không sử dụng các hành vi không xác định (*Undefined Behaviors*).
  - Vùng bảo vệ găng (*Critical Sections* - `taskENTER_CRITICAL()`): Vô hiệu hóa ngắt cục bộ với thời gian tối thiểu có thể xác định trước, ngăn chặn việc gián đoạn giữa chừng các chuỗi tính toán toán học không thể phân chia.

---

## 2. Academic Reading List (Danh mục tài liệu học thuật)

Học viên và kỹ sư cơ điện tử nghiên cứu chuyên sâu phân hệ 03 bắt buộc phải đọc và tham chiếu các giáo trình kinh điển sau:

1. **Joseph Yiu (2013)**: *The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors*, 3rd Edition, Newnes / Elsevier, Oxford, UK. ISBN: 978-0124080829.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 7 (Exceptions and Interrupts), Chương 8 (Nested Vectored Interrupt Controller - NVIC), Chương 10 (OS Support Features & SysTick), Chương 13 (Memory Protection Unit - MPU), Chương 14 (Fault Handling & Analysis). Cung cấp phân tích chi tiết cấp chu kỳ xung nhịp của phần cứng vi điều khiển.
2. **Richard Barry (2016)**: *Mastering the FreeRTOS Real Time Kernel: A Hands-On Tutorial Guide*, Real Time Engineers Ltd.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 3 (Task Management & Schedulers), Chương 4 (Queue Management), Chương 5 (Interrupt Management & Deferred Processing), Chương 7 (Resource Management, Mutexes & Priority Inversion). Cẩm nang kiến trúc trực tiếp từ tác giả sáng lập hệ điều hành FreeRTOS.
3. **Hermann Kopetz (2011)**: *Real-Time Systems: Design Principles for Distributed Embedded Applications*, 2nd Edition, Real-Time Systems Series, Springer Science+Business Media, New York. ISBN: 978-1441982360.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 2 (Real-Time Entities & Images), Chương 3 (Time and Clocks), Chương 5 (Real-Time Communication), Chương 6 (Fault Tolerance), Chương 9 (Real-Time Operating Systems). Tác phẩm kinh điển về tính đúng đắn thời gian (*Temporal Correctness*) trong hệ thống phân tán.
4. **Konrad Etschberger (2001)**: *Controller Area Network: Basics, Protocols, Chips and Applications*, Hanser Fachbuchverlag, Munich, Germany. ISBN: 978-3446217768.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 2 (Physical Layer & Transceivers per ISO 11898), Chương 3 (CAN Message Formats & Bus Arbitration), Chương 4 (Bit Timing and Synchronization), Chương 5 (Error Confinement & Fault Management). Giáo trình chuẩn mực ngành công nghiệp ô tô và tự động hóa của Đức về mạng CAN.
5. **C. L. Liu and James W. Layland (1973)**: "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment", *Journal of the ACM*, Vol. 20, No. 1, pp. 46–61.
   - *Phạm vi nghiên cứu cốt lõi:* Bài báo nền tảng chứng minh toán học định lý RMS (Rate Monotonic Scheduling) và EDF (Earliest Deadline First), dẫn xuất giới hạn sử dụng CPU $U \le n(2^{1/n}-1)$.
6. **Lui Sha, Ragunathan Rajkumar, and John P. Sathaye (1990)**: "Priority Inheritance Protocols: An Approach to Real-Time Synchronization", *IEEE Transactions on Computers*, Vol. 39, No. 9, pp. 1175–1185.
   - *Phạm vi nghiên cứu cốt lõi:* Chứng minh toán học triệt tiêu hiện tượng nghịch đảo độ ưu tiên vô hạn và loại bỏ hiện tượng bế tắc Deadlock thông qua giao thức kế thừa ưu tiên (PIP) và giao thức trần ưu tiên (PCP).
7. **Robert Bosch GmbH (1991)**: *CAN Specification Version 2.0*, Part A & Part B, Stuttgart, Germany.
   - *Phạm vi nghiên cứu cốt lõi:* Đặc tả kỹ thuật gốc định nghĩa giao thức CAN 2.0A (Standard Format 11-bit identifier) và CAN 2.0B (Extended Format 29-bit identifier), cơ chế chèn bit (bit-stuffing) và CRC.

---

## 3. Practical Labs & Simulation Projects (Bài tập thực hành & Project mô phỏng)

Hệ thống bài tập thực hành được thiết kế theo cấp độ tiệm tiến, bảo đảm kỹ sư nắm vững từ bản chất phần cứng trần (Bare-metal NVIC), kiến trúc hệ điều hành đa nhiệm (FreeRTOS) đến giao thức mạng công nghiệp thời gian thực (CAN-Bus).

---

### Lab 1: Cấu hình ngắt tiền định NVIC, đo lường độ trễ ngắt (Interrupt Latency) và chuyển ngữ cảnh trên ARM Cortex-M4
- **Mục tiêu kỹ thuật:**
  1. Cấu hình bảng vector ngắt, thiết lập nhóm ưu tiên NVIC (`NVIC_PriorityGroupConfig`) thành 4 bit preemption và 0 bit sub-priority.
  2. Đo lường chính xác chu kỳ xung nhịp của quá trình lưu ngăn xếp tự động ($T_{\text{stack}} = 12\text{ cycles}$) và hiệu ứng nối đuôi ngắt (*Tail-Chaining* = 6 chu kỳ) bằng bộ đếm chu kỳ phần cứng DWT (`CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk; DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk`).
  3. Kích hoạt ngắt phần mềm thông qua thanh ghi NVIC STIR (*Software Trigger Interrupt Register*) và xác minh tính tiền định của độ trễ ngắt trên máy hiện sóng dao động số (*Digital Storage Oscilloscope*).
- **Yêu cầu kết quả:** Độ trễ ngắt đo được từ khi kích hoạt tín hiệu GPIO đến khi chân cờ trong ISR nhảy mức logic không vượt quá $16 \cdot T_{\text{cycle}}$.

---

### Lab 2: Thiết kế hệ thống đa tác vụ FreeRTOS với Message Queue, Semaphore và cơ chế chống đảo ngược ưu tiên (Priority Inheritance)
- **Mục tiêu kỹ thuật:**
  1. Phân bổ bộ nhớ tĩnh cho 3 tác vụ định kỳ:
     - Tác vụ điều khiển nhanh $vControlTask$: Chu kỳ $T = 10\text{ ms}$, WCET $C = 2\text{ ms}$, Priority = 3.
     - Tác vụ xử lý cảm biến $vSensorProcessingTask$: Chu kỳ $T = 20\text{ ms}$, WCET $C = 4\text{ ms}$, Priority = 2.
     - Tác vụ ghi nhật ký từ xa $vTelemetryLoggingTask$: Chu kỳ $T = 50\text{ ms}$, WCET $C = 8\text{ ms}$, Priority = 1.
  2. Tạo xung đột tranh chấp tài nguyên chia sẻ (cổng SPI giao tiếp bộ nhớ Flash) bằng cờ khóa chuẩn nhị phân (*Binary Semaphore*) để tái hiện hiện tượng nghịch đảo độ ưu tiên vô hạn (*Unbounded Priority Inversion*).
  3. Thay thế cờ nhị phân bằng FreeRTOS Mutex có kích hoạt giao thức kế thừa độ ưu tiên (*Priority Inheritance*) và ghi nhận đồ thị thời gian thực thi (*Execution Trace*), chứng minh tác vụ ưu tiên cao nhất không bị tác vụ ưu tiên trung bình cướp quyền.
- **Yêu cầu kết quả:** Hệ thống đạt 0% lỗi trễ hạn chót (*Zero Missed Deadlines*), tổng tải CPU đo đạc thực tế $U = 56.00\%$ tuân thủ hoàn hảo giới hạn Liu-Layland $U_{\text{LL}} = 77.98\%$.

---

### Lab 3: Mô phỏng phân giải trọng tài bus CAN 2.0B và lập lịch tác vụ ưu tiên ngắt trước FreeRTOS (Reference Simulation: labs/lab03_can_rtos_sim.py)
- **Mục tiêu kỹ thuật:**
  - Chạy mô phỏng sự kiện rời rạc (*Discrete-Event Simulation*) tích hợp trọn vẹn cả hai cơ chế lõi của phân hệ 03:
    1. Bộ lập lịch ngắt trước FreeRTOS điều phối các tác vụ định kỳ theo chuẩn RMS, theo dõi từng bước tick 1 ms, đếm chính xác số lần chuyển ngữ cảnh (*Context Switches*) và tính toán thời gian đáp ứng trung bình/lớn nhất của từng tác vụ.
    2. Quá trình trọng tài phân giải bit trên đường truyền bus CAN 2.0B giữa 3 nút mạng ECU phát đồng thời:
       - `Node_B_BrakeECU`: Mã ID `0x050` (Ưu tiên cao nhất, điều khiển phanh khẩn cấp).
       - `Node_A_EngineECU`: Mã ID `0x120` (Ưu tiên trung bình, mô-men động cơ).
       - `Node_C_BodyECU`: Mã ID `0x750` (Ưu tiên thấp, đèn thân xe).
  - Thuật toán tự động chèn bit đồng bộ (*Bit-Stuffing*) tuân thủ nghiêm ngặt chuẩn ISO 11898-1: tự động chèn bit nghịch đảo sau mỗi chuỗi 5 bit liên tiếp cùng trạng thái logic.
  - Tính toán chính xác thời gian truyền vật lý trên đường bus ở tốc độ 500 kbps (thời gian bit $t_{\text{bit}} = 2.00\ \mu\text{s}$).
- **Tệp mã nguồn chuẩn:** `labs/lab03_can_rtos_sim.py`
- **Cách thức thực thi:**
  ```bash
  python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab03_can_rtos_sim.py
  ```
- **Chỉ số định lượng đầu ra kiểm chứng:**
  - Thời gian thực thi toàn bộ mô phỏng: $< 50\text{ ms}$ trên CPU macOS.
  - Tổng số lần chuyển ngữ cảnh trong 100 ms: $26\text{ switches}$.
  - Hệ số sử dụng CPU đo được: $U = 56.00\% \le U_{\text{Liu-Layland}} = 77.98\%$.
  - Tỷ lệ hoàn thành tác vụ: $100\%$, số hạn chót bị trễ: $0\text{ missed deadlines}$.
  - Nút thắng trọng tài bus CAN: `Node_B_BrakeECU` (ID `0x050`). Nút C mất quyền ở bit thứ 1, nút A mất quyền ở bit thứ 3.
  - Tổng số bit khung truyền hoàn chỉnh (bao gồm header đã chèn bit, payload và các trường cố định): $67\text{ bits}$.
  - Tổng độ trễ truyền dữ liệu trên bus: $134.00\ \mu\text{s}$.

---

## 4. Exact Search Queries & Bilingual Terminology Table (Từ khóa tìm kiếm & Thuật ngữ Anh-Đức)

### 4.1 Danh mục 12 Truy vấn tìm kiếm học thuật độ chính xác cao (Precision Search Queries)

Các truy vấn dưới đây được tối ưu hóa với các toán tử logic và bộ lọc định dạng tài liệu, hỗ trợ tra cứu trực tiếp các bài giảng, tiêu chuẩn và tài liệu kỹ thuật từ các nguồn hàn lâm:

1. `"Rate Monotonic Scheduling" "Liu and Layland" "utilization bound" filetype:pdf site:ethz.ch`
2. `"FreeRTOS" "TaskControlBlock" "vTaskSwitchContext" "SysTick_Handler" filetype:c OR filetype:h`
3. `"NVIC" "interrupt latency" "tail-chaining" "Cortex-M4" site:arm.com OR site:st.com filetype:pdf`
4. `"ISO 11898-1" "CAN bit timing" "propagation delay" "time quantum" filetype:pdf`
5. `"Priority Inversion" "Priority Inheritance Protocol" "Mars Pathfinder" site:nasa.gov OR site:ieee.org`
6. `site:ocw.mit.edu "embedded systems" "interrupt latency" "direct memory access"`
7. `"ARM Cortex-M" "PendSV" "context switch" assembly "PSP" "MSP"`
8. `"CAN bus" "bit stuffing" "CSMA/CA" "arbitration" "stuff bit" filetype:pdf`
9. `site:github.com "FreeRTOS" "CAN" "queue" "STM32" mechatronics`
10. `"Response Time Analysis" "critical instant" "schedulability" "Joseph and Pandya" filetype:pdf`
11. `"DIN IEC 60050-351" OR "Echtzeitbetriebssystem" "Prioritätsinversion" "Feldbus" Fachbegriffe`
12. `"STM32F4" "FreeRTOS" "CMSIS-RTOS" "hardware timer" "PWM dead-time" datasheet filetype:pdf`

---

### 4.2 Bảng thuật ngữ chuyên ngành đối chiếu Anh – Đức – Việt (Bilingual Terminology Table per DIN/IEC/ISO)

Bảng đối chiếu chuẩn hóa các thuật ngữ cốt lõi của phân hệ Hệ thống nhúng và Firmware, đối chiếu giữa thuật ngữ kỹ thuật quốc tế (English), danh từ chuyên ngành tiếng Đức (*Fachbegriffe*) theo tiêu chuẩn **DIN EN ISO 11898**, **DIN IEC 60050-351**, **DIN VDE 0100**, và thuật ngữ tiếng Việt chuẩn sư phạm kỹ thuật:

| English Term | German Fachbegriff (DIN/IEC/ISO) | Tiếng Việt chuẩn kỹ thuật (Vietnamese) |
|---|---|---|
| Embedded System | Eingebettetes System | Hệ thống nhúng |
| Real-Time Operating System (RTOS) | Echtzeitbetriebssystem (RTOS) | Hệ điều hành thời gian thực |
| Preemptive Priority Scheduling | Verdrängende / Vorbeugende Prioritätsbasierte Ablaufplanung | Lập lịch ưu tiên chiếm quyền |
| Priority Inversion | Prioritätsinversion / Prioritätsumkehr | Hiện tượng nghịch đảo độ ưu tiên |
| Priority Inheritance Protocol (PIP) | Prioritätsvererbungsprotokoll | Giao thức kế thừa độ ưu tiên |
| Priority Ceiling Protocol (PCP) | Prioritätshöchstgrenzenprotokoll | Giao thức trần độ ưu tiên |
| Context Switch | Kontextwechsel / Taskwechsel | Chuyển đổi ngữ cảnh tác vụ |
| Interrupt Service Routine (ISR) | Unterbrechungsroutine / ISR | Trình phục vụ ngắt |
| Interrupt Latency | Unterbrechungslatenz / Interrupt-Latenz | Độ trễ đáp ứng ngắt |
| Task Control Block (TCB) | Taskkontrollblock (TCB) | Khối điều khiển tác vụ |
| Controller Area Network (CAN) | CAN-Bus / Steuergerätenetzwerk (ISO 11898) | Mạng truyền thông bus CAN công nghiệp |
| Bit Timing & Time Quantum ($t_q$) | Bittiming und Zeitquant ($t_q$) | Định thời bit và lượng tử thời gian |
| Non-destructive Bitwise Arbitration | Zerstörungsfreie bitweise Busarbitrierung | Trọng tài bus phân giải theo bit phi phá hủy |
| Bit Stuffing | Bitstopfen / Bit-Stuffing | Kỹ thuật chèn bit đồng bộ xung nhịp |
| SysTick Timer | System-Tick-Timer / Systemzeittaktgeber | Bộ định thời nhịp hệ thống |
| Direct Memory Access (DMA) | Direkter Speicherzugriff (DMA) | Truy cập bộ nhớ trực tiếp |
| Memory Protection Unit (MPU) | Speicherschutzeinheit (MPU) | Khối phần cứng bảo vệ bộ nhớ |
| Worst-Case Execution Time (WCET) | Maximale Ausführungszeit (WCET) | Thời gian thực thi trường hợp xấu nhất |
| Watchdog Timer (WDT) | Überwachungstimer / Watchdog-Timer | Bộ định thời giám sát sự cố phần cứng |
| Deadlock | Verklemmung / Blockierung | Hiện tượng bế tắc tài nguyên (Deadlock) |
| Dead-Time Generation | Totzeit-Generierung | Tạo khoảng thời gian chết (bảo vệ cầu H) |
| Schedulability Analysis | Ablaufbarkeitsanalyse | Phân tích tính khả thi lập lịch |
