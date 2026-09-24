# 00. MASTER MATRIX: HỆ THỐNG KIẾN THỨC CƠ ĐIỆN TỬ & ROBOTICS CHUẨN ĐẠI HỌC VÀ CHLB ĐỨC (DIHK/AHK)

> **Tài liệu lõi điều phối toàn bộ cơ sở tri thức (Knowledge Base Central Master Matrix)**  
> **Tổng hợp từ:** MIT, Stanford, ETH Zürich, UC Berkeley, TU München (TUM), Georgia Tech  
> **Tiêu chuẩn công nghiệp & đào tạo nghề:** Khung chương trình đào tạo kép CHLB Đức (DIHK / AHK - KMK Rahmenlehrplan Mechatroniker), DIN / IEC / ISO  
> **Hệ sinh thái:** macOS (Intel Core i5, 8GB RAM) $\to$ QEMU/Virtual Bus $\to$ STM32 ARM Cortex-M $\to$ Edge SBC / ROS 2 Humble  

---

## 1. TỔNG QUAN HỆ THỐNG & TRIẾT LÝ KIẾN TRÚC (ARCHITECTURAL OVERVIEW)

Hệ thống Cơ sở tri thức Cơ điện tử & Robotics (Mechatronics & Robotics Knowledge Base) được thiết kế nhằm đồng bộ hóa hai đỉnh cao đào tạo kỹ thuật:
1. **Tư duy hàn lâm & mô hình hóa toán học từ nguyên lý gốc (First Principles):** Kế thừa từ các giáo trình và đề cương giảng dạy của các viện công nghệ hàng đầu thế giới (MIT, Stanford, ETH Zürich, UC Berkeley, TUM, Georgia Tech). Mọi hiện tượng vật lý đều được mô tả thông qua mô hình giải tích chính xác (giải tích vi tích phân, đại số tuyến tính, hình học vi phân, lý thuyết xác suất và tối ưu hóa lồi).
2. **Kỷ luật thực thi & tiêu chuẩn công nghiệp chuẩn CHLB Đức (DIHK / AHK Duale Ausbildung):** Bám sát 13 Trường học tập chuyên ngành (*Lernfelder* - `LF1` đến `LF13`) theo khung chương trình toàn quốc của Đức (KMK Rahmenlehrplan), hướng tới hai kỳ thi tốt nghiệp quốc gia: Kỳ thi phần 1 (*Abschlussprüfung Teil 1 - AP1*, chiếm 40% trọng số) và Kỳ thi phần 2 (*Abschlussprüfung Teil 2 - AP2*, chiếm 60% trọng số).

Toàn bộ hệ thống kiến thức được phân tách thành **6 Phân hệ chuyên sâu (Subsystems 01–06)**, liên kết chặt chẽ qua luồng tương tác cyber-physical khép kín, được bảo chứng bằng mã nguồn mô phỏng kiểm thử thuần Python (`labs/lab01` đến `labs/lab06`) không phụ thuộc thư viện ngoại vi nặng nề.

```
Target Root: 03_Mechatronics_Knowledge_Base/
├── 00_Master_Matrix.md                       <-- [Tài liệu hiện tại: Bản đồ điều phối trung tâm]
├── 01_Kinematics_Dynamics_Actuation.md        <-- [Subsystem 01: Động học, Động lực học & Truyền động]
├── 02_Power_Electronics_Signal_Conditioning.md<-- [Subsystem 02: Điện tử công suất & Xử lý tín hiệu]
├── 03_Embedded_Systems_Firmware.md            <-- [Subsystem 03: Hệ thống nhúng & Kiến trúc Firmware]
├── 04_Control_Theory_Estimation.md            <-- [Subsystem 04: Lý thuyết điều khiển & Ước lượng trạng thái]
├── 05_Autonomous_Robotics_ROS2_SLAM.md        <-- [Subsystem 05: Robot tự hành, ROS 2 & SLAM]
├── 06_Computer_Vision_Robot_Learning.md       <-- [Subsystem 06: Thị giác máy tính & Học máy Robot]
├── verify_knowledge_base.py                   <-- [Bộ kiểm thử tự động hóa toàn diện]
└── labs/
    ├── lab01_kinematics.py                    <-- [Mô phỏng 2-DOF Arm: Động học & Động lực học RK4]
    ├── lab02_signal_filter.py                 <-- [Mô phỏng Mạch khuếch đại vi sai, Butterworth & PWM Ripple]
    ├── lab03_can_rtos_sim.py                  <-- [Mô phỏng Định thời FreeRTOS & Trọng tài bus CAN 2.0B]
    ├── lab04_kalman_lqr.py                    <-- [Mô phỏng Con lắc ngược LQR & Bộ lọc Kalman rời rạc]
    ├── lab05_astar_rrt.py                     <-- [Mô phỏng Thuật toán tìm đường A* & Cây ngẫu nhiên RRT*]
    └── lab06_vision_feature.py                <-- [Mô phỏng Camera lỗ kim, Điểm đặc trưng & Hình học đối cực]
```

---

## 2. BẢNG ÁNH XẠ TỔNG THỂ 6 PHÂN HỆ (SUBSYSTEMS CROSS-MAPPING MATRIX)

Bảng dưới đây quy chiếu chi tiết 6 Phân hệ chuyên môn với các khóa học chuẩn tại các đại học hàng đầu thế giới, các Trường học tập của Đức (DIHK Lernfelder), năng lực kỹ thuật cốt lõi và mã nguồn bài tập mô phỏng tương ứng:

