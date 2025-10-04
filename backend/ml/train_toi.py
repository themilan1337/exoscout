import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, roc_auc_score, f1_score
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import xgboost as xgb
import joblib

df = pd.read_csv("toi.csv", comment="#")

features = [
    "pl_orbper","pl_trandurh","pl_trandep",
    "pl_rade","pl_insol","pl_eqt",
    "st_teff","st_logg","st_rad","st_tmag"
]
keep = features + ["tfopwg_disp"]
df = df.replace([np.inf, -np.inf], np.nan)[keep].dropna()

df = df[(df["pl_orbper"]>0) & (df["pl_trandurh"]>0) & (df["pl_trandep"]>0)]
df = df[(df["pl_rade"]>0) & (df["st_teff"]>0) & (df["st_rad"]>0)]

def label_A(x):
    if x in ("CP","KP"): return 1
    if x=="FP": return 0
    return np.nan  
df["y"] = df["tfopwg_disp"].map(label_A)
train = df.dropna(subset=["y"]).copy()
X = train[features]
y = train["y"].astype(int)

# 5) Сплит
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

numeric = Pipeline([
    ("imp", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
pre = ColumnTransformer([("num", numeric, features)])

xgb_clf = xgb.XGBClassifier(
    n_estimators=400, max_depth=5, learning_rate=0.05,
    subsample=0.9, colsample_bytree=0.9,
    objective="binary:logistic", eval_metric="logloss",
    n_jobs=4, scale_pos_weight=None 
)
pipe = Pipeline([("pre", pre), ("clf", xgb_clf)])
cal = CalibratedClassifierCV(pipe, cv=3, method="sigmoid")
cal.fit(Xtr, ytr)

proba = cal.predict_proba(Xva)[:,1]
pred  = (proba >= 0.5).astype(int)
print("PR-AUC:", average_precision_score(yva, proba))
print("ROC-AUC:", roc_auc_score(yva, proba))

taus = np.linspace(0.3, 0.8, 11)
best_tau = max(taus, key=lambda t: f1_score(yva, (proba>=t).astype(int)))
print("Best τ:", best_tau)

joblib.dump(cal, "toi_model.calibrated.pkl")
joblib.dump(features, "feature_order.pkl")
joblib.dump({"tau": float(best_tau)}, "decision_threshold.pkl")
