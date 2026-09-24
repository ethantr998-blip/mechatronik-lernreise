# Phân hệ 05: Robot tự hành, ROS 2 & SLAM (Autonomous Robotics, ROS 2 & SLAM)

Tài liệu chuyên sâu thuộc Hệ thống Tri thức Cơ điện tử & Robot học (*Mechatronics & Robotics Knowledge Base*), chuẩn hóa theo chương trình đào tạo của **ETH Zürich (151-0854-00L)**, **Stanford University (CS237A)**, **MIT (16.410/16.411)** và tiêu chuẩn nghề nghiệp **CHLB Đức (DIHK / AHK - Lernfeld 10 & 12)**. Được biên soạn theo nguyên lý đệ nhất (*First Principles*), phục vụ đào tạo kỹ sư Cơ điện tử làm việc tại CHLB Đức.

---

## Phần 1: Đề cương chuẩn hóa (Standardized Syllabus Breakdown)

Cấu trúc đề cương 12 module học thuật toàn diện, tích hợp cơ học phi toàn định (*non-holonomic mechanics*), lý thuyết ước lượng xác suất (*probabilistic state estimation*), định vị và lập bản đồ đồng thời (*SLAM*), hệ điều hành robot thế hệ mới (*ROS 2 Humble / Iron*), và quy hoạch quỹ đạo tối ưu (*asymptotically optimal motion planning*).

### Module 01: Động học Robot di động & Cơ cấu truyền động (Mobile Robot Kinematics & Locomotion)
- **Đại học tham chiếu**: ETH Zürich (151-0854-00L: Autonomous Mobile Robots), Stanford University (CS237A: Principles of Robot Autonomy I).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 (*Planen und Realisieren mechatronischer Systeme* - Fahrerlose Transportsysteme / FTS).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Phân loại cơ cấu di động: Bánh vi sai (*differential drive* / *Differentialantrieb*), lái kiểu Ackermann (*Ackermann-Lenkung*), bánh xe đa hướng Mecanum (*Mecanum-Räder / omnidirektionale Antriebe*), và hệ thống bánh xích (*Kettenantrieb*).
  - Ràng buộc chuyển động phi toàn định (*non-holonomic constraints* / *nichtholonome Bewegungsbeschränkungen*): Robot không thể chuyển động tức thời theo phương ngang trục bánh xe ($\dot{y} \cos\theta - \dot{x} \sin\theta = 0$). Vận tốc ngang tức thời luôn bằng 0 do ma sát bám (*pure rolling without slipping*).
  - Tâm quay tức thời (*Instantaneous Center of Curvature - ICC* / *Momentanpol*): Xác định bán kính quay cong $R$ của khung gầm dựa trên hiệu vận tốc dài giữa bánh phải $v_R$ và bánh trái $v_L$.
  - Ma trận biến đổi vận tốc từ tốc độ góc các bánh xe $(\omega_R, \omega_L)$ sang vận tốc dài trọng tâm $v$ và vận tốc góc khung thân $\omega$, với bán kính bánh $r$ và khoảng cách giữa hai vệt bánh $L$ (*Spurweite*).
- **Công thức toán học cốt lõi (LaTeX)**:
  Phương trình động học vi phân trong hệ quy chiếu toàn cục (*global reference frame*):
  $$\begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\theta} \end{bmatrix} = \begin{bmatrix} \cos\theta & 0 \\ \sin\theta & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} v \\ \omega \end{bmatrix}$$
  Với quan hệ vận tốc các bánh truyền động vi sai và bán kính quay tức thời $R$:
  $$v = \frac{r}{2} (\omega_R + \omega_L), \quad \omega = \frac{r}{L} (\omega_R - \omega_L), \quad R = \frac{v}{\omega} = \frac{L}{2} \frac{\omega_R + \omega_L}{\omega_R - \omega_L}$$
  Tọa độ tâm quay tức thời trong hệ quy chiếu thế giới:
  $$ICC = \begin{bmatrix} x - R\sin\theta \\ y + R\cos\theta \end{bmatrix}$$

