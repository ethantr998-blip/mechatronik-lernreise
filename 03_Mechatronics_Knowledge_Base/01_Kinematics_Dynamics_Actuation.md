# Subsystem 01: Kinematics, Dynamics & Actuation
## Động học, Động lực học & Cơ cấu chấp hành Mechatronics

Tài liệu này cấu thành gói tri thức chuẩn mực cấp đại học (*University-Grade Knowledge Package*) cho Phân hệ 01: **Động học, Động lực học & Cơ cấu chấp hành** trong hệ thống Cơ điện tử & Robot (*Mechatronik und Robotik*). Nội dung được tổng hợp, chuẩn hóa từ giáo trình và bài giảng của các trường đại học kỹ thuật hàng đầu thế giới: **MIT** (2.737 Mechatronics, 2.14 Control Systems), **Stanford** (CS223A Introduction to Robotics), **ETH Zürich** (151-0851-00L Robot Dynamics), **UC Berkeley** (ME102B Mechatronics Design), và **TU München (TUM)**. Đồng thời, toàn bộ kiến thức được ánh xạ trực tiếp vào hệ thống đào tạo nghề kép CHLB Đức theo chuẩn **DIHK / AHK** (*Rahmenlehrplan für den Ausbildungsberuf Mechatroniker*), gồm các khung năng lực:
- **Lernfeld 1 (LF1)**: *Fertigen von Bauelementen mit handgeführten Werkzeugen* (Chế tạo chi tiết cơ khí, dung sai lắp ghép DIN ISO 286, cặp động học).
- **Lernfeld 2 (LF2)**: *Herstellen von einfachen Baugruppen* (Chế tạo cụm kết cấu, bộ truyền bánh răng, trục-mayơ, khớp nối).
- **Lernfeld 7 (LF7)**: *Installieren und Inbetriebnehmen von mechatronischen Teilsystemen* (Lắp đặt và vận hành hệ thống truyền động cơ điện, khí nén và thủy lực DIN ISO 1219).

---

## 1. Standardized Syllabus Breakdown (Đề cương chuẩn hóa 12 tuần chuyên sâu)

### Module 01: Spatial Descriptions & Rigid Body Kinematics (Mô tả không gian & Động học vật rắn)
- **Mã môn tham chiếu**: Stanford CS223A (Tuần 1), ETH Zürich 151-0851-00L (Bài 1–2).
- **Khung năng lực Đức**: DIHK LF1 & LF2 — Xác định tọa độ vị trí và phương hướng trong gia công và định vị robot (*Koordinatensysteme und Lagebeschreibung*).
- **Nội dung lý thuyết (First Principles)**:
  - Biểu diễn vị trí của điểm trong không gian bằng vector vị trí $p \in \mathbb{R}^3$.
  - Biểu diễn định hướng thông qua ma trận quay trực giao đặc biệt $R \in SO(3)$ (Special Orthogonal Group). Nhóm $SO(3)$ có các tính chất đại số cơ bản: $R^T R = I$ và $\det(R) = +1$.
  - Biểu diễn hướng bằng góc Euler (Z-Y-X yaw-pitch-roll), vector quay / trục-góc (*Axis-Angle representation*), và số phức bốn chiều đơn vị (*Unit Quaternions* $q = [\eta, \epsilon^T]^T$ với $\eta = \cos(\theta/2)$, $\epsilon = u \sin(\theta/2)$) nhằm tránh hiện tượng khóa trục (*Gimbal Lock* / *Kardanische Blockade*).
  - Ma trận biến đổi thuần nhất $T \in SE(3)$ (Special Euclidean Group) kết hợp cả tịnh tiến và quay:
    $$T = \begin{bmatrix} R & p \\ 0_{1\times 3} & 1 \end{bmatrix} \in \mathbb{R}^{4\times 4}$$
    với ma trận nghịch đảo giải tích được tính trực tiếp mà không cần đảo ma trận tổng quát:
    $$T^{-1} = \begin{bmatrix} R^T & -R^T p \\ 0_{1\times 3} & 1 \end{bmatrix}$$
- **Bản chất vật lý & Ứng dụng**: Phép chuyển đổi hệ tọa độ gắn trên phôi (*Tool Center Point - TCP*) về hệ tọa độ gốc cơ sở (*Base Frame / Basiskoordinatensystem*) của cánh tay robot công nghiệp.

