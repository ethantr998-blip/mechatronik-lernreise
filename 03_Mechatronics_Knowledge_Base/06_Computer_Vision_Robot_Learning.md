# Phân hệ 06: Thị giác máy tính & Học máy trong Robot (Computer Vision & Robot Learning)

Tài liệu chuyên sâu thuộc Hệ thống Tri thức Cơ điện tử & Robot học (*Mechatronics & Robotics Knowledge Base*), chuẩn hóa theo chương trình đào tạo của **ETH Zürich (151-0632-00L / 263-5902-00L)**, **TU München (IN2064 / IN2228)**, **UC Berkeley (CS280 / CS285)** và tiêu chuẩn nghề nghiệp **CHLB Đức (DIHK / AHK - Lernfeld 6 & 13)**. Được biên soạn theo nguyên lý đệ nhất (*First Principles*), phục vụ đào tạo kỹ sư Cơ điện tử làm việc tại CHLB Đức.

---

## Phần 1: Đề cương chuẩn hóa (Standardized Syllabus Breakdown)

Cấu trúc đề cương 10 module học thuật chuyên sâu, bao hàm quang học hình học (*geometric camera optics*), hình học đa góc nhìn (*multi-view geometry*), đo đạc thị giác (*visual odometry*), mạng nơ-ron tích chập (*deep convolutional networks*), và học tăng cường điều khiển robot (*reinforcement learning for robotics*).

### Module 01: Quang học hình học & Mô hình máy ảnh lỗ kim (Geometric Camera Models & Pinhole Projection)
- **Đại học tham chiếu**: ETH Zürich (151-0632-00L: Vision Algorithms for Mobile Robotics), UC Berkeley (CS280: Computer Vision).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 6 (*Konzipieren und Realisieren mechatronischer Teilsysteme* - Optische Messsysteme).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Mô hình máy ảnh lỗ kim lý tưởng (*Pinhole Camera Model* / *Lochkameramodell*): Phép chiếu phối cảnh xuyên tâm (*central perspective projection*) biến đổi điểm thế giới 3D $\tilde{X} = [X, Y, Z, 1]^T$ thành điểm trên mặt phẳng cảm biến ảnh 2D $(u, v)$.
  - Ma trận nội tại (*Intrinsic Matrix* $K$ / *Intrinsische Kameramatrix*): Tiêu cự theo trục $x$ và $y$ ($f_x = f / s_x, f_y = f / s_y$), điểm chính quang học $(c_x, c_y)$ (*principal point* / *Hauptpunkt*), và hệ số nghiêng xiên trục tọa độ $s$ (*skew factor*).
  - Ma trận ngoại tại (*Extrinsic Matrix* $[R \mid t]$ / *Extrinsische Parameter*): Biến đổi tọa độ Euclid cứng từ hệ quy chiếu thế giới sang hệ quy chiếu máy ảnh gồm ma trận quay trực giao $R \in SO(3)$ và vectơ tịnh tiến $t \in \mathbb{R}^3$.
  - Công thức quay Rodrigues: Biến đổi vectơ trục quay - góc quay $(\mathbf{v}, \theta)$ sang ma trận quay trực giao giải tích.
- **Công thức toán học cốt lõi (LaTeX)**:
  Phương trình chiếu phối cảnh tuyến tính thuần nhất:
  $$\begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \sim K [R \mid t] \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix} = \begin{bmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} r_{11} & r_{12} & r_{13} & t_x \\ r_{21} & r_{22} & r_{23} & t_y \\ r_{31} & r_{32} & r_{33} & t_z \end{bmatrix} \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}$$
  Tọa độ máy ảnh chuẩn hóa (*normalized camera coordinates*):
  $$x_n = \frac{X_c}{Z_c}, \quad y_n = \frac{Y_c}{Z_c}, \quad \begin{bmatrix} u \\ v \end{bmatrix} = \begin{bmatrix} f_x x_n + c_x \\ f_y y_n + c_y \end{bmatrix}$$
  Công thức quay Rodrigues từ vectơ trục quay đơn vị $\mathbf{v}$ và góc quay $\theta$:
  $$R = I_{3 \times 3} + \sin\theta [\mathbf{v}]_\times + (1 - \cos\theta) [\mathbf{v}]_\times^2$$

