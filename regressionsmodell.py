import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

# Daten aufteilen
def df_encoden(df):
    """Kodiert die kategorische Variable 'Fach' in numerische Dummy-Variablen."""
    df_encoded = pd.get_dummies(df, columns=["Fach"], drop_first=True)
    return df_encoded
    
def daten_aufteilen(df_encoded):
    """Teilt die Daten in Trainings- und Testdatensätze auf. (80% Training, 20% Test)"""
    X = df_encoded[["Lernzeit"] + [col for col in df_encoded.columns if col.startswith("Fach_")]]
    y = df_encoded["Note"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=17
    )
    return X_train, X_test, y_train, y_test

# Modell definieren und trainieren
def modell_trainieren(X_train, y_train):
    """Trainiert ein lineares Regressionsmodell basierend auf den Trainingsdaten."""
    modell = LinearRegression()
    modell.fit(X_train, y_train)
    return modell

def modell_metriken(modell, X_test, y_test):
    """Berechnet die Metriken Mean Absolute Error (MAE) und R2-Wert für das trainierte Modell."""
    vorhersage = modell.predict(X_test)
    mae = mean_absolute_error(y_test, vorhersage)
    r2_wert = r2_score(y_test, vorhersage)

    return mae, r2_wert
