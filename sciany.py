import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from collections import defaultdict
import io

# Konfiguracja strony Streamlit (musi być pierwszą instrukcją Streamlit)
st.set_page_config(
    page_title="Kalkulator Układu Płyt",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Inteligentny Kalkulator Układu Płyt i Docinek")
st.write("Wprowadź wymiary ściany oraz dostępnych płyt, aby wygenerować plan rozkroju oraz raport PDF.")

# --- PANEL BOCZNY (INPUTY) ---
st.sidebar.header("⚙️ Parametry wejściowe")

st.sidebar.subheader("Wymiary ściany")
sciana_szer = st.sidebar.number_input("Szerokość ściany (mm)", min_value=100.0, value=12500.0, step=100.0)
sciana_wys = st.sidebar.number_input("Wysokość ściany (mm)", min_value=100.0, value=9500.0, step=100.0)

st.sidebar.subheader("Wymiary płyty")
plyta_szer = st.sidebar.number_input("Szerokość płyty (mm)", min_value=100.0, value=2000.0, step=50.0)
plyta_wys = st.sidebar.number_input("Wysokość płyty (mm)", min_value=100.0, value=2750.0, step=50.0)

# --- OBLICZENIA I TWORZENIE WYKRESU ---
fig, ax = plt.subplots(figsize=(12, 7))

# Rysowanie konturu ściany
sciana_rect = patches.Rectangle((0, 0), sciana_szer, sciana_wys, 
                                linewidth=2, edgecolor='black', facecolor='#f9f9f9')
ax.add_patch(sciana_rect)

y_pos = 0
wiersz = 1
zestawienie_wymiarow = defaultdict(int)

liczba_pelnych = 0
boczne_docinki_count = 0
gorne_docinki_count = 0
narozne_docinki_count = 0

# Pętla po rzędach i kolumnach
while y_pos < sciana_wys:
    akt_wys = min(plyta_wys, sciana_wys - y_pos)
    x_pos = 0
    kolumna = 1
    
    while x_pos < sciana_szer:
        akt_szer = min(plyta_szer, sciana_szer - x_pos)
        zestawienie_wymiarow[(akt_szer, akt_wys)] += 1
        
        is_pelna_szer = (akt_szer == plyta_szer)
        is_pelna_wys = (akt_wys == plyta_wys)
        
        if is_pelna_szer and is_pelna_wys:
            liczba_pelnych += 1
            kolor = 'lightblue'
        elif not is_pelna_szer and is_pelna_wys:
            boczne_docinki_count += 1
            kolor = 'lightgreen'
        elif is_pelna_szer and not is_pelna_wys:
            gorne_docinki_count += 1
            kolor = 'moccasin'
        else:
            narozne_docinki_count += 1
            kolor = 'lightpink'
        
        element = patches.Rectangle((x_pos, y_pos), akt_szer, akt_wys, 
                                  linewidth=1.2, edgecolor='navy', facecolor=kolor, alpha=0.6)
        ax.add_patch(element)
        
        tekst = f"R{wiersz}K{kolumna}\n{akt_szer:.0f}x{akt_wys:.0f}"
        ax.text(x_pos + akt_szer/2, y_pos + akt_wys/2, tekst, 
                ha='center', va='center', fontsize=8, weight='bold', color='black')
        
        x_pos += plyta_szer
        kolumna += 1
        
    y_pos += plyta_wys
    wiersz += 1

# Szacowanie zapotrzebowania
pionowe_paski_z_plyty = math.floor(plyta_szer / 500) if boczne_docinki_count > 0 else 1
plyty_na_boki = math.ceil(boczne_docinki_count / pionowe_paski_z_plyty) if boczne_docinki_count > 0 else 0

poziome_paski_z_plyty = math.floor(plyta_wys / 1250) if gorne_docinki_count > 0 else 1
plyty_na_gore = math.ceil(gorne_docinki_count / poziome_paski_z_plyty) if gorne_docinki_count > 0 else 0

calkowite_zapotrzebowanie = liczba_pelnych + max(plyty_na_boki, plyty_na_gore) + (1 if narozne_docinki_count > 0 else 0)

# Ustawienia wykresu
margines = max(sciana_szer, sciana_wys) * 0.05
ax.set_xlim(-margines, sciana_szer + margines)
ax.set_ylim(-margines, sciana_wys + margines)
ax.set_aspect('equal')

tytul = f"Plan rozkroju ściany ({sciana_szer:.0f} x {sciana_wys:.0f} mm) | Płyty: ok. {calkowite_zapotrzebowanie} szt."
ax.set_title(tytul, fontsize=12, pad=15, weight='bold')
ax.set_xlabel("Szerokość ściany (mm)", fontsize=11)
ax.set_ylabel("Wysokość ściany (mm)", fontsize=11)
ax.grid(True, linestyle='--', alpha=0.5)

# --- UKŁAD STRONY W STREAMLIT (2 KOLUMNY) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Wizualizacja rozkroju")
    st.pyplot(fig)

with col2:
    st.subheader("📊 Bilans i Zapotrzebowanie")
    st.success(f"**Szacowana liczba płyt do zakupu:** `{calkowite_zapotrzebowanie} szt.`")
    
    st.write("**Szczegółowy zestaw elementów:**")
    for (szer, wys), ilosc in sorted(zestawienie_wymiarow.items(), key=lambda x: (x[0][0], x[0][1]), reverse=True):
        st.text(f"• {szer:.0f} x {wys:.0f} mm -> {ilosc} szt.")
        
    st.markdown("---")
    st.subheader("📄 Raport PDF")
    st.write("Kliknij poniższy przycisk, aby wygenerować raport PDF z obecnym wykresem i danymi:")

    # Funkcja do zapisu figury do pamięci (BytesIO)
    def generuj_pdf():
        buf = io.BytesIO()
        fig.savefig(buf, format='pdf', bbox_inches='tight')
        buf.seek(0)
        return buf.getvalue()

    pdf_bytes = generuj_pdf()

    # Przycisk pobierania raportu generowany w locie
    st.download_button(
        label="📥 Pobierz raport PDF",
        data=pdf_bytes,
        file_name="raport_rozkroju_sciany.pdf",
        mime="application/pdf"
    )
