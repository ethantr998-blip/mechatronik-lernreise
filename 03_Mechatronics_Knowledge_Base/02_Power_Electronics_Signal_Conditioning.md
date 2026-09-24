# Subsystem 02: Power Electronics & Signal Conditioning
## Điện tử công suất, Mạch tương tự/số & Xử lý tín hiệu cảm biến

Tài liệu này cấu thành gói tri thức chuẩn mực cấp đại học (*University-Grade Knowledge Package*) cho Phân hệ 02: **Điện tử công suất, Mạch tương tự/số & Xử lý tín hiệu cảm biến** (*Leistungselektronik, Schaltungstechnik und Sensorsignalaufbereitung*) trong kỹ thuật Cơ điện tử. Toàn bộ nội dung được tổng hợp và chuẩn hóa từ chương trình đào tạo của các viện đại học công nghệ hàng đầu: **MIT** (6.302 Feedback Systems / Power Electronics, 6.002 Circuits and Electronics), **ETH Zürich** (227-0247-00L Power Electronics), **UC Berkeley** (EE192 Mechatronic Design Laboratory), và **TU München (TUM)**. Đồng thời, tài liệu được tích hợp chặt chẽ với khung chương trình đào tạo nghề kép CHLB Đức theo chuẩn **DIHK / AHK** (*Rahmenlehrplan für den Ausbildungsberuf Mechatroniker*):
- **Lernfeld 3 (LF3)**: *Montieren und Anschließen elektrischer Betriebsmittel* (Lắp ráp, đấu nối khí cụ điện, linh kiện bán dẫn công suất, mạch cầu công suất và kiểm tra an toàn theo DIN VDE 0100).
- **Lernfeld 4 (LF4)**: *Messen und Analysieren elektrischer Funktionen in mechatronischen Systemen* (Đo lường và phân tích hàm điện, mạch khuếch đại thuật toán, lọc tín hiệu cảm biến, kỹ thuật đo bằng dao động ký).
- **Lernfeld 8 (LF8)**: *Auswählen und Integrieren von Antrieben* (Lựa chọn và tích hợp hệ thống truyền động điện, điều chế PWM, biến tần).

---

## 1. Standardized Syllabus Breakdown (Đề cương chuẩn hóa 12 tuần chuyên sâu)

### Module 01: Electrical Network Analysis & Impedance Matching (Phân tích mạng điện & Phối hợp trở kháng)
- **Mã môn tham chiếu**: MIT 6.002 (Bài 1–4), UC Berkeley EE192.
- **Khung năng lực Đức**: DIHK LF4 — Phân tích mạch điện và phối hợp trở kháng chống suy hao tín hiệu đo lường (*Netzwerkanalyse und Impedanzanpassung*).
- **Nội dung lý thuyết (First Principles)**:
  - Định luật dòng điện Kirchhoff (KCL: $\sum I_{in} = \sum I_{out}$) và định luật điện áp Kirchhoff (KVL: $\sum V_{loop} = 0$).
  - Định lý Thévenin và Norton: Mọi mạng điện tuyến tính chứa nguồn và điện trở đều có thể rút gọn thành một nguồn áp Thévenin $V_{th} = V_{oc}$ nối tiếp với trở kháng Thévenin $R_{th} = V_{oc} / I_{sc}$, hoặc nguồn dòng Norton $I_N = I_{sc}$ song song với $R_N = R_{th}$.
  - Hiệu ứng tải tín hiệu đo lường (*Loading Effect*): Khi cảm biến có trở kháng nội $Z_{out}$ nối vào mạch thu nhận có trở kháng vào $Z_{in}$, điện áp đo được bị suy giảm theo mạch phân áp:
    $$V_{meas} = V_{sensor} \left( \frac{Z_{in}}{Z_{in} + Z_{out}} \right)$$
    Để giảm thiểu sai số đo lường xuống dưới $0.1\%$, điều kiện bắt buộc đối với cảm biến điện áp là:
    $$Z_{in} \ge 1000 \cdot Z_{out}$$
  - Phối hợp truyền công suất cực đại (*Maximum Power Transfer Theorem*): Trong các mạch truyền dẫn xung vô tuyến hoặc truyền lực cao tần, công suất truyền cực đại đạt được khi trở kháng tải là liên hợp phức của trở kháng nguồn: $Z_L = Z_S^*$.
- **Bản chất vật lý & Ứng dụng**: Thiết kế tầng đệm đầu vào cho cảm biến áp điện (*Piezoelectric*) có trở kháng ra rất lớn ($\sim \text{M}\Omega$) nhằm tránh suy sụp biên độ điện áp đo.

### Module 02: Operational Amplifiers: Fundamentals & Real Non-Idealities (Khuếch đại thuật toán & Các phi lý tưởng thực tế)
- **Mã môn tham chiếu**: MIT 6.002 (Bài 18–20), Alciatore Chương 2, TU München.
- **Khung năng lực Đức**: DIHK LF4 — Lựa chọn và kiểm tra mạch tích hợp khuếch đại thuật toán công nghiệp (*Operationsverstärker-Kenngrößen und Reale Nichtidealitäten*).
- **Nội dung lý thuyết (First Principles)**:
  - Khuếch đại thuật toán lý tưởng (*Ideal Op-Amp / Idealer OPV*):
    - Trở kháng đầu vào vi sai vô cùng lớn: $Z_{in} \to \infty \implies I_+ = I_- = 0$.
    - Trở kháng đầu ra bằng không: $Z_{out} \to 0$.
    - Hệ số khuếch đại vòng hở vô cùng lớn: $A_{OL} \to \infty$.
    - Nguyên lý đất ảo (*Virtual Ground / Virtuelle Masse*): Trong cấu hình hồi tiếp âm (*Negative Feedback*), hiệu điện áp vi sai giữa hai cổng vào triệt tiêu: $v_+ - v_- = 0 \implies v_+ = v_-$.
  - Các thông số phi lý tưởng trong OPV thực tế:
    1. Điện áp bù điểm không đầu vào (*Input Offset Voltage* $V_{os}$): Sai lệch điện áp giữa 2 ngõ vào khi điện áp ra bằng 0 ($1-5\,\text{mV}$ với Op-Amp thông dụng như LM358, $< 10\,\mu\text{V}$ với dòng Zero-Drift/Chopper).
    2. Dòng phân cực đầu vào (*Input Bias Current* $I_B$) và dòng bù (*Input Offset Current* $I_{os} = |I_+ - I_-|$): Gây ra sụt áp ký sinh trên điện trở hồi tiếp.
    3. Tốc độ tăng điện áp tối đa (*Slew Rate* $\text{SR}$):
       $$\text{SR} = \max \left| \frac{dv_{out}(t)}{dt} \right| \quad [\text{V}/\mu\text{s}]$$
       Để tín hiệu hình sin biên độ đỉnh $V_p$ tần số $f$ không bị méo dạng tam giác:
       $$\text{SR} \ge 2\pi f V_p$$
    4. Tích hệ số khuếch đại - dải thông (*Gain-Bandwidth Product* $\text{GBW}$):
       $$\text{GBW} = A_v \cdot f_{cutoff} = \text{const}$$
       Nếu khuếch đại tín hiệu dải tần $100\,\text{kHz}$ với hệ số $A_v = 100$, Op-Amp phải có $\text{GBW} \ge 10\,\text{MHz}$.
