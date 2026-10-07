import streamlit as st

def calculate_u_value(delta_i, delta_d, layers):
    """Yapı elemanının U (Isı transfer katsayısı) değerini hesaplar."""
    r_total = (1 / delta_i) + (1 / delta_d)
    for d, lam in layers:
        r_total += (d / lam)
    return 1 / r_total

def calculate_heat_loss(u, a, ti, td):
    """Spesifik yapı elemanından gerçekleşen duyulur ısı kaybını (qy) hesaplar."""
    return u * a * (ti - td)

def main():
    st.set_page_config(page_title="Kümes Havalandırma ve Isı Dengesi", layout="wide")
    st.title("Tarım Yapıları: Kümes Havalandırma Kapasitesi Hesaplayıcı")
    st.markdown("Sensör girdileri ve yapısal malzeme verilerine göre metrik sistemde optimum havalandırma debisi analizi.")

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
    rho_out_winter = st.sidebar.number_input("Kış Dış Hava Özgül Hacmi (ρ) [m³/kg]", value=0.824, format="%.3f")

    # --- YAPI ELEMANLARI U DEĞERLERİ (Örnek Katman Sabitleri) ---
    delta_i = 8.14
    delta_d = 23.26
    
    u_wall = calculate_u_value(delta_i, delta_d, [(0.01, 0.87), (0.2, 0.52), (0.02, 1.4)])
    u_roof = calculate_u_value(delta_i, delta_d, [(0.005, 0.35), (0.01, 0.041), (0.005, 0.17)])
    u_window = calculate_u_value(delta_i, delta_d, [(0.003, 1.116)])
    u_door = calculate_u_value(delta_i, delta_d, [(0.003, 20.0)])
    
    # --- YAPI ALANLARI (m2) ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Yapısal Alanlar (A) [m²]")
        a_wall = st.number_input("Duvar Alanı", value=246.2)
        a_roof = st.number_input("Çatı Alanı", value=881.0)
    with col2:
        st.subheader("Açıklık Alanları (A) [m²]")
        a_window = st.number_input("Pencere Alanı", value=83.0)
        a_door = st.number_input("Kapı Alanı", value=11.0)

    # --- ISIL KAYIPLARIN EŞİTLİKLERİ ---
    st.header("1. Kış Mevsimi Isı Kayıpları (qy)")
    qy_wall = calculate_heat_loss(u_wall, a_wall, ti_winter, td_winter)
    qy_roof = calculate_heat_loss(u_roof, a_roof, ti_winter, td_winter)
    qy_window = calculate_heat_loss(u_window, a_window, ti_winter, td_winter)
    qy_door = calculate_heat_loss(u_door, a_door, ti_winter, td_winter)
    qy_total = qy_wall + qy_roof + qy_window + qy_door
    
    st.write(f"**U Değerleri (W/m²K):** Duvar: {u_wall:.2f} | Çatı: {u_roof:.2f} | Pencere: {u_window:.2f} | Kapı: {u_door:.2f}")
    st.info(f"**Toplam Yapısal Isı Kaybı (qy):** {qy_total:.2f} W")

    # --- HAVALANDIRMA KAPASİTELERİ ---
    st.header("2. Minimum Havalandırma Kapasiteleri (Kış)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**CO₂ Dengesine Göre (m³/h)**")
        qc = st.number_input("Yayılan CO₂ (qc) [l/h]", value=2.2)
        co2_diff = st.number_input("Kabul Edilebilir ΔCO₂ (l/m³)", value=2.669, format="%.3f")
        qmin_co2 = (n_animals * qc) / co2_diff
        st.success(f"Q_min(CO₂) = {qmin_co2:.2f} m³/h")
        
    with c2:
        st.markdown("**Su Buharı Dengesine Göre (m³/h)**")
        qm = st.number_input("Yayılan Su Buharı (qm) [g/h]", value=6.3)
        qmi = st.number_input("İç Hava Özgül Nem (qmi) [g/kg]", value=12.9)
        qm0 = st.number_input("Dış Hava Özgül Nem (qm0) [g/kg]", value=2.94)
        qmin_h2o = (n_animals * qm * rho_in) / (qmi - qm0)
        st.success(f"Q_min(H₂O) = {qmin_h2o:.2f} m³/h")

    # --- GEÇİŞ VE YAZ MEVSİMİ HAVALANDIRMA ---
    st.header("3. Geçiş ve Yaz Mevsimi Havalandırma Hacimleri")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Geçiş Mevsimi (m³/h)**")
        qd_transition = st.number_input("Geçiş - Duyulur Isı (qd) [W]", value=6.8)
        dt_transition = st.number_input("Geçiş - Hedef ΔT [°C]", value=5.0)
        
        # Geçiş mevsiminde kısmi ısı kaybı tahmini
        qy_transition = calculate_heat_loss(u_wall, a_wall, ti_winter, ti_winter - dt_transition) + \
                        calculate_heat_loss(u_roof, a_roof, ti_winter, ti_winter - dt_transition) + \
                        calculate_heat_loss(u_window, a_window, ti_winter, ti_winter - dt_transition) + \
                        calculate_heat_loss(u_door, a_door, ti_winter, ti_winter - dt_transition)
        
        q_transition = ((n_animals * qd_transition - qy_transition) * rho_in) / (cp * dt_transition)
        st.metric(label="Q_geçiş", value=f"{q_transition:.2f} m³/h")

    with c4:
        st.markdown("**Yaz Mevsimi (m³/h)**")
        qd_summer = st.number_input("Yaz - Duyulur Isı (qd) [W]", value=4.3)
        dt_summer = st.number_input("Yaz - Hedef ΔT [°C]", value=3.0)
        rho_summer = st.number_input("Yaz - Havanın Özgül Hacmi [m³/kg]", value=0.88)
        
        # Yazın qy pratik olarak 0 kabul edilir
        q_summer = ((n_animals * qd_summer) * rho_summer) / (cp * dt_summer)
        st.metric(label="Q_yaz", value=f"{q_summer:.2f} m³/h")

    # --- ISI DENGESİ ANALİZİ ---
    st.header("4. Kışın Kümes İçi Isı Dengesi")
    qv_winter = (qmin_co2 * cp * (ti_winter - td_winter)) / rho_out_winter
    q_produced = n_animals * 9.3 # (qd kış = 9.3 W öngörülür)
    q_lost_total = qy_total + qv_winter
    
    st.write(f"- **Havalandırma Yoluyla Olan Isı Kaybı (qv):** {qv_winter:.2f} W")
    st.write(f"- **Hayvanların Ürettiği Toplam Duyulur Isı:** {q_produced:.2f} W")
    st.write(f"- **Toplam Kaybolan Isı (qy + qv):** {q_lost_total:.2f} W")
    
    if q_produced < q_lost_total:
        st.warning("⚠️ Kümes içinde üretilen ısı, kaybolan ısıdan daha azdır. Ek ısıtıcı gereksinimi veya havalandırma debisinde kısıtlama yapılmalıdır.")
    else:
        st.success("✅ Kümes içi ısı dengesi sağlanmaktadır.")

if __name__ == "__main__":
    main()