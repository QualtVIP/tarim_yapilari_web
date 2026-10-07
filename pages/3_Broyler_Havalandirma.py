import math
import streamlit as st

st.header("Broyler Kümesleri için Havalandırma Hesaplamaları")
st.markdown("*(Çek Standardı referans alınarak hazırlanmıştır)*")

# ---------------- Girdiler ----------------
col1, col2, col3 = st.columns(3)
with col1:
    Z = st.number_input("Hayvan Sayısı (adet)", min_value=1, max_value=500000, value=12000, step=1000)
    m_z = st.number_input("Hayvan Ağırlığı (kg/adet)", min_value=0.01, max_value=5.0, value=2.0, step=0.1)
with col2:
    t_i = st.number_input("İç Ortam Sıcaklığı - Kış (°C)", min_value=5.0, max_value=40.0, value=18.0, step=1.0)
    t_i_yaz = st.number_input("İç Ortam Sıcaklığı - Yaz (°C)", min_value=5.0, max_value=45.0, value=30.0, step=1.0)
with col3:
    x_i = st.number_input("İç Ortam Mutlak Nemi (g/kg)", min_value=1.0, max_value=40.0, value=12.9, step=0.1)
    x_e = st.number_input("Dış Ortam Mutlak Nemi (g/kg)", min_value=0.1, max_value=30.0, value=2.94, step=0.1)

if x_i <= x_e:
    st.error("Hata: Nem atılabilmesi için iç ortam mutlak nemi, dış ortam mutlak neminden büyük olmalıdır.")
    st.stop()


def biyolojik_uretim(a1, a2, a3, ti, mz, d=0.72, carpan=1.3):
    """B = (a1 + a2*ti + a3*ti^2) * mz^d * 1.3"""
    return (a1 + a2 * ti + a3 * ti ** 2) * (mz ** d) * carpan


# ---------------- 1. Biyolojik üretim ----------------
q_s = biyolojik_uretim(9.6, -0.1, 0.0, t_i, m_z)        # W/tavuk
m_d = biyolojik_uretim(0.45, 0.004, 0.0012, t_i, m_z)   # mg/s.tavuk
m_u = biyolojik_uretim(0.62, 0.0, 0.0, t_i, m_z)        # mg/s.tavuk
m_do = m_d * 1.4                                         # düzeltme faktörü o = 1,4

rw = 2500 - 2.36 * t_i                                   # kJ/kg (Excel: 2500 - 2,36.ti)
q_c = q_s - (rw * m_do * 0.001)
Q_c_toplam = q_c * Z
Q_c_kw = Q_c_toplam / 1000

st.subheader("Biyolojik Üretim Sonuçları (Hayvan Başına)")
b1, b2, b3, b4 = st.columns(4)
b1.metric("Toplam Isı Üretimi (q.s)", f"{q_s:.2f} W")
b2.metric("Nem Üretimi (m.do)", f"{m_do:.2f} mg/s")
b3.metric("CO₂ Üretimi (m.u)", f"{m_u:.2f} mg/s")
b4.metric("Duyulur Isı (q.c)", f"{q_c:.2f} W")

# ---------------- 2. Kış debisi ----------------
st.subheader("Kış Dönemi Havalandırma Debisi")
k1, k2, k3, k4 = st.columns(4)
Q_tg = k1.number_input("Bacasız gazlı ısıtıcı gücü Q.tg (kW)", min_value=0.0, value=50.0, step=5.0)
m_dt = k2.number_input("Isıtıcı nem akışı (mg/s·kW)", min_value=0.0, value=34.0)
m_ut = k3.number_input("Isıtıcı CO₂ üretimi (mg/s·kW)", min_value=0.0, value=67.0)
rho_i = k4.number_input("İç hava yoğunluğu - kış (kg/m³)", min_value=0.5, value=1.19, format="%.2f")
k5, k6 = st.columns(2)
K_ui = k5.number_input("İç ortam CO₂ konsantrasyonu (mg/m³)", value=4000.0, step=100.0)
K_ue = k6.number_input("Dış ortam CO₂ konsantrasyonu (mg/m³)", value=550.0, step=50.0)

M_d = (Z * m_do + m_dt * Q_tg) * 0.001                    # g/s
M_vd = M_d / (x_i - x_e)                                  # kg/s
M_u = Z * m_u + m_ut * Q_tg                               # mg/s
M_vu = (M_u / (K_ui - K_ue)) * rho_i                      # kg/s
M_v_kis = max(M_vd, M_vu)

t1, t2, t3 = st.columns(3)
t1.metric("Toplam Duyulur Isı (Q.c)", f"{Q_c_kw:.2f} kW")
t2.metric("Toplam Nem Yükü (M.d)", f"{M_d:.2f} g/s")
t3.metric("Toplam CO₂ Üretimi (M.u)", f"{M_u:.1f} mg/s")
t4, t5 = st.columns(2)
t4.metric("Nem Bazlı Tahliye Debisi (M.vd)", f"{M_vd:.2f} kg/s")
t5.metric("CO₂ Bazlı Tahliye Debisi (M.vu)", f"{M_vu:.2f} kg/s")
st.success(f"**Kış Dönemi Minimum Havalandırma Kütlesel Debisi (M.v):** {M_v_kis:.2f} kg/s")