- **Bản chất vật lý & Ứng dụng**: Phân tích giới hạn dải thông và độ méo biên độ khi khuếch đại tín hiệu xung encoder tốc độ cao trong công nghiệp.

### Module 03: Linear Op-Amp Topologies & Signal Conditioning Stages (Các cấu hình OPV tuyến tính & Mạch chuẩn hóa tín hiệu)
- **Mã môn tham chiếu**: MIT 6.302, Horowitz & Hill Chương 4.
- **Khung năng lực Đức**: DIHK LF4 — Thiết kế và hiệu chuẩn mạch khuếch đại điều hòa tín hiệu đo (*Lineare OPV-Grundschaltungen und Sensorschnittstellen*).
- **Nội dung lý thuyết (First Principles)**:
  - Mạch khuếch đại đảo (*Inverting Amplifier*):
    $$V_{out} = -\frac{R_f}{R_{in}} V_{in}, \quad Z_{in} = R_{in}$$
  - Mạch khuếch đại không đảo (*Non-Inverting Amplifier*):
    $$V_{out} = \left( 1 + \frac{R_f}{R_1} \right) V_{in}, \quad Z_{in} \approx \infty$$
  - Tầng đệm điện áp (*Voltage Follower / Pufferverstärker*): $R_f = 0, R_1 = \infty \implies V_{out} = V_{in}$. Trở kháng vào vô cùng lớn, trở kháng ra xấp xỉ bằng không, đóng vai trò cách ly tải hoàn hảo.
  - Mạch khuếch đại cộng đại số (*Summing Amplifier*):
    $$V_{out} = -R_f \left( \frac{V_1}{R_1} + \frac{V_2}{R_2} + \dots + \frac{V_n}{R_n} \right)$$
  - Mạch trừ vi sai một OPV (*Differential Subtractor*):
    $$V_{out} = \frac{R_2}{R_1} (V_2 - V_1) \quad (\text{khi } R_1 = R_3 \text{ và } R_2 = R_4)$$
    Nếu tỷ số điện trở sai lệch $\Delta R / R$, tỉ số triệt méo đồng pha (CMRR) bị suy giảm nghiêm trọng:
    $$\text{CMRR} \approx \frac{1 + A_d}{4 (\Delta R / R)}$$
    Ví dụ, với dung sai điện trở $1\%$ ($\Delta R / R = 0.01$) và độ lợi $A_d = 1$, $\text{CMRR}$ chỉ đạt khoảng $50 \implies 34\,\text{dB}$, không đủ triệt tiêu nhiễu trong môi trường công nghiệp.
- **Bản chất vật lý & Ứng dụng**: Chuyển đổi và nâng mức dải tín hiệu từ cảm biến nhiệt độ PT100 hoặc cảm biến quang ($0-50\,\text{mV}$) lên dải $0-3.3\,\text{V}$ phù hợp cho cổng vào ADC của vi điều khiển.

### Module 04: Instrumentation Amplifiers & Common-Mode Rejection (Khuếch đại đo lường & Triệt méo đồng pha CMRR)
- **Mã môn tham chiếu**: UC Berkeley EE192, Horowitz & Hill Chương 5.
- **Khung năng lực Đức**: DIHK LF4 — Đo lường điện áp vi sai nhỏ trong cầu điện trở Wheatstone (*Instrumentierungsverstärker und Wheatstone-Messbrücke*).
- **Nội dung lý thuyết (First Principles)**:
  - Cấu trúc khuếch đại đo lường kinh điển 3-OpAmp (Classic 3-OpAmp Instrumentation Amplifier):
    - Tầng đầu vào gồm hai OPV không đảo đóng vai trò bộ đệm với trở kháng vào cực lớn ($Z_{in} > 10^{10}\,\Omega$), khuếch đại điện áp vi sai với hệ số lớn nhưng chỉ truyền điện áp đồng pha với hệ số bằng 1.
    - Một điện trở cài đặt độ lợi duy nhất $R_G$ (*Gain Resistor*) quyết định hệ số khuếch đại tầng đầu:
      $$V_{o1} - V_{o2} = \left( 1 + \frac{2 R_1}{R_G} \right) (V_1 - V_2)$$
    - Tầng thứ hai là mạch vi sai chuẩn xác với các điện trở nội được khắc laser chính xác cao ($R_2 = R_3$):
      $$V_{out} = \left( 1 + \frac{2 R_1}{R_G} \right) \frac{R_3}{R_2} (V_2 - V_1)$$
  - Tỉ số triệt méo đồng pha (*Common-Mode Rejection Ratio* $\text{CMRR}$):
    $$\text{CMRR} = 20 \log_{10} \left( \frac{|A_d|}{|A_{cm}|} \right) \quad [\text{dB}]$$
    trong đó $A_d$ là độ lợi vi sai, $A_{cm}$ là độ lợi đồng pha. Các IC chuyên dụng (như INA128, AD620) đạt $\text{CMRR} > 100-120\,\text{dB}$, cho phép loại bỏ nhiễu đồng pha biên độ vài volt đè lên tín hiệu vi sai cấp millivolt.
  - Cầu đo điện trở Wheatstone (*Wheatstone Bridge*): Tín hiệu vi sai sinh ra khi biến dạng cảm biến đo lực (*Strain Gauge / Wägezelle*):
    $$\Delta V = V_{exc} \left( \frac{GF \cdot \epsilon}{4} \right)$$
    với $V_{exc}$ là điện áp kích thích cầu, $GF$ là hệ số cảm biến lực (*Gauge Factor*), và $\epsilon$ là độ biến dạng cơ học.
- **Bản chất vật lý & Ứng dụng**: Thu thập tín hiệu lực nén/kéo trong bàn kẹp robot công nghiệp, triệt tiêu hoàn toàn sóng nhiễu 50 Hz cảm ứng từ lưới điện nhà xưởng.

