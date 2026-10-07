import math
import streamlit as st


def calculate_u_value(delta_i, delta_d, layers):
    """Yapı elemanının U (ısı transfer katsayısı) değerini hesaplar."""
    r_total = (1 / delta_i) + (1 / delta_d)
    for d, lam in layers:
        r_total += d / lam
    return 1 / r_total


def calculate_heat_loss(u, a, ti, td):
    """Yapı elemanından olan ısı kaybı: qy = U*A*(ti-td)."""
    return u * a * (ti - td)


st.set_page_config(page_title="Kümes Havalandırma ve Isı Dengesi", layout="wide")
st.title("Tarım Yapıları: Kümes Havalandırma Kapasitesi Hesaplayıcı")
st.markdown("Sensör girdileri ve yapısal malzeme verilerine göre metrik sistemde optimum havalandırma debisi analizi.")

# ---------------- Kenar çubuğu ----------------
st.sidebar.header("Genel Parametreler")
n_animals = st.sidebar.number_input("Hayvan Sayısı (N)", value=12000, step=500)
animal_type = st.sidebar.selectbox("Hayvan Kategorisi", ["Broyler", "Yumurta Tavuğu"])

st.sidebar.header("İç/Dış Ortam Sıcaklıkları (°C)")
ti_winter = st.sidebar.number_input("Kış - İç Ortam (ti)", value=18.0, format="%.1f")
td_winter = st.sidebar.number_input("Kış - Dış Ortam (td)", value=-3.0, format="%.1f")
ti_summer = st.sidebar.number_input("Yaz - İç Ortam (ti)", value=30.0, format="%.1f")
td_summer = st.sidebar.number_input("Yaz - Dış Ortam (td)", value=26.0, format="%.1f")

st.sidebar.header("Termodinamik Sabitler")
cp = st.sidebar.number_input("Havanın Özgül Isısı (cp) [W/kg°C]", value=0.28, format="%.2f")
rho_in = st.sidebar.number_input("Barınak İçi Havası Özgül Hacmi (ρ) [m³/kg]", value=0.84, format="%.2f")
k_v = st.sidebar.number_input("Havalandırma ısı kaybı katsayısı (≈ cp/ρ_dış)", value=0.34, format="%.2f")

# ---------------- U değerleri ----------------
delta_i = 8.14
delta_d = 23.26

u_wall = calculate_u_value(delta_i, delta_d, [(0.01, 0.87), (0.2, 0.52), (0.02, 1.4)])
u_roof = calculate_u_value(delta_i, delta_d, [(0.005, 0.35), (0.01, 0.041), (0.005, 0.17)])
u_window = calculate_u_value(delta_i, delta_d, [(0.003, 1.116)])
u_door = calculate_u_value(delta_i, delta_d, [(0.003, 20.0)])

col1, col2 = st.columns(2)
with col1:
    st.subheader("Yapısal Alanlar (A) [m²]")
    a_wall = st.number_input("Duvar Alanı", value=246.2)
    a_roof = st.number_input("Çatı Alanı", value=881.0)
with col2:
    st.subheader("Açıklık Alanları (A) [m²]")
    a_window = st.number_input("Pencere Alanı", value=83.0)
    a_door = st.number_input("Kapı Alanı", value=11.0)

areas_u = [(u_wall, a_wall), (u_roof, a_roof), (u_window, a_window), (u_door, a_door)]

# ---------------- 1. Isı kayıpları ----------------
st.header("1. Kış Mevsimi Isı Kayıpları (qy)")
qy_total = sum(calculate_heat_loss(u, a, ti_winter, td_winter) for u, a in areas_u)
st.write(f"**U Değerleri (W/m²K):** Duvar: {u_wall:.2f} | Çatı: {u_roof:.2f} | Pencere: {u_window:.2f} | Kapı: {u_door:.2f}")
st.info(f"**Toplam Yapısal Isı Kaybı (qy):** {qy_total:.2f} W")

# ---------------- 2. Kış havalandırma ----------------
st.header("2. Minimum Havalandırma Kapasiteleri (Kış)")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**CO₂ Dengesine Göre (m³/h)**")
    qc = st.number_input("Yayılan CO₂ (qc) [l/h]", value=2.2)
    k_co2 = st.number_input("CO₂ katsayısı", value=0.446, format="%.3f")
    # Excel: Qmin = 0.446 * N * qc * ρ
    qmin_co2 = k_co2 * n_animals * qc * rho_in
    st.success(f"Q_min(CO₂) = {qmin_co2:.2f} m³/h")
