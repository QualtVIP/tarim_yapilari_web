import streamlit as st

st.header("Broyler Kümesleri için Havalandırma Hesaplamaları")
st.markdown("*(Çek Standartı referans alınarak optimize edilmiştir)*")

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Z = st.number_input("Hayvan Sayısı (adet)", min_value=1, max_value=500000, value=12000, step=1000)
        m_z = st.number_input("Hayvan Ağırlığı (kg/adet)", min_value=0.01, max_value=5.0, value=2.0, step=0.1)
    
    with col2:
        t_i = st.number_input("İç Ortam Sıcaklığı (°C)", min_value=5.0, max_value=40.0, value=18.0, step=1.0)
        t_e = st.number_input("Dış Ortam Sıcaklığı (°C)", min_value=-30.0, max_value=45.0, value=-5.0, step=1.0)
    
    with col3:
        x_i = st.number_input("İç Ortam Mutlak Nemi (g/kg)", min_value=1.0, max_value=40.0, value=12.9, step=0.1)
        x_e = st.number_input("Dış Ortam Mutlak Nemi (g/kg)", min_value=0.1, max_value=30.0, value=2.94, step=0.1)

if x_i <= x_e:
    st.error("Hata: Havalandırma ile nem atılabilmesi için iç ortam mutlak nemi, dış ortam mutlak neminden büyük olmalıdır.")
    st.stop()

if t_i <= t_e and x_i <= x_e:
    st.error("Hata: Termodinamik olarak mantıksız fiziksel çevre girdileri. Girdi değerlerini kontrol edin.")
    st.stop()

def biyolojik_uretim(a1, a2, a3, ti, mz, carpan=1.3):
    return (a1 + (a2 * ti) + (a3 * (ti ** 2))) * (mz ** 0.72) * carpan

qs_a = [9.6, -0.1, 0.0]
md_a = [0.45, 0.004, 0.0012]
mu_a = [0.62, 0.0, 0.0]

q_s = biyolojik_uretim(qs_a[0], qs_a[1], qs_a[2], t_i, m_z)
m_d = biyolojik_uretim(md_a[0], md_a[1], md_a[2], t_i, m_z)
m_u = biyolojik_uretim(mu_a[0], mu_a[1], mu_a[2], t_i, m_z)

o_faktoru = 1.4
m_do = m_d * o_faktoru

rw = (2501 - 2.36 * t_i) * 1000 

q_c = q_s - ((m_do * 1e-6) * rw)

Q_c_toplam = q_c * Z
Q_c_toplam_kw = Q_c_toplam / 1000

M_do_toplam_g = (m_do * Z) / 1000
M_u_toplam_mg = (m_u * Z)

M_vd = M_do_toplam_g / (x_i - x_e)

co2_farki_limit = 2.9
M_vu = (M_u_toplam_mg / 1000) / co2_farki_limit
M_v_gerekli = max(M_vd, M_vu)

st.subheader("Biyolojik Üretim Sonuçları (Hayvan Başına)")
col_b1, col_b2, col_b3 = st.columns(3)
col_b1.metric("Toplam Isı Üretimi (q.s)", f"{q_s:.2f} W")
col_b2.metric("Nem Üretimi (m.do)", f"{m_do:.2f} mg/s")
col_b3.metric("CO₂ Üretimi (m.u)", f"{m_u:.2f} mg/s")

st.subheader("Kümes İçi Toplam Yükler ve Havalandırma")
col_t1, col_t2, col_t3 = st.columns(3)
col_t1.metric("Toplam Duyulur Isı (Q.c)", f"{Q_c_toplam_kw:.2f} kW")
col_t2.metric("Toplam Nem Yükü", f"{M_do_toplam_g:.1f} g/s")
col_t3.metric("Nem Bazlı Tahliye Debisi", f"{M_vd:.2f} kg/s")

st.success(f"**Önerilen Minimum Havalandırma Kütlesel Debisi:** {M_v_gerekli:.2f} kg/s")