### Module 05: Passive & Active Analog Filter Design (Thiết kế mạch lọc tương tự thụ động & tích cực)
- **Mã môn tham chiếu**: MIT 6.302, ETH Zürich 227-0247-00L, Franco Chương 3.
- **Khung năng lực Đức**: DIHK LF4 — Thiết kế và lắp ráp bộ lọc triệt tiêu sóng hài biến tần (*Passive und aktive analoge Filterschaltungen*).
- **Nội dung lý thuyết (First Principles)**:
  - Bộ lọc thụ động RC bậc 1 (*1st-Order Passive Low-Pass*):
    $$H(s) = \frac{1}{1 + sRC}, \quad f_c = \frac{1}{2\pi RC}, \quad \text{Độ dốc suy hao: } -20\,\text{dB/decade}$$
  - Mạch lọc tích cực Sallen-Key bậc 2 (*2nd-Order Sallen-Key Low-Pass*):
    $$H(s) = \frac{K \omega_0^2}{s^2 + \frac{\omega_0}{Q} s + \omega_0^2}$$
    Tần số tự nhiên $\omega_0$ và hệ số phẩm chất $Q$:
    $$\omega_0 = \frac{1}{\sqrt{R_1 R_2 C_1 C_2}}, \quad Q = \frac{\sqrt{R_1 R_2 C_1 C_2}}{C_2(R_1 + R_2) + R_1 C_1 (1 - K)}$$
    Độ dốc suy hao dải chặn đạt $-40\,\text{dB/decade}$.
  - So sánh các họ đa thức xấp xỉ hàm truyền kinh điển:
    1. **Butterworth**: Đáp ứng biên độ phẳng cực đại ở dải thông (*Maximally Flat*), $Q = 1/\sqrt{2} \approx 0.7071$, không có gợn sóng (*No Ripple*).
    2. **Chebyshev**: Độ dốc chuyển tiếp từ dải thông sang dải chặn rất dốc, nhưng tồn tại gợn sóng biên độ (*Passband Ripple*), méo pha lớn.
    3. **Bessel-Thomson**: Đáp ứng trễ nhóm phẳng tối đa (*Maximally Flat Group Delay*), pha biến thiên tuyến tính theo tần số, bảo toàn hình dạng xung tín hiệu mà không bị vọt lố chuông dao động (*No Ringing*).
  - Phương pháp rời rạc hóa Bilinear Transform với biến dạng tần số (*Pre-warping*):
    $$s = \frac{2}{T_s} \left( \frac{1 - z^{-1}}{1 + z^{-1}} \right), \quad \omega_a = \frac{2}{T_s} \tan\left(\frac{\omega_c T_s}{2}\right)$$
- **Bản chất vật lý & Ứng dụng**: Làm tầng lọc tiền xử lý chống chồng phổ (*Anti-Aliasing Filter*) trước bộ chuyển đổi ADC, triệt tiêu xung nhiễu đóng cắt PWM tần số cao của biến tần.

### Module 06: Analog-to-Digital Conversion (ADC) & Quantization Dynamics (Chuyển đổi tương tự - số ADC & Động học lượng tử hóa)
- **Mã môn tham chiếu**: MIT 6.002, Alciatore Chương 2, Kester (Analog Devices).
- **Khung năng lực Đức**: DIHK LF4 — Cấu hình và lập trình bộ biến đổi tín hiệu tương tự sang số trên vi điều khiển (*Analog-Digital-Umsetzer und Signalquantisierung*).
- **Nội dung lý thuyết (First Principles)**:
  - Định lý lấy mẫu Nyquist-Shannon: Để khôi phục hoàn toàn tín hiệu tương tự liên tục dải thông $f_{max}$ mà không bị hiện tượng chồng phổ (*Aliasing*), tần số lấy mẫu phải thỏa mãn:
    $$f_s \ge 2 f_{max}$$
  - Kích thước bước lượng tử hóa (*Quantization Step / LSB*):
    $$q = \text{LSB} = \frac{V_{ref}}{2^N}$$
    với $V_{ref}$ là điện áp chuẩn và $N$ là số bit độ phân giải của ADC.
  - Mô hình nhiễu lượng tử hóa: Sai số lượng tử hóa $e = v_{in} - v_{quant}$ được coi là đại lượng ngẫu nhiên phân bố đều trong khoảng $[-q/2, +q/2]$.
    Phương sai công suất nhiễu lượng tử:
    $$\sigma_e^2 = \frac{1}{q} \int_{-q/2}^{q/2} e^2 de = \frac{q^2}{12}$$
  - Tỉ số tín hiệu trên nhiễu lý thuyết cực đại (*Theoretical Maximum SNR*): Đối với tín hiệu sin đầy dải (*Full-scale sine wave* $V_{peak} = V_{ref}/2$):
    $$P_{signal} = \frac{V_{peak}^2}{2} = \frac{(2^N q / 2)^2}{2} = \frac{2^{2N} q^2}{8}$$
    $$\text{SNR}_{ideal} = 10 \log_{10}\left( \frac{P_{signal}}{\sigma_e^2} \right) = 10 \log_{10}\left( \frac{3}{2} \cdot 2^{2N} \right) = 6.02 N + 1.76 \quad [\text{dB}]$$
  - Số bit hiệu dụng thực tế (*Effective Number of Bits* $\text{ENOB}$):
    $$\text{ENOB} = \frac{\text{SINAD} - 1.76}{6.02}$$
    trong đó $\text{SINAD}$ là tỉ số tín hiệu trên tổng tạp âm và méo hài (*Signal-to-Noise-and-Distortion*).
  - So sánh kiến trúc ADC:
    - **SAR (Successive Approximation Register)**: Tốc độ trung bình-cao ($1-5\,\text{MSPS}$), độ trễ thấp (1 chu kỳ), 12-16 bit, phổ biến trên STM32/ARM Cortex.
    - **Delta-Sigma ($\Delta\Sigma$)**: Tốc độ lấy mẫu quá mức (*Oversampling*), độ phân giải rất cao (16-24 bit), lọc nhiễu số mạnh, dùng cho cân điện tử và cảm biến âm học.
    - **Flash ADC**: Tốc độ cực cao ($> 1\,\text{GSPS}$), kiến trúc $2^N-1$ bộ so sánh song song, tiêu thụ công suất lớn, dùng trong radar/viễn thông.
- **Bản chất vật lý & Ứng dụng**: Phân tích sàn nhiễu ADC trên bo mạch nhúng, tính toán số mẫu trung bình giải thuật toán (*Oversampling & Decimation*) để tăng độ phân giải từ 12-bit lên 14-bit thực tế.