### Module 02: Mô hình méo thấu kính & Hiệu chuẩn máy ảnh (Lens Distortion & Zhang's Calibration)
- **Đại học tham chiếu**: ETH Zürich (151-0632-00L), Stanford University (CS231A).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 6 & Lernfeld 13 (*Optische Qualitätsprüfung*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Méo quang học phi tuyến của thấu kính (*Lens Distortion* / *Linsenverzerrung*): Sai lệch hướng tâm (*radial distortion* kiểu thùng / *barrel* $k_1 < 0$ hoặc gối / *pincushion* $k_1 > 0$) do độ cong quang học và sai lệch tiếp tuyến (*tangential distortion* $p_1, p_2$) do thấu kính không song song tuyệt đối với cảm biến CMOS/CCD.
  - Mô hình đa thức Brown-Conrady: Xấp xỉ chuỗi Taylor hàm méo quang học theo khoảng cách bán kính $r^2 = x_n^2 + y_n^2$.
  - Thuật toán hiệu chuẩn phẳng Zhang (*Zhang's Checkerboard Calibration Method*): Ước lượng ma trận đồng hình Homography $H$ từ nhiều góc chụp bảng cờ vua, giải tích xuất $K$, và tinh chỉnh phi tuyến bằng thuật toán Levenberg-Marquardt nhằm cực tiểu hóa sai số tái chiếu (*reprojection error*).
- **Công thức toán học cốt lõi (LaTeX)**:
  Biểu thức méo hướng tâm và tiếp tuyến Brown-Conrady:
  $$x_d = x_n \left( 1 + k_1 r^2 + k_2 r^4 + k_3 r^6 \right) + 2 p_1 x_n y_n + p_2 \left( r^2 + 2 x_n^2 \right)$$
  $$y_d = y_n \left( 1 + k_1 r^2 + k_2 r^4 + k_3 r^6 \right) + p_1 \left( r^2 + 2 y_n^2 \right) + 2 p_2 x_n y_n$$
  Sai số tái chiếu cần cực tiểu hóa trong không gian pixel:
  $$\mathcal{L}_{calib} = \sum_{i=1}^M \sum_{j=1}^N \left\| m_{ij} - \pi(K, k_1, k_2, R_i, t_i, M_j) \right\|^2$$
  Trích xuất ma trận quay $R$ và tịnh tiến $t$ từ các cột của ma trận đồng hình $H = [\mathbf{h}_1, \mathbf{h}_2, \mathbf{h}_3]$:
  $$\mathbf{r}_1 = \lambda K^{-1} \mathbf{h}_1, \quad \mathbf{r}_2 = \lambda K^{-1} \mathbf{h}_2, \quad \mathbf{r}_3 = \mathbf{r}_1 \times \mathbf{r}_2, \quad \mathbf{t} = \lambda K^{-1} \mathbf{h}_3 \quad \left( \lambda = \frac{1}{\|K^{-1}\mathbf{h}_1\|} \right)$$

### Module 03: Xử lý ảnh không gian, Tích chập 2D & Phát hiện biên cạnh (Spatial Filtering & Edge Detection)
- **Đại học tham chiếu**: UC Berkeley (CS280), TUM (IN2064: Machine Learning).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 6.
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Phép toán tích chập không gian 2D (*Discrete 2D Spatial Convolution* / *2D-Bildfaltung*): Nhân chập ma trận điểm ảnh với mặt nạ nhân ma trận lọc (*filter kernel*).
  - Bộ lọc Gauss làm mịn khử nhiễu (*Gaussian Smoothing Filter*): Phân bố trọng số đối xứng trục nhằm bảo toàn năng lượng tín hiệu trong khi loại trừ nhiễu trắng tần số cao.
  - Đạo hàm không gian và toán tử Sobel/Scharr: Xấp xỉ gradient cường độ sáng cục bộ $(\nabla I_x, \nabla I_y)$ theo hướng ngang và đứng.
  - Thuật toán phát hiện biên cạnh Canny (*Canny Edge Detector*): Bốn bước chuẩn mực gồm làm mịn Gauss, tính độ lớn và hướng gradient, triệt tiêu cực đại cục bộ (*non-maximum suppression*), và lọc ngưỡng trễ hysteresis với hai ngưỡng $(T_{low}, T_{high})$.
- **Công thức toán học cốt lõi (LaTeX)**:
  Hàm hạt nhân Gauss 2D đối xứng trục:
  $$G(x, y) = \frac{1}{2\pi\sigma^2} \exp\left( -\frac{x^2 + y^2}{2\sigma^2} \right)$$
  Tích chập rời rạc 2D với nhân kích thước $(2k+1) \times (2k+1)$:
  $$(I * G)(u, v) = \sum_{i=-k}^k \sum_{j=-k}^k I(u - i, v - j) \, G(i, j)$$
  Độ lớn và góc phương vị của vector gradient ảnh:
  $$|\nabla I| = \sqrt{I_x^2 + I_y^2}, \quad \theta = \operatorname{atan2}(I_y, I_x)$$

### Module 04: Trích xuất đặc trưng cục bộ & Mô tả điểm ảnh (Feature Detection: Harris, SIFT & ORB)
- **Đại học tham chiếu**: ETH Zürich (151-0632-00L), UC Berkeley (CS280).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 13 (*Optimieren von Bildverarbeitungssystemen*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Ten-sơ cấu trúc bậc hai (*Second-Moment Matrix / Structure Tensor* $M$): Đánh giá biến thiên cường độ sáng theo mọi hướng dịch chuyển $(\Delta u, \Delta v)$ trong cửa sổ lân cận $W$.
  - Trị riêng của ma trận cấu trúc $(\lambda_1, \lambda_2)$: Vùng phẳng ($\lambda_1 \approx 0, \lambda_2 \approx 0$), cạnh biên ($\lambda_1 \gg \lambda_2$ hoặc ngược lại), và góc đặc trưng ($\lambda_1, \lambda_2$ đều lớn).
  - Hàm đáp ứng góc Harris (*Harris Corner Response* $R$): Tránh phân tích trị riêng tốn kém bằng định thức và vết của ma trận $M$.
  - Đặc trưng bất biến tỉ lệ SIFT (*Scale-Invariant Feature Transform*): Không gian tỉ lệ DoG (*Difference of Gaussians*), định hướng cục bộ và vector mô tả 128 chiều.
  - Đặc trưng nhị phân tốc độ cao ORB (*Oriented FAST and Rotated BRIEF*): Tối ưu hóa thực thi thời gian thực trên hệ thống nhúng mà không cần GPU.
- **Công thức toán học cốt lõi (LaTeX)**:
  Ten-sơ cấu trúc bậc hai với trọng số Gauss $w(x, y)$:
  $$M(u, v) = \sum_{(x, y) \in W} w(x, y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}$$
  Hàm đáp ứng góc Harris với hệ số thực nghiệm $k \in [0.04, 0.06]$:
  $$R = \det(M) - k \, (\operatorname{Tr}(M))^2 = (\lambda_1 \lambda_2) - k (\lambda_1 + \lambda_2)^2$$
  Khai triển Taylor bậc 2 định vị cực trị dưới pixel trong SIFT:
  $$\hat{\mathbf{x}} = - \left( \frac{\partial^2 D}{\partial \mathbf{x}^2} \right)^{-1} \frac{\partial D}{\partial \mathbf{x}}$$

### Module 05: Hình học đối cực & Ma trận thiết yếu (Epipolar Geometry & Essential Matrix)
- **Đại học tham chiếu**: ETH Zürich (263-5902-00L: Computer Vision), ETH Zürich (151-0632-00L).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 6 & Lernfeld 10.
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Ràng buộc đối cực hai góc nhìn (*Two-View Epipolar Geometry* / *Epipolargeometrie*): Tâm quang học của hai máy ảnh $C_1, C_2$ và điểm 3D không gian $P$ cùng nằm trên một mặt phẳng đối cực (*epipolar plane*).
  - Điểm đối cực (*epipoles* $e_1, e_2$): Giao điểm của đường nối hai tâm máy ảnh (*baseline*) với các mặt phẳng ảnh.
  - Ma trận thiết yếu (*Essential Matrix* $E$): Biểu diễn quan hệ hình học thuần túy trong hệ tọa độ chuẩn hóa thông qua tích của ma trận phản đối xứng của vectơ tịnh tiến $[t]_\times$ và ma trận quay $R$.
  - Tính chất đại số của $E$: Định thức bằng $0$ ($\det(E) = 0$) và hai giá trị kỳ dị khác không bằng nhau ($\sigma_1 = \sigma_2, \sigma_3 = 0$).
  - Ma trận cơ bản (*Fundamental Matrix* $F$): Mở rộng ma trận thiết yếu lên không gian pixel chưa hiệu chuẩn $F = K'^{-T} E K^{-1}$.
- **Công thức toán học cốt lõi (LaTeX)**:
  Ràng buộc đối cực đại số trên tọa độ chuẩn hóa $x_1, x_2$:
  $$x_2^T E x_1 = 0$$
  Với ma trận thiết yếu $E \in \mathbb{R}^{3 \times 3}$ có hạng bằng 2:
  $$E = [t]_\times R = \begin{bmatrix} 0 & -t_z & t_y \\ t_z & 0 & -t_x \\ -t_y & t_x & 0 \end{bmatrix} R$$
  Ràng buộc đối cực trên tọa độ pixel $p_1, p_2$ và đường đối cực $l_2$:
  $$p_2^T F p_1 = 0, \quad \mathbf{l}_2 = F p_1, \quad F = K_2^{-T} [t]_\times R K_1^{-1}$$

### Module 06: Thuật toán 8 điểm & Ước lượng mạnh RANSAC (8-Point Algorithm & RANSAC Estimators)
- **Đại học tham chiếu**: ETH Zürich (151-0632-00L), Stanford University (CS231A).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 13 (*Robuste Parameterschätzung*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Thuật toán 8 điểm chuẩn hóa của Hartley (*Normalized 8-Point Algorithm*): Cân bằng tỉ lệ điểm ảnh về gốc tọa độ 0 và khoảng cách trung bình $\sqrt{2}$ để chống suy thoái số học ma trận tích phân khi giải hệ phương trình tuyến tính thuần nhất $A f = 0$.
  - Phân tích giá trị kỳ dị (*Singular Value Decomposition - SVD*): Ép điều kiện ma trận cơ bản có hạng bằng 2 bằng cách đặt giá trị kỳ dị bé nhất $\sigma_3 = 0$.
  - Thuật toán lọc nhiễu ngẫu nhiên RANSAC (*Random Sample Consensus* / *RANSAC-Verfahren*): Ước lượng thông số hình học vững chắc trước tỉ lệ tương ứng sai (*outliers*) có thể lên tới 50–70% trong các bài toán đối sánh thực tế.
- **Công thức toán học cốt lõi (LaTeX)**:
  Phương trình tuyến tính cho mỗi cặp điểm tương ứng $(x_i, y_i, 1) \leftrightarrow (x'_i, y'_i, 1)$:
  $$\begin{bmatrix} x'_i x_i & x'_i y_i & x'_i & y'_i x_i & y'_i y_i & y'_i & x_i & y_i & 1 \end{bmatrix} \mathbf{f} = 0$$
  Chiếu ma trận ước lượng về đa tạp hạng 2:
  $$F_{rank2} = U \operatorname{diag}(\sigma_1, \sigma_2, 0) V^T, \quad F_{final} = T'^T F_{rank2} T$$
  Số vòng lặp RANSAC cần thiết với độ tin cậy $p$, cỡ mẫu tối thiểu $s$, và tỉ lệ nhiễu $\epsilon$:
  $$N_{iter} = \frac{\log(1 - p)}{\log(1 - (1 - \epsilon)^s)}$$

### Module 07: Đo đạc thị giác & Tái tạo không gian 3D (Visual Odometry & 3D Reconstruction)
- **Đại học tham chiếu**: ETH Zürich (151-0632-00L), TUM (IN2228: Autonomous Driving).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 & Lernfeld 13.
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Đo đạc thị giác (*Visual Odometry - VO* / *Visuelle Odometrie*): Khôi phục chuyển động 6-DOF tức thời của robot qua từng khung hình camera liên tiếp.
  - Phân loại VO: Phương pháp dựa trên đặc trưng (*Feature-based*) đối sánh điểm ảnh và phương pháp trực tiếp (*Direct methods*) cực tiểu hóa sai số trắc quang (*photometric error*).
  - Đạc tam giác tuyến tính (*Linear Ray Triangulation*): Giao cắt các tia quang học từ hai vị trí máy ảnh để khôi phục tọa độ chiều sâu 3D của điểm thế giới.
  - Tối ưu hóa chùm tia (*Bundle Adjustment - BA* / *Bündelausgleichung*): Tối ưu hóa phi tuyến đồng thời tất cả tư thế máy ảnh và vị trí các điểm mốc 3D.
- **Công thức toán học cốt lõi (LaTeX)**:
  Nghiệm giải tích đạc tam giác tia đối cực cho độ sâu $Z_1$:
  $$Z_1 = -\frac{(x_2 \times t) \cdot (x_2 \times R x_1)}{\|x_2 \times R x_1\|^2}$$
  Hệ phương trình DLT biến đổi tuyến tính trực tiếp giải tọa độ điểm thế giới $\mathbf{X}$:
  $$\begin{bmatrix} u \mathbf{P}_3^T - \mathbf{P}_1^T \\ v \mathbf{P}_3^T - \mathbf{P}_2^T \\ u' \mathbf{P'}_3^T - \mathbf{P'}_1^T \\ v' \mathbf{P'}_3^T - \mathbf{P'}_2^T \end{bmatrix} \mathbf{X} = 0$$
  Hàm mục tiêu sai số tái chiếu trong tối ưu hóa Bundle Adjustment:
  $$\min_{\{R_i, t_i\}, \{X_j\}} \sum_{i} \sum_{j} \rho\left( \left\| p_{ij} - \pi(K, R_i X_j + t_i) \right\|^2 \right)$$

### Module 08: Học sâu cho nhận diện vật thể trong Robot (Deep Learning for Robotic Perception & YOLO)
- **Đại học tham chiếu**: UC Berkeley (CS280), TUM (IN2064: Machine Learning).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 6 & Lernfeld 13.
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Mạng nơ-ron tích chập (*Convolutional Neural Networks - CNNs* / *Faltungsnetzwerke*): Trích xuất đặc trưng thứ bậc từ mức thấp (cạnh, góc) đến mức ngữ nghĩa cao (bộ phận, vật thể hoàn chỉnh).
  - Kiến trúc mạng dư (*Residual Networks - ResNet*): Khối kết nối tắt (*skip connections*) triệt tiêu hiện tượng triệt tiêu gradient (*vanishing gradient*) khi mạng sâu hàng trăm tầng.
  - Mô hình nhận diện vật thể đơn giai đoạn (*Single-Stage Object Detectors - YOLO / SSD*): Dự đoán đồng thời hộp bao giới hạn tọa độ (*bounding box regression*) và xác suất phân lớp đối tượng trong một lượt quét mạng nơ-ron duy nhất đạt tốc độ 30–60 FPS.
  - Chỉ số giao cắt trên hợp (*Intersection over Union - IoU* / *Jaccard-Index*) và phép lọc phi cực đại (*Non-Maximum Suppression - NMS*).
- **Công thức toán học cốt lõi (LaTeX)**:
  Chỉ số giao cắt trên hợp của hộp dự đoán $B_{pred}$ và hộp thực tế $B_{gt}$:
  $$\operatorname{IoU}(B_{pred}, B_{gt}) = \frac{\operatorname{Area}(B_{pred} \cap B_{gt})}{\operatorname{Area}(B_{pred} \cup B_{gt})}$$
  Hàm mất mát CIoU (*Complete IoU Loss*) bảo toàn tỉ lệ khung hình:
  $$\mathcal{L}_{CIoU} = 1 - \operatorname{IoU} + \frac{\rho^2(b, b^{gt})}{c^2} + \alpha v, \quad v = \frac{4}{\pi^2}\left( \arctan\frac{w^{gt}}{h^{gt}} - \arctan\frac{w}{h} \right)^2$$
  Hàm mất mát tổng thể đa nhiệm trong nhận diện vật thể:
  $$\mathcal{L}_{total} = \lambda_{box} \mathcal{L}_{CIoU} + \lambda_{cls} \mathcal{L}_{BCE} + \lambda_{dfl} \mathcal{L}_{DFL}$$

### Module 09: Nền tảng học tăng cường trong điều khiển Robot (Reinforcement Learning & Policy Gradients)
- **Đại học tham chiếu**: UC Berkeley (CS285: Deep Reinforcement Learning), MIT (16.410).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 (*Optimierung automatisierter Bewegungsprozesse*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Tiến trình quyết định Markov (*Markov Decision Process - MDP*): Bộ 5 thành phần $(\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)$.
  - Phương trình Bellman cho hàm giá trị trạng thái $V(s)$ và hàm giá trị hành động $Q(s, a)$.
  - Định lý Gradient chính sách (*Policy Gradient Theorem*): Tối ưu hóa trực tiếp các tham số của mạng nơ-ron chính sách $\pi_\theta(a \mid s)$ mà không cần mô hình chuyển trạng thái giải tích (*model-free*).
  - Thuật toán REINFORCE và kiến trúc Diễn viên - Trọng tài (*Actor-Critic* / *A2C*): Diễn viên cập nhật chính sách theo hướng dẫn từ lợi thế (*Advantage baseline*) của Trọng tài nhằm giảm phương sai ước lượng.
- **Công thức toán học cốt lõi (LaTeX)**:
  Định lý Gradient chính sách tổng quát:
  $$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t \mid s_t) \, Q^{\pi_\theta}(s_t, a_t) \right]$$
  Cập nhật Actor-Critic với hàm lợi thế sai phân thời gian TD (*Temporal Difference Advantage*):
  $$\nabla_\theta J(\theta) = \mathbb{E} \left[ \nabla_\theta \log \pi_\theta(a_t \mid s_t) \, \delta_t \right], \quad \delta_t = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$$
  Ước lượng lợi thế tổng quát hóa GAE (*Generalized Advantage Estimation*):
  $$\hat{A}_t^{GAE(\gamma, \lambda)} = \sum_{l=0}^\infty (\gamma \lambda)^l \delta_{t+l}^V$$

### Module 10: Học sâu tăng cường & Thao tác Robot Sim-to-Real (Deep RL for Manipulation & Sim-to-Real)
- **Đại học tham chiếu**: UC Berkeley (CS285), TUM (IN2064).
- **Chuẩn nghề nghiệp Đức**: DIHK Lernfeld 10 & Lernfeld 13 (*Inbetriebnahme mechatronischer Systeme*).
- **Nội dung lý thuyết & Bản chất vật lý**:
  - Học tăng cường sâu trong không gian hành động liên tục (*Continuous Action Spaces*): Thuật toán Proximal Policy Optimization (PPO) với hàm mục tiêu kẹp (*clipped surrogate objective*) và Soft Actor-Critic (SAC) tối đa hóa entropy.
  - Vấn đề khoảng cách thực tế - mô phỏng (*Reality Gap* / *Sim-to-Real Gap*): Sai số giữa mô hình vật lý giả lập (Gazebo, Isaac Sim, MuJoCo) và robot phần cứng thực tế (độ trễ chấp hành, phi tuyến ma sát, biến dạng đàn hồi).
  - Ngẫu nhiên hóa miền giá trị (*Domain Randomization*): Biến thiên ngẫu nhiên các tham số vật lý (khối lượng, hệ số ma sát, độ trễ tín hiệu, ánh sáng môi trường) trong môi trường mô phỏng để huấn luyện chính sách bền vững với thế giới thực.
- **Công thức toán học cốt lõi (LaTeX)**:
  Hàm mục tiêu cắt kẹp PPO (*PPO Clipped Surrogate Objective*):
  $$L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \, \operatorname{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t \right) \right]$$
  Với tỷ lệ xác suất chính sách mới trên chính sách cũ:
  $$r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$$
  Mục tiêu tối đa hóa Entropy trong Soft Actor-Critic (SAC):
  $$J(\pi) = \sum_{t=0}^T \mathbb{E}_{(s_t, a_t) \sim \rho_\pi} \left[ r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot \mid s_t)) \right]$$

