import streamlit as st
import math

st.title("Karma Yem Mekanizasyonu Hesaplamaları")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Dozajlama Kapasitesi",
    "Karıştırıcı Kapasitesi",
    "Bantlı Götürücü",
    "Pnömatik Götürücü",
    "Kovalı Götürücü",
    "Helezon Götürücü"
])

with tab1:
    st.header("Genel Dozajlama Kapasitesi")
    col1, col2 = st.columns(2)
    V = col1.number_input("Dozajlama Kabı Hacmi - V (m³)", min_value=0.0, value=6.0, step=0.1)
    Pm = col2.number_input("Materyalin Dökme Özgül Kütlesi - ρm (kg/m³)", min_value=0.0, value=1.2, step=0.1)
    t = col1.number_input("Doldurup Boşaltma Süresi - t (s)", min_value=0.1, value=20.0, step=1.0)
    
    Q_genel = (V * Pm) / t
    st.metric("Dozajlama Kapasitesi - Q (kg/s)", f"{Q_genel:.4f}")

    st.markdown("---")
    st.header("Helezonlu Dozajlama Kapasitesi")
    col3, col4 = st.columns(2)
    D_hel = col3.number_input("Helezon Çapı - D (m)", min_value=0.0, value=0.2, step=0.01)
    d_hel = col4.number_input("Helezon Milinin Çapı - d (m)", min_value=0.0, value=0.05, step=0.01)
    lambda_hel = col3.number_input("Kanal Arası Uzaklık - ƛ (m)", min_value=0.0, value=0.01, step=0.005)
    S_hel = col4.number_input("Helezon Adımı - S (m)", min_value=0.0, value=0.15, step=0.01)
    alpha_hel = col3.number_input("Helezon Açısal Hızı - α (rad/s)", min_value=0.0, value=10.0, step=0.5)
    phi_hel = col4.number_input("Helezon Dolum Oranı - ч", min_value=0.0, max_value=1.0, value=0.8, step=0.05)
    
    # Qo = 3600 * (((D + 2ƛ)^2 - d^2) / 8) * S * α * ч
    Qo_hel = 3600 * (((D_hel + 2 * lambda_hel) ** 2 - d_hel ** 2) / 8) * S_hel * alpha_hel * phi_hel
    st.metric("Helezonlu Dozajlama Kapasitesi - Qo (m³/h)", f"{Qo_hel:.4f}")
    
    st.markdown("---")
    st.header("Bantlı Dozajlama Kapasitesi")
    col5, col6 = st.columns(2)
    b_bant = col5.number_input("Bant Genişliği - b (m)", min_value=0.0, value=0.5, step=0.1)
    h_bant = col6.number_input("Materyal Kalınlığı - h (m)", min_value=0.0, value=0.1, step=0.01)
    Vb_bant = col5.number_input("Bant Hızı - Vb (m/s)", min_value=0.0, value=1.5, step=0.1)
    phi_bant = col6.number_input("Bandın Yükleme Oranı - ч (Bant)", min_value=0.0, max_value=1.0, value=0.8, step=0.05)
    
    Qo_bant = 3600 * b_bant * h_bant * Vb_bant * phi_bant
    st.metric("Bantlı Dozajlama Kapasitesi - Qo (m³/h)", f"{Qo_bant:.4f}")