### Module 07: Power Semiconductor Switches: MOSFETs & IGBTs (Khóa chuyển mạch bán dẫn công suất)
- **Mã môn tham chiếu**: ETH Zürich 227-0247-00L (Bài 2–4), Mohan Chương 20–22, TU München.
- **Khung năng lực Đức**: DIHK LF3 — Lắp ráp, tản nhiệt và kiểm tra linh kiện bán dẫn công suất theo DIN EN 60747 (*Leistungshalbleiter: Leistungs-MOSFETs und IGBTs*).
- **Nội dung lý thuyết (First Principles)**:
  - Power MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor): Khóa bán dẫn điều khiển bằng điện áp cực cổng ($V_{GS}$), hạt dẫn đa số (electron trên kênh N), tốc độ đóng cắt siêu nhanh ($f_{sw} > 20 - 500\,\text{kHz}$).
    - Điện trở dẫn thuần trở $R_{DS(on)}$: Có hệ số nhiệt dương (*Positive Temperature Coefficient*), cho phép mắc song song trực tiếp nhiều MOSFET mà không sợ mất cân bằng nhiệt cục bộ.
    - Tổn hao công suất dẫn tĩnh (*Conduction Loss*):
      $$P_{cond} = I_{D,rms}^2 R_{DS(on)}$$
    - Tổn hao công suất đóng cắt động (*Switching Loss*): Do sự chồng lấn đồng thời giữa điện áp $V_{DS}$ và dòng điện $I_D$ trong quá trình mở ($t_r$) và ngắt ($t_f$):
      $$P_{sw} = \frac{1}{2} V_{DS} I_D (t_r + t_f) f_{sw}$$
    - Các điện dung ký sinh: $C_{iss} = C_{GS} + C_{GD}$, $C_{oss} = C_{DS} + C_{GD}$, $C_{rss} = C_{GD}$ (Điện dung phản hồi Miller).
  - IGBT (Insulated Gate Bipolar Transistor): Cấu trúc lai giữa cổng điều khiển cách ly MOSFET và tầng dẫn dòng BJT hạt dẫn thiểu số.
    - Thích hợp cho điện áp cao ($> 600\,\text{V}$) và dòng điện lớn ($> 50\,\text{A}$).
    - Điện áp rơi thuận bão hòa tương đối cố định $V_{CE(sat)} \approx 1.5 - 2.5\,\text{V}$, tổn hao dẫn tĩnh:
      $$P_{cond,IGBT} = V_{CE0} I_{C,avg} + r_c I_{C,rms}^2$$
    - Hiện tượng đuôi dòng ngắt (*Current Tail*): Do sự tái hợp chậm của hạt dẫn thiểu số trong lớp đế, giới hạn tần số đóng cắt dưới $20-30\,\text{kHz}$.
  - Vùng làm việc an toàn (*Safe Operating Area* SOA): Giới hạn dòng điện cực đại, điện áp đánh thủng $V_{(BR)DSS}$, và giới hạn tản nhiệt phá hủy thứ cấp (*Thermal Instability*).
- **Bản chất vật lý & Ứng dụng**: Tính toán nhiệt trở hệ thống tản nhiệt $R_{\theta JA} = R_{\theta JC} + R_{\theta CH} + R_{\theta HA}$ đảm bảo nhiệt độ mối nối bán dẫn $T_J \le 125^\circ\text{C}$ khi điều khiển động cơ 24V/15A.

### Module 08: Gate Driver Circuits & Bootstrap Topologies (Mạch kích cực cổng & Cấu hình Bootstrap)
- **Mã môn tham chiếu**: ETH Zürich 227-0247-00L, UC Berkeley EE192.
- **Khung năng lực Đức**: DIHK LF3 — Thiết kế mạch lái cách ly galvanic bảo vệ cổng vi điều khiển (*Gate-Treiber-Schaltungen und Bootstrap-Versorgung*).
- **Nội dung lý thuyết (First Principles)**:
  - Để đóng mở hoàn toàn MOSFET công suất kênh N phía cao (*High-Side Switch*), điện áp cực cổng phải cao hơn điện áp cực nguồn một khoảng $V_{GS} \ge 10 - 12\,\text{V}$. Nhưng khi van phía cao dẫn thông, chân nguồn $S$ bị kéo lên điện áp thanh cái $V_{DC}$, do đó cực cổng cần điện áp cấp nổi $V_G = V_{DC} + V_{GS}$.
  - Mạch nguồn nổi Bootstrap (*Bootstrap Supply Circuit*):
    - Hoạt động theo 2 pha chu kỳ: Khi khóa phía thấp dẫn, chân nguồn $S$ nối mass, tụ bootstrap $C_{boot}$ được nạp điện từ nguồn phụ $V_{CC}$ (12V) qua đi-ốt bootstrap $D_{boot}$. Khi khóa phía cao đóng, tụ $C_{boot}$ nổi lên cùng cực nguồn và xả điện cung cấp dòng nạp cổng cho khóa phía cao.
    - Công thức tính toán dung lượng tụ Bootstrap tối thiểu:
      $$C_{boot} \ge \frac{2 \left[ 2 Q_g + \frac{I_{qbs}}{f_{sw}} + Q_{ls} + \frac{I_{cbs}}{f_{sw}} \right]}{\Delta V_{boot,max}}$$
      với $Q_g$ là tổng điện tích cực cổng, $I_{qbs}$ là dòng tĩnh của driver, và $\Delta V_{boot,max}$ là độ sụt áp cho phép trên tụ (thường chọn $C_{boot} \ge 10 - 20 \times C_{iss}$).
  - Hiện tượng thềm Miller (*Miller Plateau*): Khi điện áp cổng $V_{GS}$ đạt ngưỡng $V_{th}$, điện áp $V_{DS}$ bắt đầu sụt giảm cực nhanh, làm dòng dịch chuyển $i_{Miller} = C_{GD} \frac{dV_{DS}}{dt}$ chạy qua điện dung Miller hút kiệt dòng từ driver, giữ điện áp cổng đứng yên ở mức thềm Miller trong khoảng thời gian chuyển mạch.
  - Tự kích mở ký sinh do $dV/dt$ (*Parasitic dV/dt Turn-on*): Khi khóa đối diện bật nhanh với $dV/dt$ lớn, dòng qua $C_{GD}$ chạy qua điện trở xả cực cổng $R_G$ có thể nâng áp cổng vượt $V_{th}$ gây ngắn mạch xuyên nhánh (*Shoot-Through*). Giải pháp: Sử dụng mạch dập kẹp Miller chủ động (*Active Miller Clamp*).
- **Bản chất vật lý & Ứng dụng**: Cách ly điện áp cao thanh cái $48\,\text{V}-300\,\text{V}$ khỏi tín hiệu điều khiển logic nhạy cảm $3.3\,\text{V}$ của vi điều khiển STM32.