| Phân hệ (Subsystem) & Tệp tài liệu | Trọng tâm học thuật (Academic Focus) | Khóa học đại học quy chiếu (Benchmark Courses) | Khung DIHK Đức (Lernfelder) | Năng lực kỹ thuật cốt lõi (Core Competencies) | Bài thí nghiệm mô phỏng (Simulation Lab) |
|---|---|---|---|---|---|
| **Subsystem 01: Kinematics, Dynamics & Actuation**<br>`01_Kinematics_Dynamics_Actuation.md` | Động học thuận/nghịch (DH parameters), Động lực học Euler-Lagrange, Jacobian, Lựa chọn động cơ & hộp số giảm tốc | **MIT** 2.737 / 2.14<br>**Stanford** CS223A<br>**ETH Zürich** 151-0851-00L | `LF1`, `LF2`, `LF7` | Tính toán biến đổi tọa độ không gian, ma trận quán tính $M(q)$, mô men Coriolis $C(q,\dot{q})$, trọng lực $g(q)$, khớp chấp hành chấp nhận tải | `labs/lab01_kinematics.py`<br>(2-DOF Forward/Inverse Kinematics, Jacobian & RK4 Forward Dynamics) |
| **Subsystem 02: Power Electronics & Signal Conditioning**<br>`02_Power_Electronics_Signal_Conditioning.md` | Cầu H MOSFET/IGBT, PWM switching, Mạch Op-Amp đo lường vi sai (InAmp), Bộ lọc tích cực Butterworth/Sallen-Key, ADC front-end | **MIT** 6.302<br>**ETH Zürich** 227-0247-00L<br>**UC Berkeley** EE192 | `LF3`, `LF4`, `LF8` | Thiết kế tầng công suất điều khiển động cơ, triệt tiêu nhiễu đồng pha (CMRR), khử nhiễu răng cưa (Anti-Aliasing), bù nhiệt cảm biến dòng Shunt | `labs/lab02_signal_filter.py`<br>(Instrumentation Amp CMRR, 2nd-order Butterworth Filter & PWM Ripple) |
| **Subsystem 03: Embedded Systems & Firmware Architecture**<br>`03_Embedded_Systems_Firmware.md` | Vi điều khiển STM32 ARM Cortex-M (NVIC, DMA), Hệ điều hành thời gian thực FreeRTOS, Bus công nghiệp CAN 2.0B, SPI, I2C, UART | **ETH Zürich** 227-0124-00L<br>**UC Berkeley** EE192<br>**Georgia Tech** ECE 4550 | `LF5`, `LF7`, `LF9` | Lập trình ngắt ưu tiên tiền định, định thời đa tác vụ (RMS/EDF), chống nghịch đảo ưu tiên (Priority Inheritance), giao thức đóng gói khung CAN thời gian thực | `labs/lab03_can_rtos_sim.py`<br>(FreeRTOS Preemptive Priority Scheduler & CAN 2.0B Bus Arbitration) |
| **Subsystem 04: Modern Control Theory & State Estimation**<br>`04_Control_Theory_Estimation.md` | Điều khiển không gian trạng thái (State-Space), Bộ điều khiển PID số, LQR tối ưu, Bộ lọc Kalman rời rạc (DKF) & EKF, MPC | **MIT** 2.14 / 6.302<br>**ETH Zürich** 151-0591-00L<br>**ETH Zürich** 151-0566-00L | `LF8`, `LF11` | Khảo sát tính điều khiển được/quan sát được, đặt cực trạng thái (Pole Placement), tối ưu hóa hàm mục tiêu năng lượng, hợp nhất dữ liệu cảm biến đa nguồn | `labs/lab04_kalman_lqr.py`<br>(Inverted Pendulum Cart LQR Stabilization & Discrete Kalman Filter Fusion) |
| **Subsystem 05: Autonomous Robotics, ROS 2 & SLAM**<br>`05_Autonomous_Robotics_ROS2_SLAM.md` | Động học vi sai (Differential Drive), Bản đồ lưới xác suất (Occupancy Grid), EKF SLAM, Tìm đường A*, Cây ngẫu nhiên RRT*, Nav2, micro-ROS | **ETH Zürich** 151-0854-00L<br>**Stanford** CS237A<br>**MIT** 16.410 | `LF10`, `LF12` | Xây dựng bản đồ thời gian thực, định vị xác suất Monte-Carlo (MCL), quy hoạch quỹ đạo toàn cục và cục bộ tránh vật cản động, kiến trúc ROS 2 DDS | `labs/lab05_astar_rrt.py`<br>(2D Grid-based A* Heuristic Planner & Continuous Space Obstacle-avoiding RRT*) |
| **Subsystem 06: Computer Vision & Robot Learning**<br>`06_Computer_Vision_Robot_Learning.md` | Quang học hình học, Mô hình camera lỗ kim (Pinhole), Hiệu chỉnh méo thấu kính Brown-Conrady, Trích xuất đặc trưng Harris/ORB, Epipolar Geometry, 8-Point, Deep RL | **ETH Zürich** 151-0632-00L<br>**TUM** IN2064 / IN2228<br>**UC Berkeley** CS280 / CS285 | `LF6`, `LF10`, `LF13` | Tái tạo không gian 3D từ cặp ảnh Stereo, tính toán Ma trận thiết yếu $E$ và cơ bản $F$, ước lượng chuyển động thị giác (Visual Odometry), điều khiển tay máy bằng học tăng cường | `labs/lab06_vision_feature.py`<br>(Pinhole Camera Projection, Lens Distortion, Harris Corner & Epipolar Verification) |

---

## 3. MA TRẬN 13 TRƯỜNG HỌC TẬP DIHK CHLB ĐỨC (GERMAN DIHK LERNFELDER LF1 – LF13)

Trong hệ thống đào tạo nghề kép (*Duale Ausbildung*) của CHLB Đức, ngành **Mechatroniker/in** được chuẩn hóa theo khung chương trình KMK (*Kultusministerkonferenz*) gồm đúng 13 Trường học tập (*Lernfelder*). Mỗi Lernfeld là một tổ hợp năng lực hành động thực tế (*Handlungskompetenz*), từ gia công cơ khí cơ bản, mạch điện tử, lập trình PLC/vi điều khiển cho đến tích hợp toàn diện hệ thống robot và bảo trì công nghiệp.

Dưới đây là bản đồ ánh xạ chi tiết 13 Trường học tập (`LF1` đến `LF13`) trong bối cảnh chuẩn DIHK/AHK:

```
[SƠ ĐỒ TIẾN TRÌNH ĐÀO TẠO KÉP DIHK MECHATRONIKER]
Năm 1 (Cơ sở nền tảng):
  ├── LF1: Bearbeiten mechanischer Teile (Cơ khí & Dung sai chế tạo)
  ├── LF2: Installieren elektrischer Betriebsmittel (An toàn & Khí cụ điện)
  ├── LF3: Analysieren von Schaltungen der Steuerungstechnik (Điện & Khí nén cơ bản)
  └── LF4: Programmieren mechatronischer Systeme (Thuật toán & Lập trình cơ sở)
Năm 2 (Phân hệ & Tích hợp bước 1 -> Kỳ thi tốt nghiệp Phần 1 - AP1: 40%):
  ├── LF5: Herstellen mechatronischer Teilsysteme (Cơ cấu chấp hành & Cung cấp năng lượng)
  ├── LF6: Konzipieren mechatronischer Teilsysteme (Cảm biến, Xử lý ảnh & Lựa chọn phần cứng)
  ├── LF7: Installieren von Hard- und Softwarekomponenten (Bus truyền thông & Firmware)
  └── LF8: Aufbauen und Prüfen von Steuerungen (Mạch điều khiển tương tự & Số)
Năm 3 & 4 (Hệ thống phức tạp, Tự hành & Tối ưu -> Kỳ thi tốt nghiệp Phần 2 - AP2: 60%):
  ├── LF9: Programmieren mechatronischer Systeme (RTOS, Hệ thống nhúng công nghiệp)
  ├── LF10: Planen und Realisieren mechatronischer Systeme (Robot tự hành, FTS, ROS 2)
  ├── LF11: Ändern und Optimieren mechatronischer Systeme (Lý thuyết điều khiển hiện đại, LQR/MPC)
  ├── LF12: Instandhalten mechatronischer Systeme (Chẩn đoán lỗi, Bảo trì, Cân chỉnh cảm biến)
  └── LF13: Übergeben von mechatronischen Systemen (Nghiệm thu, An toàn ISO 13849, Bảo vệ dự án)
```

### Phân tích chi tiết từng Lernfeld (Detailed DIHK Vocational Context)

