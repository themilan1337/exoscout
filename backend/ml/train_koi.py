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

# 1) Читаем cumulative KOI
df = pd.read_csv("cumulative.csv", comment="#")

# 2) Лейбл
def to_label(x):
    if x in ("CONFIRMED", "CANDIDATE"):
        return 1
    if x == "FALSE POSITIVE":
        return 0
    return np.nan
df["y"] = df["koi_disposition"].map(to_label)

# 3) Фичи
features = [
    "koi_period","koi_duration","koi_depth","koi_model_snr","koi_impact",
    "koi_prad","koi_teq","koi_insol",
    "koi_steff","koi_slogg","koi_srad"
]

df = df[features + ["y"]].replace([np.inf, -np.inf], np.nan)

# 4) Чистим
df = df.dropna(subset=["y"])
df = df[(df["koi_period"] > 0) & (df["koi_duration"] > 0) & (df["koi_depth"] > 0)]

X = df[features]
y = df["y"].astype(int)

# 5) Train/test split
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 6) Препроцессинг
numeric = Pipeline([
    ("imp", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
pre = ColumnTransformer([("num", numeric, features)])

# 7) Модель
xgb_clf = xgb.XGBClassifier(
    n_estimators=400, max_depth=6, learning_rate=0.05,
    subsample=0.9, colsample_bytree=0.9,
    objective="binary:logistic", eval_metric="logloss"
)
pipe = Pipeline([("pre", pre), ("clf", xgb_clf)])
cal = CalibratedClassifierCV(pipe, cv=3, method="sigmoid")

cal.fit(Xtr, ytr)

# 8) Метрики
proba = cal.predict_proba(Xva)[:,1]
print("ROC-AUC:", roc_auc_score(yva, proba))
print("PR-AUC:", average_precision_score(yva, proba))

taus = np.linspace(0.3,0.8,6)
best_tau = max(taus, key=lambda t: f1_score(yva, (proba>=t).astype(int)))
print("Best τ:", best_tau)

# 9) Сохраняем
joblib.dump(cal, "koi_model.calibrated.pkl")
joblib.dump(features, "koi_feature_order.pkl")
joblib.dump({"tau": float(best_tau)}, "koi_threshold.pkl")