### Module 09: H-Bridge Topologies & PWM Modulation Strategies (Mạch cầu H & Chiến lược điều chế độ rộng xung PWM)
- **Mã môn tham chiếu**: MIT 6.302, ETH Zürich 227-0247-00L, UC Berkeley EE192.
- **Khung năng lực Đức**: DIHK LF3 & LF8 — Đấu nối và lập trình điều khiển đảo chiều động cơ DC và Servo 4 góc phần tư (*H-Brücken-Topologien und 4-Quadranten-Betrieb*).
- **Nội dung lý thuyết (First Principles)**:
  - Cấu trúc mạch cầu H (*H-Bridge / Vollbrücke*) gồm 4 van bán dẫn ($Q_1, Q_2, Q_3, Q_4$) và 4 đi-ốt dẫn dòng ngược nối song song.
  - Vận hành 4 góc phần tư (*4-Quadrant Operation*):
    - **Góc I**: Quay thuận - Sinh công động cơ ($V_a > 0, I_a > 0$).
    - **Góc II**: Quay thuận - Hãm tái sinh năng lượng ($V_a > 0, I_a < 0$, động cơ phát điện trả về nguồn).
    - **Góc III**: Quay nghịch - Sinh công động cơ ($V_a < 0, I_a < 0$).
    - **Góc IV**: Quay nghịch - Hãm tái sinh năng lượng ($V_a < 0, I_a > 0$).
  - Các kỹ thuật điều chế PWM:
    1. **PWM Lưỡng cực (Bipolar PWM)**: Hai cặp chéo ($Q_1, Q_4$) và ($Q_2, Q_3$) được kích luân phiên nghịch đảo nhau.
       Điện áp tức thời đặt lên tải nhảy giữa $+V_{dc}$ và $-V_{dc}$. Điện áp trung bình:
       $$V_{avg} = (2D - 1) V_{dc}$$
       với $D \in [0, 1]$ là hệ số chu kỳ công tác (*Duty Cycle*). Khi $D = 0.5$, $V_{avg} = 0$.
    2. **PWM Đơn cực (Unipolar PWM)**: Mỗi nhánh cầu được điều chế độc lập lệch pha $180^\circ$. Điện áp tức thời nhảy giữa $+V_{dc} \leftrightarrow 0$ hoặc $-V_{dc} \leftrightarrow 0$.
       Tần số gợn sóng dòng điện tăng gấp đôi tần số đóng cắt ($2 f_{sw}$), giúp giảm một nửa độ nhấp nhô dòng điện mà không cần tăng tần số chuyển mạch bán dẫn.
  - Thời gian chết (*Dead Time / Totzeit* $t_d$): Khoảng trễ an toàn bắt buộc chèn vào giữa thời điểm ngắt van này và mở van kia trên cùng một nhánh đứng:
    $$t_d > t_{off,max} - t_{on,min} + t_{prop,skew}$$
    Nếu không có thời gian chết, cả hai van trên cùng một nhánh sẽ dẫn đồng thời gây ngắn mạch xuyên thẳng nguồn thanh cái (*Shoot-Through / Brückenkurzschluss*), phá hủy nổ MOSFET tức thì.
- **Bản chất vật lý & Ứng dụng**: Điều khiển chính xác mô-men và hướng quay của động cơ servo trong cánh tay robot với hiệu suất biến đổi năng lượng trên $95\%$.

### Module 10: Inductive Switching, Current Ripple & Freewheeling Diodes (Đóng cắt tải cảm, Sóng hài dòng điện & Đi-ốt dẫn tự do)
- **Mã môn tham chiếu**: MIT 6.302, Mohan Chương 7, TU München.
- **Khung năng lực Đức**: DIHK LF3 & LF4 — Phân tích sóng hài dòng điện tải cảm và tính toán tụ bù DC-Link (*Induktive Schaltvorgänge, Stromwelligkeit und Freilaufkreise*).
- **Nội dung lý thuyết (First Principles)**:
  - Khi ngắt đột ngột dòng điện qua cuộn cảm tải động cơ $L$, hiện tượng tự cảm sinh ra sức phản điện động cực lớn:
    $$v_L(t) = -L \frac{di}{dt}$$
    Nếu không có đường dẫn dòng xả kín mạch, xung điện áp này sẽ đánh thủng mối nối bán dẫn của khóa chuyển mạch.
  - Đi-ốt dẫn dòng tự do (*Freewheeling Diode / Freilaufdiode*): Mắc song song ngược với van công suất. Khi van ngắt, dòng cảm ứng tiếp tục chạy tuần hoàn qua đi-ốt giải phóng năng lượng từ trường $\frac{1}{2} L i^2$.
  - Hiện tượng phục hồi ngược (*Reverse Recovery* $t_{rr}$): Khi đi-ốt chuyển từ dẫn sang ngắt, các hạt dẫn thiểu số tích lũy phải biến mất, tạo ra một đỉnh dòng ngược lớn $I_{rrm}$ gây tổn hao chuyển mạch phụ và tạo ra gai áp ký sinh $L_{loop} \frac{dI_{rr}}{dt}$. Do đó, đi-ốt Schottky hoặc MOSFET dẫn đồng bộ (*Synchronous Rectification*) được ưu tiên sử dụng.
  - Phân tích độ nhấp nhô dòng điện đỉnh-đỉnh (*Peak-to-Peak Current Ripple* $\Delta I_L$) trong chế độ dẫn liên tục (CCM):
    Phương trình vi phân khi van mở ($0 \le t < D \cdot T_{sw}$):
    $$L \frac{di}{dt} = V_{dc} - R i - E_b \approx V_{dc} - E_b$$
    Phương trình vi phân khi van ngắt (chế độ dẫn tự do $D \cdot T_{sw} \le t < T_{sw}$):
    $$L \frac{di}{dt} = -R i - E_b \approx -E_b$$
    Giải hệ phương trình xác lập chu kỳ, độ gợn dòng điện đỉnh-đỉnh là:
    $$\Delta I_L = \frac{V_{dc} \cdot D(1-D)}{f_{sw} \cdot L}$$
    Độ gợn dòng đạt cực đại khi hệ số công tác $D = 0.5$:
    $$\Delta I_{L,max} = \frac{V_{dc}}{4 f_{sw} L}$$
  - Lựa chọn tụ điện thanh cái (*DC-Link Capacitor*): Tụ điện phải có điện trở tương đương nối tiếp (ESR) cực nhỏ và chịu được dòng điện hiệu dụng gợn sóng:
    $$I_{C,rms} = I_{load} \sqrt{D(1-D)}$$
- **Bản chất vật lý & Ứng dụng**: Xác định tần số đóng cắt tối thiểu $f_{sw}$ (thường chọn $20-25\,\text{kHz}$ vượt ngưỡng nghe thấy của tai người để tránh tiếng rít âm học và giữ độ gợn dòng điện $< 5\%$).

### Module 11: Switched-Mode Power Supplies (SMPS) & DC-DC Converters (Nguồn xung & Bộ biến đổi DC-DC)
- **Mã môn tham chiếu**: ETH Zürich 227-0247-00L, Mohan Chương 7, TU München.
- **Khung năng lực Đức**: DIHK LF3 — Lắp đặt và vận hành nguồn điều chỉnh điện áp xung trong tủ điện điều khiển (*Schaltnetzteile und Gleichspannungswandler*).
- **Nội dung lý thuyết (First Principles)**:
  - Khác với nguồn ổn áp tuyến tính (*Linear Regulator* LDO) có hiệu suất thấp do tiêu tán năng lượng dưới dạng nhiệt $P_{loss} = (V_{in} - V_{out}) I_{out}$, bộ nguồn xung chuyển đổi năng lượng bằng các phần tử lưu trữ năng lượng phản kháng (cuộn cảm $L$ và tụ điện $C$) với hiệu suất lý tưởng $100\%$ (thực tế $85-95\%$).
  - Nguyên lý cân bằng diện tích điện áp trên cuộn cảm (*Volt-Second Balance*): Ở trạng thái xác lập chu kỳ, điện áp trung bình trên cuộn cảm trong một chu kỳ đóng cắt phải bằng không:
    $$\int_0^{T_{sw}} v_L(t) dt = 0 \implies \langle v_L \rangle = 0$$
  - Nguyên lý cân bằng điện tích trên tụ điện (*Capacitor Charge Balance*): Ở trạng thái xác lập chu kỳ, dòng điện trung bình qua tụ trong một chu kỳ phải bằng không:
    $$\int_0^{T_{sw}} i_C(t) dt = 0 \implies \langle i_C \rangle = 0$$
  - Ba cấu hình cơ bản không cách ly trong chế độ dẫn liên tục (CCM):
    1. **Bộ biến đổi Buck (Hạ áp)**:
       $$\frac{V_{out}}{V_{in}} = D, \quad \Delta V_{out} = \frac{V_{out}(1-D)}{8 L C f_{sw}^2}$$
    2. **Bộ biến đổi Boost (Tăng áp)**:
       $$\frac{V_{out}}{V_{in}} = \frac{1}{1-D}$$
    3. **Bộ biến đổi Buck-Boost (Đảo cực / Tăng-Hạ áp)**:
       $$\frac{V_{out}}{V_{in}} = -\frac{D}{1-D}$$
  - Độ tự cảm tới hạn phân định ranh giới giữa chế độ liên tục (CCM) và gián đoạn (DCM):
    $$L_{crit} = \frac{(1-D) R_L}{2 f_{sw}}$$