# ---------------- 3. Yaz debisi ----------------
st.subheader("Yaz Dönemi Havalandırma Debisi")
y1, y2, y3, y4 = st.columns(4)
b_k = y1.number_input("Broyler katsayısı b", value=1.8)
y_f = y2.number_input("Kümes kütlesi düzeltme faktörü y", value=1.0)
z_f = y3.number_input("Yarı şeffaf yüzey düzeltme faktörü z", value=1.0)
V_kumes = y4.number_input("Kümes hacmi (m³)", min_value=1.0, value=2650.0, step=50.0)

m_v_max = b_k * (m_z ** 0.72) * 0.001 * 1.3               # kg/s.tavuk
M_v_yaz = y_f * z_f * Z * m_v_max                         # kg/s
I_hava = 3000 * M_v_yaz / V_kumes                         # 1/h

s1, s2, s3 = st.columns(3)
s1.metric("Hayvan Başına Debi (m.v,max)", f"{m_v_max:.5f} kg/s")
s2.metric("Yaz Dönemi Debisi (M.v,max)", f"{M_v_yaz:.2f} kg/s")
s3.metric("Hava Yenileme Sayısı (I)", f"{I_hava:.2f} 1/h")
if I_hava >= 60:
    st.warning("I ≥ 60: Barınak içinde havalandırma yapmak güçtür; hayvanların olduğu bölgeye etkin hava akımı yönlendirilmelidir.")
elif I_hava > 45:
    st.info("45 < I < 60: Hava yenileme sayısı ayarlanarak havalandırma ekipmanının gücü sınırlandırılabilir.")

# ---------------- 4. Isı dengesi ----------------
st.subheader("Kış Isı Dengesi (Q.c + Q.t − Q.p − Q.v = 0)")
h1, h2, h3, h4 = st.columns(4)
Q_p = h1.number_input("Kondüksiyon/konveksiyon ısı kaybı Q.p (W)", value=100000.0, step=5000.0)
V_a = h2.number_input("Fan hacimsel debisi V.a (m³/s)", value=13.5)
rho_kis = h3.number_input("Havanın yoğunluğu - kış (kg/m³)", value=1.3)
dT_ie = h4.number_input("İç-dış sıcaklık farkı ΔT (K)", value=5.0)
c_a = 1010.0                                              # J/kg.K

zemin = st.checkbox("Zeminden ısıtma yapılan kümes (ek nem buharlaşması dikkate alınsın)", value=True)
if zemin:
    z1, z2, z3 = st.columns(3)
    w_a = z1.number_input("Islak yüzey boyunca hava hızı w.a (m/s)", value=1.0)
    x_p = z2.number_input("Islak yüzeydeki doymuş havanın nemi x\"p (g/kg)", value=17.24)
    s_taban = z3.number_input("Hayvan başına taban alanı s (m²)", value=0.069, format="%.3f")
    Dm_do = (7 + 5.3 * w_a) * (x_p - x_i) * s_taban       # mg/s.tavuk
else:
    Dm_do = 0.0
q_c_denge = q_s - rw * (m_do + Dm_do) * 0.001             # W/tavuk
Q_c_denge = Z * q_c_denge                                 # W

M_v_fan = V_a * rho_kis                                   # kg/s
Q_v = M_v_fan * c_a * dT_ie                               # W
Q_t = Q_p + Q_v - Q_c_denge                               # W (ısıtıcı gücü)

st.caption(f"Isı dengesinde kullanılan Q.c = {Q_c_denge:.1f} W")
e1, e2, e3 = st.columns(3)
e1.metric("Fanlarla Temiz Hava Debisi (M.v)", f"{M_v_fan:.2f} kg/s")
e2.metric("Havalandırma Isı Kaybı (Q.v)", f"{Q_v:.1f} W")
e3.metric("Gerekli Isıtıcı Gücü (Q.t)", f"{Q_t:.1f} W")

# ---------------- 5. Doğal havalandırma açıklıkları ----------------
st.subheader("Doğal Havalandırmada Hava Giriş-Çıkış Açıklıkları")
a1, a2, a3 = st.columns(3)
H = a1.number_input("Giriş-çıkış arası düşey uzaklık H (m)", value=3.25)
so_sp = a2.number_input("So/Sp oranı (0,4 – 0,6)", min_value=0.1, max_value=1.0, value=0.5)
rho_yaz_i = a3.number_input("İç hava yoğunluğu - yaz (kg/m³)", value=1.12)
a4, a5, a6 = st.columns(3)
m_p = a4.number_input("Giriş akım faktörü μp", value=0.35)
m_o = a5.number_input("Çıkış akım faktörü μo", value=0.65)
dT_ac = a6.number_input("Açıklık hesabı ΔT (K)", value=5.0)

f27a = (0.23 * M_v_fan) / (m_o * rho_yaz_i)
f27b = 1 + ((m_o / m_p) * so_sp) ** 2
f27c = H * (dT_ac / (t_i_yaz + 273))
f27d = math.sqrt(f27b / f27c)
S_out = f27a * f27d
S_in = S_out / so_sp

g1, g2 = st.columns(2)
g1.metric("Gereken Min. Hava Çıkış Açıklığı Alanı", f"{S_out:.2f} m²")
g2.metric("Gereken Min. Hava Giriş Açıklığı Alanı", f"{S_in:.2f} m²")