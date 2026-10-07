import streamlit as st

st.set_page_config(page_title="Yüksek Lisans Ödevleri", layout="wide")


def ana_sayfa():
    st.title("Bilgisayar Programcılığı ve Tarımda Kullanımı")
    st.markdown("Sol taraftaki menüden ilgili ödevi seçerek hesaplama modüllerine ulaşabilirsiniz.")
    st.subheader("Modüller")
    st.markdown(
        """
- **Kümes Havalandırma:** Yapı elemanlarından ısı kaybı, CO₂ ve su buharı dengesine göre havalandırma kapasiteleri, ısı dengesi ve hava giriş-çıkış açıklıkları.
- **Karma Yem Mekanizasyonu:** Dozajlama, karıştırıcı, bantlı/kovalı/helezon/pnömatik götürücü kapasite ve güç hesapları.
- **Broyler Havalandırma (Çek Standardı):** Biyolojik üretim değerleri, kış ve yaz havalandırma debileri, ısı dengesi ve açıklık alanları.
"""
    )
    st.caption("Hesaplamalar, ders kapsamında verilen Excel dosyalarındaki eşitliklerin web uygulamasına dönüştürülmesiyle hazırlanmıştır.")


pg = st.navigation(
    [
        st.Page(ana_sayfa, title="Ana Sayfa", icon="🏠", default=True),
        st.Page("pages/1_Havalandirma.py", title="Kümes Havalandırma", icon="🌡️"),
        st.Page("pages/2_Karma_Yem_Mekanizasyonu.py", title="Karma Yem Mekanizasyonu", icon="⚙️"),
        st.Page("pages/3_Broyler_Havalandirma.py", title="Broyler Havalandırma", icon="🐔"),
    ]
)
pg.run()