---

## Phần 2: Danh mục tài liệu học thuật (Academic Reading List)

Danh mục các giáo trình kinh điển và tài liệu nghiên cứu quốc tế cốt lõi cho thị giác máy tính và học máy robot:

1. **Szeliski, Richard** (2022). *Computer Vision: Algorithms and Applications* (2nd Edition). Springer, Cham.
   - Trọng tâm nghiên cứu: Chương 2 (Image Formation - Quang học hình học và cảm biến), Chương 4 (Feature Detection and Matching - Trích xuất đặc trưng Harris, SIFT và đối sánh), Chương 7 (Structure from Motion - Tái tạo 3D từ chuỗi ảnh), Chương 11 (Dense Motion Estimation - Quang thông Optical Flow Lucas-Kanade).
2. **Hartley, Richard; Zisserman, Andrew** (2004). *Multiple View Geometry in Computer Vision* (2nd Edition). Cambridge University Press, Cambridge, UK.
   - Trọng tâm nghiên cứu: Chương 6 (Camera Models - Mô hình máy ảnh và ma trận chiếu $P$), Chương 9 (Epipolar Geometry and the Fundamental Matrix - Nền tảng hình học đối cực và ma trận cơ bản), Chương 11 (Computation of the Fundamental Matrix - Thuật toán 8 điểm chuẩn hóa), Chương 12 (Structure Computation - Phương pháp đạc tam giác tối ưu).
