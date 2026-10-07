import streamlit as st
import math

st.title("Karma Yem Mekanizasyonu Hesaplamaları")

tab1, tab2, tab3, tab4 = st.tabs([
    "Dozajlama Kapasitesi", 
    "Karıştırıcı Kapasitesi", 
    "Bantlı Götürücü", 
    "Pnömatik Götürücü"
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
    
    Qo_hel = 3600 * ((D_hel + 2 * lambda_hel) - d_hel) * S_hel * alpha_hel * phi_hel / 2
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
    v_sur = col2.number_input("Taşınma Hızı - v (m/s) ", min_value=0.0, value=2.0, step=0.1)
    Pm_sur = col1.number_input("Özgül Kütle - ρm (t/m³)", min_value=0.0, value=0.8, step=0.1)
    
    Qm_sur = 3600 * F_sur * v_sur * Pm_sur
    st.metric("Sürekli Yük Kapasitesi - Qm (t/h)", f"{Qm_sur:.2f}")
    
    st.markdown("---")
    st.subheader("Parça Yük Taşıma Kapasitesi")
    col3, col4 = st.columns(2)
    M_parca = col3.number_input("Parça Kütlesi - M (kg)", min_value=0.0, value=15.0, step=1.0)
    v_parca = col4.number_input("Bant Hızı - v (m/s)  ", min_value=0.0, value=1.5, step=0.1)
    alpha_parca = col3.number_input("Parçalar Arası Uzaklık - α (m)", min_value=0.1, value=1.0, step=0.1)
    
    Qm_parca = 3.6 * M_parca * v_parca / alpha_parca
    st.metric("Parça Yük Kapasitesi - Qm (t/h)", f"{Qm_parca:.2f}")

    st.markdown("---")
    st.subheader("Hareket Silindiri Motor Gücü")
    col5, col6 = st.columns(2)
    P_motor = col5.number_input("Gerekli Kuvvet - P (N)", min_value=0.0, value=1500.0, step=50.0)
    v_motor = col6.number_input("Bant Hızı (Motor) - v (m/s)   ", min_value=0.0, value=2.0, step=0.1)
    verim_motor = col5.number_input("İletim Sistemi Verimi - ı", min_value=0.01, max_value=1.0, value=0.85, step=0.05)
    
    N_kw = (P_motor * v_motor) / (1000 * verim_motor)
    st.metric("Gereksinilen Motor Gücü - N (kW)", f"{N_kw:.2f}")

with tab4:
    st.header("Pnömatik Götürücü Kapasitesi")
    col1, col2 = st.columns(2)
    D_pno = col1.number_input("Taşıma Kanalı Çapı - D (m) ", min_value=0.0, value=0.2, step=0.01)
    Vh_pno = col2.number_input("Hava Hızı - Vh (m/s)", min_value=0.0, value=25.0, step=1.0)
    Ph_pno = col1.number_input("Havanın Özgül Kütlesi - Ph (kg/m³)", min_value=0.0, value=1.2, step=0.1)
    mu_pno = col2.number_input("Konsantrasyon Katsayısı - μ", min_value=0.0, value=0.5, step=0.1)
    
    Qh_pno = (3.6 * math.pi * (D_pno ** 2) * Vh_pno * Ph_pno) / 4
    Qm_pno = Qh_pno * mu_pno
    
    col3, col4 = st.columns(2)
    col3.metric("Hava Kapasitesi - Qh (t/h)", f"{Qh_pno:.2f}")
    col4.metric("Taşıma Kapasitesi - Qm (t/h)", f"{Qm_pno:.2f}")