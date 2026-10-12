import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from pathlib import Path
import csv
import matplotlib.dates as mdates
import streamlit as st

csv_datei = Path(__file__).resolve().parent / "leistungen.csv"

def daten_speichern(daten, spalten, csv_datei) -> None:
    """
    Speichert die eingegebenen Daten in einer CSV-Datei.
    Wenn die Datei nicht existiert, wird sie erstellt und die Spaltenüberschriften werden hinzugefügt.
    """
    
    if not csv_datei.exists():
        with open(csv_datei, mode="w", newline="", encoding="utf-8") as datei:
            writer = csv.DictWriter(datei, fieldnames=spalten)
            writer.writeheader()
            writer.writerow(daten)
    else:
        with open(csv_datei, mode="a", newline="", encoding="utf-8") as datei:
            writer = csv.DictWriter(datei, fieldnames=spalten)
            writer.writerow(daten)



def auswertung_lernzeit(csv_datei) -> None:
    """Erstellt eine Auswertung der durchschnittlichen Lernzeit und der Noten basierend auf den gespeicherten Daten."""
    # Daten einlesen und aufbereiten
    df = pd.read_csv(csv_datei)
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

    df_auswertung = df[:]
    df_auswertung = df_auswertung.sort_values(by="Datum", ascending=True)

    kategorien_bar = (
        df_auswertung.groupby("Fach")
        .agg({"Lernzeit": "mean", "Note": "mean"})
        .reset_index()
    )


    # Spalte 1: Durchschnittliche Lernzeit
    fig1, ax1 = plt.subplots()
    sb.barplot(data=kategorien_bar, x="Fach", y="Lernzeit", ax=ax1)
    ax1.set_title("Durchschnittliche Lernzeit pro Fach")
    ax1.set_xlabel("Fach")
    ax1.set_ylabel("Lernzeit")

    ax1.tick_params(axis="x", rotation=45)
    
    for label in ax1.get_xticklabels():
        label.set_horizontalalignment("right")
    
    st.pyplot(fig1)

    # Spalte 2: Durchschnittliche Note
    fig2, ax2 = plt.subplots()
    sb.barplot(data=kategorien_bar, x="Fach", y="Note", ax=ax2)
    ax2.set_title("Durchschnittliche Note pro Fach")
    ax2.set_xlabel("Fach")
    ax2.set_ylabel("Prüfungsnote")

    ax2.tick_params(axis="x", rotation=45)

    for label in ax2.get_xticklabels():
        label.set_horizontalalignment("right")

    st.pyplot(fig2)


def auswertung_note(csv_datei, fach_eingabe) -> None:
    """Erstellt eine Auswertung der Notenentwicklung für ein bestimmtes Fach basierend auf den gespeicherten Daten."""
    # Daten einlesen und aufbereiten
    df = pd.read_csv(csv_datei)
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

    df_auswertung = df[:]
    df_auswertung = df_auswertung[df_auswertung["Fach"] == fach_eingabe]
    df_auswertung = df_auswertung.sort_values(by="Datum", ascending=True)


    # Spalte 1: Durchschnittliche Note über die Zeit
    fig3, ax3 = plt.subplots()
    sb.lineplot(data=df_auswertung, x="Datum", y="Note", ax=ax3, marker="o")
    ax3.set_title(f"Entwicklung der {fach_eingabe} Note über die Zeit")
    ax3.set_xlabel("Datum")
    ax3.set_ylabel("Prüfungsnote")

    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
    ax3.xaxis.set_major_locator(mdates.AutoDateLocator())
    
    for label in ax3.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    st.pyplot(fig3)
