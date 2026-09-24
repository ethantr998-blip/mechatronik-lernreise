# 04. LÝ THUYẾT ĐIỀU KHIỂN HIỆN ĐẠI & ƯỚC LƯỢNG TRẠNG THÁI (MODERN CONTROL THEORY & STATE ESTIMATION)

> **Tài liệu tri thức phân hệ 04 (Subsystem 04 Knowledge Package)**  
> **Các trường đại học tham chiếu:** MIT (2.14 / 6.302), ETH Zürich (151-0591-00L / 151-0566-00L / 151-0660-00L), Stanford (ENGR205), UC Berkeley (ME C232), TU München (TUM)  
> **Tiêu chuẩn công nghiệp & CHLB Đức:** DIN IEC 60050-351 (IEV 351 Leittechnik), DIN 19226 (Regelungs- und Steuerungstechnik), DIHK Lernfelder `LF8`, `LF11`  
> **Mã nguồn mô phỏng kiểm chứng:** `labs/lab04_kalman_lqr.py` (Inverted Pendulum LQR Stabilization & Discrete Kalman Filter Fusion)  

---

## 1. Standardized Syllabus Breakdown (Đề cương chuẩn hóa)

Trong kỹ thuật cơ điện tử và robotics, phân hệ Lý thuyết điều khiển và Ước lượng trạng thái đóng vai trò quyết định độ chính xác, độ ổn định động học và khả năng kháng nhiễu của toàn hệ thống. Nếu như lý thuyết điều khiển cổ điển (*Classical Control*) dựa trên miền tần số và hàm truyền SISO ($G(s)$) giải quyết tốt các bài toán điều tốc động cơ đơn lẻ, thì các cỗ máy cơ điện tử phức tạp (tay máy nhiều bậc tự do, xe tự hành FTS, con lắc ngược cân bằng động) bắt buộc phải chuyển dịch sang **Lý thuyết điều khiển hiện đại trong không gian trạng thái (State-Space Control)** và **Ước lượng ngẫu nhiên tối ưu (Optimal Stochastic Estimation)**.

Chương trình đào tạo chuẩn hóa gồm 12 modules chuyên sâu được xây dựng dựa trên giáo trình của **MIT** (2.14 *Analysis and Design of Feedback Control Systems*, 6.302 *Feedback Systems*), **ETH Zürich** (151-0591-00L *Control Systems I & II*, 151-0566-00L *Recursive Estimation*, 151-0660-00L *Model Predictive Control*), đối chiếu trực tiếp với các Trường học tập `LF8` (*Aufbauen und Prüfen von Steuerungen*) và `LF11` (*Ändern und Optimieren mechatronischer Systeme*) theo chuẩn đào tạo nghề kép CHLB Đức (**DIHK / AHK**).

```
[BẢN ĐỒ TIẾN HÓA LÝ THUYẾT ĐIỀU KHIỂN & ƯỚC LƯỢNG TRONG CƠ ĐIỆN TỬ]
┌────────────────────────────────────────────────────────────────────────┐
│ Điều khiển tối ưu & Dự báo: LQR, LQG, Model Predictive Control (MPC)   │
├────────────────────────────────────────────────────────────────────────┤
│ Ước lượng trạng thái tối ưu: Luenberger Observer, Kalman Filter (DKF)  │
├────────────────────────────────────────────────────────────────────────┤
│ Không gian trạng thái hiện đại: x_dot = A*x + B*u, Điều khiển được/QS  │
├────────────────────────────────────────────────────────────────────────┤
│ Điều khiển cổ điển: PID số, Quỹ đạo nghiệm số (Root Locus), Bode/Nyquist│
└────────────────────────────────────────────────────────────────────────┘
```

---

### Module 01: Nền tảng điều khiển cổ điển & Giới hạn miền tần số (Classical vs. Modern Control Foundations & Frequency-Domain Limitations)
- **Quy chiếu đại học & Tiêu chuẩn:** MIT 2.14 (Lec 1-4), ETH Zürich 151-0591-00L, DIHK `LF8` (*Aufbauen und Prüfen von Steuerungen*).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Hàm truyền hệ đơn biến SISO ($G(s) = \frac{Y(s)}{U(s)}$), Điểm cực (*Poles*) quyết định tính ổn định tiệm cận, Điểm không (*Zeros*) định hình đáp ứng quá độ.
  - Quỹ đạo nghiệm số (Root Locus - *Wurzelortskurve*): Khảo sát sự di dịch của các cực kín khi hệ số khuếch đại thay đổi.
  - Tiêu chuẩn ổn định Nyquist và các đại lượng độ dự trữ ổn định: Độ dự trữ biên độ (Gain Margin - *Amplitudenrand* $A_R$) và độ dự trữ pha (Phase Margin - *Phasenrand* $\Phi_R$).
  - Giới hạn cơ bản miền tần số: Định lý tích phân độ nhạy Poisson-Bode (*Bode Sensitivity Integral / Waterbed Effect*). Khi ta nén độ nhạy $|S(j\omega)|$ ở dải tần thấp để triệt tiêu sai số xác lập, diện tích độ nhạy ở dải tần số cao bắt buộc phải tăng lên, làm khuếch đại nhiễu đo lường của cảm biến.
  - Giới hạn nội tại của điều khiển cổ điển khi áp dụng cho hệ đa biến MIMO (*Multi-Input Multi-Output*), ghép kênh chéo giữa các trục khớp robot (*Cross-Coupling Dynamics*).

---