- **Bản chất vật lý & Ứng dụng**: Thiết kế mạch nguồn cách ly hạ áp từ điện áp công nghiệp $24\,\text{V}$ xuống $5\,\text{V}$ và $3.3\,\text{V}$ cấp nguồn cho mạch xử lý số và cảm biến trong tủ điều khiển mechatronics.

### Module 12: Electromagnetic Compatibility (EMC), Grounding & Shielding (Tương thích điện từ EMC, Nối đất & Bọc kim chống nhiễu)
- **Mã môn tham chiếu**: Horowitz & Hill Chương 8, UC Berkeley EE192, TU München.
- **Khung năng lực Đức**: DIHK LF3 & LF4 — Chống nhiễu điện từ, nối đất bảo vệ và bọc giáp theo chuẩn DIN EN 61000 (*Elektromagnetische Verträglichkeit, Schirmung und Erdungskonzepte*).
- **Nội dung lý thuyết (First Principles)**:
  - Hiện tượng ghép nhiễu trong hệ thống cơ điện tử:
    1. **Ghép trở kháng chung (*Common Impedance Coupling*)**: Khi dòng tải công suất lớn ($dI/dt$ lớn) đi chung dây mass hồi tiếp với mạch tín hiệu nhỏ nhạy cảm, sụt áp $V = R_{ground} I + L_{ground} \frac{dI}{dt}$ gây nhiễu loạn điểm điện thế đất tham chiếu.
    2. **Ghép điện dung (*Capacitive / Electric Field Coupling*)**: Biến thiên điện áp cực nhanh $dV/dt$ tại chân chuyển mạch MOSFET phóng dòng dịch chuyển qua điện dung ký sinh $i = C_{stray} \frac{dV}{dt}$ vào các đường mạch lân cận.
    3. **Ghép cảm ứng (*Inductive / Magnetic Field Coupling*)**: Biến thiên dòng điện lớn $dI/dt$ tạo ra từ trường biến thiên xuyên qua diện tích vòng lặp dây cảm biến, sinh ra điện áp cảm ứng theo định luật Faraday $V_{ind} = -\frac{d\Phi}{dt} = -M \frac{dI}{dt}$.
  - Giải pháp thiết kế triệt tiêu nhiễu:
    - **Nối đất một điểm hình sao (*Star Grounding / Sternpunkt-Erdung*)**: Tách biệt hoàn toàn mặt đất tương tự (AGND), mặt đất số (DGND), và mặt đất công suất (PGND); chỉ kết nối chúng duy nhất tại một điểm sao (*Single-point star junction*) tại tụ nguồn DC-Link chính.
    - **Cực tiểu hóa diện tích vòng lặp dòng điện (*Minimizing High-di/dt Current Loop Area*)**: Bố trí đường dây nguồn và đường dây hồi tiếp chạy sát nhau hoặc trên hai lớp đối xứng của PCB để từ trường tự triệt tiêu lẫn nhau.
    - **Cáp bọc kim xoắn đôi (*Shielded Twisted Pair - STP*)**: Các cặp dây xoắn làm đảo chiều cực tính cảm ứng từ trường trên từng bước xoắn, tự triệt tiêu điện áp nhiễu; lớp giáp kim loại bọc ngoài được nối đất bảo vệ tại tủ điện để thoát nhiễu điện trường.
  - Các tiêu chuẩn kiểm định quốc tế bắt buộc:
    - **DIN EN 61000-6-2**: Khả năng miễn nhiễm đối với môi trường công nghiệp (*Störfestigkeit für Industriebereiche*).
    - **DIN EN 61000-6-4**: Tiêu chuẩn phát xạ điện từ đối với môi trường công nghiệp (*Störaussendung für Industriebereiche*).
    - **DIN VDE 0100-410**: Biện pháp bảo vệ chống điện giật và nối đất bảo vệ (*Schutzmaßnahmen gegen elektrischen Schlag*).
- **Bản chất vật lý & Ứng dụng**: Đảm bảo toàn bộ hệ thống tủ điện điều khiển robot vận hành ổn định liên tục, không bị treo vi điều khiển hoặc đọc sai cảm biến khi các contactor và biến tần công suất lớn đóng ngắt.

---

## 2. Academic Reading List (Danh mục tài liệu học thuật tiêu chuẩn)

Dưới đây là các giáo trình và tài liệu chuẩn mực kinh điển về điện tử công suất, kỹ thuật đo lường và mạch tương tự trong hệ thống cơ điện tử:

1. **Alciatore, David G., & Histand, Michael B.** (2019). *Introduction to Mechatronics and Measurement Systems* (5th ed.). McGraw-Hill Education.
   - *Phạm vi nghiên cứu*: Chương 2 (Chuẩn hóa tín hiệu tương tự - Analog Signal Conditioning), Chương 3 (Cảm biến và bộ chuyển đổi đo lường), Chương 4 (Cơ cấu chấp hành và động cơ), Chương 8 (Mạch điện tử công suất và điều khiển động cơ).
2. **Horowitz, Paul, & Hill, Winfield** (2015). *The Art of Electronics* (3rd ed.). Cambridge University Press.
   - *Phạm vi nghiên cứu*: Chương 4 (Khuếch đại thuật toán chuyên sâu), Chương 5 (Mạch đo lường chính xác và khuếch đại vi sai), Chương 8 (Đóng cắt bán dẫn công suất thấp và công suất lớn), Chương 9 (Bộ ổn áp và kỹ thuật nguồn xung SMPS).
3. **Mohan, Ned, Undeland, Tore M., & Robbins, William P.** (2003). *Power Electronics: Converters, Applications, and Design* (3rd ed.). John Wiley & Sons.
   - *Phạm vi nghiên cứu*: Chương 7 (Bộ biến đổi nguồn xung DC-DC Buck, Boost, Buck-Boost), Chương 8 (Nghịch lưu cầu H và kỹ thuật điều chế PWM), Chương 20 (Đặc tính vật lý MOSFET công suất), Chương 22 (Mạch kích cực cổng và mạch bảo vệ cách ly).
