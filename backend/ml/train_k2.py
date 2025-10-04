import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.calibration import CalibratedClassifierCV
import xgboost as xgb
import joblib

df = pd.read_csv("k2.csv", comment="#")

features = [
    "pl_orbper","pl_orbsmax","pl_rade","pl_bmasse",
    "pl_insol","pl_eqt","pl_orbeccen",
    "st_teff","st_rad","st_mass","st_logg","st_met"
]
df = df.replace([np.inf, -np.inf], np.nan)

# 3) Лейбл
def to_label(x):
    if x == "CONFIRMED" or x == "CANDIDATE": return 1
    if x == "FALSE POSITIVE": return 0
    return np.nan
df["y"] = df["disposition"].map(to_label)

df = df[features + ["y"]].dropna(subset=["y"])
X = df[features]
y = df["y"].astype(int)

Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

numeric = Pipeline([
    ("imp", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
pre = ColumnTransformer([("num", numeric, features)])

xgb_clf = xgb.XGBClassifier(
    n_estimators=400, max_depth=5, learning_rate=0.05,
    subsample=0.9, colsample_bytree=0.9,
    objective="binary:logistic", eval_metric="logloss"
)
pipe = Pipeline([("pre", pre), ("clf", xgb_clf)])
cal = CalibratedClassifierCV(pipe, cv=3, method="sigmoid")

cal.fit(Xtr, ytr)

# 7) Метрики
proba = cal.predict_proba(Xva)[:,1]
print("ROC-AUC:", roc_auc_score(yva, proba))
print("PR-AUC:", average_precision_score(yva, proba))

taus = np.linspace(0.3,0.8,6)
best_tau = max(taus, key=lambda t: f1_score(yva, (proba>=t).astype(int)))
print("Best τ:", best_tau)

# 8) Сохранение
joblib.dump(cal, "k2_model.calibrated.pkl")
joblib.dump(features, "k2_feature_order.pkl")
joblib.dump({"tau": float(best_tau)}, "k2_threshold.pkl")