3. **Goodfellow, Ian; Bengio, Yoshua; Courville, Aaron** (2016). *Deep Learning*. MIT Press, Cambridge, MA.
   - Trọng tâm nghiên cứu: Chương 6 (Deep Feedforward Networks - Nền tảng mạng nơ-ron truyền thẳng), Chương 9 (Convolutional Networks - Tích chập không gian và kiến trúc CNN), Chương 14 (Autoencoders - Trích xuất đặc trưng không giám sát).
4. **Sutton, Richard S.; Barto, Andrew G.** (2018). *Reinforcement Learning: An Introduction* (2nd Edition). MIT Press, Cambridge, MA.
   - Trọng tâm nghiên cứu: Chương 3 (Finite Markov Decision Processes - Tiến trình quyết định Markov), Chương 6 (Temporal-Difference Learning - Học sai phân thời gian $TD(\lambda)$), Chương 13 (Policy Gradient Methods - Định lý gradient chính sách và REINFORCE).
5. **Forsyth, David A.; Ponce, Jean** (2011). *Computer Vision: A Modern Approach* (2nd Edition). Pearson, Boston, MA.
   - Trọng tâm nghiên cứu: Chương 1 (Cameras - Quang học hình học), Chương 4 (Linear Filters - Lọc tuyến tính và làm mịn Gauss), Chương 5 (Local Image Features - Nhận diện điểm đặc trưng), Chương 7 (Stereopsis - Thị giác nổi hai mắt).