with tab2:
    st.header("Karıştırıcı Kapasitesi Hesabı")
    col1, col2 = st.columns(2)
    V_kar = col1.number_input("Karıştırıcı Depo Hacmi - V (m³)", min_value=0.0, value=2.0, step=0.1)
    Pm_kar = col2.number_input("Dökme Özgül Kütlesi - ρm (kg/m³)", min_value=0.0, value=600.0, step=10.0)
    phi_kar = col1.number_input("Depo Dolum Oranı - ч", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    
    t1_kar = col2.number_input("Doldurulma Süresi - t1 (dak)", min_value=0.0, value=3.0, step=0.5)
    t2_kar = col1.number_input("Aktif Karıştırma Süresi - t2 (dak)", min_value=0.0, value=5.0, step=0.5)
    t3_kar = col2.number_input("Boşaltılıp Temizlenme Süresi - t3 (dak)", min_value=0.0, value=2.0, step=0.5)
    
    M_kar = V_kar * Pm_kar * phi_kar
    # NOT: Excel dosyasında t = t1 - t2 - t3 yazıyor; fiziksel olarak toplam süre t1 + t2 + t3 olmalıdır.
    t_total = t1_kar + t2_kar + t3_kar
    
    Q_kar = 60 * (M_kar / t_total) if t_total > 0 else 0.0
    
    col3, col4 = st.columns(2)
    col3.metric("Doldurulan Materyal Miktarı - M (kg)", f"{M_kar:.2f}")
    col4.metric("Karıştırıcı Kapasitesi - Q (kg/h)", f"{Q_kar:.2f}")

with tab3:
    st.header("Bantlı Götürücüler")
    st.subheader("Sürekli Yük Taşıma Kapasitesi")
    col1, col2 = st.columns(2)
    F_sur = col1.number_input("Enine Kesit Alanı - F (m²)", min_value=0.0, value=0.05, step=0.01)
    v_sur = col2.number_input("Taşınma Hızı - v (m/s)", min_value=0.0, value=2.0, step=0.1, key="v_sur")
    Pm_sur = col1.number_input("Özgül Kütle - ρm (t/m³)", min_value=0.0, value=0.8, step=0.1)
    
    Qm_sur = 3600 * F_sur * v_sur * Pm_sur
    st.metric("Sürekli Yük Kapasitesi - Qm (t/h)", f"{Qm_sur:.2f}")
    
    st.markdown("---")
    st.subheader("Parça Yük Taşıma Kapasitesi")
    col3, col4 = st.columns(2)
    M_parca = col3.number_input("Parça Kütlesi - M (kg)", min_value=0.0, value=15.0, step=1.0)
    v_parca = col4.number_input("Bant Hızı - v (m/s)", min_value=0.0, value=1.5, step=0.1, key="v_parca")
    alpha_parca = col3.number_input("Parçalar Arası Uzaklık - α (m)", min_value=0.1, value=1.0, step=0.1)
    
    Qm_parca = 3.6 * M_parca * v_parca / alpha_parca
    st.metric("Parça Yük Kapasitesi - Qm (t/h)", f"{Qm_parca:.2f}")

    st.markdown("---")
    st.subheader("Hareket Silindiri Motor Gücü")
    col5, col6 = st.columns(2)
    P_motor = col5.number_input("Gerekli Kuvvet - P (N)", min_value=0.0, value=1500.0, step=50.0)
    v_motor = col6.number_input("Bant Hızı (Motor) - v (m/s)", min_value=0.0, value=2.0, step=0.1, key="v_motor")
    verim_motor = col5.number_input("İletim Sistemi Verimi - ı", min_value=0.01, max_value=1.0, value=0.85, step=0.05)
    
    N_kw = (P_motor * v_motor) / (1000 * verim_motor)
    st.metric("Gereksinilen Motor Gücü - N (kW)", f"{N_kw:.2f}")

with tab4:
    st.header("Pnömatik Götürücü Kapasitesi")
    col1, col2 = st.columns(2)
    D_pno = col1.number_input("Taşıma Kanalı Çapı - D (m)", min_value=0.0, value=0.2, step=0.01, key="D_pno")
    Vh_pno = col2.number_input("Hava Hızı - Vh (m/s)", min_value=0.0, value=25.0, step=1.0)
    Ph_pno = col1.number_input("Havanın Özgül Kütlesi - Ph (kg/m³)", min_value=0.0, value=1.2, step=0.1)
    mu_pno = col2.number_input("Konsantrasyon Katsayısı - μ", min_value=0.0, value=0.5, step=0.1)
    
    Qh_pno = (3.6 * math.pi * (D_pno ** 2) * Vh_pno * Ph_pno) / 4
    Qm_pno = Qh_pno * mu_pno
    
    col3, col4 = st.columns(2)
    col3.metric("Hava Kapasitesi - Qh (t/h)", f"{Qh_pno:.2f}")
    col4.metric("Taşıma Kapasitesi - Qm (t/h)", f"{Qm_pno:.2f}")

with tab5:
    st.header("Kovalı Götürücünün Taşıma Kapasitesi")
    col1, col2 = st.columns(2)
    v_kov = col1.number_input("Kova (Bant) Hızı - v (m/s)", min_value=0.0, value=1.0, step=0.1, key="v_kov")
    V_kov = col2.number_input("Her Bir Kovanın Hacmi - V (m³)", min_value=0.0, value=0.005, step=0.001, format="%.4f", key="V_kov")
    Pm_kov = col1.number_input("Dökme Özgül Kütlesi - ρm (t/m³)", min_value=0.0, value=0.8, step=0.1, key="Pm_kov")
    phi_kov = col2.number_input("Kovalar İçin Dolum Oranı - ч", min_value=0.0, max_value=1.0, value=0.8, step=0.05, key="phi_kov")
    alpha_kov = col1.number_input("Kovalar Arası Uzaklık - α (m)", min_value=0.01, value=0.4, step=0.05, key="alpha_kov")
    H_kov = col2.number_input("Materyalin Taşıma Yüksekliği - H (m)", min_value=0.0, value=5.0, step=0.5, key="H_kov")

    Q_kov = 3600 * v_kov * V_kov * Pm_kov * phi_kov / alpha_kov
    N_kov = 3.6 * Q_kov * H_kov / 102
    c1, c2 = st.columns(2)
    c1.metric("Taşıma Kapasitesi - Q (t/h)", f"{Q_kov:.2f}")
    c2.metric("Hareket Silindirinde Gereksinilen Motor Gücü - N (kW)", f"{N_kov:.2f}")
    st.caption("Derin ve sığ kovalarda α = (2,5–3)·h, V tipi kovalarda α = h alınır.")

with tab6:
    st.header("Helezon Götürücünün Taşıma Kapasitesi")
    col1, col2 = st.columns(2)
    D_g = col1.number_input("Helezonun Dış Çapı - D (m)", min_value=0.0, value=0.2, step=0.01, key="D_g")
    d_g = col2.number_input("Helezonun İç Çapı - d (m)", min_value=0.0, value=0.05, step=0.01, key="d_g")
    S_g = col1.number_input("Helezon Vida Adımı - S (m)", min_value=0.0, value=0.15, step=0.01, key="S_g")
    lam_g = col2.number_input("Helezon Ucu ile Kanal Arası Uzaklık - ƛ (m)", min_value=0.0, value=0.01, step=0.005, key="lam_g")
    alpha_g = col1.number_input("Helezon Açısal Hızı - α (rad/s)", min_value=0.0, value=10.0, step=0.5, key="alpha_g")
    phi_g = col2.number_input("Helezon Dolum Oranı - ч", min_value=0.0, max_value=1.0, value=0.8, step=0.05, key="phi_g")
    Pm_g = col1.number_input("Dökme Özgül Kütlesi - ρm (t/m³)", min_value=0.0, value=0.8, step=0.1, key="Pm_g")

    # Düzeltme katsayısı k (Excel tablosu: eğim açısı -> k)
    k_tablo = {0: 1.0, 5: 0.75, 10: 0.94, 15: 0.92, 20: 0.88, 30: 0.82, 40: 0.76, 50: 0.70}
    egim = col2.selectbox("Eğim Açısı (°)", list(k_tablo.keys()), key="egim_g")
    k_g = k_tablo[egim]

    Qm_g = 450 * ((D_g + 2 * lam_g) ** 2 - d_g ** 2) * S_g * alpha_g * phi_g * k_g * Pm_g
    Qo_g = Qm_g / Pm_g if Pm_g > 0 else 0.0
    st.metric("Helezon Götürücü Taşıma Kapasitesi - Qm (t/h)", f"{Qm_g:.2f}")

    st.markdown("---")
    st.subheader("Helezon Götürücüyü Çalıştırmak İçin Gerekli Güç")
    col3, col4 = st.columns(2)
    L_g = col3.number_input("Götürücü Uzunluğu - L (m)", min_value=0.0, value=5.0, step=0.5, key="L_g")
    ang_g = col4.number_input("Götürücünün Yatayla Yaptığı Açı - α (°)", min_value=0.0, max_value=90.0, value=0.0, step=5.0, key="ang_g")
    gam_g = col3.number_input("Dökme Hacim Ağırlığı - γm (N/m³)", min_value=0.0, value=7850.0, step=100.0, key="gam_g")
    Wo_g = col4.number_input("Toplam Direnç Katsayısı - Wo", min_value=0.0, value=1.2, step=0.05, key="Wo_g")
    st.caption("Wo: mısır, soya, hububat 1,15–1,20 | mineral gübre 1,70–2,50 | yumru bitkiler 1,20–1,70 | öğütülmüş kaya tuzu 2,50")

    N_g = Qo_g * gam_g * L_g * (Wo_g + math.sin(math.radians(ang_g))) / (3.6 * 10 ** 6)
    st.metric("Gerekli Güç - N (kW)", f"{N_g:.2f}")