with c2:
    st.markdown("**Su Buharı Dengesine Göre (m³/h)**")
    qm = st.number_input("Yayılan Su Buharı (qm) [g/h]", value=6.3)
    qmi = st.number_input("İç Hava Özgül Nem (qmi) [g/kg]", value=12.9)
    qm0 = st.number_input("Dış Hava Özgül Nem (qm0) [g/kg]", value=2.94)
    if qmi <= qm0:
        st.error("İç hava nemi dış hava neminden büyük olmalıdır.")
        st.stop()
    qmin_h2o = (n_animals * qm / (qmi - qm0)) * rho_in
    st.success(f"Q_min(H₂O) = {qmin_h2o:.2f} m³/h")

# ---------------- 3. Geçiş ve yaz ----------------
st.header("3. Geçiş ve Yaz Mevsimi Havalandırma Hacimleri")
c3, c4 = st.columns(2)
with c3:
    st.markdown("**Geçiş Mevsimi (m³/h)**")
    qd_transition = st.number_input("Geçiş - Duyulur Isı (qd) [W]", value=6.8)
    dt_transition = st.number_input("Geçiş - Hedef ΔT [°C]", value=5.0)
    # Excel: qy(geçiş) = qy/(ti-td) * 5
    qy_transition = sum(u * a for u, a in areas_u) * dt_transition
    q_transition = ((n_animals * qd_transition - qy_transition) * rho_in) / (cp * dt_transition)
    st.metric("Q_geçiş", f"{q_transition:.2f} m³/h")
    st.caption(f"Geçiş mevsimi yapısal ısı kaybı: {qy_transition:.2f} W")
with c4:
    st.markdown("**Yaz Mevsimi (m³/h)**")
    qd_summer = st.number_input("Yaz - Duyulur Isı (qd) [W]", value=4.3)
    dt_summer = st.number_input("Yaz - Hedef ΔT [°C]", value=3.0)
    rho_summer = st.number_input("Yaz - Havanın Özgül Hacmi [m³/kg]", value=0.88)
    q_summer = ((n_animals * qd_summer) * rho_summer) / (cp * dt_summer)
    st.metric("Q_yaz", f"{q_summer:.2f} m³/h")

# ---------------- 4. Isı dengesi ----------------
st.header("4. Kışın Kümes İçi Isı Dengesi")
qd_winter = st.number_input("Kış - Hayvan Başına Duyulur Isı (qd) [W]", value=9.3)
qv_winter = k_v * qmin_co2 * (ti_winter - td_winter)
q_produced = n_animals * qd_winter
q_lost_total = qy_total + qv_winter

st.write(f"- **Havalandırma Yoluyla Olan Isı Kaybı (qv):** {qv_winter:.2f} W")
st.write(f"- **Hayvanların Ürettiği Toplam Duyulur Isı:** {q_produced:.2f} W")
st.write(f"- **Toplam Kaybolan Isı (qy + qv):** {q_lost_total:.2f} W")

extra_flow = (q_produced - q_lost_total) / (k_v * (ti_winter - td_winter))
max_winter_flow = extra_flow + qmin_co2
m1, m2 = st.columns(2)
m1.metric("Gerekli Ek Havalandırma Debisi", f"{extra_flow:.2f} m³/h")
m2.metric("Kış İçin Maksimum Havalandırma Kapasitesi", f"{max_winter_flow:.2f} m³/h")

if q_produced < q_lost_total:
    st.warning("⚠️ Kümes içinde üretilen ısı, kaybolan ısıdan daha azdır. Havalandırma debisinin azaltılması gerekir.")
else:
    st.success("✅ Kümes içi ısı dengesi sağlanmaktadır.")

# ---------------- 5. Açıklık alanları ----------------
st.header("5. Hava Giriş-Çıkış Açıklıklarının Alanları")
c5, c6, c7 = st.columns(3)
h_baca = c5.number_input("Baca yüksekliği [m]", value=4.2)
dt_baca = c6.number_input("Baca sıcaklık farkı ΔT [°C]", value=5.0)
v_mech = c7.number_input("Mekanik havalandırma giriş hızı [m/s]", value=1.0)

v_baca = 0.11 * math.sqrt(h_baca * dt_baca) * 3600          # m/h
a_out = q_transition / v_baca                                # m²
a_in = (2 / 3) * a_out                                       # m²
a_in_mech = q_summer / (3600 * v_mech)                       # m²

r1, r2, r3, r4 = st.columns(4)
r1.metric("Baca Hava Hızı", f"{v_baca:.2f} m/h")
r2.metric("Hava Çıkış Açıklığı", f"{a_out:.2f} m²")
r3.metric("Hava Giriş Açıklığı", f"{a_in:.2f} m²")
r4.metric("Mekanik Havalandırma Giriş Açıklığı", f"{a_in_mech:.2f} m²")