4. **Franco, Sergio** (2015). *Design with Operational Amplifiers and Analog Integrated Circuits* (4th ed.). McGraw-Hill Education.
   - *Phạm vi nghiên cứu*: Chương 2 (Các giới hạn thực tế của Op-Amp: Slew rate, bù offset, dải thông), Chương 3 (Thiết kế mạch lọc tích cực Butterworth, Chebyshev, Bessel), Chương 8 (Bộ chuyển đổi tương tự - số ADC và lượng tử hóa).
5. **Mancini, Ron** (2002). *Op Amps for Everyone* (Design Reference SLOD006B). Texas Instruments.
   - *Giá trị học thuật*: Cẩm nang thiết kế mạch thực tế của Texas Instruments, phân tích toàn diện mạch lọc tương tự, bù tần số hồi tiếp âm và bố trí linh kiện trên bo mạch in PCB.
6. **Kester, Walt** (2005). *The Data Conversion Handbook*. Newnes / Analog Devices.
   - *Phạm vi nghiên cứu*: Phần 2 (Các cấu trúc kiến trúc ADC: SAR, Sigma-Delta, Flash), Phần 5 (Phương pháp đo kiểm và đặc tính hóa: SNR, SFDR, SINAD, ENOB, nhiễu lượng tử).

---

## 3. Practical Labs & Simulation Projects (Bài tập thực hành & Project mô phỏng)

### Lab 01: Chuỗi Xử lý Tín hiệu Cảm biến, Mạch lọc Số Butterworth & Mô phỏng Sóng hài Cầu H PWM
- **Mã file thực thi**: `labs/lab02_signal_filter.py`
- **Mục tiêu kỹ thuật**:
  1. Tạo tín hiệu cảm biến thực tế bị suy biến gồm: Tín hiệu vật lý chậm ($2\,\text{Hz}$), nhiễu điện từ trường công nghiệp ($50\,\text{Hz}$), và tạp âm trắng Gauss ngẫu nhiên (nhiễu nhiệt/nhiễu lượng tử ADC).
  2. Xây dựng mô hình mạch khuếch đại đo lường 3-OpAmp với độ lợi vi sai $A_d = 5.0$ và tỉ số triệt méo đồng pha $\text{CMRR} = 80\,\text{dB}$ để loại bỏ thành phần điện áp đồng pha $V_{cm} = 2.5\,\text{V}$.
  3. Thiết kế bộ lọc số IIR thông thấp Butterworth bậc 2 tần số cắt $f_c = 8\,\text{Hz}$ tại tần số lấy mẫu $f_s = 1000\,\text{Hz}$ bằng phương pháp biến đổi song tuyến tính (Bilinear Transform) có biến dạng tần số trước (*Pre-warping*).
  4. Lập trình tính toán chỉ số tỉ số tín hiệu trên nhiễu (SNR) có bù trễ pha/trễ nhóm ($\tau_g \approx 29\,\text{mẫu}$), chứng minh độ cải thiện SNR vượt mức $20\,\text{dB}$.
  5. Mô phỏng động học quá độ và xác lập dòng điện cuộn cảm phần ứng động cơ DC điều khiển bởi mạch cầu H đóng cắt PWM ở tần số $20\,\text{kHz}$; kiểm chứng độ nhấp nhô dòng điện mô phỏng khớp với công thức giải tích $\Delta I_L = \frac{V_{dc} D (1-D)}{f_{sw} L}$ với sai số nhỏ hơn $0.2\%$.
- **Tiêu chí nghiệm thu định lượng**:
  - Độ cải thiện SNR: $\Delta \text{SNR} > 20.0\,\text{dB}$.
  - Sai số tương đối giữa mô phỏng và công thức lý thuyết dòng gợn: $\text{Error} < 0.20\%$.
  - Thời gian thực thi toàn bộ script trên macOS: $< 50\,\text{ms}$ (Chuẩn Python thuần, không phụ thuộc gói ngoài).
  - Trạng thái kiểm tra: Đạt chuẩn xác nhận `[PASS]` trong suite kiểm thử tự động.

### Lab 02: Thiết kế Mạch Chuẩn hóa Cầu Đo Biến dạng (Strain Gauge Bridge Conditioning)
- **Mục tiêu kỹ thuật**:
  1. Thiết kế mạch đo cầu Wheatstone 4 nhánh cân bằng ($R_0 = 350\,\Omega$) sử dụng hai cảm biến biến dạng tích cực và hai điện trở bù nhiệt độ.
  2. Ghép nối đầu ra cầu đo với IC khuếch đại đo lường chuyên dụng INA128. Tính toán điện trở ngoại vi $R_G$ để đạt hệ số khuếch đại $A_d = 200$.
  3. Thiết kế tầng lọc thông thấp chủ động Sallen-Key bậc 2 sử dụng Op-Amp OPA340 với tần số cắt $f_c = 20\,\text{Hz}$ để triệt tiêu dao động cơ học tần số cao của khung giá đỡ.
  4. Lập bảng tính toán bù điểm zero và hiệu chuẩn hệ số tỷ lệ (*Span Calibration*) đầu ra từ $0\,\text{V}$ đến $3.0\,\text{V}$ tương ứng dải tải trọng $0 - 50\,\text{kg}$.
- **Kết quả bàn giao**: Sơ đồ nguyên lý mạch chi tiết, biểu thức toán học xác định sai số bù nhiệt độ, và script kiểm tra độ tuyến tính.

### Lab 03: Tính toán Tổn hao Nhiệt Khóa Bán dẫn & Thiết kế Tản nhiệt cho Driver Động cơ 24V/10A
- **Mục tiêu kỹ thuật**:
  1. Chọn mã linh kiện Power MOSFET kênh N (ví dụ: IRFB4110: $V_{DS} = 100\,\text{V}, I_D = 180\,\text{A}, R_{DS(on)} = 4.5\,\text{m}\Omega, Q_g = 150\,\text{nC}$).
  2. Tính toán tổn hao dẫn tĩnh $P_{cond} = I_{rms}^2 R_{DS(on)}$ tại dòng định mức $I_{rms} = 10\,\text{A}$.
  3. Tính toán tổn hao đóng cắt $P_{sw}$ tại tần số PWM $f_{sw} = 25\,\text{kHz}$ với thời gian tăng $t_r = 30\,\text{ns}$ và thời gian giảm $t_f = 25\,\text{ns}$ ở điện áp thanh cái $V_{dc} = 24\,\text{V}$.
  4. Lập sơ đồ mạch nhiệt tương đương ($T_J, R_{\theta JC}, R_{\theta CH}, R_{\theta HA}, T_A$). Xác định nhiệt trở tản nhiệt yêu cầu $R_{\theta HA}$ để nhiệt độ mối nối MOSFET không vượt quá $100^\circ\text{C}$ khi nhiệt độ môi trường công nghiệp lên tới $T_A = 50^\circ\text{C}$.