6. **Scaramuzza, Davide; Fraundorfer, Friedrich** (2011). *Visual Odometry: Part I and Part II*. IEEE Robotics & Automation Magazine, Vol. 18, No. 4, pp. 80-92 & Vol. 19, No. 1, pp. 78-91.
   - Trọng tâm nghiên cứu: Tổng quan toàn diện về thuật toán đo đạc thị giác cho robot di động, từ tiền xử lý ảnh, trích xuất đặc trưng, giải phương trình hình học đối cực đến tối ưu hóa Bundle Adjustment cục bộ.
7. **Lowe, David G.** (2004). *Distinctive Image Features from Scale-Invariant Keypoints*. International Journal of Computer Vision (IJCV), Vol. 60, No. 2, pp. 91-110.
   - Trọng tâm nghiên cứu: Thuật toán SIFT trích xuất vector đặc trưng bất biến tỷ lệ, xoay và thay đổi cường độ sáng; kỹ thuật định vị cực trị không gian tỷ lệ Difference-of-Gaussians.
8. **Schulman, John; Wolski, Filip; Dhariwal, Prafulla; Radford, Alec; Klimov, Oleg** (2017). *Proximal Policy Optimization Algorithms*. arXiv preprint arXiv:1707.06347.
   - Trọng tâm nghiên cứu: Thuật toán PPO với cơ chế kẹp hàm mất mát chính sách nhằm ổn định quá trình huấn luyện điều khiển robot liên tục.