1. **`LF1` — Bearbeiten mechanischer Teile und Herstellen einfacher Baugruppen (Gia công chi tiết cơ khí và chế tạo cụm lắp ráp đơn giản)**
   - *Phân hệ liên kết cốt lõi:* `01_Kinematics_Dynamics_Actuation.md` (Subsystem 01).
   - *Bối cảnh thực hành DIHK:* Làm quen với bản vẽ kỹ thuật cơ khí theo chuẩn DIN ISO 128, dung sai kích thước và hình học (GD&T per DIN EN ISO 1101), thao tác cưa, dũa, khoan, cắt ren, tiện, phay các chi tiết gá lắp cho động cơ, ổ bi và trục truyền động.
   - *Mở rộng học thuật:* Tính toán ứng suất cơ học, chọn vật liệu (hợp kim nhôm, thép kết cấu), phân tích độ cứng vững và ma sát tĩnh/động của khớp quay robot.

2. **`LF2` — Installieren elektrischer Betriebsmittel unter Beachtung sicherheitstechnischer Aspekte (Lắp đặt thiết bị điện tuân thủ an toàn kỹ thuật)**
   - *Phân hệ liên kết cốt lõi:* `01_Kinematics_Dynamics_Actuation.md` (Subsystem 01).
   - *Bối cảnh thực hành DIHK:* Quy chuẩn an toàn điện theo tiêu chuẩn DIN VDE 0100/0113, đấu nối tủ điện, thiết bị đóng cắt bảo vệ (MCB, RCD, Contactor), nút dừng khẩn cấp (*Not-Halt* per DIN EN ISO 13850), tiếp địa bảo vệ (*Schutzleiter PE*).
   - *Mở rộng học thuật:* Lựa chọn và đấu nối cáp cấp nguồn cho động cơ Servo/BLDC, bảo vệ chống quá dòng và quá nhiệt trong các cơ cấu chấp hành công suất lớn.

3. **`LF3` — Analysieren und Prüfen von Schaltungen der Steuerungstechnik (Phân tích và kiểm tra các mạch kỹ thuật điều khiển)**
   - *Phân hệ liên kết cốt lõi:* `02_Power_Electronics_Signal_Conditioning.md` (Subsystem 02).
   - *Bối cảnh thực hành DIHK:* Đọc và thiết kế sơ đồ nguyên lý mạch khí nén (*Pneumatik*), điện khí nén (*Elektropneumatik*), van đảo chiều 5/2, 3/2 và rơ le điều khiển theo chuẩn DIN ISO 1219.
   - *Mở rộng học thuật:* Phân tích mạch khuếch đại tín hiệu chuyển mạch, điều khiển đóng cắt cuộn hút van điện từ (*Solenoid valves*), thời gian trễ đáp ứng và bảo vệ bằng Diode chặn xung ngược (*Flyback Diode*).

4. **`LF4` — Programmieren mechatronischer Systeme (Lập trình hệ thống cơ điện tử cơ bản)**
   - *Phân hệ liên kết cốt lõi:* `02_Power_Electronics_Signal_Conditioning.md` (Subsystem 02).
   - *Bối cảnh thực hành DIHK:* Nhập môn lập trình điều khiển tuần tự bằng ngôn ngữ Grafcet (DIN EN 60848) và PLC cơ bản (Siemens LOGO! / S7-1200 qua TIA Portal), lấy mẫu tín hiệu số và tương tự (0–10V, 4–20mA).
   - *Mở rộng học thuật:* Thiết kế thuật toán đọc ADC, giải mã độ phân giải, tính toán điện áp tham chiếu và lập trình tạo chuỗi xung PWM phần cứng.

5. **`LF5` — Herstellen und Inbetriebnehmen mechatronischer Teilsysteme (Chế tạo và đưa vào vận hành các phân hệ cơ điện tử)**
   - *Phân hệ liên kết cốt lõi:* `03_Embedded_Systems_Firmware.md` (Subsystem 03).
   - *Bối cảnh thực hành DIHK:* Lắp ráp cơ cấu truyền động tích hợp (động cơ bước, xilanh khí nén, cảm biến tiệm cận quang/từ), đấu nối với bo mạch trung gian và kiểm tra chức năng từng cụm trước khi ghép nối hệ thống.
   - *Mở rộng học thuật:* Cấu hình ngoại vi vi điều khiển (Timer, GPIO, UART), kiểm thử vận hành không tải và có tải của hệ truyền động góc/tịnh tiến.

6. **`LF6` — Konzipieren und Realisieren mechatronischer Systeme (Thiết kế và hiện thực hóa các phân hệ cơ điện tử quang - cơ)**
   - *Phân hệ liên kết cốt lõi:* `06_Computer_Vision_Robot_Learning.md` (Subsystem 06).
   - *Bối cảnh thực hành DIHK:* Tích hợp các hệ thống cảm biến quang học, công tắc quang điện, camera công nghiệp phục vụ nhận dạng phôi (*Werkstückerkennung*) và phân loại sản phẩm trên băng chuyền.
   - *Mở rộng học thuật:* Lựa chọn cảm biến hình ảnh CMOS, thiết kế hệ chiếu sáng công nghiệp (chiếu sáng vòng, chiếu sáng ngược), tính toán tiêu cự thấu kính và trường nhìn (*Field of View - FoV*).

7. **`LF7` — Installieren und Testen von Hard- und Softwarekomponenten (Cài đặt và thử nghiệm các thành phần phần cứng và phần mềm)**
   - *Phân hệ liên kết cốt lõi:* `01_Kinematics_Dynamics_Actuation.md`, `03_Embedded_Systems_Firmware.md` (Subsystems 01 & 03).
   - *Bối cảnh thực hành DIHK:* Nạp firmware, cấu hình cổng giao tiếp công nghiệp, kết nối máy tính điều khiển với vi điều khiển/PLC qua cáp công nghiệp, kiểm tra tính tương thích driver.
   - *Mở rộng học thuật:* Thiết lập chuỗi công cụ nạp mã (*Toolchain GCC ARM/OpenOCD*), đo đạc dạng sóng tín hiệu logic bằng máy phân tích logic (*Logic Analyzer*), kiểm tra trễ đồng bộ phần cứng.

8. **`LF8` — Aufbauen und Prüfen von elektrischen, pneumatischen und hydraulischen Steuerungen (Lắp ráp và kiểm tra hệ thống điều khiển điện, khí nén, thủy lực)**
   - *Phân hệ liên kết cốt lõi:* `02_Power_Electronics_Signal_Conditioning.md`, `04_Control_Theory_Estimation.md` (Subsystems 02 & 04).
   - *Bối cảnh thực hành DIHK:* Lắp ráp các hệ thống điều khiển vòng kín cơ bản (điều tốc động cơ DC bằng phản hồi bộ mã hóa Encoder, điều áp khí nén), kiểm tra độ tuyến tính của bộ chấp hành.
   - *Mở rộng học thuật:* Phân tích hàm truyền hệ hở và hệ kín, tối ưu hóa các thông số khuếch đại tỷ lệ $K_p$, tích phân $K_i$ và vi phân $K_d$ theo phương pháp Ziegler-Nichols và quỹ đạo nghiệm số (*Root Locus*).