### Module 02: Manipulator Kinematics & Denavit-Hartenberg (DH) Convention (Quy ước Denavit-Hartenberg)
- **Mã môn tham chiếu**: Stanford CS223A (Tuần 2), MIT 2.737, UC Berkeley ME102B.
- **Khung năng lực Đức**: DIHK LF2 & LF7 — Thiết lập chuỗi động học của tay máy nhiều khâu (*Kinematische Kette von Mehrkörpersystemen*).
- **Nội dung lý thuyết (First Principles)**:
  - Chuỗi động học mở (*Open Kinematic Chain*) gồm $n$ khâu nối tiếp nhau bởi các khớp quay (*Revolute Joint / Drehgelenk*) hoặc khớp tịnh tiến (*Prismatic Joint / Schubgelenk*).
  - Quy ước tham số Denavit-Hartenberg chuẩn (*Standard DH*) và sửa đổi (*Modified DH / Craig's convention*). Mỗi khâu $i$ được định nghĩa duy nhất bằng 4 tham số hình học:
    1. Độ dài khâu $a_i$ (*Link length*): Khoảng cách dọc theo trục $x_i$ giữa trục $z_{i-1}$ và $z_i$.
    2. Góc xoắn khâu $\alpha_i$ (*Link twist*): Góc quay quanh trục $x_i$ từ $z_{i-1}$ đến $z_i$.
    3. Khoảng dịch chuyển khớp $d_i$ (*Link offset*): Khoảng cách dọc theo trục $z_{i-1}$ từ $x_{i-1}$ đến $x_i$ (biến số đối với khớp tịnh tiến).
    4. Góc khớp $\theta_i$ (*Joint angle*): Góc quay quanh trục $z_{i-1}$ từ $x_{i-1}$ đến $x_i$ (biến số đối với khớp quay).
  - Ma trận biến đổi đồng nhất từng khâu:
    $$A_i = T_i^{i-1} = \begin{bmatrix} \cos\theta_i & -\sin\theta_i \cos\alpha_i & \sin\theta_i \sin\alpha_i & a_i \cos\theta_i \\ \sin\theta_i & \cos\theta_i \cos\alpha_i & -\sin\theta_i \sin\alpha_i & a_i \sin\theta_i \\ 0 & \sin\alpha_i & \cos\alpha_i & d_i \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
  - Động học thuận toàn cục (*Global Forward Kinematics*):
    $$T_n^0(q) = A_1(q_1) A_2(q_2) \dots A_n(q_n)$$
- **Bản chất vật lý & Ứng dụng**: Xác định vị trí/tư thế tuyệt đối của bàn kẹp (*Endeffektor*) dựa trên các giá trị đọc được từ cảm biến góc quay (*Encoder / Drehgeber*) tại từng trục động cơ.

### Module 03: Inverse Kinematics (IK) & Solvability (Động học nghịch & Khả năng giải)
- **Mã môn tham chiếu**: Stanford CS223A (Tuần 3), ETH Zürich 151-0851-00L (Bài 3).
- **Khung năng lực Đức**: DIHK LF2 & LF7 — Lập trình quỹ đạo điểm-đến-điểm (*Punkt-zu-Punkt Steuerung - PTP*) trong dây chuyền sản xuất tự động.
- **Nội dung lý thuyết (First Principles)**:
  - Bài toán động học nghịch: Cho trước ma trận biến đổi mong muốn $T_{des} \in SE(3)$, tìm tập nghiệm góc khớp $q = [q_1, q_2, \dots, q_n]^T$ thỏa mãn $T_n^0(q) = T_{des}$.
  - Điều kiện tồn tại nghiệm giải tích (*Closed-form Solvability*): Tiêu chuẩn Pieper (*Pieper's Criterion*) cho robot 6-DOF có ba trục khớp liên tiếp giao nhau tại một điểm (cổ tay hình cầu — *Spherical Wrist*), cho phép tách bài toán thành giải vị trí tâm cổ tay (*Wrist Center*) trước, sau đó giải định hướng bằng phép quay Euler $ZYZ$.
  - Phương pháp giải tích hình học (*Geometric Method*) cho tay máy phẳng 2-DOF:
    $$\cos(q_2) = \frac{x^2 + y^2 - l_1^2 - l_2^2}{2 l_1 l_2}$$
    $$\sin(q_2) = \pm \sqrt{1 - \cos^2(q_2)} \implies q_2 = \text{atan2}(\sin(q_2), \cos(q_2))$$
    $$q_1 = \text{atan2}(y, x) - \text{atan2}(l_2 \sin(q_2), l_1 + l_2 \cos(q_2))$$
    Dấu $\pm$ tương ứng với hai cấu hình hình học: khuỷu tay hướng lên (*Elbow-Up*) và khuỷu tay hướng xuống (*Elbow-Down*).
  - Phương pháp số (*Numerical IK*) bằng thuật toán Damped Least Squares (Levenberg-Marquardt):
    $$\Delta q = J^T (J J^T + \lambda^2 I)^{-1} e$$
    với $\lambda > 0$ là hệ số suy giảm (*Damping Factor*) giúp thuật toán ổn định vượt qua lân cận các điểm kỳ dị.
- **Bản chất vật lý & Ứng dụng**: Cho phép người vận hành ra lệnh robot di chuyển theo hệ tọa độ Đề-các ($X, Y, Z$) trong khi bộ điều khiển cấp xung vị trí tương ứng tới từng driver động cơ servo.

### Module 04: Differential Kinematics & Manipulator Jacobian (Động học vi phân & Ma trận Jacobian)
- **Mã môn tham chiếu**: Stanford CS223A (Tuần 4), MIT 2.14, ETH Zürich 151-0851-00L (Bài 4).
- **Khung năng lực Đức**: DIHK LF7 — Điều khiển vận tốc tiếp tuyến và tốc độ cắt gọt trên đường biên liên tục (*Continuous Path - CP Steuerung*).
- **Nội dung lý thuyết (First Principles)**:
  - Vận tốc của khâu công tác cuối bao gồm vận tốc dài $v_e = \dot{p}_e$ và vận tốc góc $\omega_e$. Vector vận tốc không gian thao tác $\dot{x}_e = [v_e^T, \omega_e^T]^T \in \mathbb{R}^6$.
  - Ma trận Geometric Jacobian $J(q) \in \mathbb{R}^{6\times n}$ thiết lập mối liên hệ tuyến tính cục bộ giữa vận tốc góc khớp $\dot{q}$ và vận tốc khâu tác động cuối $\dot{x}_e$:
    $$\dot{x}_e = J(q) \dot{q} = \begin{bmatrix} J_v(q) \\ J_\omega(q) \end{bmatrix} \dot{q}$$
  - Công thức xác định từng cột thứ $i$ của ma trận Jacobian:
    - Với khớp quay (*Revolute Joint*):
      $$J_{v,i} = z_{i-1} \times (p_e - p_{i-1}), \quad J_{\omega,i} = z_{i-1}$$
    - Với khớp tịnh tiến (*Prismatic Joint*):
      $$J_{v,i} = z_{i-1}, \quad J_{\omega,i} = 0_{3\times 1}$$
    trong đó $z_{i-1}$ là vector đơn vị trục quay/tịnh tiến của khớp $i$, $p_{i-1}$ là gốc tọa độ của khâu $i-1$, và $p_e$ là vị trí của khâu tác động cuối.
- **Bản chất vật lý & Ứng dụng**: Là cơ sở để ánh xạ sai số vị trí thành lệnh vận tốc khớp trong bộ điều khiển vòng kín; tính toán năng lượng động học và lực tương tác với môi trường gia công.

### Module 05: Singularities, Workspace & Manipulability Analysis (Điểm kỳ dị, Không gian làm việc & Khả năng thao tác)
- **Mã môn tham chiếu**: Stanford CS223A (Tuần 5), ETH Zürich 151-0851-00L (Bài 5).
- **Khung năng lực Đức**: DIHK LF2 & LF7 — An toàn vận hành, phòng ngừa quá tải động cơ và mất kiểm soát cơ học (*Vermeidung von Singularitäten und mechanischer Überlastung*).
- **Nội dung lý thuyết (First Principles)**:
  - Điểm kỳ dị động học (*Kinematic Singularity / Kinematische Singularität*) xuất hiện khi ma trận Jacobian $J(q)$ suy biến (giảm hạng):
    $$\text{rank}(J(q)) < \min(6, n) \iff \det(J(q)) = 0 \quad (\text{với } n = 6)$$
  - Phân loại kỳ dị:
    - Kỳ dị biên (*Boundary Singularity*): Khi robot vươn hết tầm hoặc gập sát vào gốc; khâu tác động cuối không thể chuyển động ra ngoài không gian làm việc.
    - Kỳ dị trong (*Interior Singularity*): Khi hai hoặc nhiều trục quay thẳng hàng (ví dụ: khớp 4 và khớp 6 của robot 6 trục thẳng hàng khi khớp 5 bằng 0), làm mất 1 bậc tự do tức thời.
  - Hậu quả vật lý: Để tạo ra vận tốc hữu hạn của khâu tác động cuối theo phương bị suy biến, vận tốc khớp $\dot{q} = J^{-1} \dot{x}_e$ phải tiến tới vô cùng ($\dot{q} \to \infty$), gây quá tải dòng điện và ngắt an toàn (*Emergency Stop*).
  - Thước đo khả năng thao tác Yoshikawa (*Yoshikawa Manipulability Measure*):
    $$w(q) = \sqrt{\det(J(q) J^T(q))}$$
    Với tay máy vuông $6\times 6$, $w(q) = |\det(J(q))|$. Tại điểm kỳ dị, $w(q) = 0$.
  - Ellipsoid vận tốc (*Velocity Ellipsoid*): Tập hợp các vận tốc $\dot{x}_e$ tạo bởi vector vận tốc khớp chuẩn hóa $\|\dot{q}\|_2 \le 1$:
    $$\dot{x}_e^T (J J^T)^{-1} \dot{x}_e \le 1$$
- **Bản chất vật lý & Ứng dụng**: Tối ưu hóa quỹ đạo chuyển động gia công sao cho cấu hình khớp luôn duy trì chỉ số thao tác $w(q)$ cách xa ngưỡng 0, bảo vệ động cơ và cơ cấu giảm tốc.

### Module 06: Static Forces & Duality Principles (Lực tĩnh học & Nguyên lý đối ngẫu Vận tốc - Lực)
- **Mã môn tham chiếu**: Stanford CS223A (Tuần 6), MIT 2.737, UC Berkeley ME102B.
- **Khung năng lực Đức**: DIHK LF1 & LF2 — Phân tích tải trọng cơ học, lực kẹp gắp phôi và độ bền chi tiết (*Kräfteanalyse und Spannungsberechnung*).
- **Nội dung lý thuyết (First Principles)**:
  - Theo nguyên lý công ảo (*Principle of Virtual Work / Prinzip der virtuellen Arbeit*), công ảo thực hiện bởi mô-men khớp $\tau$ phải cân bằng với công ảo thực hiện bởi lực và mô-men tương tác tại khâu tác động cuối $F_e = [f_e^T, \mu_e^T]^T$:
    $$\delta W = \tau^T \delta q - F_e^T \delta x_e = 0$$
  - Vì $\delta x_e = J(q) \delta q$, ta có:
    $$\tau^T \delta q - F_e^T J(q) \delta q = 0 \implies \tau = J^T(q) F_e$$
  - Quan hệ đối ngẫu hình học: Ma trận chuyển vị Jacobian $J^T(q)$ ánh xạ trực tiếp vector lực/mô-men ngoài tác dụng lên đầu gắp thành mô-men cần thiết tại các trục khớp động cơ.
  - Đối ngẫu Ellipsoid: Trục dài nhất của Ellipsoid vận tốc ứng với phương robot di chuyển nhanh nhất, nhưng lại là trục ngắn nhất của Ellipsoid lực (phương sinh lực yếu nhất).
- **Bản chất vật lý & Ứng dụng**: Xác định yêu cầu mô-men xoắn cực đại (*Peak Torque*) của động cơ khi robot thực hiện thao tác ép khuôn, siết bu-lông hoặc nâng phôi tải trọng lớn.

### Module 07: Rigid Body Dynamics & Euler-Lagrange Formulation (Động lực học vật rắn & Phương trình Euler-Lagrange)
- **Mã môn tham chiếu**: MIT 2.14, ETH Zürich 151-0851-00L (Bài 5–6), Stanford CS223A (Tuần 7).
- **Khung năng lực Đức**: DIHK LF7 — Mô hình hóa động học và động lực học phục vụ điều khiển chuyển động gia tốc cao (*Modellierung dynamischer Systeme für die Regelung*).
- **Nội dung lý thuyết (First Principles)**:
  - Hàm Lagrange $L(q, \dot{q}) = K(q, \dot{q}) - P(q)$ là hiệu số giữa tổng động năng $K$ và tổng thế năng trọng trường $P$ của toàn bộ cơ cấu.
  - Động năng toàn phần dạng toàn phương:
    $$K(q, \dot{q}) = \frac{1}{2} \dot{q}^T M(q) \dot{q} = \frac{1}{2} \sum_{i=1}^n \left( m_i v_{c,i}^T v_{c,i} + \omega_i^T I_i \omega_i \right)$$
    với $M(q) \in \mathbb{R}^{n\times n}$ là ma trận quán tính khối lượng (*Mass / Inertia Matrix*).
  - Phương trình Euler-Lagrange:
    $$\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right) - \frac{\partial L}{\partial q} = \tau$$
  - Phương trình vi phân chuyển động chuẩn tắc:
    $$M(q)\ddot{q} + C(q, \dot{q})\dot{q} + G(q) = \tau$$
    trong đó:
    - $M(q)$ là ma trận đối xứng và xác định dương thực sự ($M(q) = M^T(q) > 0, \forall q$).
    - $C(q, \dot{q})\dot{q}$ là vector lực Coriolis và quán tính ly tâm, với các phần tử tính qua ký hiệu Christoffel loại 1:
      $$c_{ijk} = \frac{1}{2}\left( \frac{\partial M_{ij}}{\partial q_k} + \frac{\partial M_{ik}}{\partial q_j} - \frac{\partial M_{jk}}{\partial q_i} \right)$$
    - $G(q) = \frac{\partial P(q)}{\partial q}$ là vector mô-men trọng trường tác dụng lên các khớp.
  - Tính chất phản đối xứng then chốt (*Skew-symmetry Property*): Ma trận $N(q, \dot{q}) = \dot{M}(q) - 2C(q, \dot{q})$ là ma trận phản đối xứng, tức là:
    $$x^T \left( \dot{M}(q) - 2C(q, \dot{q}) \right) x = 0, \quad \forall x \in \mathbb{R}^n$$
    Tính chất này đảm bảo định luật bảo toàn cơ năng trong hệ thống không có ma sát, và là nền tảng chứng minh tính ổn định Lyapunov của các bộ điều khiển bù động lực học (*Computed Torque Control*).
- **Bản chất vật lý & Ứng dụng**: Tính toán mô-men động học phi tuyến theo thời gian thực nhằm bù lực quán tính khi robot chuyển động ở gia tốc cao ($> 2G$).

### Module 08: Recursive Newton-Euler Dynamics & Spatial Vectors (Thuật toán Newton-Euler đệ quy)
- **Mã môn tham chiếu**: ETH Zürich 151-0851-00L (Bài 7), Stanford CS223A, TU München.
- **Khung năng lực Đức**: DIHK LF7 & LF9 — Thuật toán tính toán số thời gian thực trên vi điều khiển công nghiệp (*Echtzeit-Berechnungsalgorithmen für Industrie-Controller*).
- **Nội dung lý thuyết (First Principles)**:
  - Phương pháp Euler-Lagrange có độ phức tạp tính toán $O(n^4)$ khi khai triển biểu thức giải tích, không phù hợp cho tay máy nhiều bậc tự do ($n \ge 6$).
  - Thuật toán Newton-Euler đệ quy (Luh-Walker-Paul Algorithm) đạt độ phức tạp tuyến tính $O(n)$:
    - **Bước quét tiến (Forward Recursion, $i = 1 \to n$)**: Truyền vận tốc góc $\omega_i$, gia tốc góc $\dot{\omega}_i$, và gia tốc dài tuyến tính $\dot{v}_{c,i}$ từ khâu gốc lên khâu ngọn:
      $$\omega_i = R_i^{i-1} \omega_{i-1} + z_0 \dot{q}_i$$
      $$\dot{\omega}_i = R_i^{i-1} \dot{\omega}_{i-1} + R_i^{i-1} \omega_{i-1} \times z_0 \dot{q}_i + z_0 \ddot{q}_i$$
      $$\dot{v}_i = R_i^{i-1} \dot{v}_{i-1} + \dot{\omega}_i \times p_i + \omega_i \times (\omega_i \times p_i)$$
      $$\dot{v}_{c,i} = \dot{v}_i + \dot{\omega}_i \times r_{c,i} + \omega_i \times (\omega_i \times r_{c,i})$$
    - **Bước quét lùi (Backward Recursion, $i = n \to 1$)**: Tính lực quán tính D'Alembert $F_i = m_i \dot{v}_{c,i}$ và mô-men quán tính Euler $N_i = I_i \dot{\omega}_i + \omega_i \times (I_i \omega_i)$; sau đó cân bằng lực $f_i$ và mô-men $n_i$ truyền qua các khớp:
      $$f_i = R_{i+1}^i f_{i+1} + F_i$$
      $$n_i = R_{i+1}^i n_{i+1} + p_i \times f_i + r_{c,i} \times F_i + N_i$$
      $$\tau_i = n_i^T z_0 + b_i \dot{q}_i$$
- **Bản chất vật lý & Ứng dụng**: Cho phép chu trình điều khiển vòng kín chạy ở tần số cao ($1\,\text{kHz}$) trên CPU máy tính công nghiệp nhúng x86/ARM.

### Module 09: Actuator Fundamentals: DC & Brushless DC (BLDC) Motors (Nguyên lý truyền động Động cơ DC & BLDC)
- **Mã môn tham chiếu**: MIT 2.737 (Bài giảng 4–6), UC Berkeley ME102B, TU München.
- **Khung năng lực Đức**: DIHK LF3 — Lắp đặt, đấu nối và phân tích đặc tính động cơ điện (*Elektrische Antriebe, Gleichstrommotoren und bürstenlose Servomotoren*).
- **Nội dung lý thuyết (First Principles)**:
  - Động cơ DC nam châm vĩnh cửu (*PMDC Motor*): Nguyên lý lực Lorentz $F = I (L \times B)$ sinh ra mô-men quay $\tau_m = K_t i_a$, trong đó $K_t$ là hằng số mô-men (*Torque Constant*, đơn vị $\text{N}\cdot\text{m/A}$).
  - Khi rotor quay cắt từ trường, suất điện động cảm ứng (*Back-EMF*) sinh ra: $e_b = K_b \omega_m$, trong đó $K_b$ là hằng số phản điện động (*Back-EMF Constant*, đơn vị $\text{V}/(\text{rad/s})$).
  - Định luật bảo toàn công suất điện - cơ lý tưởng: $P_{elec} = e_b i_a = (K_b \omega_m) i_a = P_{mech} = \tau_m \omega_m = (K_t i_a) \omega_m \implies K_t \equiv K_b$ trong hệ đơn vị SI tiêu chuẩn.
  - Phương trình vi phân mạch phần ứng:
    $$V_a(t) = R_a i_a(t) + L_a \frac{d i_a(t)}{dt} + K_b \omega_m(t)$$
  - Phương trình cân bằng mô-men cơ học:
    $$J_m \frac{d\omega_m(t)}{dt} + B_m \omega_m(t) = \tau_m(t) - \tau_L(t) = K_t i_a(t) - \tau_L(t)$$
  - Hàm truyền từ điện áp phần ứng $V_a(s)$ đến tốc độ góc rotor $\Omega_m(s)$ khi không tải ($\tau_L = 0$):
    $$G(s) = \frac{\Omega_m(s)}{V_a(s)} = \frac{K_t}{(J_m s + B_m)(L_a s + R_a) + K_t K_b} = \frac{K_t}{J_m L_a s^2 + (J_m R_a + B_m L_a)s + (B_m R_a + K_t K_b)}$$
  - Vì hằng số thời gian điện $\tau_e = L_a / R_a$ nhỏ hơn rất nhiều so với hằng số thời gian cơ $\tau_m = J_m R_a / (K_t K_b)$, hàm truyền có thể xấp xỉ quán tính bậc 1:
    $$G(s) \approx \frac{K_m}{\tau_{eff} s + 1}$$
- **Bản chất vật lý & Ứng dụng**: Lựa chọn điểm làm việc danh định (*Nominal Operating Point*), đường cong đặc tính cơ Tốc độ - Mô-men (*Torque-Speed Curve*), và giới hạn dòng điện đỉnh an toàn cho driver.

### Module 10: Mechanical Transmissions, Gearboxes & Reflected Inertia (Hộp giảm tốc, Bộ truyền cơ khí & Quán tính tương đương)
- **Mã môn tham chiếu**: MIT 2.737, UC Berkeley ME102B.
- **Khung năng lực Đức**: DIHK LF2 — Lắp ráp bộ truyền động cơ khí, căn chỉnh khe hở ăn khớp bánh răng (*Mechanische Getriebe, Passungen und Zahnflankenspiel*).
- **Nội dung lý thuyết (First Principles)**:
  - Hộp giảm tốc lý tưởng có tỉ số truyền $N = \omega_{in} / \omega_{out} > 1$. Vận tốc góc giảm $N$ lần, mô-men tải tăng $N$ lần kèm hiệu suất truyền động $\eta \le 1$:
    $$\omega_{out} = \frac{\omega_{in}}{N}, \quad \tau_{out} = \eta \cdot N \cdot \tau_{in}$$
  - Quán tính khối lượng tương đương phản xạ về trục động cơ (*Reflected Inertia*): Năng lượng động học của tải $J_L$ khi quy đổi về trục động cơ:
    $$K_L = \frac{1}{2} J_L \omega_{out}^2 = \frac{1}{2} J_L \left(\frac{\omega_{in}}{N}\right)^2 = \frac{1}{2} \left(\frac{J_L}{N^2}\right) \omega_{in}^2$$
    Suy ra quán tính tương đương toàn phần đặt lên trục rotor động cơ:
    $$J_{eff} = J_m + \frac{J_L}{N^2}$$
    Mô-men ma sát và cản phản xạ:
    $$B_{eff} = B_m + \frac{B_L}{N^2}$$
  - Định luật phối hợp quán tính tối ưu (*Inertia Matching Theorem*): Để gia tốc tải lớn nhất với một mô-men động cơ hữu hạn cho trước, tỉ số truyền tối ưu là:
    $$N_{opt} = \sqrt{\frac{J_L}{J_m}}$$
  - Các loại hộp giảm tốc chuyên dụng trong robot:
    - Bánh răng sóng (*Harmonic Drive / Strain Wave Gear*): Tỉ số truyền lớn ($50:1$ đến $160:1$) trong thể tích nhỏ, độ rơ bằng không (*Zero-Backlash*), nhưng độ cứng vững xoắn hữu hạn (*Torsional Flexibility*).
    - Hộp số hành tinh chính xác (*Precision Planetary Gearbox / Planetengetriebe*): Hiệu suất cao ($> 95\%$), tải trọng va đập tốt, độ rơ thấp ($< 1-3\,\text{arcmin}$).
    - Bánh răng xích-lô-it (*Cycloidal Drive*): Khả năng chịu quá tải va đập cực lớn, dùng cho các trục gốc robot tải nặng.
- **Bản chất vật lý & Ứng dụng**: Thiết kế khớp robot công nghiệp đảm bảo không bị dao động cộng hưởng cơ học do độ rơ (*Backlash / Zahnflankenspiel*) gây ra.

### Module 11: Fluid Power Actuation: Pneumatics & Hydraulics (Truyền động Thủy lực & Khí nén công nghiệp DIN ISO 1219)
- **Mã môn tham chiếu**: DIHK LF7 (Khung năng lực cốt lõi), MIT 2.14.
- **Khung năng lực Đức**: DIHK LF7 — Lắp đặt, hiệu chuẩn và thử nghiệm hệ thống khí nén và thủy lực (*Pneumatische und hydraulische Steuerungen nach DIN ISO 1219*).
- **Nội dung lý thuyết (First Principles)**:
  - Khí nén (*Pneumatik*): Sử dụng không khí nén áp suất làm việc tiêu chuẩn $p = 6\,\text{bar} = 0.6\,\text{MPa}$. Không khí có tính nén được cao (*High Compressibility*), mô hình dòng chảy qua tiết diện van tuân theo phương trình xả khí đẳng nhiệt/đoạn nhiệt:
    $$\dot{m} = C \cdot p_1 \cdot \rho_0 \sqrt{\frac{T_0}{T_1}} \quad (\text{khi dòng chảy nghẽn/tới hạn } p_2/p_1 \le b)$$
  - Lực sinh ra bởi xi lanh khí nén tác động kép (*Doppelwirkender Zylinder*):
    $$F_{th,forward} = p \cdot \frac{\pi D^2}{4}, \quad F_{th,return} = p \cdot \frac{\pi (D^2 - d^2)}{4}$$
    Lực hiệu dụng thực tế: $F_{eff} = \eta_{mech} \cdot F_{th} - F_{spring}$, với $\eta_{mech} \approx 0.85 - 0.95$ do ma sát gioăng làm kín.
  - Thủy lực (*Hydraulik*): Sử dụng dầu khoáng áp suất cao ($p = 50 - 315\,\text{bar}$). Dầu thủy lực hầu như không nén được, đặc trưng bởi mô-đun đàn hồi thể tích (*Bulk Modulus*) $\beta \approx 1.5 \times 10^9\,\text{Pa}$:
    $$\Delta p = \beta \frac{\Delta V}{V_0}$$
  - Phương trình dòng chảy qua khe hở van tỉ lệ (*Proportional Servo Valve*):
    $$Q = C_d A_v \sqrt{\frac{2 \Delta p}{\rho}}$$
  - Phương trình vi phân áp suất trong buồng xi lanh thủy lực:
    $$\frac{V(x)}{\beta} \frac{d p_1}{dt} = Q_1 - A_1 \frac{dx}{dt} - C_{leak}(p_1 - p_2)$$
- **Bản chất vật lý & Ứng dụng**: Khí nén dùng cho chuyển động nhanh kẹp nhả linh kiện đơn giản; thủy lực dùng cho các cơ cấu nâng tải trọng nặng hàng chục tấn trong máy ép và cánh tay robot công nghiệp nặng.

### Module 12: Trajectory Generation & Motion Profiling (Quy hoạch quỹ đạo chuyển động)
- **Mã môn tham chiếu**: Stanford CS223A (Tuần 8), ETH Zürich 151-0851-00L (Bài 9), TU München.
- **Khung năng lực Đức**: DIHK LF7 — Lập trình điều khiển nội suy tọa độ robot (*Bahnplanung und Bewegungsprofile*).
- **Nội dung lý thuyết (First Principles)**:
  - Quy hoạch quỹ đạo trong không gian khớp (*Joint-Space Trajectory*) vs trong không gian thao tác (*Cartesian-Space Trajectory*).
  - Đa thức bậc 3 (*Cubic Polynomial Trajectory*): Thỏa mãn điều kiện biên vị trí và vận tốc tại $t_0$ và $t_f$:
    $$q(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3$$
    với gia tốc biến thiên tuyến tính, đạo hàm gia tốc giật (*Jerk* $j(t) = \dddot{q}(t)$) có giá trị không liên tục tại các điểm mút.
  - Đa thức bậc 5 (*Quintic Polynomial Trajectory*): Bổ sung điều kiện biên gia tốc ban đầu và kết thúc bằng 0 ($\ddot{q}(t_0) = \ddot{q}(t_f) = 0$):
    $$q(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5$$
    đảm bảo biên dạng gia tốc trơn tru, triệt tiêu xung giật kích thích dao động cơ học.
  - Biên dạng vận tốc hình thang (*Trapezoidal / Bang-Coast-Bang Velocity Profile*): Chia hành trình thành 3 pha: tăng tốc không đổi ($a = a_{max}$), chuyển động đều ($v = v_{max}$), và giảm tốc không đổi ($a = -a_{max}$).
  - Biên dạng S-Curve (*Jerk-Limited Motion Profile*): Giới hạn độ giật cực đại $|j(t)| \le j_{max}$ gồm 7 giai đoạn chuyển động, loại bỏ hoàn toàn bước nhảy gia tốc tức thời, bảo vệ hộp giảm tốc và kéo dài tuổi thọ cơ cấu chấp hành.
- **Bản chất vật lý & Ứng dụng**: Tối ưu hóa chu kỳ làm việc (*Cycle Time*) của thao tác gắp đặt (*Pick-and-Place*) trong nhà máy tự động mà không làm rung lắc đầu gắp.

---

## 2. Academic Reading List (Danh mục tài liệu học thuật tiêu chuẩn)

Dưới đây là danh mục các giáo trình và công trình khoa học kinh điển định hình toàn bộ nền tảng động học, động lực học và điều khiển robot hiện đại:

1. **Craig, John J.** (2018). *Introduction to Robotics: Mechanics and Control* (4th ed.). Pearson Education.
   - *Phạm vi nghiên cứu*: Chương 2 (Mô tả không gian và biến đổi thuần nhất), Chương 3 (Động học thuận và quy ước DH), Chương 4 (Động học nghịch giải tích), Chương 5 (Jacobian: Vận tốc và lực tĩnh học), Chương 6 (Động lực học tay máy Euler-Lagrange), Chương 7 (Quy hoạch quỹ đạo chuyển động).
2. **Spong, Mark W., Hutchinson, Seth, & Vidyasagar, M.** (2020). *Robot Modeling and Control* (2nd ed.). John Wiley & Sons.
   - *Phạm vi nghiên cứu*: Chương 3 (Forward & Inverse Kinematics), Chương 4 (Differential Kinematics & The Manipulator Jacobian), Chương 6 (Dynamics: Euler-Lagrange Formulation & Skew-Symmetry Properties), Chương 7 (Independent Joint Control and Actuator Dynamics).
3. **Siciliano, Bruno, Sciavicco, Lorenzo, Villani, Luigi, & Oriolo, Giuseppe** (2009). *Robotics: Modelling, Planning and Control*. Springer-Verlag.
   - *Phạm vi nghiên cứu*: Chương 2 (Kinematics of Robot Manipulators), Chương 3 (Differential Kinematics and Statics), Chương 7 (Rigid Body Dynamics & Recursive Algorithms), Chương 8 (Motion Planning & Trajectory Generation).
4. **Featherstone, Roy** (2008). *Rigid Body Dynamics Algorithms*. Springer Science & Business Media.
   - *Phạm vi nghiên cứu*: Chương 3 (Spatial Motion Vectors), Chương 4 (Spatial Inertia & Transformations), Chương 5 (Recursive Newton-Euler Algorithms & Articulated-Body Inertia).
5. **Denavit, Jacques, & Hartenberg, Richard S.** (1955). "A kinematic notation for lower-pair mechanisms based on matrices." *ASME Journal of Applied Mechanics*, 22(2), 215–221.
   - *Giá trị học thuật*: Bài báo gốc thiết lập phương pháp ma trận đồng nhất 4 tham số biểu diễn chuyển động tương đối của các khâu cơ học.
6. **Luh, J. Y. S., Walker, Michael W., & Paul, Richard P. C.** (1980). "On-line computational scheme for mechanical manipulators." *ASME Journal of Dynamic Systems, Measurement, and Control*, 102(2), 69–76.
   - *Giá trị học thuật*: Công bố thuật toán Newton-Euler đệ quy thời gian thực $O(n)$ đầu tiên cho tay máy công nghiệp.
7. **Yoshikawa, Tsuneo** (1985). "Manipulability of robotic mechanisms." *The International Journal of Robotics Research*, 4(2), 3–9.
   - *Giá trị học thuật*: Khởi xướng khái niệm định lượng khả năng thao tác và phân tích ellipsoid vận tốc/lực cho robot.

---

## 3. Practical Labs & Simulation Projects (Bài tập thực hành & Project mô phỏng)

### Lab 01: Mô phỏng Động học & Động lực học Thuận Tay máy phẳng 2-DOF
- **Mã file thực thi**: `labs/lab01_kinematics.py`
- **Mục tiêu kỹ thuật**:
  1. Lập trình tính toán Động học thuận (FK) và Động học nghịch (IK) giải tích cho tay máy 2 khâu phẳng ($l_1 = 1.0\,\text{m}, l_2 = 0.8\,\text{m}$).
  2. Triển khai thuật toán lựa chọn nhánh nghiệm hình học: Khuỷu tay hướng lên (*Elbow-Up*) và Khuỷu tay hướng xuống (*Elbow-Down*).
  3. Tính toán ma trận Jacobian giải tích $J(q)$, định thức $\det(J(q))$, và chỉ số khả năng thao tác Yoshikawa $w(q) = |\det(J(q))|$. Xác định cấu hình kỳ dị biên tại $q_2 = 0$.
  4. Lập trình ma trận quán tính Euler-Lagrange $M(q)$, vector Coriolis $C(q, \dot{q})\dot{q}$, và vector trọng trường $G(q)$. Kiểm tra tính xác định dương của $M(q)$.
  5. Tích phân số phương trình vi phân chuyển động phi tuyến bằng phương pháp Runge-Kutta bậc 4 (RK4) trong 1000 bước thời gian với bộ điều khiển bù trọng trường PD.
- **Tiêu chí nghiệm thu định lượng**:
  - Sai số khép vòng Động học thuận - nghịch: $\text{RMSE} < 10^{-12}\,\text{m}$.
  - Thời gian thực thi toàn bộ thuật toán trên CPU macOS: $< 50\,\text{ms}$ (Không sử dụng thư viện ngoài).
  - Trạng thái kiểm tra: Đạt chuẩn xác nhận `[PASS]` trong suite kiểm thử tự động.

### Lab 02: Thiết lập Bảng thông số DH & Phân tích Điểm kỳ dị Tay máy Không gian 3-DOF Anthropomorphic
- **Mục tiêu kỹ thuật**:
  1. Gắn các hệ tọa độ khâu theo quy ước DH chuẩn cho robot không gian 3 bậc tự do (gồm khớp quay đế xoay, khớp vai và khớp khuỷu).
  2. Lập bảng 4 tham số DH ($a_i, \alpha_i, d_i, \theta_i$) và nhân chuỗi ma trận thuần nhất $T_3^0(q)$.
  3. Lập trình biểu thức giải tích của ma trận Geometric Jacobian $J(q) \in \mathbb{R}^{3\times 3}$ đối với vận tốc dài của điểm tác động cuối.
  4. Giải phương trình giải tích $\det(J(q)) = 0$ để vẽ mặt kỳ dị trong không gian cấu hình khớp $(q_1, q_2, q_3)$.
- **Kết quả bàn giao**: Script Python độc lập xuất đồ thị dạng ASCII/số liệu biểu diễn vùng kỳ dị biên và kỳ dị trong.

### Lab 03: Tính toán Phối hợp Quán tính (Inertia Matching) Động cơ - Hộp số Harmonic & Quy hoạch Quỹ đạo S-Curve
- **Mục tiêu kỹ thuật**:
  1. Cho một cánh tay tải trọng có mô-men quán tính $J_L = 0.8\,\text{kg}\cdot\text{m}^2$, quán tính rotor động cơ servo $J_m = 1.2 \times 10^{-4}\,\text{kg}\cdot\text{m}^2$. Tính tỉ số truyền tối ưu $N_{opt} = \sqrt{J_L / J_m}$ và chọn mã hộp số bánh răng sóng Harmonic Drive thực tế ($N = 80:1$ hoặc $N = 100:1$).
  2. Lập trình thuật toán sinh quỹ đạo chuyển động S-Curve 7 đoạn với giới hạn gia tốc $a_{max} = 10\,\text{rad/s}^2$ và giới hạn giật $j_{max} = 100\,\text{rad/s}^3$.
  3. So sánh mô-men xoắn đỉnh yêu cầu giữa quỹ đạo hình thang (Trapezoidal) và quỹ đạo S-Curve khi gia tốc qua hộp số có độ cứng xoắn $K_{gear} = 14000\,\text{N}\cdot\text{m/rad}$.
- **Kết quả bàn giao**: Báo cáo số liệu phân tích độ vọt lố mô-men quán tính và giảm thiểu dao động cơ học.

---

## 4. Exact Search Queries & Bilingual Terminology Table (Từ khóa tìm kiếm & Thuật ngữ Anh-Đức-Việt)

### Precision Academic Search Queries
1. `site:ocw.mit.edu "2.737" "manipulator kinematics" "Lagrangian dynamics" filetype:pdf`
2. `site:ethz.ch "151-0851-00L" "Robot Dynamics" "Euler-Lagrange" "Jacobian" filetype:pdf`
3. `site:stanford.edu "CS223A" "Introduction to Robotics" "inverse kinematics" "Craig" filetype:pdf`
4. `"Euler-Lagrange" "manipulator dynamics" "skew-symmetric" "Coriolis matrix" filetype:pdf`
5. `"Denavit-Hartenberg" "modified DH parameters" "Craig" robotics lecture notes filetype:pdf`
6. `site:dihk.de "Mechatroniker" "Rahmenlehrplan" "Lernfeld 1" "Lernfeld 2" filetype:pdf`
7. `"Lernfeld 7" "Installieren von hydraulischen und pneumatischen Systemen" "Mechatroniker" filetype:pdf`
8. `"reflected inertia" "gear ratio" "motor sizing" "harmonic drive" robotics filetype:pdf`
9. `site:ieee.org "manipulator Jacobian" "singularity analysis" "Yoshikawa manipulability"`
10. `intitle:"Robot Dynamics and Control" Spong Vidyasagar "equations of motion"`
11. `intitle:"Introduction to Robotics" Craig "Inverse Manipulator Kinematics" filetype:pdf`
12. `github topic:robotics "forward-kinematics" "euler-lagrange" "jacobian" language:python`

### Bilingual Terminology Table (DIN 2860, ISO 8373, DIN ISO 1219)

| STT | English Term | German Fachbegriff (DIN/ISO) | Tiếng Việt Chuyên Ngành | Ngữ Cảnh Kỹ Thuật & Tiêu Chuẩn Áp Dụng |
|:---:|:---|:---|:---|:---|
| 1 | Kinematics | **Kinematik** (*f.*) | Động học | Khảo sát vị trí, vận tốc và gia tốc chuyển động hình học không xét đến lực (DIN ISO 8373). |
| 2 | Dynamics | **Dynamik** (*f.*) | Động lực học | Khảo sát mối quan hệ giữa lực, mô-men và chuyển động sinh ra trong hệ nhiều vật rắn. |
| 3 | Forward Kinematics | **Vorwärtskinematik** (*f.*) | Động học thuận | Phép toán biến đổi từ tọa độ góc khớp sang tọa độ không gian làm việc của bàn kẹp ($q \to x_e$). |
| 4 | Inverse Kinematics | **Inverse Kinematik** (*f.*) | Động học nghịch | Phép toán xác định các góc khớp cần thiết để đạt tư thế mong muốn trong không gian ($x_e \to q$). |
| 5 | Manipulator Jacobian | **Jacobi-Matrix** (*f.*) | Ma trận Jacobian | Ma trận đạo hàm riêng liên hệ giữa vận tốc khớp với vận tốc dài và vận tốc góc của khâu công tác cuối. |
| 6 | Degree of Freedom (DoF) | **Freiheitsgrad** (*m.*) | Bậc tự do | Số tọa độ độc lập tối thiểu cần thiết để xác định hoàn toàn cấu hình hình học của cơ cấu (DIN 2860). |
| 7 | Joint Coordinate | **Gelenkkoordinate** (*f.*) | Tọa độ khớp | Biến số suy rộng đại diện cho góc quay (khớp bản lề) hoặc khoảng tịnh tiến của khớp robot. |
| 8 | End-Effector | **Endeffektor** (*m.*) | Khâu công tác cuối | Cơ cấu lắp ở đầu cánh tay robot để thao tác với đối tượng (tay gắp, mỏ hàn, đầu laser). |
| 9 | Torque | **Drehmoment** (*n.*) | Mô-men xoắn | Đại lượng vật lý đo xu hướng làm quay vật thể quanh một trục, đơn vị chuẩn $\text{N}\cdot\text{m}$. |
| 10 | Moment of Inertia | **Massenträgheitsmoment** (*n.*) | Mô-men quán tính khối lượng | Đại lượng đo mức độ cản trở biến thiên vận tốc góc của vật thể quay ($I = \int r^2 dm$). |
| 11 | Angular Velocity | **Winkelgeschwindigkeit** (*f.*) | Vận tốc góc | Đạo hàm theo thời gian của góc quay, vector biểu thị tốc độ và trục quay ($\text{rad/s}$). |
| 12 | Kinematic Singularity | **Kinematische Singularität** (*f.*) | Điểm kỳ dị động học | Cấu hình khớp làm ma trận Jacobian giảm hạng, khiến robot mất khả năng chuyển động theo một số hướng. |
| 13 | Manipulability | **Manipulierbarkeit** (*f.*) | Khả năng thao tác | Chỉ số Yoshikawa biểu thị độ linh hoạt và khoảng cách từ cấu hình hiện tại tới điểm kỳ dị gần nhất. |
| 14 | Actuator | **Aktor** (*m.*) / **Stellglied** (*n.*) | Cơ cấu chấp hành | Thiết bị chuyển hóa năng lượng điện, khí nén hoặc thủy lực thành công cơ học. |
| 15 | Gear Ratio | **Übersetzungsverhältnis** (*n.*) | Tỉ số truyền giảm tốc | Tỉ số giữa vận tốc góc đầu vào và vận tốc góc đầu ra của bộ truyền ($N = \omega_{in} / \omega_{out}$). |
| 16 | Backlash | **Zahnflankenspiel** (*n.*) | Độ rơ ăn khớp bánh răng | Khe hở giữa các biên dạng răng ăn khớp gây ra sai số vị trí khi cơ cấu đảo chiều quay. |
| 17 | Fluid Power Actuation | **Fluidische Antriebe** (*m.pl.*) | Truyền động thủy khí | Hệ thống sử dụng năng lượng chất lỏng có áp suất hoặc khí nén để sinh lực (DIN ISO 1219). |
| 18 | Trajectory Planning | **Trajektorienplanung** (*f.*) | Quy hoạch quỹ đạo | Thiết lập quy luật thời gian cho vị trí, vận tốc và gia tốc chuyển động của các trục robot. |