---

## Phần 3: Bài tập thực hành & Project mô phỏng (Practical Labs & Simulation Projects)

Hệ thống 3 đồ án thực hành thiết kế tối ưu trên máy tính xách tay macOS (Intel Core i5, 8GB RAM), vận hành hoàn toàn trên thư viện chuẩn của Python hoặc môi trường tính toán nhẹ.

### Lab 01: Hiệu chuẩn máy ảnh & Nắn thẳng méo thấu kính Brown-Conrady (Camera Calibration & Lens Undistortion)
- **Mục tiêu kỹ thuật**:
  - Lập trình bộ nắn ảnh méo quang học bằng phương pháp ánh xạ tọa độ ngược (*inverse coordinate mapping*).
  - Áp dụng các hệ số méo hướng tâm $k_1 = -0.15, k_2 = 0.02$ và tiêu cự $f_x = 800, f_y = 800, c_x = 320, c_y = 240$.
  - Tính toán bảng ánh xạ pixel $(u_d, v_d) \to (u, v)$ và nội suy song tuyến tính (*bilinear interpolation*) giá trị độ xám.
- **Phương pháp thực thi**:
  1. Xây dựng lưới tọa độ chuẩn hóa từ kích thước cảm biến $640 \times 480$.
  2. Áp dụng mô hình đa thức Brown-Conrady để tính độ dời bán kính $r^2$.
  3. Lập bản đồ ánh xạ và kiểm tra sự thẳng hàng của các đường thẳng thực tế (như mép bàn, góc tường) sau khi nắn méo.
  4. Đánh giá sai số độ thẳng đường biên trước và sau khi bù méo quang học.