9. **`LF9` — Programmieren und Inbetriebnehmen mechatronischer Systeme (Lập trình thời gian thực và vận hành hệ thống cơ điện tử phức hợp)**
   - *Phân hệ liên kết cốt lõi:* `03_Embedded_Systems_Firmware.md` (Subsystem 03).
   - *Bối cảnh thực hành DIHK:* Lập trình nâng cao trên PLC/SPS (Ngôn ngữ SCL/ST per IEC 61131-3) và vi điều khiển nhúng, cấu hình mạng truyền thông trường Profinet / CANopen, quản lý lỗi vận hành.
   - *Mở rộng học thuật:* Triển khai nhân hệ điều hành thời gian thực FreeRTOS, lập lịch ưu tiên ngắt trước (*Preemptive Priority Scheduling*), giao tiếp liên tác vụ qua Message Queue, Semaphores và Mutex bảo vệ tài nguyên chia sẻ.

10. **`LF10` — Planen und Realisieren mechatronischer Systeme (Lập kế hoạch và thực hiện hệ thống cơ điện tử tự hành / Robotics)**
    - *Phân hệ liên kết cốt lõi:* `05_Autonomous_Robotics_ROS2_SLAM.md`, `06_Computer_Vision_Robot_Learning.md` (Subsystems 05 & 06).
    - *Bối cảnh thực hành DIHK:* Thực hiện đồ án thực tế (*Betrieblicher Auftrag*) chuẩn bị cho kỳ thi tốt nghiệp phần 2 (AP2). Tích hợp xe tự hành vận chuyển hàng trong nhà máy (*Fahrerlose Transportsysteme - FTS/AGV*) hoặc cánh tay robot công nghiệp gắp đặt phôi (*Pick & Place Robot*).
    - *Mở rộng học thuật:* Kiến trúc ROS 2 phân tán, thiết lập khung điều hướng Nav2, ánh xạ chi phí chướng ngại vật (*Costmap 2D*), thuật toán lập quỹ đạo tối ưu A* và RRT*.

11. **`LF11` — Ändern und Optimieren mechatronischer Systeme (Thay đổi, tinh chỉnh và tối ưu hóa hệ thống cơ điện tử)**
    - *Phân hệ liên kết cốt lõi:* `04_Control_Theory_Estimation.md` (Subsystem 04).
    - *Bối cảnh thực hành DIHK:* Phân tích các thông số hoạt động của dây chuyền, cải tiến năng suất, tối ưu hóa mức tiêu hao năng lượng, giảm độ rung giật cơ khí khi khởi động/dừng.
    - *Mở rộng học thuật:* Xây dựng bộ điều khiển tối ưu LQR, tối ưu hóa hàm bậc hai đại số Riccati (CARE/DARE), lọc nhiễu ngẫu nhiên bằng bộ lọc Kalman rời rạc (DKF) để ước lượng trạng thái tối ưu.

12. **`LF12` — Instandhalten mechatronischer Systeme (Bảo trì, bảo dưỡng và chẩn đoán sự cố hệ thống cơ điện tử)**
    - *Phân hệ liên kết cốt lõi:* `05_Autonomous_Robotics_ROS2_SLAM.md` (Subsystem 05).
    - *Bối cảnh thực hành DIHK:* Quy trình chẩn đoán lỗi có hệ thống (*Systematische Fehlersuche*), kiểm tra suy giảm chất lượng linh kiện, cân chỉnh lại cảm biến góc/vị trí, lập kế hoạch bảo trì phòng ngừa (*Präventive Instandhaltung per DIN 31051*).
    - *Mở rộng học thuật:* Đo đạc và bù trừ sai số trôi dạt tích phân của cảm biến con quay hồi chuyển (IMU Drift), ước lượng phương sai Allan, hiệu chuẩn mô hình dịch chuyển bánh xe (*Odometry Calibration*).

13. **`LF13` — Übergeben von mechatronischen Systemen und Einweisen von Nutzern (Bàn giao hệ thống cơ điện tử, nghiệm thu và đào tạo người sử dụng)**
    - *Phân hệ liên kết cốt lõi:* `06_Computer_Vision_Robot_Learning.md` (Subsystem 06).
    - *Bối cảnh thực hành DIHK:* Lập tài liệu kỹ thuật, hướng dẫn vận hành (*Bedienungsanleitung*), đánh giá rủi ro máy móc theo chỉ thị CE và chuẩn an toàn chức năng ISO 13849 (Performance Level PL r), thực hiện phỏng vấn chuyên môn (*Fachgespräch*) bảo vệ đồ án tốt nghiệp trước chuyên gia DIHK/AHK.
    - *Mở rộng học thuật:* Đánh giá độ tin cậy của mô hình học máy (Confusion Matrix, Precision/Recall, Latency Budget), xây dựng rào chắn an toàn dự phòng (*Safety Fallback Monitoring*) trong điều khiển robot thông minh.

---

## 4. KIẾN TRÚC LUỒNG DỮ LIỆU XUYÊN SUỐT (CROSS-CUTTING DATAFLOW ARCHITECTURE)

Trong một hệ thống cơ điện tử và robotics hoàn chỉnh, 6 phân hệ không tồn tại độc lập mà tạo thành một vòng lặp kín tác động qua lại chặt chẽ giữa môi trường vật lý (*Physical Plant*) và các lớp tính toán số (*Cyber / Embedded Compute*).

### Sơ đồ luồng tương tác Cyber-Physical khép kín (Closed-Loop Dataflow Graph)