### Module 02: Biểu diễn hệ động học tuyến tính trong không gian trạng thái (State-Space Representation of Continuous Dynamic Systems)
- **Quy chiếu đại học & Tiêu chuẩn:** Ogata (2010) Ch. 10, Franklin, Powell & Workman (1998) Ch. 6, ETH Zürich 151-0591-00L, MIT 2.14.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Khái niệm biến trạng thái (*State Variables*): Tập hợp tối thiểu các biến vật lý mang đầy đủ thông tin về quá khứ và hiện tại để xác định hoàn toàn quỹ đạo tương lai của hệ thống.
  - Ma trận hệ thống động học $A$, Ma trận ngõ vào điều khiển $B$, Ma trận ngõ ra đo lường $C$, và Ma trận truyền thẳng $D$.
  - Biến đổi tọa độ không gian trạng thái tuyến tính ($z = T x$): Tính bất biến của các giá trị riêng (*Eigenvalue Invariance*), phương trình đặc tính không phụ thuộc vào hệ tọa độ cơ sở.
  - Các dạng chuẩn tắc kinh điển: Dạng chuẩn tắc điều khiển được (*Controllable Canonical Form*), Dạng chuẩn tắc quan sát được (*Observable Canonical Form*), và Dạng chuẩn Jordan.
- **Mô hình toán học & Phương trình thiết kế:**
  Hệ phương trình không gian trạng thái tuyến tính liên tục dừng (LTI):
  $$\dot{x}(t) = A x(t) + B u(t)$$
  $$y(t) = C x(t) + D u(t)$$
  Dẫn xuất hàm truyền ma trận tương đương từ mô hình trạng thái:
  $$G(s) = C (s I - A)^{-1} B + D = \frac{C \cdot \text{adj}(s I - A) \cdot B}{\det(s I - A)} + D$$
  Trong đó nghiệm của đa thức đặc tính $\det(s I - A) = 0$ chính là các cực hệ thống kín.

---

### Module 03: Rời rạc hóa hệ thống & Điều khiển dữ liệu lấy mẫu (Discretization & Sampled-Data Control Systems)
- **Quy chiếu đại học & Tiêu chuẩn:** Franklin, Powell & Workman (1998) Ch. 3 & 9, DIHK `LF9` (*Programmieren mechatronischer Systeme*).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Khâu giữ mẫu bậc không (ZOH - *Zero-Order Hold / Halteglied nullter Ordnung*): Tín hiệu điều khiển $u(t)$ được giữ hằng số giữa hai chu kỳ trích mẫu liên tiếp $t \in [k T_s, (k+1) T_s)$.
  - Tính toán ma trận hàm mũ $e^{A T_s}$ bằng chuỗi Taylor, biến đổi Laplace ngược $\mathcal{L}^{-1}\{(sI - A)^{-1}\}$, hoặc định lý Cayley-Hamilton.
  - Lựa chọn chu kỳ trích mẫu $T_s$ trong cơ điện tử: Quy tắc thực nghiệm chọn tần số lấy mẫu $f_s = \frac{1}{T_s} \ge 10 \text{ đến } 20 \cdot f_{\text{bandwidth}}$ để giảm thiểu độ trễ pha do trích mẫu ($e^{-s T_s/2}$).
- **Mô hình toán học & Phương trình thiết kế:**
  Hệ phương trình trạng thái thời gian rời rạc:
  $$x[k+1] = A_d x[k] + B_d u[k], \quad y[k] = C_d x[k] + D_d u[k]$$
  Các ma trận rời rạc tương đương tính toán chính xác từ mô hình liên tục:
  $$A_d = e^{A T_s} = I + A T_s + \frac{(A T_s)^2}{2!} + \frac{(A T_s)^3}{3!} + \dots$$
  $$B_d = \int_0^{T_s} e^{A \tau} B \, d\tau = \left( \sum_{k=0}^{\infty} \frac{A^k T_s^{k+1}}{(k+1)!} \right) B$$
  $$C_d = C, \quad D_d = D$$

---

### Module 04: Tính điều khiển được, tính quan sát được & Điều kiện hạng Kalman (Controllability, Observability & Kalman Rank Conditions)
- **Quy chiếu đại học & Tiêu chuẩn:** Ogata (2010) Ch. 10, MIT 2.151, Rudolf E. Kálmán (1960).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Tính điều khiển được (*Controllability* - *Steuerbarkeit*): Khả năng lái trạng thái hệ thống từ một điểm bất kỳ $x(0)$ về gốc tọa độ $x(t_1) = 0$ trong khoảng thời gian hữu hạn bằng tín hiệu điều khiển không bị ràng buộc $u(t)$.
  - Tính quan sát được (*Observability* - *Beobachtbarkeit*): Khả năng khôi phục duy nhất trạng thái ban đầu $x(0)$ thông qua việc theo dõi ngõ ra $y(t)$ và ngõ vào $u(t)$ trong khoảng thời gian hữu hạn.
  - Ma trận điều khiển được $\mathcal{C}$ và ma trận quan sát được $\mathcal{O}$ của Kalman.
  - Kiểm định PBH (Popov-Belevitch-Hautus Test): Khảo sát từng giá trị riêng $\lambda_i$ của $A$ để phát hiện chính xác mode động học nào không điều khiển được hoặc không quan sát được.
- **Mô hình toán học & Phương trình thiết kế:**
  Điều kiện đủ và cần về hạng của Kalman cho hệ thống liên tục $n$ bậc tự do:
  $$\mathcal{C} = \begin{bmatrix} B & AB & A^2 B & \dots & A^{n-1} B \end{bmatrix}, \quad \text{rank}(\mathcal{C}) = n$$
  $$\mathcal{O} = \begin{bmatrix} C \\ CA \\ CA^2 \\ \vdots \\ CA^{n-1} \end{bmatrix}, \quad \text{rank}(\mathcal{O}) = n$$
  Kiểm định PBH đối với tính điều khiển được:
  $$\text{rank}\begin{bmatrix} s I - A & B \end{bmatrix} = n, \quad \forall s \in \mathbb{C}$$

