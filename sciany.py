import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from collections import defaultdict
import io

# Konfiguracja strony Streamlit
st.set_page_config(
    page_title="Układ Płyt GRAFEXPO",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Układ Płyt GRAFEXPO")
st.write("Wprowadź wymiary ściany oraz dostępnych płyt, aby wygenerować plan rozkroju oraz pełny raport PDF ze spisem.")

# --- PANEL BOCZNY (INPUTY) ---
st.sidebar.header("⚙️ Parametry wejściowe")
sciana_szer = st.sidebar.number_input("Szerokość ściany (mm)", min_value=100.0, value=12500.0, step=100.0)
sciana_wys = st.sidebar.number_input("Wysokość ściany (mm)", min_value=100.0, value=9500.0, step=100.0)
plyta_szer = st.sidebar.number_input("Szerokość płyty (mm)", min_value=100.0, value=2000.0, step=50.0)
plyta_wys = st.sidebar.number_input("Wysokość płyty (mm)", min_value=100.0, value=2750.0, step=50.0)

# --- OBLICZENIA I DANE ---
y_pos = 0
wiersz = 1
zestawienie_wymiarow = defaultdict(int)
elementy_szczegoly = []

liczba_pelnych = 0
boczne_docinki_count = 0
gorne_docinki_count = 0
narozne_docinki_count = 0

while y_pos < sciana_wys:
    akt_wys = min(plyta_wys, sciana_wys - y_pos)
    x_pos = 0
    kolumna = 1
    while x_pos < sciana_szer:
        akt_szer = min(plyta_szer, sciana_szer - x_pos)
        zestawienie_wymiarow[(akt_szer, akt_wys)] += 1
        elementy_szczegoly.append({
            "nazwa": f"R{wiersz}K{kolumna}",
            "szer": akt_szer,
            "wys": akt_wys,
            "x": x_pos,
            "y": y_pos
        })
        
        is_pelna_szer = (akt_szer == plyta_szer)
        is_pelna_wys = (akt_wys == plyta_wys)
        
        if is_pelna_szer and is_pelna_wys:
            liczba_pelnych += 1
        elif not is_pelna_szer and is_pelna_wys:
            boczne_docinki_count += 1
        elif is_pelna_szer and not is_pelna_wys:
            gorne_docinki_count += 1
        else:
            narozne_docinki_count += 1
            
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

# --- WYKRES DLA INTERFEJSU STREAMLIT ---
fig_app, ax_app = plt.subplots(figsize=(10, 6))
sciana_rect_app = patches.Rectangle((0, 0), sciana_szer, sciana_wys, linewidth=2, edgecolor='black', facecolor='#f9f9f9')
ax_app.add_patch(sciana_rect_app)

for el in elementy_szczegoly:
    is_pelna_szer = (el["szer"] == plyta_szer)
    is_pelna_wys = (el["wys"] == plyta_wys)
    if is_pelna_szer and is_pelna_wys:
        kolor = 'lightblue'
    elif not is_pelna_szer and is_pelna_wys:
        kolor = 'lightgreen'
    elif is_pelna_szer and not is_pelna_wys:
        kolor = 'moccasin'
    else:
        kolor = 'lightpink'
        
    rect = patches.Rectangle((el["x"], el["y"]), el["szer"], el["wys"], linewidth=1.2, edgecolor='navy', facecolor=kolor, alpha=0.6)
    ax_app.add_patch(rect)
    ax_app.text(el["x"] + el["szer"]/2, el["y"] + el["wys"]/2, f"{el['nazwa']}\n{el['szer']:.0f}x{el['wys']:.0f}", ha='center', va='center', fontsize=7, weight='bold', color='black')

margines = max(sciana_szer, sciana_wys) * 0.05
ax_app.set_xlim(-margines, sciana_szer + margines)
ax_app.set_ylim(-margines, sciana_wys + margines)
ax_app.set_aspect('equal')
ax_app.set_title(f"Układ Płyt GRAFEXPO – Ściana ({sciana_szer:.0f} x {sciana_wys:.0f} mm) | Szacunek: {calkowite_zapotrzebowanie} płyt", fontsize=11, weight='bold')
ax_app.set_xlabel("Szerokość (mm)")
ax_app.set_ylabel("Wysokość (mm)")
ax_app.grid(True, linestyle='--', alpha=0.5)

# --- UKŁAD STRONY W STREAMLIT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Wizualizacja rozkroju")
    st.pyplot(fig_app)

with col2:
    st.subheader("📊 Bilans i Zapotrzebowanie")
    st.success(f"**Szacowana liczba płyt do zakupu:** `{calkowite_zapotrzebowanie} szt.`")
    
    st.write("**Spis potrzebnych płyt i elementów:**")
    for (szer, wys), ilosc in sorted(zestawienie_wymiarow.items(), key=lambda x: (x[0][0], x[0][1]), reverse=True):
        st.text(f"• {szer:.0f} x {wys:.0f} mm -> {ilosc} szt.")
        
    st.markdown("---")
    st.subheader("📄 Raport PDF ze spisem")
    st.write("Kliknij poniższy przycisk, aby wygenerować profesjonalny plik PDF zawierający **spis materiałów** oraz **schemat graficzny**:")

# --- FUNKCJA GENERUJĄCA KOMPLEKSOWY RAPORT PDF ZE SPISEM ---
def generuj_raport_pdf_ze_spisem():
    fig_pdf = plt.figure(figsize=(10, 14))
    
    gs = fig_pdf.add_gridspec(2, 1, height_ratios=[1.2, 2.5])
    
    # 1. Górna sekcja tekstowa (Spis materiałów)
    ax_text = fig_pdf.add_subplot(gs[0])
    ax_text.axis('off')
    
    tekst_raportu = (
        f"UKŁAD PŁYT GRAFEXPO - RAPORT ROZKROJU I ZAPOTRZEBOWANIA\n"
        f"========================================================================\n"
        f"• Wymiary ściany: {sciana_szer:.0f} x {sciana_wys:.0f} mm\n"
        f"• Wymiary płyty bazowej: {plyta_szer:.0f} x {plyta_wys:.0f} mm\n"
        f"• Szacowana całkowita liczba płyt do zakupu: {calkowite_zapotrzebowanie} szt.\n\n"
        f"SPIS POTRZEBNYCH ELEMENTÓW (WYMIARY DOCINEK):\n"
    )
    for idx, ((szer, wys), ilosc) in enumerate(sorted(zestawienie_wymiarow.items(), key=lambda x: (x[0][0], x[0][1]), reverse=True), 1):
        tekst_raportu += f"  {idx}. Element {szer:.0f} x {wys:.0f} mm  -->  {ilosc} szt.\n"
        
    ax_text.text(0.05, 0.95, tekst_raportu, transform=ax_text.transAxes, fontsize=10, verticalalignment='top', fontfamily='monospace', weight='bold')

    # 2. Dolna sekcja graficzna (Schemat)
    ax_pdf = fig_pdf.add_subplot(gs[1])
    sciana_rect_pdf = patches.Rectangle((0, 0), sciana_szer, sciana_wys, linewidth=2, edgecolor='black', facecolor='#f9f9f9')
    ax_pdf.add_patch(sciana_rect_pdf)

    for el in elementy_szczegoly:
        is_pelna_szer = (el["szer"] == plyta_szer)
        is_pelna_wys = (el["wys"] == plyta_wys)
        if is_pelna_szer and is_pelna_wys:
            kolor = 'lightblue'
        elif not is_pelna_szer and is_pelna_wys:
            kolor = 'lightgreen'
        elif is_pelna_szer and not is_pelna_wys:
            kolor = 'moccasin'
        else:
            kolor = 'lightpink'
            
        rect = patches.Rectangle((el["x"], el["y"]), el["szer"], el["wys"], linewidth=1.2, edgecolor='navy', facecolor=kolor, alpha=0.6)
        ax_pdf.add_patch(rect)
        ax_pdf.text(el["x"] + el["szer"]/2, el["y"] + el["wys"]/2, f"{el['nazwa']}\n{el['szer']:.0f}x{el['wys']:.0f}", ha='center', va='center', fontsize=7, weight='bold', color='black')

    ax_pdf.set_xlim(-margines, sciana_szer + margines)
    ax_pdf.set_ylim(-margines, sciana_wys + margines)
    ax_pdf.set_aspect('equal')
    ax_pdf.set_title("Układ Płyt GRAFEXPO – Schemat rozkroju", fontsize=11, weight='bold')
    ax_pdf.set_xlabel("Szerokość (mm)")
    ax_pdf.set_ylabel("Wysokość (mm)")
    ax_pdf.grid(True, linestyle='--', alpha=0.5)

    fig_pdf.tight_layout()
    
    buf = io.BytesIO()
    fig_pdf.savefig(buf, format='pdf', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig_pdf)
    return buf.getvalue()

pdf_data = generuj_raport_pdf_ze_spisem()

with col2:
    st.download_button(
        label="📥 Pobierz raport PDF ze spisem",
        data=pdf_data,
        file_name="grafexpo_raport_rozkroju.pdf",
        mime="application/pdf"
    )
