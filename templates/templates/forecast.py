"""Demonstration forecast using a reproducible synthetic dataset.
Replace the sample observations with verified factory production history for real forecasts."""
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_production():
    months = np.arange(1, 13).reshape(-1, 1)
    # Synthetic example data; not real company data.
    produced = np.array([420, 450, 465, 490, 510, 530, 555, 570, 590, 615, 630, 660])
    model = LinearRegression().fit(months, produced)
    next_month = int(model.predict(np.array([[13]]))[0])
    score = float(model.score(months, produced))
    return {
        "next_month": next_month,
        "r2": round(score, 3),
        "months": months.flatten().tolist(),
        "values": produced.tolist(),
        "note": "Namoyish uchun sun’iy ma’lumot. Haqiqiy prognoz uchun korxonaning tarixiy ma’lumotlari kerak."
    }
