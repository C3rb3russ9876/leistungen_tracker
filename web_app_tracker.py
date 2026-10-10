import streamlit as st
from lern_tracker import daten_speichern, auswertung_lernzeit, auswertung_note, csv_datei
import pandas as pd


def dateieingabe():
    """Funktion für die Dateneingabe und Speicherung in der CSV-Datei."""
    
    st.title("Lern-Tracker")

    st.header("1. Dateneingabe")

    datum = st.date_input("Bitte Datum der Prüfung angeben. (YYYY/MM/DD)")
    datum = datum.strftime("%d.%m.%Y")
    fach = st.text_input("In welchem Fach hattest du die Prüfung?").strip().lower()
    lernzeit = st.number_input("Wie viel hast du für die Prüfung gelernt? (h)", min_value=0.0, step=0.5)
    note = st.slider("Bitte die Note bei der Prüfung angeben.", min_value=1.0, max_value=6.0, value=4.0, step=0.05)



    if st.button("Lernzeit und Note speichern"):
        if not fach:
            st.warning("Bitte gib ein Fach ein.")
        else:
            daten = {
                "Datum": datum,
                "Fach": fach,
                "Lernzeit": lernzeit,
                "Note": note
            }
            spalten = ["Datum", "Fach", "Lernzeit", "Note"]

            daten_speichern(daten, spalten, csv_datei)

            st.success("Daten wurden erfolgreich gespeichert!")

            
    if csv_datei.exists():
        auswertung_lernzeit(csv_datei)
        st.header("2. Noten Entwicklung")
        fach_eingabe = st.selectbox("Bitte das Fach auswählen, um die Notenentwicklung zu sehen:", options=pd.read_csv(csv_datei)["Fach"].dropna().unique())
        auswertung_note(csv_datei, fach_eingabe)



def regressionsmodell_auswertung(modell, mae, r2_wert):
    """Funktion zur Anzeige der Ergebnisse des Regressionsmodells und zur Vorhersage der Note basierend auf der Lernzeit."""

    st.header("3. Regressionsmodell")
    st.write("Das Regressionsmodell wurde mit den neuen bzw. bestehenden Daten trainiert.")
    st.write(f"Mean Absolute Error (Wie weit ist der Fehler vom echten Wert entfernt?): {mae:.2f}")
    st.write(f"R2-Wert (Bestimmtheitsmass): {r2_wert:.2f}")
    lernzeit_input = st.number_input("Bitte die Lernzeit (h) für die Vorhersage der Note eingeben:", min_value=0.0)
    fach_input = st.selectbox("In welchem Fach hattest du die Prüfung?", options=pd.read_csv(csv_datei)["Fach"].dropna().unique())
    if st.button("Vorhersage der Note basierend auf der Lernzeit"):
        input_data = [lernzeit_input]
        for col in modell.feature_names_in_:
            if col.startswith("Fach_"):
                input_data.append(1 if col == f"Fach_{fach_input}" else 0)
        
        vorhersage = modell.predict([input_data])[0]
        if vorhersage < 1.0:
            st.write(f"Die vorhergesagte Note für eine Lernzeit von {lernzeit_input} Stunden beträgt: 1.00")
        elif vorhersage > 6.0:
            st.write(f"Die vorhergesagte Note für eine Lernzeit von {lernzeit_input} Stunden beträgt: 6.00")
        else:
            st.write(f"Die vorhergesagte Note für eine Lernzeit von {lernzeit_input} Stunden beträgt: {vorhersage:.2f}")

    st.warning("Bitte beachten Sie, dass das Modell nur eine lineare Regression ist und die Vorhersagen nicht immer genau sein können.")
    st.warning(
        "Die Vorhersagequalität hängt von der Menge, Qualität "
        "und Relevanz der Daten ab."
    )
def main():
    """Hauptfunktion, die die Dateneingabe, Auswertung und das Regressionsmodell trainiert und steuert."""
    if csv_datei.exists():
        anzahl_eintraege = len(pd.read_csv(csv_datei))
        if anzahl_eintraege >= 20:
            from regressionsmodell import modell_trainieren, modell_metriken, daten_aufteilen, df_encoden
            dateieingabe()
            df = pd.read_csv(csv_datei)
            df_encoded = df_encoden(df)
            X_train, X_test, y_train, y_test = daten_aufteilen(df_encoded)
            modell = modell_trainieren(X_train, y_train)
            mae, r2_wert = modell_metriken(modell, X_test, y_test)
            regressionsmodell_auswertung(modell, mae, r2_wert)
        else:
            st.info("Es sind mindestens 20 Einträge erforderlich, um das Regressionsmodell zu trainieren. Bitte geben Sie weitere Daten ein.")
            dateieingabe()
    else:
        dateieingabe()

main()