- **Tiêu chí nghiệm thu**: Sai số độ cong đường thẳng sau khi nắn $< 0.5$ pixel; thời gian nắn toàn khung hình $< 30$ ms.

### Lab 02: Trích xuất đặc trưng Harris & Đối sánh ảnh hai mắt (Harris Feature Matching & Epipolar Geometry)
- **Mục tiêu kỹ thuật**:
  - Hiện thực hóa toàn diện ma trận cấu trúc ten-sơ bậc hai $M$ trên mảng ảnh 2D.
  - Tính toán đáp ứng góc Harris $R = \det(M) - 0.04(\operatorname{Tr}(M))^2$ và áp dụng lọc triệt tiêu cực đại cục bộ trong cửa sổ $5 \times 5$.
  - Trích xuất vector mô tả cường độ sáng xung quanh điểm góc, đối sánh tương quan chéo chuẩn hóa (*Normalized Cross Correlation - NCC*).
  - Vẽ đường đối cực (*epipolar lines*) tương ứng trên ảnh thứ hai $l_2 = F p_1$ và xác minh khoảng cách từ điểm đối sánh tới đường đối cực.
- **Phương pháp thực thi**:
  1. Tạo hai góc nhìn mô phỏng của một bàn thao tác cơ điện tử.
  2. Áp dụng mặt nạ Sobel tính đạo hàm không gian ngang $I_x$ và đứng $I_y$.
  3. Lọc ngưỡng phản hồi Harris và giữ lại 50 điểm đặc trưng có năng lượng cao nhất.
  4. Đối sánh tương quan chéo giữa hai ảnh và vẽ biểu đồ phân bố sai số đối cực.
- **Tiêu chí nghiệm thu**: Tỷ lệ đối sánh đúng (*Inlier Ratio*) $> 80\%$; khoảng cách đối cực trung bình $< 1.0$ pixel.

### Lab 03: Mô phỏng chiếu Pinhole, Méo quang học, Đáp ứng Harris & Triangulation 3D (`labs/lab06_vision_feature.py`)
- **Mục tiêu kỹ thuật**:
  - Triển khai toàn bộ đường ống xử lý hình học máy ảnh và đặc trưng thị giác trong file chuẩn độc lập `labs/lab06_vision_feature.py` chỉ sử dụng thư viện chuẩn của Python (`math`, `random`, `time`).
  - **Mô hình máy ảnh Pinhole**: Chiếu 8 điểm mốc không gian 3D dạng khối lập phương từ khoảng cách $Z \in [1.5, 3.2]$ mét lên cảm biến máy ảnh, áp dụng méo hướng tâm thùng ($k_1 = -0.12, k_2 = 0.015$).
  - **Phát hiện góc Harris**: Đánh giá trên 3 mảng ảnh nhân tạo điển hình: Miền góc (Corner patch), Miền cạnh (Edge patch), và Miền đồng nhất phẳng (Flat patch) để kiểm chứng tính chất toán học của đáp ứng $R$.
  - **Hình học đối cực & Đạc tam giác**: Thiết lập cặp máy ảnh stereo với khoảng cách cơ sở $t_x = -0.20$ m và góc xoay yaw $2.5^\circ$, tính toán Ma trận thiết yếu $E = [t]_\times R$, kiểm chứng phương trình $x_2^T E x_1 = 0$, và khôi phục tọa độ không gian 3D bằng công thức nghiệm kín đạc tam giác tia đối cực.
  - Tối ưu hóa hiệu năng: Toàn bộ quá trình tính toán hoàn thành trong thời gian $< 5$ ms trên CPU Intel Core i5 của máy Mac.
- **Lệnh thực thi & Kiểm chứng**:
  ```bash
  python3 /Users/trangiaphat/Documents/Inbox_HocTap/03_Mechatronics_Knowledge_Base/labs/lab06_vision_feature.py
  ```
- **Kết quả định lượng chuẩn**:
  - Độ dịch chuyển do méo thấu kính: $1.300$ pixels tại biên ảnh.
  - Đáp ứng góc Harris: Góc $R = +2.0154 \times 10^3 > 0$, Cạnh $R = -1.0240 \times 10^3 < 0$, Mặt phẳng $R \approx 0.0$.
  - Sai số đối cực đại số cực đại: $6.9389 \times 10^{-18} \approx 0.0$ (chính xác đến giới hạn số thực kép máy tính).
  - Sai số tái tạo 3D RMSE: $0.000000$ mm (khôi phục hoàn hảo tọa độ mốc).
  - Thời gian thực thi toàn bộ script: $\approx 0.33$ ms.

---

## Phần 4: Từ khóa tìm kiếm & Thuật ngữ Anh-Đức (Exact Search Queries & Bilingual Terminology Table)

