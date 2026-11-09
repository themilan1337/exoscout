# ExoScout

ExoScout was a two-person project at NASA Space Apps Challenge Astana 2025 (4 and 5 October 2025), for the challenge [A World Away: Hunting for Exoplanets with AI](https://www.spaceappschallenge.org/2025/challenges/a-world-away-hunting-for-exoplanets-with-ai/). It is a web app. You enter a Kepler, K2 or TESS target ID. The backend looks up the object's catalog parameters in the NASA Exoplanet Archive, a per-mission XGBoost model scores them, and the page shows the result next to the object's light curve.

I built the frontend. My teammate and I built the backend and the models. The hosted demo is no longer running.

## What it does and does not do

The model sees only catalog parameters (period, radius, stellar temperature and so on). It never sees a light curve. The light curve on the page is displayed for the user: it is downloaded, summed or stitched, normalised as (flux minus median) divided by median and plotted. There is no detrending, no transit search and no detection from photometry anywhere in this code. ExoScout sorts catalog rows into two groups, "planet or planet candidate" and "false positive". It does not find planets in telescope data, and it does not separate confirmed planets from candidates.

There is no neural network in the repository, and no comparison between XGBoost and any other model was made. The choice of XGBoost rests on the inputs being a few thousand rows of catalog columns.

## Results

Measured on the 20 percent of rows that each training script holds out (80/20 split, `random_state=42`, stratified by label), with the scripts in `backend/ml/` run unmodified (scikit-learn 1.7.2, XGBoost 3.2.0). Refitting a script gives the same scores as the saved model in `backend/models/`.

| | Kepler | K2 | TESS |
|---|---|---|---|
| Held-out rows (label 1 / label 0) | 1,840 (924 / 916) | 797 (738 / 59) | 436 (246 / 190) |
| ROC-AUC | 0.927 | 0.945 | 0.912 |
| PR-AUC | 0.923 | 0.993 | 0.920 |

So the ROC-AUC is 0.91 to 0.95 across the three missions, on a random split by row. Read these numbers with the limits below: the split is not by star, and for K2 the label can be predicted from missing values alone (limit 1). They are not evidence that the models find planets.

An earlier version of this README stated accuracy above 95 percent, precision above 92 percent, recall above 89 percent and a false-positive rate below 5 percent, and listed uptime and speed figures. None of those was measured, and they have been removed. At the saved thresholds, accuracy on the held-out rows is 0.85 for Kepler and TESS and 0.95 for K2, where 738 of the 797 held-out rows are label 1.

## Architecture

- Frontend (`frontend/`): Nuxt 4 and Vue 3, Three.js for procedurally generated planet pictures (`app/composables/usePlanetGenerator.ts`, shaders in `shaders.ts`), ApexCharts for the light curve (`app/components/ApexLightcurveChart.vue`). Single-page app (`ssr: false` in `nuxt.config.ts`).
- Backend (`backend/`): FastAPI (`main.py`), routes under `/api/v1`: `resolve`, `features`, `lightcurve`, `predict`. Archive queries go to the NASA Exoplanet Archive TAP service (`services/nasa_api.py`), with a disk cache (`utils/cache.py`).
- Models (`backend/ml/`, `backend/models/`): one calibrated XGBoost classifier per mission, trained by `train_koi.py` (Kepler), `train_k2.py` (K2) and `train_toi.py` (TESS), saved as pickle files and loaded by `services/model.py`.

Data flow for a prediction (`routers/predict.py`): target ID, then an archive query that returns the catalog row, then the model's feature columns in the saved order, then median imputation, scaling, XGBoost and Platt calibration, then a probability. The probability is compared with the mission's threshold. The response says `CONFIRMED` above the threshold and `FALSE_POSITIVE` below it (line 156). `CONFIRMED` here means label 1, which also contains candidates (see below).

Light curves (`routers/lightcurve.py`):

- TESS: a 5 by 5 pixel cutout from MAST TESSCut (lines 62 to 69). The flux is summed over the 25 pixels (line 144), normalised as (flux minus median) divided by median and returned (lines 160 to 163). The cutout is not a calibrated aperture or a PDCSAP light curve.
- Kepler and K2: searched and downloaded with lightkurve, stitched, normalised as (flux minus median) divided by median (lines 238 to 364). If lightkurve returns nothing there is an astroquery fallback (line 400).

## Models and data

| | Kepler | K2 | TESS |
|---|---|---|---|
| Archive table | KOI cumulative list | K2 Planets and Candidates (inferred from the columns; the file header does not name it) | TESS Project Candidates (TOI) |
| File in `backend/` | `cumulative.csv`, 9,564 rows | `k2.csv`, 4,004 rows, 1,806 distinct planet names | `toi.csv`, 7,703 rows |
| Label 1 | `CONFIRMED` or `CANDIDATE` | `CONFIRMED` or `CANDIDATE` | `CP` or `KP` |
| Label 0 | `FALSE POSITIVE` | `FALSE POSITIVE` | `FP` |
| Dropped | 364 labelled rows with a missing or non-positive `koi_period`, `koi_duration` or `koi_depth` (`train_koi.py` lines 25 to 35) | `REFUTED` (22 rows) | `PC`, `APC`, `FA` by label; and 288 labelled rows (2,464 to 2,176) with any of the 10 features missing, or `pl_orbper`, `pl_trandurh`, `pl_trandep`, `pl_rade`, `st_teff` or `st_rad` not above zero (`train_toi.py` lines 10 to 30) |
| Rows used (label 1 / label 0) | 9,200 (4,618 / 4,582) | 3,982 (3,689 / 293) | 2,176 (1,227 / 949) |
| Feature columns | 11: `koi_period`, `koi_duration`, `koi_depth`, `koi_model_snr`, `koi_impact`, `koi_prad`, `koi_teq`, `koi_insol`, `koi_steff`, `koi_slogg`, `koi_srad` | 12: `pl_orbper`, `pl_orbsmax`, `pl_rade`, `pl_bmasse`, `pl_insol`, `pl_eqt`, `pl_orbeccen`, `st_teff`, `st_rad`, `st_mass`, `st_logg`, `st_met` | 10: `pl_orbper`, `pl_trandurh`, `pl_trandep`, `pl_rade`, `pl_insol`, `pl_eqt`, `st_teff`, `st_logg`, `st_rad`, `st_tmag` |
| XGBoost | 400 trees, depth 6, learning rate 0.05 | 400 trees, depth 5, learning rate 0.05 | 400 trees, depth 5, learning rate 0.05 |
| Threshold grid | 0.3 to 0.8, 6 values, step 0.1 | 0.3 to 0.8, 6 values, step 0.1 | 0.3 to 0.8, 11 values, step 0.05 |
| Threshold in the saved file | 0.4 | 0.6 | 0.4 |

Common to all three: subsample 0.9 and column sample 0.9; median imputation and standard scaling inside the pipeline; Platt (sigmoid) calibration with `CalibratedClassifierCV(cv=3)`; a random 80/20 split with `random_state=42`, stratified by label. The decision threshold is the grid value with the best F1 score on the held-out fifth of the rows. Training code: `backend/ml/train_koi.py`, `train_k2.py`, `train_toi.py`. The archive tables are the CSV files in `backend/`; their headers say they were produced by the archive on Saturday 4 October 2025.

Missing inputs differ by mission. The Kepler and TESS training rows have no missing input values at all (the filters above remove them before training), yet the served model still imputes medians when a live archive row has gaps. K2 is the opposite: 3,927 of the 3,982 training rows have at least one input missing, and the median imputer fills them.

The labels are the archive's own dispositions, so the models learn to reproduce earlier human and pipeline vetting from catalog values. The Kepler feature list contains none of the archive's vetting flag columns (`koi_fpflag_*`) or its disposition score.

## Known limits

Each limit points to the code at commit 7a239ba.

1. **The K2 label leaks through missing values.** Among the 3,982 labelled K2 rows, 3,171 lack the semi-major axis, 3,554 the planet mass, 3,355 the insolation, 3,140 the equilibrium temperature and 3,560 the eccentricity (`train_k2.py` lines 14 to 28). The number of missing columns alone is only weakly related to the label (ROC-AUC 0.407, so false positives miss slightly more), but the pattern of which columns are missing is not. A model that sees only which of the 12 columns are missing, not their values, ranks label 1 above label 0 with ROC-AUC 0.906 on the same held-out split, against 0.945 for the K2 model itself. Method: the features are the 12 yes/no indicators "this column is missing" for the model's own input columns, the labels and the split are those of `train_k2.py` (`test_size=0.2`, `random_state=42`, stratified), the classifier is XGBoost with the hyperparameters of `train_k2.py`, and the score is ROC-AUC on the held-out rows. Over stratified 5-fold cross-validation the same setup gives 0.881 with standard deviation 0.034; a logistic regression on the same indicators gives 0.857. The K2 model can therefore score well by reading missingness, not astrophysics. The classes are also lopsided (3,689 label 1 against 293 label 0), which is why the K2 PR-AUC of 0.993 says little.
2. **The split is random, not by star.** `train_test_split(..., test_size=0.2, random_state=42, stratify=y)` (`train_koi.py` line 41, `train_k2.py` line 32, `train_toi.py` line 35). The K2 file has 4,004 rows for 1,806 distinct planet names (default and non-default parameter sets), so the same planet, and any star with several planets, can sit on both sides of the split. The ROC-AUC values above are probably optimistic for that reason.
3. **The threshold is tuned on the evaluation split.** The F1-best threshold is picked on `yva`, the held-out fifth that is also used to report scores (`train_koi.py` lines 66 to 68, `train_k2.py` lines 55 to 57, `train_toi.py` lines 58 to 60). Threshold-dependent scores (accuracy, precision, recall, F1) measured there are optimistic. ROC-AUC does not depend on the threshold. There is no separate test set.
4. **No baseline was compared.** There is no logistic regression, no single-feature rule and no other model in the repository, so there is nothing to say how much XGBoost adds. Nothing compares it with the Kepler Robovetter, ExoMiner or a light-curve network.
5. **The planet card is not data.** The type, mass, radius, temperature, distance and discovery year on the dashboard are generated pseudo-randomly from the target ID (`frontend/app/composables/usePlanetGenerator.ts` lines 190 to 232, shown in `frontend/app/pages/dashboard.vue` lines 205 to 279). The planet picture is also generated from the ID and the prediction (lines 53 to 75). Treat the card as an illustration.
6. **The K2 lookup returns none of the model's inputs.** `get_k2_features` queries the archive table `k2targets` (`services/nasa_api.py` line 257). On 18 October and again on 9 November 2026 a query for EPIC 206103150 returned 86 columns and none of the 12 columns the K2 model expects, so for that target every K2 input would be imputed. Only this one target was checked, and no K2 prediction was run end to end. The Kepler and TESS lookups return their model columns.
7. **The model does not use the light curve.** The TESS light curve sums a whole 5 by 5 cutout, so nearby stars contaminate it, and it is only displayed.

## Run it locally

I ran these steps on 9 November 2026 on macOS with Python 3.12 and Node 25 and pnpm 10, in a clean copy of this repository. The backend answered `/health` and a TESS prediction, and the frontend served its page with HTTP 200 (I did not click through the interface). The Docker setup was not run. On macOS, XGBoost needs the OpenMP runtime (`brew install libomp`).

Backend:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install "scikit-learn==1.7.2" # the pickled models were saved with this version
mkdir -p logs                     # main.py opens logs/app.log at import and does not create it
uvicorn main:app --port 8000
```

Run it from `backend/`, because the model files are loaded from `models/` relative to the working directory. `requirements.txt` does not pin versions. With scikit-learn 1.9.1 the models load and `GET /api/v1/predict/models/status` looks fine, but every prediction fails with `'SimpleImputer' object has no attribute '_fill_dtype'`. With scikit-learn 1.7.2 and XGBoost 3.2.0 predictions work.

Check it:

```bash
curl localhost:8000/health
curl localhost:8000/api/v1/predict/models/status
curl localhost:8000/api/v1/predict/TESS/307210830     # looks up the TOI table at the NASA archive, needs internet
```

Frontend:

```bash
cd frontend
pnpm install
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000 pnpm dev   # http://localhost:3000
```

`nuxt.config.ts` ships with the address of an old tunnel as the default API address, so set `NUXT_PUBLIC_API_BASE_URL` as shown (Nuxt overrides `runtimeConfig.public.apiBaseUrl` from that variable). There is no `.env.example` in this repository.

Reproduce the numbers in Results: copy one training script and its CSV from `backend/` into an empty folder, run the script there with scikit-learn 1.7.2 and XGBoost 3.2.0, and read the `ROC-AUC` and `PR-AUC` lines it prints. The scripts read their CSV from the working directory and write the pickle files into it, so never run them inside `backend/models/`; to retrain the served models, run them in `backend/` and move the pickles into `backend/models/` yourself.

## Data sources and acknowledgement

- NASA Exoplanet Archive: [KOI cumulative list](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=cumulative), [K2 Planets and Candidates](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=k2pandc), [TESS Project Candidates](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=TOI). Live queries use the archive's TAP service.
- [MAST TESSCut](https://mast.stsci.edu/tesscut/) for TESS cutouts, and [lightkurve](https://lightkurve.github.io/lightkurve/) for Kepler and K2 light curves.
- The procedural planet shader code in `frontend/threejs-procedural-planets/` is Daniel Greenheck's `threejs-procedural-planets` (MIT License, copyright 2023; the licence file is in that folder).
- Event: [NASA Space Apps Challenge 2025](https://www.nasa.gov/nasa-space-apps-challenge-2025/), 4 and 5 October 2025.

The archive asks for this acknowledgement:

> This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

It also asks to cite Christiansen et al. (2025), the archive's paper in the Planetary Science Journal (see the [acknowledgement page](https://exoplanetarchive.ipac.caltech.edu/docs/acknowledge.html)).
