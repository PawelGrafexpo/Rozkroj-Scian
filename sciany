import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from collections import defaultdict

def inteligentny_kalkulator_z_pdf():
    print("=== KALKULATOR UKŁADU PŁYT Z EKSPORTEM DO PDF ===")
    try:
        sciana_szer = float(input("Podaj szerokość ściany w mm (np. 12500): "))
        sciana_wys = float(input("Podaj wysokość ściany w mm (np. 9500): "))
        
        p_szer_input = input("Podaj szerokość płyty w mm [domyślnie 2000]: ")
        plyta_szer = float(p_szer_input) if p_szer_input.strip() else 2000
        
        p_wys_input = input("Podaj wysokość płyty w mm [domyślnie 2750]: ")
        plyta_wys = float(p_wys_input) if p_wys_input.strip() else 2750
        
    except ValueError:
        print("\n[BŁĄD] Wprowadź poprawne wartości liczbowe!")
        return

    # Większy format figury, aby zmieścił się wykres i raport tekstowy
    fig, ax = plt.subplots(figsize=(14, 10))
    
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

    # Obliczenia zapotrzebowania
    pionowe_paski_z_plyty = math.floor(plyta_szer / 500) if boczne_docinki_count > 0 else 1
    plyty_na_boki = math.ceil(boczne_docinki_count / pionowe_paski_z_plyty) if boczne_docinki_count > 0 else 0
    
    poziome_paski_z_plyty = math.floor(plyta_wys / 1250) if gorne_docinki_count > 0 else 1
    plyty_na_gore = math.ceil(gorne_docinki_count / poziome_paski_z_plyty) if gorne_docinki_count > 0 else 0
    
    calkowite_zapotrzebowanie = liczba_pelnych + max(plyty_na_boki, plyty_na_gore) + (1 if narozne_docinki_count > 0 else 0)

    # Przygotowanie tekstu podsumowania w konsoli i na wykresie PDF
    podsumowanie_tekst = (
        f"RAPORT ROZKROJU: Ściana {sciana_szer:.0f}x{sciana_wys:.0f} mm | Płyta {plyta_szer:.0f}x{plyta_wys:.0f} mm\n"
        f"Zapotrzebowanie szacunkowe: OK. {calkowite_zapotrzebowanie} PŁYT "
        f"(Pełne: {liczba_pelnych}, Boczne: {boczne_docinki_count}, Górne: {gorne_docinki_count}, Narożnik: {narozne_docinki_count})"
    )
    
    print("\n" + "="*60)
    print("      RAPORT WYGENEROWANY PŁYNNIE DO PLIKU PDF      ")
    print("="*60)
    print(podsumowanie_tekst)
    print("="*60 + "\n")

    # Ustawienia wykresu i umieszczenie raportu na górze
    margines = max(sciana_szer, sciana_wys) * 0.05
    ax.set_xlim(-margines, sciana_szer + margines)
    ax.set_ylim(-margines, sciana_wys + margines)
    ax.set_aspect('equal')
    
    plt.title(podsumowanie_tekst, fontsize=10, pad=20, weight='bold')
    plt.xlabel("Szerokość ściany (mm)", fontsize=11)
    plt.ylabel("Wysokość ściany (mm)", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Zapis do pliku PDF
    nazwa_pliku_pdf = "raport_rozkroju_sciany.pdf"
    plt.savefig(nazwa_pliku_pdf, format='pdf', bbox_inches='tight')
    print(f"[SUKCES] Zapisano plik: {nazwa_pliku_pdf}")
    
    plt.show()

    # Automatyczne pobranie pliku w Google Colab
    try:
        from google.colab import files
        files.download(nazwa_pliku_pdf)
    except ImportError:
        print(f"Plik PDF '{nazwa_pliku_pdf}' jest dostępny w folderze roboczym.")

# Uruchomienie
inteligentny_kalkulator_z_pdf()