### Module 02: Koppelnavigation & Đo đạc cự ly bánh xe (Dead Reckoning & Wheel Odometry)
- **Đại học tham chiếu**: Stanford University (CS237A), ETH Zürich (151-0854-00L).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 & Lernfeld 4 (*Messen und Analysieren elektrischer Systeme*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Đo lường tư thế tự thân (*proprioceptive sensing*): Cảm biến quang học đo xung quay (*optical quadrature encoder* / *Inkrementalgeber*), con quay hồi chuyển (*gyroscope* / *Gyroskop*) và đơn vị đo quán tính (*IMU* / *Trägheitsmesseinheit*).
  - Tích phân số học theo cung tròn chuẩn xác (*exact circular arc odometry integration*): Tránh sai số tuyến tính hóa Euler khi vận tốc góc $\omega \neq 0$.
  - Mô hình lan truyền phương sai sai số (*covariance error propagation*): Sai số tích lũy không giới hạn theo thời gian do hiện tượng trượt bánh (*wheel slip* / *Radschlupf*), sai số đường kính bánh thực tế và độ rung mặt sàn.
  - Phân tích phương sai Allan (*Allan Variance* / *Allan-Varianz*): Phân rã các nguồn nhiễu cảm biến góc IMU thành bước đi ngẫu nhiên của góc (*Angle Random Walk - ARW*), trôi độ lệch điểm không (*Bias Instability*) và độ dốc tốc độ (*Rate Random Walk*).
- **Công thức toán học cốt lõi (LaTeX)**:
  Tích phân vị sai trong chu kỳ lấy mẫu $\Delta t$ khi $\omega \neq 0$:
  $$\Delta \theta = \omega \Delta t, \quad \Delta x = \frac{v}{\omega} \left( \sin(\theta + \Delta \theta) - \sin\theta \right), \quad \Delta y = -\frac{v}{\omega} \left( \cos(\theta + \Delta \theta) - \cos\theta \right)$$
  Mô hình lan truyền ma trận hiệp phương sai sai số tư thế $\Sigma_t \in \mathbb{R}^{3 \times 3}$:
  $$\Sigma_t = F_t \Sigma_{t-1} F_t^T + V_t M_t V_t^T$$
  Trong đó ma trận Jacobian chuyển trạng thái $F_t = \frac{\partial f}{\partial x_{t-1}}$ và Jacobian nhiễu điều khiển $V_t = \frac{\partial f}{\partial u_t}$ với ma trận hiệp phương sai nhiễu động cơ $M_t = \operatorname{diag}(\alpha_1 v^2 + \alpha_2 \omega^2, \, \alpha_3 v^2 + \alpha_4 \omega^2)$.

### Module 03: Cảm biến ngoại quan & Nhận thức không gian (Perception: LiDAR, Sonar & Depth Cameras)
- **Đại học tham chiếu**: ETH Zürich (151-0854-00L), MIT (16.410: Principles of Autonomy and Decision Making).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 & Lernfeld 12 (*Instandhalten mechatronischer Systeme*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Cảm biến LiDAR quang học 2D/3D quét thời gian bay (*Time-of-Flight LiDAR* / *Laufzeitmessung*): Độ phân giải góc, tần số quét (10–30 Hz), mô hình tán xạ quang học trên bề mặt gương hoặc vật liệu hấp thụ.
  - Cảm biến siêu âm (*ultrasonic sensors* / *Ultraschallsensoren*): Hiệu ứng phản xạ gương (*specular reflection*) và góc mở búp sóng (*beam aperture angle*).
  - Camera đo chiều sâu RGB-D (*structured light / stereo depth cameras*): Đám mây điểm không gian (*3D point cloud* / *Punktwolke*), lọc nhiễu ngoại lai thống kê (*Statistical Outlier Removal - SOR*).
- **Công thức toán học cốt lõi (LaTeX)**:
  Mô hình chùm tia xác suất của cảm biến đo cự ly (*Beam model of range finders*):
  $$p(z_t^k \mid x_t, m) = z_{hit} \, p_{hit}(z_t^k \mid x_t, m) + z_{short} \, p_{short}(z_t^k \mid x_t, m) + z_{max} \, p_{max}(z_t^k \mid x_t, m) + z_{rand} \, p_{rand}(z_t^k \mid x_t, m)$$
  Trong đó các thành phần phân phối xác suất thành phần thỏa mãn điều kiện chuẩn hóa:
  $$p_{hit}(z \mid x, m) = \frac{1}{\sqrt{2\pi\sigma_{hit}^2}} \exp\left( -\frac{(z - z^*)^2}{2\sigma_{hit}^2} \right), \quad z_{hit} + z_{short} + z_{max} + z_{rand} = 1$$

### Module 04: Bản đồ lưới xác suất chiếm chỗ (Occupancy Grid Mapping)
- **Đại học tham chiếu**: Stanford University (CS237A), ETH Zürich (151-0854-00L), MIT (16.410).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 (*Fahrerlose Transportsysteme - Navigationsgrundlagen*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Không gian trạng thái lưới rời rạc hóa (*discretized spatial grid*): Mỗi ô lưới $m_i$ là một biến ngẫu nhiên nhị phân mang giá trị bị chiếm (*occupied* / $1$) hoặc trống (*free* / $0$).
  - Biểu diễn tỷ số logarit xác suất (*log-odds representation* / *Log-Odds-Formulierung*): Chuyển tích các xác suất điều kiện thành phép cộng đại số, triệt tiêu nguy cơ tràn số thực dưới (*floating-point underflow*).
  - Thuật toán vẽ tia Bresenham (*Bresenham ray-casting algorithm*): Cập nhật trạng thái các ô lưới dọc theo chùm tia laser từ robot tới vật cản một cách tối ưu với phép toán số nguyên.
- **Công thức toán học cốt lõi (LaTeX)**:
  Cập nhật đệ quy tỷ số log-odds $l_t(m_i) = \log \frac{p(m_i \mid z_{1:t}, x_{1:t})}{1 - p(m_i \mid z_{1:t}, x_{1:t})}$:
  $$l_t(m_i) = l_{t-1}(m_i) + \operatorname{inv\_sensor\_model}(m_i, x_t, z_t) - l_0$$
  Khôi phục xác suất chiếm chỗ tức thời từ giá trị log-odds:
  $$p(m_i \mid z_{1:t}, x_{1:t}) = 1 - \frac{1}{1 + \exp(l_t(m_i))}$$

### Module 05: Nền tảng lọc Bayes & Định vị hạt Monte Carlo (Bayes Filters & MCL)
- **Đại học tham chiếu**: MIT (16.410), Stanford University (CS237A), ETH Zürich (151-0854-00L).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 (*Zustandsschätzung und Lokalisierung*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Giả định Markov trong ước lượng trạng thái robot: Trạng thái hiện tại $x_t$ chứa toàn bộ thông tin lịch sử cần thiết.
  - Chu trình lặp hai bước: Bước dự báo chuyển động (*prediction via Chapman-Kolmogorov*) và bước hiệu chỉnh cảm biến (*measurement update via Bayes rule*).
  - Định vị Monte Carlo (*Monte Carlo Localization - MCL* / *Partikelfilter*): Xấp xỉ phân phối xác suất niềm tin tùy ý (*arbitrary non-Gaussian belief*) bằng tập hợp $M$ phần tử mẫu trọng số (hạt).
  - Thuật toán tái lấy mẫu phương sai thấp (*low-variance resampling*) và giải pháp chống bắt cóc robot (*kidnapped robot problem* bằng phương pháp bổ sung hạt ngẫu nhiên KLD-sampling theo cự ly Kullback-Leibler).
- **Công thức toán học cốt lõi (LaTeX)**:
  Phương trình lọc đệ quy Bayes (*Continuous recursive Bayes filter*):
  $$\bar{bel}(x_t) = \int p(x_t \mid x_{t-1}, u_t) \, bel(x_{t-1}) \, dx_{t-1}$$
  $$bel(x_t) = \eta \, p(z_t \mid x_t) \, \bar{bel}(x_t) = \frac{p(z_t \mid x_t) \bar{bel}(x_t)}{\int p(z_t \mid x'_t) \bar{bel}(x'_t) dx'_t}$$
  Cập nhật trọng số của hạt thứ $m$ và số lượng hạt hiệu dụng $N_{eff}$:
  $$w_t^{[m]} = w_{t-1}^{[m]} \cdot p(z_t \mid x_t^{[m]}), \quad N_{eff} = \frac{1}{\sum_{m=1}^M (w_t^{[m]})^2}$$

### Module 06: EKF SLAM & Ước lượng trạng thái phi tuyến (Extended Kalman Filter SLAM)
- **Đại học tham chiếu**: ETH Zürich (151-0854-00L), Stanford University (CS237A).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 & Lernfeld 12.
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Trạng thái kết hợp (*augmented state vector*): Ghép vectơ tư thế robot $x_t = [x, y, \theta]^T$ với tọa độ 2D của $N$ điểm mốc không gian (*landmarks* / *Merkmalspunkte*) $m = [m_{1,x}, m_{1,y}, \dots, m_{N,x}, m_{N,y}]^T$.
  - Tuyến tính hóa Taylor bậc 1 mô hình quan sát phi tuyến $h(y_t, j)$ đo cự ly $r_j$ và góc phương vị $\phi_j$.
  - Ma trận hiệp phương sai đầy đủ $\Sigma \in \mathbb{R}^{(3+2N) \times (3+2N)}$: Lưu giữ tương quan chéo giữa robot và các mốc địa vật; độ phức tạp tính toán bậc hai $O(N^2)$ dẫn tới hạn chế khi bản đồ mở rộng quy mô lớn.
- **Công thức toán học cốt lõi (LaTeX)**:
  Mô hình đo khoảng cách và góc phương vị tới mốc thứ $j$:
  $$z_t^j = h(y_t, j) = \begin{bmatrix} \sqrt{(m_{j,x} - x)^2 + (m_{j,y} - y)^2} \\ \operatorname{atan2}(m_{j,y} - y, \, m_{j,x} - x) - \theta \end{bmatrix}$$
  Ma trận Jacobian quan sát $H_t^j = \nabla_{y} h(y_t, j)$ với khoảng cách bình phương $q = (m_{j,x} - x)^2 + (m_{j,y} - y)^2$:
  $$H_t^j = \frac{1}{q} \begin{bmatrix} -\sqrt{q}(m_{j,x} - x) & -\sqrt{q}(m_{j,y} - y) & 0 & \dots & \sqrt{q}(m_{j,x} - x) & \sqrt{q}(m_{j,y} - y) & \dots \\ (m_{j,y} - y) & -(m_{j,x} - x) & -q & \dots & -(m_{j,y} - y) & (m_{j,x} - x) & \dots \end{bmatrix}$$
  Cập nhật độ lợi Kalman $K_t$ và ma trận hiệp phương sai trạng thái kết hợp:
  $$K_t = \bar{\Sigma}_t H_t^T (H_t \bar{\Sigma}_t H_t^T + Q_t)^{-1}, \quad \Sigma_t = (I - K_t H_t) \bar{\Sigma}_t$$

### Module 07: Graph-Based SLAM & Tối ưu hóa đồ thị tư thế (Pose Graph SLAM)
- **Đại học tham chiếu**: ETH Zürich (151-0854-00L), Stanford University (CS237A), TUM (IN2228).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10.
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Cấu trúc đồ thị yếu tố (*Factor Graph* / *Faktorgraph*): Các đỉnh đồ thị (*nodes*) biểu diễn tư thế robot tại từng thời điểm $x_i$, các cạnh (*edges*) biểu diễn ràng buộc không gian tương đối thu được từ odometry hoặc đối sánh quét laser (*scan matching ICP*).
  - Đóng vòng lặp quỹ đạo (*Loop Closure Detection* / *Schleifenschluss*): Nhận diện khu vực môi trường đã từng đi qua, thiết lập ràng buộc phi cục bộ để nắn chỉnh sai số tích lũy dài hạn.
  - Tối ưu hóa bình phương tối thiểu phi tuyến (*Nonlinear Least Squares Optimization*): Phương pháp Gauss-Newton và Levenberg-Marquardt trên nhóm Lie $SE(2)$ và $SE(3)$ thông qua các thư viện g2o hoặc GTSAM.
- **Công thức toán học cốt lõi (LaTeX)**:
  Hàm mục tiêu năng lượng sai số đồ thị cần tối thiểu hóa:
  $$F(x) = \sum_{ij} e_{ij}(x_i, x_j)^T \, \Omega_{ij} \, e_{ij}(x_i, x_j)$$
  Trong đó sai số tương đối giữa hai tư thế $x_i, x_j$ và phép đo tương đối $z_{ij}$:
  $$e_{ij}(x_i, x_j) = \operatorname{t2v}\left( Z_{ij}^{-1} (X_i^{-1} X_j) \right), \quad \Delta x = -(J^T \Omega J)^{-1} J^T \Omega e$$

### Module 08: Kiến trúc ROS 2 & Truyền thông thời gian thực (ROS 2 Architecture & DDS)
- **Đại học tham chiếu**: Tiêu chuẩn công nghiệp Open Robotics, ETH Zürich, Stanford University.
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 (*Realisieren mechatronischer Teilsysteme*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Lớp hạ tầng phân tán DDS (*Data Distribution Service* / *Datenverteilungsdienst*): Loại bỏ hoàn toàn điểm nghẽn nút trung tâm `roscore` của ROS 1, cung cấp khả năng phát hiện nút tự động (*dynamic peer-to-peer discovery*).
  - Cấu hình chất lượng dịch vụ (*QoS Profiles* / *Dienstgüte*): Kiểm soát độ tin cậy (*Reliability: Reliable vs. Best Effort*), lịch sử hàng đợi (*History: Keep Last vs. Keep All*), và độ trễ (*Durability: Transient Local vs. Volatile*).
  - Vòng đời nút quản lý (*Lifecycle Nodes* / *Lebenszyklus-Knoten*): Trạng thái hữu hạn gồm Unconfigured, Inactive, Active, Finalized đảm bảo trình tự khởi động an toàn cho robot công nghiệp.
  - Vi điều khiển nhúng với micro-ROS: Giao thức XRCE-DDS kết nối trực tiếp bo mạch STM32/FreeRTOS vào không gian topic của ROS 2.

### Module 09: Quy hoạch đường đi toàn cục trên lưới (Global Path Planning: Dijkstra, A*, Jump Point Search)
- **Đại học tham chiếu**: MIT (16.410), Stanford University (CS237A).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10.
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Không gian cấu hình rời rạc (*discretized configuration space* $\mathcal{C}_{space}$): Bơm phồng bán kính robot vào vật cản (*obstacle inflation*).
  - Thuật toán tìm kiếm A*: Kết hợp khoảng cách đã đi $g(n)$ với hàm ước lượng chi phí tới đích $h(n)$ để định hướng tìm kiếm trên đồ thị có hướng.
  - Tính hợp lệ (*admissibility*) và tính nhất quán (*consistency / monotonicity*): Đảm bảo thuật toán A* tìm ra đường đi ngắn nhất tuyệt đối mà không cần mở lại các nút đã đóng.
- **Công thức toán học cốt lõi (LaTeX)**:
  Hàm lượng giá nút A*:
  $$f(n) = g(n) + h(n)$$
  Điều kiện tính nhất quán của hàm heuristic:
  $$h(n) \le c(n, a, n') + h(n'), \quad \forall n, n'$$
  Với khoảng cách Euclidean trong không gian 2D thỏa mãn tính nhất quán:
  $$h(n) = \sqrt{(x_n - x_{goal})^2 + (y_n - y_{goal})^2} \le h^*(n)$$

### Module 10: Quy hoạch chuyển động dựa trên lấy mẫu (Sampling-Based Motion Planning: RRT & RRT*)
- **Đại học tham chiếu**: Stanford University (CS237A), MIT (16.410), ETH Zürich (151-0854-00L).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 (*Optimierung von Fahrwegen*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Cây ngẫu nhiên mở rộng nhanh (*Rapidly-exploring Random Tree - RRT*): Phù hợp cho không gian trạng thái nhiều chiều và có ràng buộc vi phân động học (*differential kinematic constraints*).
  - Tính tối ưu tiệm cận của RRT* (*Asymptotic Optimality - Karaman & Frazzoli 2011*): Khác với RRT truyền thống chỉ đảm bảo tính đầy đủ xác suất (*probabilistic completeness*), RRT* liên tục tái cấu trúc nhánh cây (*rewiring*) để chi phí đường đi hội tụ về nghiệm tối ưu khi số mẫu $N \to \infty$.
  - Cơ chế chọn cha tối ưu (*Choose Best Parent*) trong lân cận bán kính $r_n = \min\left( \gamma_{RRT^*} \left(\frac{\log n}{n}\right)^{1/d}, \, \eta \right)$ và kiểm tra va chạm đoạn thẳng với vật cản hình học.
- **Công thức toán học cốt lõi (LaTeX)**:
  Quy tắc chọn đỉnh cha tối ưu cho nút mới $x_{new}$:
  $$x_{min} = \arg\min_{x \in X_{near}} \left\{ \operatorname{Cost}(x) + c(\operatorname{Line}(x, x_{new})) \mid \operatorname{CollisionFree}(x, x_{new}) \right\}$$
  Biểu thức tái cấu trúc cây (*Rewiring Rule*) áp dụng cho mọi nút láng giềng $x_{near} \in X_{near} \setminus \{x_{min}\}$:
  $$\text{Nếu } \operatorname{Cost}(x_{new}) + c(\operatorname{Line}(x_{new}, x_{near})) < \operatorname{Cost}(x_{near}) \land \operatorname{CollisionFree}(x_{new}, x_{near}):$$
  $$\operatorname{Parent}(x_{near}) \leftarrow x_{new}, \quad \operatorname{Cost}(x_{near}) \leftarrow \operatorname{Cost}(x_{new}) + c(\operatorname{Line}(x_{new}, x_{near}))$$

### Module 11: Quy hoạch quỹ đạo cục bộ & Tránh va chạm thời gian thực (Local Trajectory Planning & DWA)
- **Đại học tham chiếu**: ETH Zürich (151-0854-00L), Stanford University (CS237A).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 (*Sicherheitsfunktionen mobiler Roboter - DIN EN ISO 3691-4*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Không gian vận tốc cho phép (*Dynamic Window Approach - DWA* / *Dynamisches Geschwindigkeitsfenster*): Giới hạn không gian tìm kiếm $(v, \omega)$ trong khoảng vận tốc mà động cơ có thể đạt được trong bước thời gian kế tiếp dưới giới hạn gia tốc $(\dot{v}_{max}, \dot{\omega}_{max})$ và giới hạn phanh an toàn.
  - Bộ quy hoạch dải đàn hồi có định thời (*Timed Elastic Band - TEB Local Planner*): Tối ưu hóa biến dạng quỹ đạo theo thời gian để đi vòng qua vật cản động.
  - Tích phân đường dẫn mô hình dự báo (*Model Predictive Path Integral - MPPI*): Quy hoạch dựa trên GPU/CPU đa lõi cho robot hoạt động ở tốc độ cao trên địa hình phức tạp.
- **Công thức toán học cốt lõi (LaTeX)**:
  Cửa sổ động học vận tốc $V_d$ tại thời điểm $t$:
  $$V_d = \left\{ (v, \omega) \mid v \in [v_t - \dot{v}_{max} \Delta t, \, v_t + \dot{v}_{max} \Delta t] \cap [v_{min}, v_{max}], \quad \omega \in [\omega_t - \dot{\omega}_{max} \Delta t, \, \omega_t + \dot{\omega}_{max} \Delta t] \cap [\omega_{min}, \omega_{max}] \right\}$$
  Hàm mục tiêu đánh giá vector điều khiển cục bộ $G(v, \omega)$:
  $$G(v, \omega) = \alpha \cdot \operatorname{heading}(v, \omega) + \beta \cdot \operatorname{clearance}(v, \omega) + \gamma \cdot \operatorname{velocity}(v, \omega)$$

### Module 12: Hệ thống điều hướng Nav2 & Cây hành vi (ROS 2 Nav2 & Behavior Trees)
- **Đại học tham chiếu**: Nav2 Working Group, Open Robotics, TU München.
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 & Lernfeld 12 (*Inbetriebnahme und Fehlersuche an autonomen Systemen*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Kiến trúc phân lớp của Nav2: Bộ điều phối trung tâm (*BT Navigator*), bộ quy hoạch toàn cục (*Global Planner Server*), bộ điều khiển cục bộ (*Controller Server / Local Planner*), và các hành vi phục hồi (*Recovery Behaviors* như xoay tại chỗ, lùi xe, dọn dẹp bản đồ chi phí).
  - Bản đồ chi phí đa tầng (*Costmap 2D Layering*): Lớp tĩnh (*Static Layer*), lớp chướng ngại vật tức thời (*Obstacle Layer từ LiDAR/Radar*), và lớp mở rộng biên an toàn (*Inflation Layer* theo hàm suy giảm hàm mũ).
  - Cây hành vi (*Behavior Trees* / *Verhaltensbäume*): Cấu trúc cây phân cấp với các nút điều khiển luồng (Sequence, Fallback/Selector, Parallel) và các nút lá thực thi (Action, Condition) thay thế cho máy trạng thái hữu hạn (FSM) truyền thống.

---

## Phần 2: Danh mục tài liệu học thuật (Academic Reading List)

Danh mục các giáo trình kinh điển và công trình khoa học nền tảng quốc tế, cung cấp cơ sở toán học và mã nguồn kỹ thuật cho phân hệ:

1. **Thrun, Sebastian; Burgard, Wolfram; Fox, Dieter** (2005). *Probabilistic Robotics*. MIT Press, Cambridge, MA.
   - Trọng tâm nghiên cứu: Chương 2 (Recursive State Estimation - Ước lượng trạng thái đệ quy), Chương 3 (Gaussian Filters - Bộ lọc Kalman và EKF), Chương 5 (Robot Motion Models - Mô hình chuyển động vi sai), Chương 7 (Mobile Robot Localization - Định vị robot di động bằng MCL), Chương 9 (Occupancy Grid Mapping - Bản đồ lưới chiếm chỗ), Chương 10 (Simultaneous Localization and Mapping - EKF SLAM và FastSLAM).
2. **Siegwart, Roland; Nourbakhsh, Illah R.; Scaramuzza, Davide** (2011). *Introduction to Autonomous Mobile Robots* (2nd Edition). MIT Press, Cambridge, MA.
   - Trọng tâm nghiên cứu: Chương 2 (Locomotion - Cơ cấu di động và bánh xe), Chương 3 (Mobile Robot Kinematics - Động học vi sai và bánh omni), Chương 4 (Perception - Cảm biến LiDAR, thị giác và siêu âm), Chương 5 (Localization - Phối hợp Koppelnavigation và đối sánh mốc địa vật), Chương 6 (Planning and Navigation - Quy hoạch đường đi và tránh vật cản DWA).
3. **LaValle, Steven M.** (2006). *Planning Algorithms*. Cambridge University Press, Cambridge, UK.
   - Trọng tâm nghiên cứu: Chương 2 (Discrete Planning - Thuật toán đồ thị Dijkstra và A*), Chương 4 (The Configuration Space - Lý thuyết không gian cấu hình $\mathcal{C}_{space}$), Chương 5 (Sampling-Based Motion Planning - Nền tảng toán học của RRT và RRT*), Chương 14 (Differential Models and Nonholonomic Constraints - Quy hoạch dưới ràng buộc vi phân).
4. **Macenski, Steven; Foote, Tully; Gerkey, Brian; Lalancette, Chris; Woodall, William** (2022). *Robot Operating System 2: Design, architecture, and uses in the wild*. Science Robotics, Vol. 7, No. 66, eabm6074.
   - Trọng tâm nghiên cứu: Kiến trúc DDS thời gian thực, cơ chế giao tiếp Publish-Subscribe phi tập trung, mô hình nút vòng đời (*Lifecycle Nodes*), phân tích thông lượng dữ liệu độ trễ thấp và ứng dụng thực tiễn của Nav2 trong công nghiệp tự hành.
5. **Choset, Howie; Lynch, Kevin M.; Hutchinson, Seth; Kantor, George A.; Burgard, Wolfram; Kavraki, Lydia E.; Thrun, Sebastian** (2005). *Principles of Robot Motion: Theory, Algorithms, and Implementations*. MIT Press, Cambridge, MA.
   - Trọng tâm nghiên cứu: Chương 4 (Potential Functions - Hàm thế năng nhân tạo và trường lực thế), Chương 7 (Sampling-based Motion Planning - PRM và RRT), Chương 9 (Kalman Filtering and SLAM - Cực tiểu hóa bình phương sai số và bài toán tương quan mốc).
6. **Durrant-Whyte, Hugh; Bailey, Tim** (2006). *Simultaneous Localization and Mapping: Part I and Part II*. IEEE Robotics & Automation Magazine, Vol. 13, No. 2, pp. 99-110 & Vol. 13, No. 3, pp. 108-117.
   - Trọng tâm nghiên cứu: Đạo hàm giải tích ma trận hiệp phương sai SLAM, chứng minh giới hạn hội tụ của các mốc địa vật và phân tích tính toán độ phức tạp của bộ lọc EKF SLAM.
7. **Karaman, Sertac; Frazzoli, Emilio** (2011). *Sampling-based algorithms for optimal motion planning*. International Journal of Robotics Research (IJRR), Vol. 30, No. 7, pp. 846-894.
   - Trọng tâm nghiên cứu: Bằng chứng toán học chứng minh RRT không tối ưu tiệm cận (xác suất hội tụ về quỹ đạo tối ưu bằng 0) và định lý toán học khẳng định tính tối ưu tiệm cận của RRT* thông qua tái cấu trúc láng giềng.

---

## Phần 3: Bài tập thực hành & Project mô phỏng (Practical Labs & Simulation Projects)

Hệ thống 3 đồ án thực hành từ mô phỏng toán học giải tích đến thuật toán điều hướng tự hành chạy trực tiếp trên máy Mac (Intel Core i5, 8GB RAM).

### Lab 01: Mô phỏng động học vi sai & Đánh giá sai số trượt Koppelnavigation (Differential Drive Odometry Drift Simulator)
- **Mục tiêu kỹ thuật**:
  - Lập trình bộ tích phân chuyển động vi sai theo mô hình cung tròn chuẩn xác (*exact arc integration*) bằng Python thuần.
  - Mô phỏng sai số cơ học thực tế: Sai số bán kính bánh xe $\Delta r = 0.5\%$, sai số vệt bánh $\Delta L = 1.0\%$, và nhiễu trượt Gauss $\mathcal{N}(0, \sigma^2)$.
  - Cho robot chạy theo quỹ đạo hình chữ nhật $4 \times 4$ mét, ghi nhận độ lệch vị trí cuối cùng (*final pose error* $\Delta x, \Delta y, \Delta \theta$) để chứng minh sự cần thiết của cảm biến ngoại quan (LiDAR/SLAM).
- **Phương pháp thực thi**:
  1. Khởi tạo trạng thái ban đầu: $x_0 = 0.0, y_0 = 0.0, \theta_0 = 0.0$.
  2. Tạo chuỗi điều khiển vận tốc: Đi thẳng $v = 0.5$ m/s trong 8 s, quay góc $90^\circ$ với $\omega = \pi/4$ rad/s trong 2 s; lặp lại 4 cạnh.
  3. Áp dụng nhiễu trượt bánh ngẫu nhiên vào xung encoder tại mỗi bước thời gian $\Delta t = 20$ ms.
  4. Tính toán sai số vị trí Euclide cuối hành trình và vẽ elip phương sai sai số $\Sigma_{xy}$.
- **Tham số thực nghiệm**: Bán kính bánh $r = 0.08$ m, khoảng cách vệt bánh $L = 0.35$ m, chu kỳ trích mẫu $\Delta t = 20$ ms, tổng thời gian chạy 80 s.
- **Tiêu chí nghiệm thu**: So sánh sai số giữa phương pháp Euler bậc 1 và phương pháp cung tròn chính xác; tính ma trận hiệp phương sai sai số $\Sigma_{pose}(t)$.

### Lab 02: Lập bản đồ xác suất chiếm chỗ từ chùm tia Laser (2D Log-Odds Occupancy Grid Mapping)
- **Mục tiêu kỹ thuật**:
  - Hiện thực hóa thuật toán vẽ tia Bresenham (*Bresenham ray-casting*) để xác định các ô lưới nằm trên đường truyền của tia laser 2D.
  - Áp dụng mô hình cảm biến nghịch đảo (*inverse sensor model*): Gán giá trị $l_{free} = -0.4$ cho các ô lưới trống dọc theo tia và $l_{occ} = +0.85$ cho ô lưới va chạm vật cản.
  - Cập nhật bản đồ dạng mảng hai chiều kích thước $100 \times 100$ ô (độ phân giải $0.05$ m/ô tương đương diện tích $5 \times 5$ m) từ tập dữ liệu quét mô phỏng 360 tia với góc quét $270^\circ$.
- **Phương pháp thực thi**:
  1. Rời rạc hóa môi trường liên tục sang lưới chỉ số $(row, col)$.
  2. Duyệt qua từng tia quét laser: Chuyển đổi tọa độ cực $(r_k, \theta_k)$ sang tọa độ Descartes trong hệ quy chiếu robot, sau đó sang hệ bản đồ thế giới thông qua phép biến đổi đồng nhất $T_{map}^{robot}$.
  3. Thực thi thuật toán vẽ tia Bresenham số nguyên từ tọa độ robot đến điểm phản hồi laser.
  4. Cộng dồn log-odds và áp dụng ngưỡng cắt giá trị $[-5.0, +5.0]$ để tránh bão hòa xác suất.
- **Tiêu chí nghiệm thu**: Xuất ma trận xác suất chiếm chỗ $P(m_i)$, kiểm tra độ sắc nét của góc tường phòng và khả năng loại trừ nhiễu cảm biến ngẫu nhiên.

### Lab 03: Thuật toán quy hoạch đường đi tối ưu A* và RRT* (`labs/lab05_astar_rrt.py`)
- **Mục tiêu kỹ thuật**:
  - Triển khai hoàn chỉnh hai thuật toán quy hoạch đường đi kinh điển trong file mã nguồn chuẩn độc lập `labs/lab05_astar_rrt.py` sử dụng thư viện chuẩn của Python (`math`, `heapq`, `random`, `time`, `dataclasses`).
  - **A\* Grid Planner**: Tìm kiếm đường đi ngắn nhất trên lưới 2D $30 \times 30$ ô có tường chắn và khe cửa hẹp, sử dụng hàm đánh giá heuristic khoảng cách Euclidean và hàng đợi ưu tiên `heapq`.
  - **RRT\* Continuous Planner**: Mở rộng cây ngẫu nhiên trong không gian liên tục $[0, 30] \times [0, 30]$ với 4 vật cản tròn bán kính từ $2.5$ đến $3.2$ m; tích hợp cơ chế chọn đỉnh cha tối ưu và tái liên kết nhánh cây (*rewiring*) để hội tụ về quỹ đạo mượt mà ngắn nhất.
  - Tối ưu hóa hiệu năng tính toán: Toàn bộ quá trình giải thuật hoàn thành trong thời gian $< 100$ ms trên CPU Intel Core i5 của máy Mac.
- **Lệnh thực thi & Kiểm chứng**:
  ```bash
  python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab05_astar_rrt.py
  ```
- **Kết quả định lượng chuẩn**:
  - A* Planner: Tìm đường thành công qua 31 bước lưới, chi phí khoảng cách $38.28$ m, duyệt qua 176 nút trong thời gian $\approx 3.0$ ms.
  - RRT* Planner: Khởi tạo 456 nút cây ngẫu nhiên qua 500 bước lặp, chi phí quỹ đạo $35.87$ m, thời gian giải thuật $\approx 59.7$ ms.
  - Tất cả các đoạn thẳng quỹ đạo đều được kiểm tra hình học và chứng minh không giao cắt với bất kỳ vật cản nào.

---

## Phần 4: Từ khóa tìm kiếm & Thuật ngữ Anh-Đức (Exact Search Queries & Bilingual Terminology Table)

### Danh sách từ khóa tìm kiếm chuyên sâu (Precision Academic Search Queries)

Các truy vấn tìm kiếm độ chính xác cao phục vụ tra cứu giáo trình, bài báo khoa học và mã nguồn mẫu chuẩn công nghiệp:

1. `"probabilistic robotics" "recursive state estimation" "Bayes filter" filetype:pdf`
2. `"differential drive kinematics" "dead reckoning error propagation" site:ocw.mit.edu`
3. `"occupancy grid mapping" "log-odds" "bresenham" site:ethz.ch`
4. `"A* algorithm" "consistent heuristic" "monotonicity" "path planning" filetype:pdf`
5. `"RRT*" "asymptotic optimality" "Karaman" "Frazzoli" "proof" filetype:pdf`
6. `"EKF SLAM" "Jacobian derivation" "landmark based" site:stanford.edu`
7. `"Nav2 architecture" "behavior trees" "costmap_2d" site:github.com/ros-planning`
8. `"graph SLAM" "pose graph optimization" "factor graphs" site:gtsam.org`
9. `"particle filter" "monte carlo localization" "kld sampling" site:tum.de`
10. `"dynamic window approach" "local trajectory planner" "Fox" "Burgard" filetype:pdf`
11. `"FastSLAM 2.0" "Rao-Blackwellized particle filter" "convergence proof" filetype:pdf`
12. `"micro-ROS" "embedded RTOS" "client architecture" "STM32" site:micro.ros.org`
13. `"timed elastic band" "teb_local_planner" "kinematic constraints" filetype:pdf`
14. `"model predictive path integral" "mppi" "gpu robot navigation" site:arxiv.org`
15. `"Cartographer SLAM" "submap optimization" "sparse pose adjustment" site:github.com/cartographer-project`

### Bảng đối chiếu thuật ngữ chuyên ngành Anh - Đức - Việt

Bảng thuật ngữ đối chiếu 3 thứ tiếng chuẩn hóa theo tiêu chuẩn công nghiệp CHLB Đức (DIN EN ISO 8373, DIN 19226, VDI/VDE 2860, ISO 13482) và chương trình đào tạo nghề kép DIHK/AHK:

| English Term | German Fachbegriff (DIN/ISO) | Tiếng Việt (Chuyên ngành) | Tiêu chuẩn / Chuẩn hóa |
|---|---|---|---|
| Autonomous Mobile Robot (AMR) | Autonomer mobiler Roboter (AMR) | Robot di động tự hành | DIN EN ISO 8373 / ISO 3691-4 |
| Automated Guided Vehicle (AGV) | Fahrerloses Transportfahrzeug (FTF) | Xe tự hành công nghiệp dẫn đường | VDI 2510 / VDI 4451 |
| Automated Guided Vehicle System | Fahrerloses Transportsystem (FTS) | Hệ thống xe tự hành vận chuyển | DIN EN 1525 / VDI 2510 |
| Dead Reckoning / Odometry | Koppelnavigation / Radodometrie | Định vị thủy triều / Cự ly bánh xe | VDI/VDE 2860 |
| Path Planning | Pfadplanung | Quy hoạch đường đi | VDI/VDE 2860 |
| Trajectory Tracking | Trajektorienverfolgung | Bám quỹ đạo chuyển động | DIN 19226 |
| State Estimation | Zustandsschätzung | Ước lượng trạng thái hệ thống | DIN 19226 |
| Obstacle Avoidance | Hindernisvermeidung | Tránh vật cản an toàn | ISO 13482 / ISO 3691-4 |
| Bayes Filter | Bayes-Filter | Bộ lọc xác suất Bayes | Thống kê toán học |
| Occupancy Grid Map | Wahrscheinlichkeitsbelegungskarte | Bản đồ lưới xác suất chiếm chỗ | IEEE Robotics & Automation |
| Simultaneous Localization and Mapping (SLAM) | Simultane Lokalisierung und Kartierung | Định vị và lập bản đồ đồng thời | IEEE RAS / VDI 2860 |
| Particle Filter / Monte Carlo Localization | Partikelfilter (Monte-Carlo-Lokalisierung) | Bộ lọc hạt / Định vị Monte Carlo | IEEE Trans. Robotics |
| Differential Drive | Differentialantrieb | Hệ thống truyền động vi sai | DIN EN ISO 8373 |
| Non-holonomic Constraint | Nichtholonome Bewegungsbeschränkung | Ràng buộc cơ học phi toàn định | Cơ học giải tích Euler-Lagrange |
| Rapidly-exploring Random Tree (RRT*) | Schnell erforschender Zufallsbaum (RRT*) | Cây ngẫu nhiên mở rộng nhanh tối ưu | Giải thuật quy hoạch tối ưu |
| A* Search Algorithm | A*-Suchalgorithmus | Thuật toán tìm kiếm A* | Khoa học máy tính lý thuyết |
| Cost Function | Kostenfunktion / Bewertungsfunktion | Hàm chi phí / Hàm mục tiêu | Lý thuyết điều khiển tối ưu |
| Extended Kalman Filter (EKF) | Erweitertes Kalman-Filter (EKF) | Bộ lọc Kalman mở rộng phi tuyến | Xử lý tín hiệu ngẫu nhiên |
| Costmap Inflation Layer | Belegungskarten-Expansionsschicht | Lớp mở rộng biên an toàn bản đồ | ROS 2 Navigation Stack |
| Behavior Tree | Verhaltensbaum | Cây hành vi điều phối tác vụ | Kiến trúc phần mềm AI robot |
| Dynamic Window Approach (DWA) | Dynamisches Geschwindigkeitsfenster | Phương pháp cửa sổ động học vận tốc | Thuật toán điều khiển cục bộ |
| Scan Matching | Scan-Abgleich (ICP-Algorithmus) | Đối sánh chùm quét laser | Thị giác máy tính & SLAM |
