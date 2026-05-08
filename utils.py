# ── Risk computation ──────────────────────────────────────────────────────────
def compute_risk(model_prob, bp, chol, triglyceride, fasting, crp,
                 homocysteine, bmi, smoking, diabetes, family,
                 high_bp, low_hdl, high_ldl, age, exercise, sleep):
    med = 0
    if bp > 180:             med += 20
    elif bp > 160:           med += 12
    elif bp > 140:           med += 6
    if chol > 300:           med += 15
    elif chol > 240:         med += 8
    if triglyceride > 400:   med += 15
    elif triglyceride > 200: med += 7
    if fasting > 126:        med += 15
    elif fasting > 100:      med += 6
    if crp > 10:             med += 15
    elif crp > 3:            med += 7
    if homocysteine > 20:    med += 12
    elif homocysteine > 15:  med += 6
    if bmi > 40:             med += 12
    elif bmi > 35:           med += 7
    elif bmi > 30:           med += 3
    if smoking:              med += 15
    if diabetes:             med += 12
    if family:               med += 10
    if high_bp:              med += 8
    if low_hdl:              med += 7
    if high_ldl:             med += 7
    if age > 65:             med += 10
    elif age > 55:           med += 5
    if exercise:             med -= 8
    if 7 <= sleep <= 8:      med -= 4
    med = max(0, min(med, 100))

    prob = 0.6 * model_prob + 0.4 * med
    if bp > 200 or chol > 400 or triglyceride > 500 or fasting > 200 or crp > 15 or homocysteine > 30 or bmi > 45:
        prob = max(prob, 80.0)
    prob = min(prob, 99.0)

    flags = sum([
        bp > 180, chol > 300, bmi > 35, smoking, diabetes,
        crp > 10, triglyceride > 400, fasting > 126,
        high_bp, low_hdl, high_ldl, homocysteine > 20, family
    ])
    health = max(0, 100 - int(prob) - flags * 2)
    return prob, med, flags, health


def sub_scores(bp, chol, bmi, stress, sleep, sugar,
               smoking, diabetes, family, crp, fasting, exercise):
    cardiac   = min(100, (max(0, bp - 100) / 200) * 40 + (max(0, chol - 150) / 350) * 35 + (25 if smoking else 0))
    metabolic = min(100, (max(0, bmi - 18) / 42) * 30 + (max(0, fasting - 70) / 230) * 35 + (max(0, sugar) / 10) * 20 + (15 if diabetes else 0))
    lifestyle = min(100, stress * 8 + max(0, 8 - sleep) * 6 + (30 if smoking else 0) + (0 if exercise else 15))
    inflam    = min(100, (crp / 20) * 60 + (25 if family else 0) + 15)
    return {
        "Cardiac Risk":   int(cardiac),
        "Metabolic Risk": int(metabolic),
        "Lifestyle Risk": int(lifestyle),
        "Inflammation":   int(inflam),
    }
