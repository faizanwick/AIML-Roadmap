def calculate_bmi(height: float, weight: float) -> float:
    height /= 100
    return round(weight / (height**2), 2)

def get_bmi_verdict(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"