```
========================================================================================================================
                             MÔI TRƯỜNG VẬT LÝ & ĐỘNG LỰC HỌC TAY MÁY / KHUNG GẦM (PHYSICAL WORLD)
========================================================================================================================
                                                    ▲                                   │
                               [Actuator Torques /  │                                   │ [Joint Positions, Forces,
                                Motor Phase Current]│                                   │  Wheel Speeds & Back-EMF]
                                                    │                                   ▼
┌───────────────────────────────────────────────────┴───────────────────────────────────┬──────────────────────────────┐
│                                     [01. Kinematics, Dynamics & Actuation]                                           │
│               Mô hình vật lý: M(q)*q'' + C(q,q')*q' + g(q) = tau_actuator - J(q)^T * F_ext                           │
└───────────────────────────────────────────────────▲───────────────────────────────────┬──────────────────────────────┘
                                                    │                                   │
                                 [PWM Duty Cycles / │                                   │ [Raw Analog Signals: Current,
                                  Gate Drive Pulses]│                                   │  Hall Shunts, Resolver, Tach]
                                                    │                                   ▼
┌───────────────────────────────────────────────────┴───────────────────────────────────┬──────────────────────────────┐
│                                 [02. Power Electronics & Signal Conditioning]                                        │
│          Cầu H MOSFET/IGBT Driver <--- PWM Switching (20kHz) | Đo lường InAmp + Lọc Butterworth (Anti-Aliasing)      │
└───────────────────────────────────────────────────▲───────────────────────────────────┬──────────────────────────────┘
                                                    │                                   │
                                  [Control Commands │                                   │ [Conditioned ADC Voltages &
                                   via Timers/PWM]  │                                   │  QEI Encoder Ticks via DMA]
                                                    │                                   ▼
┌───────────────────────────────────────────────────┴───────────────────────────────────┬──────────────────────────────┐
│                                  [03. Embedded Systems & Firmware Architecture]                                       │
│          STM32 ARM Cortex-M: FreeRTOS 1kHz Periodic Tasks, NVIC Trọng tài ngắt, Bộ đệm DMA, Mạng Bus CAN 2.0B        │
└───────────────────────────────────────────────────▲───────────────────────────────────┬──────────────────────────────┘
                                                    │                                   │
                                 [State-Space U(k)  │                                   │ [Synchronized Sensor Telemetry
                                  Torque Targets]   │                                   │  & Filtered Observations Y(k)]
                                                    │                                   ▼
┌───────────────────────────────────────────────────┴───────────────────────────────────┬──────────────────────────────┐
│                                  [04. Modern Control Theory & State Estimation]                                       │
│          Ước lượng trạng thái: Kalman Filter x_hat(k) | Tối ưu hóa phản hồi: LQR U(k) = -K * x_hat(k)                │
└───────────────────────────────────────────────────▲───────────────────────────────────┬──────────────────────────────┘
                                                    │                                   │
                                 [Chassis Twist     │                                   │ [High-rate Fused Odometry
                                  cmd_vel (v, omega)]│                                  │  Pose (x, y, theta) @ 100Hz]
                                                    │                                   ▼
┌───────────────────────────────────────────────────┴───────────────────────────────────┬──────────────────────────────┐
│                                   [05. Autonomous Robotics, ROS 2 & SLAM]                                            │
│          Quy hoạch toàn cục A*/RRT* | Điều hướng cục bộ DWA/TEB | Định vị xác suất EKF/MCL | Bản đồ Costmap 2D       │
└───────────────────────────────────────────────────▲───────────────────────────────────┬──────────────────────────────┘
                                                    │                                   │
                                 [Target 6-DOF Poses│                                   │ [Visual Odometry (VO) Poses,
                                  & Visual Guidance]│                                   │  Depth Point Clouds, Obstacles]
                                                    │                                   ▼
┌───────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────┐
│                                   [06. Computer Vision & Robot Learning]                                             │
│          Mô hình Pinhole, Méo Brown-Conrady, Epipolar Two-View Geometry, Trích xuất đặc trưng & Deep Reinforcement    │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Hợp đồng giao tiếp giữa các phân hệ (Interface Contracts & Timing Budgets)

Mỗi điểm giao cắt giữa hai phân hệ kế cận đều phải tuân thủ nghiêm ngặt các quy ước kỹ thuật sau:

1. **Giao diện Interface 01 $\leftrightarrow$ 02 (Động lực học $\leftrightarrow$ Điện tử công suất):**
   - *Hướng truyền 01 $\to$ 02:* Điện áp sức phản điện động ($V_{emf} = K_e \cdot \omega$) và mô men cản cơ học phản xạ lên trục động cơ.
   - *Hướng truyền 02 $\to$ 01:* Dòng điện pha thực tế ($I_a, I_b, I_c$) tạo ra mô men điện từ ($\tau_m = K_t \cdot I_a$) tác động lên ma trận quán tính $M(q)$.
   - *Tần số & Ràng buộc thời gian:* Tần số băm xung PWM $f_{pwm} \ge 20\text{ kHz}$ (để vượt khỏi ngưỡng nghe được của con người và giảm dòng gợn $\Delta I_{ripple} < 5\%$).

2. **Giao diện Interface 02 $\leftrightarrow$ 03 (Điện tử công suất $\leftrightarrow$ Firmware nhúng):**
   - *Hướng truyền 02 $\to$ 03:* Tín hiệu điện áp tương tự đã lọc nhiễu qua bộ khuếch đại đo lường đưa vào chân ADC của STM32, tín hiệu xung Encoder số đưa vào Timer kênh đếm xung góc vi sai (Quadrature Encoder Interface - QEI).
   - *Hướng truyền 03 $\to$ 02:* Tín hiệu logic điều khiển cực cổng MOSFET (*Gate Drive Signals*) từ các thanh ghi Timer đếm lên/xuống (*Center-aligned PWM*) kèm thời gian chết chống trùng dẫn (*Dead-time* $t_{dead} \approx 200 - 500\text{ ns}$).
   - *Tần số & Ràng buộc thời gian:* Tốc độ lấy mẫu ADC đồng bộ kích hoạt bởi phần cứng Timer qua DMA với tần số $10\text{ kHz}$ ($100\,\mu\text{s}$ chu kỳ).

3. **Giao diện Interface 03 $\leftrightarrow$ 04 (Firmware nhúng $\leftrightarrow$ Lý thuyết điều khiển):**
   - *Hướng truyền 03 $\to$ 04:* Vector quan sát thô $y(k) = [\theta_{raw}, \omega_{raw}, i_{raw}]^T$ được đóng gói sau khi chuyển đổi ADC và đếm xung Timer.
   - *Hướng truyền 04 $\to$ 03:* Vector điều khiển $u(k)$ (giá trị đặt điện áp hoặc dòng điện băm xung) tính toán từ luật điều khiển phản hồi.
   - *Tần số & Ràng buộc thời gian:* Tác vụ định thời thời gian thực (FreeRTOS Task) chạy tại chu kỳ chuẩn $T_s = 1\text{ ms}$ ($1\text{ kHz}$). Yêu cầu độ rung nháy thời gian (*Jitter*) $< 5\,\mu\text{s}$.

4. **Giao diện Interface 04 $\leftrightarrow$ 05 (Điều khiển hiện đại $\leftrightarrow$ Robot tự hành & ROS 2):**
   - *Hướng truyền 04 $\to$ 05:* Dữ liệu cự ly dịch chuyển xe và tư thế tích phân Odometry ($\Delta x, \Delta y, \Delta \theta, v_x, \omega_z$) gửi lên máy tính nhúng SBC qua bus CAN 2.0B (1 Mbps) hoặc micro-ROS qua Serial UART (921600 baud).
   - *Hướng truyền 05 $\to$ 04:* Lệnh vận tốc khung xe mong muốn `geometry_msgs/Twist` (`cmd_vel`: $v_x, \omega_z$) phát ra từ thuật toán điều hướng cục bộ (TEB/DWA).
   - *Tần số & Ràng buộc thời gian:* Chu kỳ gửi nhận Odometry $\ge 50 - 100\text{ Hz}$ ($10 - 20\text{ ms}$). Thời gian trễ đường truyền cho phép $< 10\text{ ms}$.

5. **Giao diện Interface 05 $\leftrightarrow$ 06 (Robot tự hành $\leftrightarrow$ Thị giác máy tính & Học máy):**
   - *Hướng truyền 06 $\to$ 05:* Bản tin tư thế dịch chuyển thị giác (Visual Odometry `nav_msgs/Odometry`), đám mây điểm 3D vật cản (`sensor_msgs/PointCloud2`), và vị trí vật thể nhận dạng để cập nhật lớp chi phí Costmap 2D.
   - *Hướng truyền 05 $\to$ 06:* Tư thế ước lượng toàn cục hiện tại của robot (`map` $\to$ `base_link`) để đồng bộ hóa khung hình chiếu và kích hoạt tác vụ thị giác đúng vị trí địa lý.
   - *Tần số & Ràng buộc thời gian:* Tần số xử lý khung hình camera $30\text{ Hz}$ ($33.3\text{ ms}$/frame). Trễ xử lý mạng nơ-ron nhận dạng $< 50\text{ ms}$.

---

## 5. LỘ TRÌNH KIỂM THỬ HARDWARE-IN-THE-LOOP (HIL PROGRESSION ROADMAP)

Để đảm bảo tính khả thi trên máy tính cá nhân của Phát (MacBook Pro Intel Core i5, 8GB RAM) đồng thời mở rộng liền mạch sang phần cứng vật lý công nghiệp tại CHLB Đức, hệ thống áp dụng chiến lược kiểm thử HIL 4 cấp độ (HIL-0 đến HIL-3):

```
+-------------------------------------------------------------------------------------------------------+
|                                    HIL VALIDATION ROADMAP                                             |
+-----------------------------------+-----------------------------------+-------------------------------+
| Giai đoạn (Stage)                 | Nền tảng thực thi (Execution Env) | Tiêu chí nghiệm thu (Metric)  |
+-----------------------------------+-----------------------------------+-------------------------------+
| HIL-0: Pure Simulation            | macOS CPU (Intel i5, 8GB RAM)     | labs/lab01-lab06 chạy < 0.1s, |
|                                   | Python 3 Standard Library         | sai số hội tụ < 1e-4          |
+-----------------------------------+-----------------------------------+-------------------------------+
| HIL-1: Virtual Emulation          | Host OS QEMU ARM Cortex-M         | Zero dropped frames trên CAN, |
|                                   | Virtual CAN (vcan0) & FreeRTOS-SIM| độ trễ định thời < 1ms        |
+-----------------------------------+-----------------------------------+-------------------------------+
| HIL-2: Target Silicon MCU         | STM32F4/G4 (ARM Cortex-M4 @168MHz)| Stack High-Water Mark an toàn,|
|                                   | Hardware CAN Tranceiver, ADC DMA  | ADC DMA 10kHz chính xác       |
+-----------------------------------+-----------------------------------+-------------------------------+
| HIL-3: Edge SBC & Distributed Nav2| Raspberry Pi 4 / Jetson Nano      | micro-ROS bridge trễ < 20ms,  |
|                                   | ROS 2 Humble + Camera + Nav2 Stack| SLAM đóng vòng lặp thành công |
+-----------------------------------+-----------------------------------+-------------------------------+
```

### Chi tiết 4 cấp độ kiểm thử

1. **Giai đoạn HIL-0: Mô hình hóa giải tích & Thuật toán thuần túy (Pure Mathematical Simulation)**
   - *Phần cứng thực thi:* MacBook Pro cá nhân của Phát (macOS Sequoia, Intel Core i5, RAM 8GB).
   - *Môi trường:* Python 3 tiêu chuẩn, tuyệt đối không dùng thư viện C-extensions cồng kềnh.
   - *Nội dung kiểm thử:* Chạy toàn bộ 6 tệp mã nguồn tham chiếu trong `labs/` (`lab01_kinematics.py` đến `lab06_vision_feature.py`). Kiểm tra động học vi phân, tích phân số Runge-Kutta 4 (RK4), thuật toán tối ưu LQR, bộ lọc Kalman, tìm đường A*/RRT* và hình học đối cực.
   - *Tiêu chí đạt:* Toàn bộ các script thực thi trong thời gian $< 0.1$ giây, bộ nhớ RAM chiếm dụng $< 50\text{ MB}$, kết quả số học khớp với giải tích sai số $< 10^{-4}$.

2. **Giai đoạn HIL-1: Giả lập ngoại vi & Hệ điều hành nhúng (Virtual Peripheral & Middleware Emulation)**
   - *Phần cứng thực thi:* QEMU ARM System Emulator trên macOS hoặc máy ảo Linux nhẹ.
   - *Môi trường:* Trình mô phỏng nhân vi điều khiển STM32 Cortex-M4, mạng mạng ảo SocketCAN (`vcan0`), bản phân phối FreeRTOS POSIX Simulator.
   - *Nội dung kiểm thử:* Mô phỏng định thời đa tác vụ tiền định của FreeRTOS, cơ chế giải quyết xung đột bus CAN 2.0B giữa các nút cảm biến ảo, truyền nhận thông điệp qua hàng đợi không làm tràn bộ nhớ đệm (*Zero Packet Drop*).
   - *Tiêu chí đạt:* Không có lỗi trễ deadline tác vụ thời gian thực (*Zero Deadline Miss*), độ dao động thời gian (*Jitter*) giữa các chu kỳ $< 1\text{ ms}$.

3. **Giai đoạn HIL-2: Phần cứng vi điều khiển mục tiêu (Target Silicon Microcontroller Hardware-in-the-Loop)**
   - *Phần cứng thực thi:* Bo mạch phát triển vi điều khiển công nghiệp STM32F401RE / STM32G474 (Cortex-M4 với FPU), bo mạch mở rộng CAN Transceiver (TJA1050 / SN65HVD230).
   - *Môi trường:* Trình biên dịch `arm-none-eabi-gcc`, nạp và gỡ lỗi qua ST-Link v2 / OpenOCD.
   - *Nội dung kiểm thử:* Chạy mã C nhúng thực tế: cấu hình bộ đếm xung ngắt Timer ở chế độ Center-aligned PWM tạo thời gian chết $300\text{ ns}$, kích hoạt ADC đọc điện áp shunt dòng điện đồng bộ qua DMA, truyền nhận gói tin CAN thời gian thực 1Mbps ra máy hiện sóng (*Oscilloscope*) hoặc máy phân tích logic.
   - *Tiêu chí đạt:* Tác vụ điều khiển 1kHz chạy ổn định, mức sử dụng ngăn xếp (*Stack High-Water Mark*) an toàn $> 30\%$, sai số đo dòng điện qua ADC $< 1.5\%$.

4. **Giai đoạn HIL-3: Máy tính biên & Hệ thống robot phân tán (Edge SBC & Distributed Nav2 Execution)**
   - *Phần cứng thực thi:* Máy tính biên Raspberry Pi 4 (4GB RAM) hoặc Nvidia Jetson Orin Nano kết nối với bo mạch STM32 qua cổng UART công nghiệp hoặc CAN bus.
   - *Môi trường:* Ubuntu 22.04 LTS, ROS 2 Humble Hawksbill, micro-ROS Agent, Navigation 2 (Nav2).
   - *Nội dung kiểm thử:* Cầu nối micro-ROS Agent giao tiếp thời gian thực hai chiều với vi điều khiển; máy tính biên tiếp nhận luồng dữ liệu quét laser 2D LiDAR (RPLIDAR) và camera RGB-D, chạy thuật toán SLAM tạo bản đồ, xác định vị trí Monte-Carlo và xuất lệnh vận tốc `cmd_vel` điều khiển khung gầm xe tự hành bám quỹ đạo tránh chướng ngại vật thực tế.
   - *Tiêu chí đạt:* Độ trễ đóng vòng lặp đầu-cuối từ cảm biến tới bộ chấp hành $< 20\text{ ms}$, xe hoàn thành chu trình di chuyển không va chạm, bản đồ SLAM khép vòng (*Loop Closure*) thành công không bị méo.

---

## 6. DANH MỤC CÁC BÀI THÍ NGHIỆM MÔ PHỎNG (COMPREHENSIVE LAB CATALOG)

Toàn bộ 6 bài lab mô phỏng chuẩn mực nằm trong thư mục con `labs/`, được tối ưu hóa cho hệ điều hành macOS, không phụ thuộc thư viện bên ngoài và xuất các chỉ số định lượng cụ thể:

### 1. `lab01_kinematics.py` — 2-DOF Planar Robot Arm Kinematics & RK4 Dynamics
- **Phân hệ quy chiếu:** `01_Kinematics_Dynamics_Actuation.md` (Subsystem 01).
- **Mục tiêu kỹ thuật:** Tính toán giải tích Động học thuận (Forward Kinematics), Động học nghịch (Inverse Kinematics) với 2 nghiệm (Elbow Up/Down), Ma trận Jacobian $J(q)$, phân tích điểm kỳ dị ma trận ($\det(J) = 0$), và tích phân số phương trình vi phân chuyển động phi tuyến Euler-Lagrange sử dụng phương pháp Runge-Kutta bậc 4 (RK4).
- **Thuật toán cốt lõi:**
  $$\begin{bmatrix} \dot{\theta}_1 \\ \dot{\theta}_2 \end{bmatrix} = J^{-1} \begin{bmatrix} \dot{x} \\ \dot{y} \end{bmatrix}, \quad M(q)\ddot{q} + C(q,\dot{q})\dot{q} + g(q) = \tau$$
- **Chỉ số định lượng đầu ra:** Sai số vị trí động học nghịch ($< 10^{-6}\text{ m}$), thời gian tích phân số RK4 ($< 20\text{ ms}$ cho 1000 bước tích phân), năng lượng cơ học bảo toàn trong dao động tự do.

### 2. `lab02_signal_filter.py` — Instrumentation Amplifier CMRR, Butterworth Filter & PWM Current Ripple
- **Phân hệ quy chiếu:** `02_Power_Electronics_Signal_Conditioning.md` (Subsystem 02).
- **Mục tiêu kỹ thuật:** Mô phỏng mạch khuếch đại đo lường 3 Op-Amp với điện trở sai số dung sai gây suy giảm hệ số khử đồng pha (CMRR); thiết kế bộ lọc tích cực hạ thông Butterworth bậc 2 cấu hình Sallen-Key để lọc nhiễu tần số cao; phân tích dòng điện gợn $\Delta I_{L}$ trong cuộn cảm động cơ DC dưới tác động của điện áp đóng cắt cầu H PWM tần số cao.
- **Thuật toán cốt lõi:**
  $$\text{CMRR} = 20 \log_{10} \left|\frac{A_d}{A_{cm}}\right|\text{ dB}, \quad H(s) = \frac{\omega_c^2}{s^2 + \sqrt{2}\omega_c s + \omega_c^2}, \quad \Delta I_{pp} = \frac{V_{dc} \cdot D(1-D)}{f_{pwm} \cdot L}$$
- **Chỉ số định lượng đầu ra:** Hệ số CMRR đạt chuẩn ($> 80\text{ dB}$), hệ số triệt tiêu tín hiệu ngoài dải thông tại tần số cắt $f_c$, dòng gợn thực tế $\Delta I$ so sánh với lý thuyết sai lệch $< 2\%$.

### 3. `lab03_can_rtos_sim.py` — FreeRTOS Preemptive Priority Scheduler & CAN 2.0B Bus Arbitration
- **Phân hệ quy chiếu:** `03_Embedded_Systems_Firmware.md` (Subsystem 03).
- **Mục tiêu kỹ thuật:** Giả lập hành vi của bộ lập lịch thời gian thực ưu tiên ngắt trước (Preemptive Priority-based Scheduler) với 3 tác vụ chu kỳ khác nhau; mô phỏng cơ chế giải quyết xung đột không phá hủy trên đường truyền bus CAN 2.0B (Wired-AND Bitwise Arbitration) dựa trên mã định danh ID chuẩn 11-bit.
- **Thuật toán cốt lõi:**
  $$\text{CAN Arbitration: } \text{Bit dominant (0) wins over Recessive (1)}, \quad \text{CPU Utilization: } U = \sum \frac{C_i}{T_i} \le N(2^{1/N}-1)$$
- **Chỉ số định lượng đầu ra:** Số lượng chuyển ngữ cảnh (*Context Switches*), xác nhận gói tin ID mức ưu tiên cao nhất luôn giành quyền phát mà không làm chậm trễ dữ liệu khẩn cấp, thời gian thực thi của bộ lập lịch $< 15\text{ ms}$.

### 4. `lab04_kalman_lqr.py` — Inverted Pendulum LQR Stabilization & Discrete Kalman Filter Fusion
- **Phân hệ quy chiếu:** `04_Control_Theory_Estimation.md` (Subsystem 04).
- **Mục tiêu kỹ thuật:** Mô hình hóa phi tuyến hệ con lắc ngược trên xe trượt (Inverted Pendulum on a Cart), tuyến tính hóa quanh điểm cân bằng thẳng đứng không bền; giải phương trình đại số Riccati để tìm ma trận khuếch đại phản hồi tối ưu $K_{LQR}$; xây dựng bộ lọc Kalman rời rạc (DKF) để ước lượng góc nghiêng và vận tốc góc khi tín hiệu đo bị nhiễu Gaussian trắng làm bẩn.
- **Thuật toán cốt lõi:**
  $$u(k) = -K x(k), \quad P_{k|k-1} = A P_{k-1|k-1} A^T + Q, \quad K_k = P_{k|k-1} H^T (H P_{k|k-1} H^T + R)^{-1}$$
- **Chỉ số định lượng đầu ra:** Thời gian ổn định hệ thống con lắc ($< 1.5\text{ s}$), góc lệch dư ổn định ($< 0.01\text{ rad}$), độ cải thiện tỷ số tín hiệu trên nhiễu (SNR) của bộ lọc Kalman ($> 15\text{ dB}$).

### 5. `lab05_astar_rrt.py` — 2D Grid A* Path Search & Continuous Space RRT* Motion Planning
- **Phân hệ quy chiếu:** `05_Autonomous_Robotics_ROS2_SLAM.md` (Subsystem 05).
- **Mục tiêu kỹ thuật:** Triển khai thuật toán tìm đường trên lưới A* với hàm lượng giá $f(n) = g(n) + h(n)$ bảo đảm tính nhất quán (Consistent Euclidean Heuristic); triển khai thuật toán cây mở rộng ngẫu nhiên tiệm cận tối ưu RRT* trong không gian liên tục $\mathcal{C}_{space}$ kèm cơ chế nối lại nhánh lân cận (*Tree Rewiring*) và kiểm tra va chạm với vật cản hình tròn.
- **Thuật toán cốt lõi:**
  $$f(n) = g(n) + \sqrt{(x_n - x_g)^2 + (y_n - y_g)^2}, \quad x_{min} = \arg\min_{x \in X_{near}} (\text{Cost}(x) + c(x, x_{new}))$$
- **Chỉ số định lượng đầu ra:** Chiều dài đường đi tối ưu, số lượng nút mở rộng, thời gian thực thi thuật toán A* ($< 5\text{ ms}$ trên lưới $30\times 30$), xác nhận đường đi không cắt qua bất kỳ vật cản nào.

### 6. `lab06_vision_feature.py` — Pinhole Camera Model, Radial Distortion & Two-View Epipolar Geometry
- **Phân hệ quy chiếu:** `06_Computer_Vision_Robot_Learning.md` (Subsystem 06).
- **Mục tiêu kỹ thuật:** Chiếu các điểm tọa độ thế giới thực 3D lên mặt phẳng ảnh 2D thông qua ma trận thông số nội $K$ và ma trận thông số ngoại $[R \mid t]$; áp dụng mô hình biến dạng xuyên tâm Brown-Conrady ($k_1, k_2$); tính toán ma trận phản ứng góc Harris trên mảng ma trận điểm ảnh; xác thực ràng buộc hình học đối cực thông qua ma trận thiết yếu $x_2^T E x_1 = 0$ và tái tạo tọa độ 3D bằng đạc tam giác (*Linear Triangulation*).
- **Thuật toán cốt lõi:**
  $$p = K [R \mid t] P_w, \quad x_d = x_n (1 + k_1 r^2 + k_2 r^4), \quad R_{Harris} = \det(M) - 0.04(\operatorname{Tr}(M))^2, \quad x_2^T [t]_\times R x_1 = 0$$
- **Chỉ số định lượng đầu ra:** Phần dư sai số đối cực ($x_2^T E x_1 \approx 0.00$), sai số tái tạo tọa độ 3D trung bình ($< 10^{-4}\text{ m}$), thời gian thực thi toàn bộ quy trình $< 10\text{ ms}$.

---

## 7. BẢNG TRA CỨU TIÊU CHUẨN CÔNG NGHIỆP ĐỨC & QUỐC TẾ (GERMAN & INTERNATIONAL STANDARDS)

Để phục vụ tốt nhất cho kỳ thi tốt nghiệp chuẩn DIHK/AHK và quá trình làm việc trực tiếp tại các tập đoàn công nghiệp chế tạo máy ở Đức, mọi thiết kế và phân tích trong tài liệu đều tuân thủ các bộ tiêu chuẩn sau:

| Mã tiêu chuẩn (Standard) | Tên tiêu chuẩn / Lĩnh vực áp dụng | Nội dung kỹ thuật & Ứng dụng trong hệ thống |
|---|---|---|
| **DIN EN ISO 8373** | *Roboter und Robotikgeräte — Wörterbuch* | Chuẩn hóa toàn bộ thuật ngữ robot công nghiệp, tọa độ khớp, bậc tự do (DoF), độ lặp lại vị trí. |
| **DIN 19226** | *Leittechnik — Regelungstechnik und Steuerungstechnik* | Định nghĩa các khái niệm điều khiển vòng hở (*Steuerung*), vòng kín (*Regelung*), hàm truyền và ổn định hệ thống. |
| **VDI/VDE 2860** | *Montage- und Handhabungstechnik; Handhabungsfunktionen* | Chuẩn hóa các chuyển động gắp đặt, cơ cấu tay kẹp, động học vi sai của robot dịch chuyển phôi. |
| **DIN EN 60617** | *Graphische Symbole für Schaltpläne* | Ký hiệu quy ước bản vẽ sơ đồ mạch điện, điện tử công suất, rơ le, công tắc và nguồn điện. |
| **DIN ISO 1219** | *Fluidtechnik — Schaltzeichen und Schaltpläne* | Ký hiệu tiêu chuẩn sơ đồ van khí nén, xi lanh tác động đơn/kép, bộ lọc điều áp bôi trơn (FRL). |
| **ISO 13849-1** | *Sicherheit von Maschinen — Sicherheitsbezogene Teile von Steuerungen* | Đánh giá an toàn chức năng máy móc, mức hiệu năng an toàn (*Performance Level* PL a đến PL e). |
| **DIN EN ISO 13850** | *Sicherheit von Maschinen — Not-Halt-Funktion* | Nguyên tắc thiết kế và bố trí nút dừng khẩn cấp cơ điện tử (*Not-Halt-Einrichtung*). |
| **DIN EN 61131-3** | *Speicherprogrammierbare Steuerungen — Programmiersprachen* | Ngôn ngữ lập trình PLC chuẩn quốc tế: ST (Structured Text), LD (Ladder), FBD, SFC và IL. |
| **ISO 11898-1/2** | *Road vehicles — Controller area network (CAN)* | Tiêu chuẩn lớp liên kết dữ liệu và lớp vật lý tốc độ cao của bus mạng truyền thông công nghiệp CAN. |
| **DIN ISO 9039** | *Optik und Photonik — Qualitätsbewertung optischer Systeme* | Đo lường và đánh giá độ méo hình học của thấu kính máy ảnh công nghiệp (*Verzeichnung*). |
| **DIN 31051** | *Grundlagen der Instandhaltung* | Khung tiêu chuẩn bảo trì kỹ thuật công nghiệp: Bảo dưỡng (*Wartung*), Kiểm tra (*Inspektion*), Sửa chữa (*Instandsetzung*). |

---

## 8. HƯỚNG DẪN KIỂM CHỨNG & VẬN HÀNH (VERIFICATION & EXECUTION INSTRUCTIONS)

Toàn bộ hệ thống kiến thức được tích hợp sẵn công cụ kiểm thử tự động `verify_knowledge_base.py`. Người học và kỹ sư có thể kiểm tra tính toàn vẹn của hệ thống bất kỳ lúc nào bằng lệnh:

```bash
# Kiểm thử liên tục theo tiến độ các phân hệ hiện có (Progressive Mode):
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/verify_knowledge_base.py --progressive

# Kiểm thử nghiêm ngặt toàn bộ 13 thành phần (Strict Mode khi hoàn thành toàn dự án):
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/verify_knowledge_base.py

# Kiểm thử độc lập từng bài thí nghiệm mô phỏng:
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab01_kinematics.py
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab02_signal_filter.py
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab03_can_rtos_sim.py
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab04_kalman_lqr.py
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab05_astar_rrt.py
python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab06_vision_feature.py
```

*Tài liệu Master Matrix này là kim chỉ nam điều phối, đảm bảo tính nhất quán cao nhất về mặt học thuật và thực tiễn cho toàn bộ 6 gói kiến thức chuyên sâu tiếp theo.*