---

### Module 05: Hồi tiếp trạng thái toàn phần & Kỹ thuật đặt cực (Full-State Feedback & Pole Placement Design)
- **Quy chiếu đại học & Tiêu chuẩn:** Ogata (2010) Ch. 11, ETH Zürich 151-0591-00L, UC Berkeley EE192.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Luật điều khiển hồi tiếp trạng thái tuyến tính $u = -K x$: Cho phép dịch chuyển tùy ý toàn bộ $n$ cực của hệ kín trên mặt phẳng phức nếu hệ thống hoàn toàn điều khiển được.
  - Đa thức đặc tính mong muốn $\phi_d(s) = \prod_{i=1}^n (s - \lambda_{d,i})$: Lựa chọn vị trí cực cân bằng giữa tốc độ đáp ứng (thời gian quá độ $t_s$) và giới hạn lực đẩy của cơ cấu chấp hành ($|u(t)| \le u_{\max}$).
  - Công thức Ackermann (*Ackermann-Formel*): Phương pháp giải tích tính toán trực tiếp vectơ hệ số khuếch đại $K$ cho hệ SISO mà không cần biến đổi ma trận phức tạp.
  - Bám tín hiệu đặt thông qua hệ số tiền định $N$ (*Pre-filter / Reference Feedforward Gain*): Khử sai số xác lập khi điều khiển vị trí/vận tốc.
- **Mô hình toán học & Phương trình thiết kế:**
  Luật điều khiển có bù tín hiệu chuẩn $r(t)$:
  $$u(t) = -K x(t) + N r(t)$$
  Công thức Ackermann xác định ma trận khuếch đại $K$:
  $$K = \begin{bmatrix} 0 & 0 & \dots & 0 & 1 \end{bmatrix} \mathcal{C}^{-1} \phi_d(A)$$
  Trong đó $\phi_d(A) = A^n + \alpha_{n-1} A^{n-1} + \dots + \alpha_1 A + \alpha_0 I$.
  Hệ số bám tiền định $N$ để triệt tiêu sai số xác lập ngõ ra $y(\infty) = r$:
  $$N = \left[ C (B K - A)^{-1} B + D \right]^{-1}$$

---

### Module 06: Bộ quan sát trạng thái & Bộ quan sát Luenberger (State Observers & The Luenberger Observer)
- **Quy chiếu đại học & Tiêu chuẩn:** Ogata (2010) Ch. 11, Franklin, Powell & Workman (1998) Ch. 7, MIT 6.302.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Vấn đề thực tế trong cơ điện tử: Trong thực tế ta không thể gắn cảm biến đo lường toàn bộ các biến trạng thái $x(t)$ (ví dụ: chỉ có cảm biến góc encoder nhưng không có cảm biến đo vận tốc góc hoặc gia tốc). Cần một thuật toán ước lượng trạng thái nội tại $\hat{x}(t)$.
  - Cấu trúc bộ quan sát Luenberger toàn phần (*Full-Order Luenberger Observer*): Kết hợp mô hình toán học song song của đối tượng với khâu bù trừ sai lệch dự báo thông qua ma trận khuếch đại quan sát $L$.
  - Động học sai số quan sát: $e(t) = x(t) - \hat{x}(t) \implies \dot{e}(t) = (A - L C) e(t)$.
  - Nguyên lý tách rời (Separation Principle - *Separationsprinzip*): Thiết kế ma trận điều khiển $K$ và ma trận quan sát $L$ hoàn toàn độc lập với nhau mà không làm thay đổi các cực riêng phần của hệ thống kín.
- **Mô hình toán học & Phương trình thiết kế:**
  Phương trình động học bộ quan sát Luenberger:
  $$\dot{\hat{x}}(t) = A \hat{x}(t) + B u(t) + L \left( y(t) - C \hat{x}(t) \right)$$
  Phương trình đặc tính của toàn bộ hệ kín khi kết hợp bộ điều khiển hồi tiếp trạng thái và bộ quan sát:
  $$\det \begin{bmatrix} s I - (A - B K) & B K \\ 0 & s I - (A - L C) \end{bmatrix} = \det(s I - (A - B K)) \cdot \det(s I - (A - L C)) = 0$$
  Quy tắc chọn cực quan sát: Cực quan sát thường được chọn nằm sâu về bên trái mặt phẳng phức gấp 3 đến 5 lần cực điều khiển ($\text{Re}(\lambda_{\text{obs}}) \approx (3 \dots 5) \cdot \text{Re}(\lambda_{\text{ctrl}})$) để tốc độ hội tụ của bộ quan sát nhanh hơn tốc độ phản ứng của cơ cấu chấp hành.

---