- **Kết quả bàn giao**: Báo cáo phân tích công suất tiêu tán chi tiết và bản vẽ kích thước tấm nhôm tản nhiệt profile công nghiệp.

---

## 4. Exact Search Queries & Bilingual Terminology Table (Từ khóa tìm kiếm & Thuật ngữ Anh-Đức-Việt)

### Precision Academic Search Queries
1. `site:ocw.mit.edu "6.302" "Feedback Systems" "operational amplifier" "compensation" filetype:pdf`
2. `site:ethz.ch "227-0247-00L" "Power Electronics" "H-bridge" "PWM inverter" filetype:pdf`
3. `site:berkeley.edu "EE192" "Mechatronic Design" "signal conditioning" "motor drive" filetype:pdf`
4. `"Sallen-Key" "Butterworth filter" "Bilinear transform" discrete difference equation filetype:pdf`
5. `"Instrumentation Amplifier" "CMRR" "3-OpAmp" "strain gauge" "common-mode" filetype:pdf`
6. `site:ti.com "SLOD006" "Op Amps for Everyone" Ron Mancini filetype:pdf`
7. `site:analog.com "MT-001" "Taking the Mystery out of the Infamous Formula SNR = 6.02N + 1.76dB"`
8. `"H-bridge" "current ripple" "inductance" "switching frequency" formula filetype:pdf`
9. `site:dihk.de "Mechatroniker" "Lernfeld 3" "Lernfeld 4" "elektrische Betriebsmittel" filetype:pdf`
10. `intitle:"The Art of Electronics" Horowitz Hill "active filters" "power switching"`
11. `intitle:"Introduction to Mechatronics and Measurement Systems" Alciatore Histand "signal conditioning"`
12. `github topic:power-electronics "h-bridge" "pwm" "buck-converter" simulation language:python`

### Bilingual Terminology Table (DIN EN 60617, IEC 60050, DIN 40110)

| STT | English Term | German Fachbegriff (DIN/IEC) | Tiếng Việt Chuyên Ngành | Ngữ Cảnh Kỹ Thuật & Tiêu Chuẩn Áp Dụng |
|:---:|:---|:---|:---|:---|
| 1 | Power Electronics | **Leistungselektronik** (*f.*) | Điện tử công suất | Ngành kỹ thuật ứng dụng linh kiện bán dẫn để điều khiển và biến đổi điện năng (IEC 60050-551). |
| 2 | Operational Amplifier | **Operationsverstärker** (*m.*, OPV) | Khuếch đại thuật toán | Vi mạch khuếch đại vi sai hệ số mở lớn dùng trong xử lý tín hiệu tương tự (DIN EN 60617). |
| 3 | Low-Pass Filter | **Tiefpassfilter** (*m./n.*) | Mạch lọc thông thấp | Mạch điện cho các thành phần tần số thấp đi qua và làm suy giảm các thành phần tần số cao. |
| 4 | Cutoff Frequency | **Grenzfrequenz** (*f.*) | Tần số cắt | Tần số tại đó công suất tín hiệu giảm một nửa (biên độ giảm $3\,\text{dB}$, tức còn $70.7\%$). |
| 5 | Sampling Rate | **Abtastrate** (*f.*) / **Abtastfrequenz** (*f.*) | Tần số lấy mẫu | Số lần đọc và chuyển đổi mẫu tín hiệu tương tự sang số trong một giây ($f_s = 1/T_s$). |
| 6 | Pulse-Width Modulation | **Pulsweitenmodulation** (*f.*, PWM) | Điều chế độ rộng xung | Phương pháp điều khiển điện áp/công suất trung bình bằng cách thay đổi tỷ lệ thời gian đóng van. |
| 7 | H-Bridge | **H-Brücke** (*f.*) / **Vollbrücke** (*f.*) | Mạch cầu H | Cấu hình gồm 4 van chuyển mạch cho phép đảo chiều điện áp và dòng điện chạy qua tải cảm. |
| 8 | Signal Conditioning | **Signalaufbereitung** (*f.*) | Chuẩn hóa / Điều hòa tín hiệu | Quá trình khuếch đại, lọc nhiễu và dịch mức tín hiệu từ cảm biến vào bộ vi xử lý. |
| 9 | Common-Mode Rejection Ratio | **Gleichtaktunterdrückung** (*f.*, CMRR) | Tỉ số triệt méo đồng pha | Thước đo khả năng suy hao điện áp nhiễu chung tác động đồng thời lên cả hai ngõ vào vi sai. |
| 10 | Instrumentation Amplifier | **Instrumentierungsverstärker** (*m.*) | Khuếch đại đo lường | Bộ khuếch đại vi sai độ chính xác cao có trở kháng vào cực lớn và CMRR vượt trội. |
| 11 | Quantization Noise | **Quantisierungsrauschen** (*n.*) | Nhiễu lượng tử hóa | Tạp âm phát sinh do sai số làm tròn khi rời rạc hóa tín hiệu điện áp liên tục sang số bit số học. |
| 12 | Dead Time | **Totzeit** (*f.*) | Thời gian chết | Khoảng trễ ngắt an toàn giữa hai van đối diện trên cùng một nhánh cầu để tránh ngắn mạch nguồn. |
| 13 | Freewheeling Diode | **Freilaufdiode** (*f.*) | Đi-ốt dẫn dòng tự do | Đi-ốt mắc song song ngược tải cảm để tiêu tán năng lượng từ trường khi khóa công suất ngắt. |
| 14 | Duty Cycle | **Tastgrad** (*m.*) / **Tastverhältnis** (*n.*) | Chu kỳ công tác (Duty Cycle) | Tỷ số giữa khoảng thời gian xung ở mức dẫn ($t_{on}$) và tổng chu kỳ đóng cắt ($T_{sw}$). |
| 15 | Noise | **Rauschen** (*n.*) / **Störsignal** (*n.*) | Nhiễu / Tín hiệu tạp âm | Thành phần dao động điện không mong muốn làm sai lệch tín hiệu mang thông tin hữu ích. |
| 16 | Power MOSFET | **Leistungs-MOSFET** (*m.*) | Transistor trường công suất | Linh kiện chuyển mạch bán dẫn công suất điều khiển đóng mở bằng điện áp cực cổng (DIN EN 60747-8). |
| 17 | Switched-Mode Power Supply | **Schaltnetzteil** (*n.*, SMPS) | Nguồn xung | Bộ nguồn chuyển đổi điện áp hiệu suất cao bằng kỹ thuật đóng cắt van phản kháng (IEC 60050). |
| 18 | Electromagnetic Compatibility | **Elektromagnetische Verträglichkeit** (*f.*, EMV) | Tương thích điện từ (EMC) | Khả năng thiết bị hoạt động ổn định trong môi trường điện từ mà không gây nhiễu cho hệ khác (DIN EN 61000). |