### Danh sách từ khóa tìm kiếm chuyên sâu (Precision Academic Search Queries)

Các truy vấn tìm kiếm độ chính xác cao phục vụ tra cứu tài liệu học thuật và mã nguồn chuẩn công nghiệp:

1. `"multiple view geometry" "essential matrix" "epipolar constraint" filetype:pdf`
2. `"pinhole camera model" "radial distortion" "brown conrady" site:ethz.ch`
3. `"normalized 8-point algorithm" "Hartley" "singular value decomposition" filetype:pdf`
4. `"harris corner detector" "second moment matrix" "structure tensor" filetype:pdf`
5. `"visual odometry" "tutorial" "Scaramuzza" "Fraundorfer" filetype:pdf`
6. `"Lucas-Kanade optical flow" "pyramidal implementation" filetype:pdf`
7. `"policy gradient theorem" "reinforce" "Sutton" "Barto" filetype:pdf`
8. `"actor critic" "continuous action space" "robotics" site:berkeley.edu`
9. `"sim-to-real transfer" "domain randomization" "robot manipulation" site:arxiv.org`
10. `"deep visual servoing" "convolutional neural network" filetype:pdf`
11. `"bundle adjustment" "ceres solver" "levenberg marquardt" site:github.com`
12. `"YOLOv8 architecture" "anchor free" "robot perception" site:github.com`
13. `"Zhang's camera calibration" "planar pattern" "homography" filetype:pdf`
14. `"proximal policy optimization" "clipped objective" "Schulman" filetype:pdf`
15. `"stereo vision" "disparity map" "semi global matching" site:tum.de`

### Bảng đối chiếu thuật ngữ chuyên ngành Anh - Đức - Việt

Bảng thuật ngữ đối chiếu 3 thứ tiếng chuẩn hóa theo tiêu chuẩn công nghiệp CHLB Đức (DIN EN ISO 8373, DIN 4522, ISO 12233, DIN ISO 9039) và chương trình đào tạo nghề kép DIHK/AHK:

| English Term | German Fachbegriff (DIN/ISO) | Tiếng Việt (Chuyên ngành) | Tiêu chuẩn / Chuẩn hóa |
|---|---|---|---|
| Computer Vision | Industrielle Bildverarbeitung | Thị giác máy tính / Xử lý ảnh công nghiệp | DIN EN ISO 8373 |
| Pinhole Camera Model | Lochkameramodell | Mô hình máy ảnh lỗ kim | Quang học hình học |
| Focal Length | Brennweite | Tiêu cự quang học của ống kính | DIN 4522 |
| Principal Point | Hauptpunkt (Bildmittelpunkt) | Điểm chính quang học trên mặt cảm biến | ISO 12233 |
| Radial Lens Distortion | Radiale Linsenverzerrung | Độ méo quang học hướng tâm | DIN ISO 9039 |
| Tangential Distortion | Tangentiale Linsenverzerrung | Độ méo quang học tiếp tuyến | DIN ISO 9039 |
| Essential Matrix | Wesentliche Matrix (Essential-Matrix) | Ma trận thiết yếu | Hình học đa góc nhìn |
| Fundamental Matrix | Fundamentalmatrix | Ma trận cơ bản | ISO 19288 |
| Epipolar Geometry | Epipolargeometrie | Hình học đối cực | Thị giác máy tính 3D |
| Feature Point / Keypoint | Merkmalspunkt (Schlüsselpunkt) | Điểm đặc trưng ảnh | Xử lý tín hiệu hình ảnh |
| Feature Descriptor | Merkmalsdeskriptor | Vector mô tả đặc trưng | AI & Xử lý ảnh |
| Feature Matching | Merkmalsabgleich | Đối sánh điểm đặc trưng | Thị giác máy tự động |
| Visual Odometry (VO) | Visuelle Odometrie | Đo đạc cự ly thị giác (Định vị camera) | IEEE Robotics & Automation |
| Triangulation | Triangulation (3D-Rückprojektion) | Phương pháp đạc tam giác không gian 3D | Đo đạc quang học |
| 2D Spatial Convolution | 2D-Bildfaltung | Tích chập không gian 2D | Xử lý tín hiệu số |
| Reinforcement Learning | Bestärkendes Lernen | Học tăng cường | Trí tuệ nhân tạo |
| Policy Gradient | Richtliniengradient | Gradient của hàm chính sách | Học máy điều khiển |
| Multiple View Geometry | Mehransichtsgeometrie | Hình học đa góc nhìn | Thị giác máy tính |
| Optical Flow | Optischer Fluss | Quang thông (Dòng chuyển động quang học) | Xử lý video số |
| Bundle Adjustment | Bündelausgleichung | Tối ưu hóa chùm tia không gian | Đo đạc ảnh & Trắc địa |
| Homography Matrix | Homographie-Matrix | Ma trận đồng hình phẳng | Biến đổi xạ ảnh |
| Reprojection Error | Rückprojektionsfehler | Sai số chiếu ngược không gian | Tối ưu hóa thị giác 3D |