### Module 07: Điều khiển tối ưu & Bộ điều chỉnh toàn phương tuyến tính LQR (Optimal Control & Linear Quadratic Regulator)
- **Quy chiếu đại học & Tiêu chuẩn:** Stengel (1994) Ch. 3, ETH Zürich 151-0591-00L, Stanford ENGR205.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Đặt bài toán tối ưu: Thay vì gán cực tùy ý theo trực giác, LQR tìm luật điều khiển tối ưu hóa một hàm mục tiêu năng lượng bậc hai xác định dương $J$.
  - Ý nghĩa vật lý của các ma trận trọng số $Q$ và $R$:
    - $Q \succeq 0$ (Bán xác định dương): Phạt độ lệch của các biến trạng thái so với điểm cân bằng.
    - $R \succ 0$ (Xác định dương): Phạt năng lượng tiêu thụ hoặc biên độ lực đẩy của cơ cấu chấp hành.
  - Quy tắc Bryson (*Bryson's Rule*): Khởi tạo ma trận trọng số theo nghịch đảo bình phương giá trị sai lệch tối đa cho phép: $Q_{ii} = \frac{1}{x_{i,\max}^2}, R_{jj} = \frac{1}{u_{j,\max}^2}$.
  - Độ dự trữ bền vững kinh điển của LQR: Đạt độ dự trữ biên độ vô hạn ($A_R = \infty$) và độ dự trữ pha tối thiểu $\Phi_R \ge 60^\circ$.
- **Mô hình toán học & Phương trình thiết kế:**
  Hàm mục tiêu chi phí năng lượng toàn phương thời gian liên tục vô hạn:
  $$J = \int_0^{\infty} \left( x(t)^T Q x(t) + u(t)^T R u(t) \right) dt$$
  Phương trình đại số Riccati liên tục (CARE - *Continuous Algebraic Riccati Equation*):
  $$A^T P + P A - P B R^{-1} B^T P + Q = 0$$
  Luật điều khiển tối ưu và vectơ hệ số khuếch đại LQR:
  $$u(t) = -K x(t), \quad K = R^{-1} B^T P$$
  Đối với hệ thống thời gian rời rạc, giải phương trình đại số Riccati rời rạc (DARE):
  $$P = A_d^T P A_d - A_d^T P B_d \left( R + B_d^T P B_d \right)^{-1} B_d^T P A_d + Q$$
  $$K = \left( R + B_d^T P B_d \right)^{-1} B_d^T P A_d$$

---

### Module 08: Hệ thống ngẫu nhiên & Mô hình hóa nhiễu cảm biến (Stochastic Systems & Sensor Noise Characterization)
- **Quy chiếu đại học & Tiêu chuẩn:** Arthur Gelb (1974) Ch. 2-3, ETH Zürich 151-0566-00L (Recursive Estimation).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Giới hạn của bộ quan sát tất định Luenberger: Luenberger giả định phép đo cảm biến là chính xác tuyệt đối; khi cảm biến bị nhiễm nhiễu trắng ngẫu nhiên, việc đặt cực quan sát quá nhanh sẽ biến bộ quan sát thành một "máy khuếch đại nhiễu" làm rung giật hệ cơ khí.
  - Quá trình ngẫu nhiên dừng, Tiếng ồn trắng Gauss (AWGN - *Additive White Gaussian Noise*).
  - Ma trận hiệp phương sai nhiễu quá trình $Q_k = \mathbb{E}[w_k w_k^T]$ (đại diện cho nhiễu gió, rung động cơ khí, ma sát ngẫu nhiên).
  - Ma trận hiệp phương sai nhiễu đo lường $R_k = \mathbb{E}[v_k v_k^T]$ (đại diện cho nhiễu nhiệt ADC, nhiễu lượng tử hóa encoder).
  - Phân tích phương sai Allan (*Allan Variance*) và đặc tính lỗi cảm biến IMU (Random Walk, Bias Instability).

---

### Module 09: Bộ lọc Kalman rời rạc: Ước lượng trạng thái tối ưu (Discrete-Time Linear Kalman Filtering)
- **Quy chiếu đại học & Tiêu chuẩn:** Rudolf E. Kálmán (1960), Gelb (1974) Ch. 4, ETH Zürich 151-0566-00L.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Bộ lọc Kalman là bộ ước lượng tuyến tính tối ưu không chệch có phương sai cực tiểu (BLUE - *Best Linear Unbiased Estimator*).
  - Kiến trúc đệ quy hai pha kinh điển:
    1. **Pha dự báo (Time Update / Prediction - *Prädiktion*):** Lan truyền trạng thái và hiệp phương sai lỗi dựa trên mô hình toán học của cơ cấu chuyển động.
    2. **Pha hiệu chỉnh (Measurement Update / Correction - *Korrektur*):** Đo lường thực tế, tính toán phần dư đổi mới (*Innovation Residual*), và dung hòa giữa dự báo lý thuyết với dữ liệu cảm biến thực tế thông qua ma trận khuếch đại Kalman Gain $K_k$.
  - Dạng hiệp phương sai bền vững số học Joseph (*Joseph Stabilized Covariance Form*): Đảm bảo ma trận hiệp phương sai $P_{k|k}$ luôn đối xứng và xác định dương tuyệt đối trong môi trường tính toán số dấu phẩy động 32-bit/64-bit trên vi điều khiển nhúng.
- **Mô hình toán học & Phương trình thiết kế:**
  Mô hình hệ thống ngẫu nhiên rời rạc:
  $$x_k = A_d x_{k-1} + B_d u_{k-1} + w_{k-1}, \quad z_k = H x_k + v_k$$
  **1. Pha dự báo (Time Update):**
  $$\hat{x}_{k|k-1} = A_d \hat{x}_{k-1|k-1} + B_d u_{k-1}$$
  $$P_{k|k-1} = A_d P_{k-1|k-1} A_d^T + Q_k$$
  **2. Pha hiệu chỉnh (Measurement Update):**
  $$y_k = z_k - H \hat{x}_{k|k-1} \quad (\text{Phần dư đổi mới - Innovation})$$
  $$S_k = H P_{k|k-1} H^T + R_k \quad (\text{Hiệp phương sai đổi mới})$$
  $$K_k = P_{k|k-1} H^T S_k^{-1} \quad (\text{Hệ số khuếch đại Kalman})$$
  $$\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k y_k$$
  $$P_{k|k} = (I - K_k H) P_{k|k-1} (I - K_k H)^T + K_k R_k K_k^T \quad (\text{Dạng ổn định Joseph})$$

---

### Module 10: Điều khiển Gauss toàn phương tuyến tính LQG & Ranh giới bền vững (Linear Quadratic Gaussian & Robustness Boundaries)
- **Quy chiếu đại học & Tiêu chuẩn:** Stengel (1994) Ch. 5, MIT 6.302, Doyle (1978).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Kiến trúc điều khiển LQG: Ghép nối tối ưu giữa bộ điều khiển trạng thái LQR với bộ ước lượng trạng thái tối ưu Kalman Filter ($u = -K \hat{x}$).
  - Định lý tách rời ngẫu nhiên (*Certainty Equivalence Principle*): Khẳng định rằng thiết kế bộ lọc Kalman và thiết kế bộ điều khiển LQR có thể giải riêng rẽ độc lập.
  - Phản ví dụ chấn động của John Doyle (1978): "Guaranteed Margins for LQG Regulators". Mặc dù LQR thuần túy có độ dự trữ pha $\ge 60^\circ$ và biên độ $\infty$, nhưng khi ghép với bộ lọc Kalman (hệ LQG), độ dự trữ pha có thể suy biến về $0^\circ$ và biên độ về 0 dB nếu hệ thống bị trôi thông số mô hình.
  - Phương pháp khôi phục hàm truyền mạch vòng (LTR - *Loop Transfer Recovery*): Bơm nhiễu giả định vào ma trận $Q$ để kéo gần đặc tính bền vững của LQG tiệm cận về LQR chuẩn.

---

### Module 11: Ước lượng phi tuyến: Extended Kalman Filter (EKF) & Unscented Kalman Filter (UKF)
- **Quy chiếu đại học & Tiêu chuẩn:** Gelb (1974) Ch. 6, ETH Zürich 151-0566-00L, Thrun et al. *Probabilistic Robotics*.
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Bài toán phi tuyến thực tế trong robotics: Động học góc Euler/Quaternion, phương trình đo khoảng cách và góc của cảm biến LiDAR/Camera là các hàm phi tuyến: $\dot{x} = f(x, u) + w, z = h(x) + v$.
  - Bộ lọc Kalman mở rộng (EKF - *Extended Kalman Filter*): Tuyến tính hóa Taylor bậc 1 xung quanh điểm ước lượng trạng thái hiện thời thông qua ma trận Jacobi ($F = \frac{\partial f}{\partial x}, H = \frac{\partial h}{\partial x}$). Nguy cơ phân kỳ (*Divergence*) khi mức độ phi tuyến quá mạnh hoặc khởi tạo xa điểm làm việc.
  - Bộ lọc Kalman vô hương (UKF - *Unscented Kalman Filter*): Sử dụng phép biến đổi vô hương (*Unscented Transform*) chọn tập các điểm Sigma đối xứng để bắt chính xác giá trị kỳ vọng và hiệp phương sai đến bậc 3 của chuỗi Taylor mà không cần tính đạo hàm ma trận Jacobi phức tạp.

---

### Module 12: Điều khiển dự báo theo mô hình MPC & Tối ưu hóa ràng buộc (Model Predictive Control & Constrained Optimization)
- **Quy chiếu đại học & Tiêu chuẩn:** Camacho & Bordons (2007) Ch. 2-3, ETH Zürich 151-0660-00L, DIHK `LF11` (*Ändern und Optimieren mechatronischer Systeme*).
- **Bản chất nguyên lý & Trọng tâm học thuật:**
  - Khái niệm chân trời lùi dần (Receding Horizon Principle - *Prinzip des weichenden Horizonts*): Tại mỗi chu kỳ trích mẫu, giải một bài toán quy hoạch tối ưu trên chân trời dự báo $N_p$, áp dụng duy nhất hành động điều khiển ở bước đầu tiên $u_0$, sau đó dịch chuyển cửa sổ thời gian và lặp lại tối ưu ở chu kỳ tiếp theo.
  - Xử lý tường minh các ràng buộc vật lý: Ràng buộc bão hòa điện áp/dòng điện cơ cấu chấp hành ($u_{\min} \le u_k \le u_{\max}$), tốc độ biến thiên ngõ vào ($\Delta u_{\min} \le \Delta u_k \le \Delta u_{\max}$), và vùng không gian an toàn của cánh tay robot ($x_{\min} \le x_k \le x_{\max}$).
  - Chuyển đổi bài toán MPC tuyến tính thành bài toán Quy hoạch toàn phương lồi (QP - *Quadratic Programming*).
- **Mô hình toán học & Phương trình thiết kế:**
  Bài toán tối ưu hóa MPC trên chân trời dự báo $N_p$:
  $$\min_{\{u_k\}_{k=0}^{N_p-1}} \sum_{k=0}^{N_p-1} \left( x_{t+k|t}^T Q_{\text{mpc}} x_{t+k|t} + u_{t+k|t}^T R_{\text{mpc}} u_{t+k|t} \right) + x_{t+N_p|t}^T P_{\text{terminal}} x_{t+N_p|t}$$
  Thỏa mãn các ràng buộc đẳng thức mô hình và bất đẳng thức vật lý:
  $$x_{k+1} = A_d x_k + B_d u_k$$
  $$u_{\min} \le u_k \le u_{\max}, \quad x_{\min} \le x_k \le x_{\max}$$

---

## 2. Academic Reading List (Danh mục tài liệu học thuật)

Học viên và kỹ sư cơ điện tử nghiên cứu chuyên sâu phân hệ 04 bắt buộc phải đọc và tham chiếu các giáo trình kinh điển sau:

1. **Katsuhiko Ogata (2010)**: *Modern Control Engineering*, 5th Edition, Prentice Hall / Pearson, Boston, MA. ISBN: 978-0136156734.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 5 (Transient and Steady-State Response Analysis), Chương 9 (PID Controllers & Modified PID), Chương 10 (Analysis of Control Systems in State Space - Controllability/Observability), Chương 11 (Design of Control Systems in State Space - Pole Placement & State Observers). Giáo trình kinh điển định hình toàn diện nền tảng không gian trạng thái.
2. **Gene F. Franklin, J. David Powell, and Michael L. Workman (1998)**: *Digital Control of Dynamic Systems*, 3rd Edition, Addison-Wesley Longman, Menlo Park, CA. ISBN: 978-0201820546.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 3 (Sampled-Data Systems & Z-Transform), Chương 6 (State-Space Design of Digital Systems), Chương 7 (Observer Design and State Estimation), Chương 8 (Quantization & Finite Wordlength Effects). Tác phẩm chuẩn mực về chuyển đổi hệ thống liên tục sang vi điều khiển số.
3. **Arthur Gelb (Editor) (1974)**: *Applied Optimal Estimation*, The Analytic Sciences Corporation (TASC), MIT Press, Cambridge, MA. ISBN: 978-0262570480.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 2 (Mathematical Review of Linear Random Variables), Chương 3 (Optimal Linear Filtering), Chương 4 (Linear Smoothing), Chương 6 (Nonlinear Estimation & Extended Kalman Filter). Cẩm nang gối đầu giường của các kỹ sư ước lượng hàng không vũ trụ và điều khiển tự động.
4. **Eduardo F. Camacho and Carlos Bordons (2007)**: *Model Predictive Control*, 2nd Edition, Advanced Textbooks in Control and Signal Processing, Springer, London. ISBN: 978-1852336943.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 1 (Introduction to MPC), Chương 2 (Commercial Model Predictive Control Schemes), Chương 3 (Elements of Model Predictive Control), Chương 4 (Tuning and Stability of MPC). Nguồn tài liệu hệ thống hóa toàn diện kỹ thuật MPC công nghiệp.
5. **Robert F. Stengel (1994)**: *Optimal Control and Estimation*, Dover Books on Aeronautical Engineering, Dover Publications, New York. ISBN: 978-0486682006.
   - *Phạm vi nghiên cứu cốt lõi:* Chương 2 (Deterministic Optimal Control), Chương 3 (Linear-Quadratic Regulators - LQR), Chương 4 (Optimal State Estimation - Kalman Filter), Chương 5 (Linear Quadratic Gaussian - LQG & Robust Control).
6. **Rudolf E. Kálmán (1960)**: "A New Approach to Linear Filtering and Prediction Problems", *Journal of Basic Engineering (Transactions of the ASME)*, Vol. 82, Series D, No. 1, pp. 35–45.
   - *Phạm vi nghiên cứu cốt lõi:* Bài báo khoa học nguyên bản khai sinh ra bộ lọc Kalman, chứng minh tính đệ quy tối ưu trong miền thời gian rời rạc.

---

## 3. Practical Labs & Simulation Projects (Bài tập thực hành & Project mô phỏng)

Hệ thống bài tập thực hành được xây dựng theo chuẩn mực thực nghiệm cao, kết hợp giữa mô phỏng giải tích thuần toán học và mã nguồn thực thi độc lập.

---

### Lab 1: Thiết kế bộ điều khiển PID số với kỹ thuật chống bão hòa tích phân (Anti-Windup) và lọc đạo hàm trên vi điều khiển
- **Mục tiêu kỹ thuật:**
  1. Rời rạc hóa bộ điều khiển PID liên tục theo phương pháp xấp xỉ hình thang Tustin:
     $$u[k] = u[k-1] + K_p \left( e[k] - e[k-1] \right) + K_i \frac{T_s}{2} \left( e[k] + e[k-1] \right) + K_d \frac{2}{2 \tau + T_s} \left( e[k] - 2e[k-1] + e[k-2] \right)$$
  2. Bổ sung bộ lọc thông thấp quán tính bậc nhất cho khâu vi phân ($N = \frac{1}{\tau} \approx 10 \dots 20$) để triệt tiêu việc khuếch đại nhiễu tần số cao của cảm biến đo.
  3. Hiện thực hóa thuật toán chống bão hòa tích phân dạng kẹp giá trị (*Clamping / Conditional Integration*) hoặc hồi tiếp bù sai lệch bão hòa (*Back-Calculation Anti-Windup*): Khi tín hiệu ngõ ra chạm ngưỡng bão hòa phần cứng của PWM ($u(t) \in [0, 100\%]$) và sai số $e[k]$ cùng dấu với trạng thái bão hòa, lập tức ngắt việc cộng dồn khâu tích phân.
- **Yêu cầu kết quả:** Triệt tiêu hoàn toàn hiện tượng vọt lố quá mức (*Overshoot*) do khâu tích phân bị tích lũy năng lượng khi cơ cấu chấp hành bị bão hòa.

---

### Lab 2: Khảo sát tính điều khiển được/quan sát được và thiết kế bộ quan sát trạng thái Luenberger (Luenberger Observer) cho hệ cơ điện tử
- **Mục tiêu kỹ thuật:**
  1. Xây dựng mô hình không gian trạng thái của hệ trục truyền động động cơ DC kèm tải đàn hồi (hệ 4 biến trạng thái: góc quay rotor $\theta_m$, vận tốc góc rotor $\omega_m$, góc quay tải $\theta_L$, vận tốc góc tải $\omega_L$).
  2. Tính toán ma trận điều khiển được $\mathcal{C}$ và ma trận quan sát được $\mathcal{O}$, chứng minh $\text{rank}(\mathcal{C}) = 4$ và $\text{rank}(\mathcal{O}) = 4$ khi chỉ đo duy nhất cảm biến vị trí góc tải $\theta_L$.
  3. Sử dụng công thức Ackermann thiết kế ma trận khuếch đại quan sát $L$ để các cực sai số quan sát hội tụ nhanh gấp 4 lần cực hệ kín, kiểm chứng khả năng khôi phục vận tốc góc khi tín hiệu đo bị mất mát.
- **Yêu cầu kết quả:** Sai số ước lượng trạng thái $\|x(t) - \hat{x}(t)\|$ tiệm cận về 0 trong vòng $0.2\text{ s}$.

---

### Lab 3: Cân bằng con lắc ngược trên xe trượt bằng bộ điều khiển LQR và bộ lọc Kalman rời rạc (Reference Simulation: labs/lab04_kalman_lqr.py)
- **Mục tiêu kỹ thuật:**
  - Mô hình hóa đối tượng cơ điện tử kinh điển: Con lắc ngược trên xe trượt (*Inverted Pendulum on a Cart* / *Wagen mit inversem Pendel*).
    - Khối lượng xe trượt $M = 1.0\text{ kg}$, khối lượng thanh lắc $m = 0.1\text{ kg}$, chiều dài thanh lắc $l = 0.5\text{ m}$, hệ số ma sát trượt $b = 0.1\text{ N}\cdot\text{s/m}$, gia tốc trọng trường $g = 9.81\text{ m/s}^2$.
    - Vectơ trạng thái 4 chiều: $x = [p, \dot{p}, \theta, \dot{\theta}]^T$ (vị trí xe, vận tốc xe, góc nghiêng thanh lắc, vận tốc góc).
  - Tuyến tính hóa hệ phi tuyến quanh điểm cân bằng thẳng đứng ($\theta \approx 0$).
  - Giải phương trình đại số Riccati rời rạc (DARE) bằng phương pháp lặp giá trị thuần Python (*Value Iteration*) để tính toán vectơ hồi tiếp trạng thái tối ưu $K_{\text{LQR}}$.
  - Xây dựng Bộ lọc Kalman rời rạc (DKF) chuẩn ổn định số học Joseph ước lượng trạng thái từ tín hiệu đo vị trí và góc bị pha tạp tiếng ồn trắng Gauss ($\sigma_p = 10\text{ mm}, \sigma_\theta = 0.28^\circ$).
  - Thực thi vòng lặp phản hồi kín khép kín với giới hạn lực bão hòa của động cơ kéo xe ($|u| \le 20\text{ N}$).
- **Tệp mã nguồn chuẩn:** `labs/lab04_kalman_lqr.py`
- **Cách thức thực thi:**
  ```bash
  python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab04_kalman_lqr.py
  ```
- **Chỉ số định lượng đầu ra kiểm chứng:**
  - Thời gian tính toán toàn bộ mô phỏng: $< 150\text{ ms}$ (đạt $\approx 80\text{ ms}$ trên CPU macOS).
  - Thuật toán DARE hội tụ thành công tìm ra vectơ khuếch đại: $K \approx [-8.98, -11.84, 81.68, 21.45]$.
  - Điều kiện nhiễu cảm biến: Nhiễu vị trí $\sigma_p = 10\text{ mm}$, nhiễu góc $\sigma_\theta = 0.28^\circ$.
  - Sai số căn phương trung bình bộ lọc Kalman: RMSE vị trí $= 9.30\text{ mm} < 20.0\text{ mm}$, RMSE góc $= 0.264^\circ$.
  - Đáp ứng quá độ ổn định hệ thống: Xuất phát từ độ lệch ban đầu $p(0) = 0.20\text{ m}$, góc nghiêng $\theta(0) = 0.15\text{ rad} \approx 8.6^\circ$.
  - Thời gian xác lập cân bằng (|$\theta| < 0.01\text{ rad}$): $1.50\text{ s} < 2.50\text{ s}$.
  - Sai số xác lập cuối cùng: Vị trí xe $|p_{\text{final}}| = 0.0059\text{ m} < 0.02\text{ m}$, góc nghiêng $|\theta_{\text{final}}| = 0.00426\text{ rad} < 0.005\text{ rad}$.
  - Trạng thái kiểm chứng: `System Stabilized (PASS) : True`.

---

## 4. Exact Search Queries & Bilingual Terminology Table (Từ khóa tìm kiếm & Thuật ngữ Anh-Đức)

### 4.1 Danh mục 12 Truy vấn tìm kiếm học thuật độ chính xác cao (Precision Search Queries)

Các truy vấn dưới đây giúp tra cứu nhanh các tài liệu gốc, mã nguồn thuật toán và bài giảng chuyên sâu từ các viện nghiên cứu hàng đầu thế giới:

1. `"Linear Quadratic Regulator" "Algebraic Riccati Equation" "Schur decomposition" filetype:pdf site:mit.edu`
2. `"Kalman Filter" "Joseph form" "covariance update" "numerical stability" filetype:pdf`
3. `site:ethz.ch "151-0591-00L" "Control Systems" "State-Space" lecture notes filetype:pdf`
4. `site:ethz.ch "151-0566-00L" "Recursive Estimation" "Kalman Filter" "Riccati"`
5. `"Inverted pendulum on cart" "state-space model" "linearization" "LQR" filetype:pdf`
6. `"Model Predictive Control" "receding horizon" "quadratic programming" "Camacho" filetype:pdf`
7. `"Ackermann formula" "pole placement" "controllability matrix" "Ogata" filetype:pdf`
8. `"Luenberger observer" "separation principle" "eigenvalue assignment" filetype:pdf`
9. `site:ocw.mit.edu "2.14" OR "6.302" "state feedback" "LQR" "Riccati"`
10. `"DIN 19226" "DIN IEC 60050-351" "Führungsgröße" "Regelgröße" "Stellgröße" Regelungstechnik`
11. `site:github.com "inverted pendulum" "LQR" "Kalman filter" "python" simulation`
12. `"Extended Kalman Filter" "Jacobian" "robotics state estimation" "quaternion" filetype:pdf`

---

### 4.2 Bảng thuật ngữ chuyên ngành đối chiếu Anh – Đức – Ký hiệu DIN 19226 / DIN IEC – Việt

> **CẢNH BÁO QUAN TRỌNG VỀ SỰ KHÁC BIỆT KÝ HIỆU GIỮA CHUẨN ĐỨC DIN 19226 VÀ LÝ THUYẾT HIỆN ĐẠI:**  
> Trong tiêu chuẩn truyền thống của Đức (**DIN 19226** - vẫn được sử dụng phổ biến trong các sách tra cứu nghề *Europa Tabellenbuch Mechatronik* và đề thi DIHK), ký hiệu $x$ được dùng để chỉ **Đại lượng được điều khiển / Ngõ ra (Regelgröße)**, còn $y$ được dùng để chỉ **Đại lượng tác động / Tín hiệu điều khiển (Stellgröße)**.  
> Trong khi đó, trong **Lý thuyết không gian trạng thái hiện đại và tiêu chuẩn quốc tế DIN IEC 60050-351**, ký hiệu $x$ đại diện cho **Vectơ trạng thái (State Vector)**, $y$ là **Ngõ ra đo lường (Output)**, và $u$ là **Tín hiệu điều khiển (Control Input)**. Bảng dưới đây làm rõ sự đối chiếu này để tránh nhầm lẫn tai hại trong nghiên cứu và thi cử:

| English Term | German Fachbegriff (DIN/IEC) | DIN 19226 Ký hiệu | Modern / DIN IEC 60050-351 | Tiếng Việt chuẩn kỹ thuật (Vietnamese) |
|---|---|---|---|---|
| Control Engineering | Regelungstechnik | – | – | Kỹ thuật điều khiển tự động |
| Reference Variable / Setpoint | Führungsgröße | $w$ | $r$ hoặc $w$ | Tín hiệu đặt / Giá trị chuẩn mong muốn |
| Controlled Variable (Output) | Regelgröße | $x$ | $y$ | Đại lượng được điều khiển (Ngõ ra) |
| Manipulated Variable (Input) | Stellgröße | $y$ | $u$ | Đại lượng tác động điều khiển (Ngõ vào) |
| Disturbance Variable | Störgröße | $z$ | $d$ hoặc $z$ | Đại lượng nhiễu loạn |
| Control Error / Deviation | Regeldifferenz | $e = w - x$ | $e = r - y$ | Sai lệch điều khiển |
| Plant / Dynamic Process | Regelstrecke | – | – | Đối tượng điều khiển (Hệ động học) |
| Controller | Regler | – | – | Bộ điều khiển |
| Actuator | Stellglied / Aktor | – | – | Cơ cấu chấp hành |
| State-Space Representation | Zustandsraumdarstellung | – | $\dot{x} = Ax + Bu$ | Biểu diễn không gian trạng thái |
| State Vector | Zustandsvektor | – | $x = [x_1, \dots, x_n]^T$ | Vectơ trạng thái hệ thống |
| Controllability | Steuerbarkeit (Kalman) | – | $\text{rank}(\mathcal{C}) = n$ | Tính điều khiển được |
| Observability | Beobachtbarkeit (Kalman) | – | $\text{rank}(\mathcal{O}) = n$ | Tính quan sát được |
| State Feedback Controller | Zustandsregler | – | $u = -K x$ | Bộ điều khiển hồi tiếp trạng thái |
| Linear Quadratic Regulator | LQ-Regler (Linear-quadratischer Regler) | – | $J = \int (x^T Q x + u^T R u) dt$ | Bộ điều chỉnh toàn phương tuyến tính (LQR) |
| Algebraic Riccati Equation | Algebraische Riccati-Gleichung (ARE) | – | $A^T P + P A - P B R^{-1} B^T P + Q = 0$ | Phương trình đại số Riccati |
| Kalman Filter | Kalman-Filter (Zustandsschätzer) | – | $\hat{x}_{k|k}, P_{k|k}, K_k$ | Bộ lọc Kalman (Ước lượng trạng thái tối ưu) |
| Model Predictive Control | Modellprädiktive Regelung (MPC) | – | $\min \sum (x^T Q x + u^T R u)$ | Điều khiển dự báo theo mô hình (MPC) |
| Pole Placement Design | Polvorgabe / Polplatzierung | – | $\det(sI - (A - BK)) = 0$ | Kỹ thuật đặt cực không gian trạng thái |
| Luenberger Observer | Luenberger-Beobachter | – | $\dot{\hat{x}} = A\hat{x} + Bu + L(y - C\hat{x})$ | Bộ quan sát trạng thái Luenberger |
| Separation Principle | Separationsprinzip | – | – | Nguyên lý tách rời (Điều khiển & Quan sát) |
| Anti-Windup | Anti-Windup-Schaltung | – | – | Kỹ thuật chống bão hòa khâu tích phân |
