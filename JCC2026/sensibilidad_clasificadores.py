# -*- coding: utf-8 -*-
"""
Experimento de sensibilidad al clasificador (JCC2026).

Replica el diseno experimental del paper (particion 67/33 estratificada,
seleccion de caracteristicas segun select_measure, balanceo solo sobre el
conjunto de entrenamiento con ROS/RUS/SMOTE) y lo ejecuta con tres
clasificadores de paradigmas distintos:
  - RF   : Random Forest (referencia, mismo del estudio)
  - XGB  : XGBoost (boosting de gradiente)
  - SVML : SVM lineal con estandarizacion
Todas las variantes de un mismo conjunto de datos comparten la MISMA
particion train/test, de modo que las comparaciones son pareadas.
Se almacenan metricas agregadas (ponderadas) y por clase (F1-bug, MCC, AUC).
"""
import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
import pyodbc
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

BASE = r"c:\Users\danyr\OneDrive\Documents\Visual Studio 2022\Project\PaperJordanys"
DATA = os.path.join(BASE, r"Data\Python\full")
OUT = os.path.join(BASE, r"JCC2026\resultados_sensibilidad_clasificadores.csv")
SELECT_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "select_measure_export.csv")

SEED = 42
SCHEMES = ["cs_su", "ig_su", "rf_su", "cs_cos", "ig_cos", "rf_cos"]
RANKS = ["0.5", "0.7", "0.9"]
BS = ["0.5", "0.7", "0.9"]
BALANCE = ["NONE", "ROS", "RUS", "SMOTE"]
CLFS = ["RF", "XGB", "SVML"]

COLS = ["project", "level", "scheme", "rank", "b", "balance", "clf", "n_feats",
        "n_train", "n_test", "prec_w", "rec_w", "f1_w", "acc",
        "prec_bug", "rec_bug", "f1_bug", "mcc", "auc", "error"]


def export_select_measure():
    if os.path.exists(SELECT_CACHE):
        return pd.read_csv(SELECT_CACHE, dtype=str)
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};Server=.;Database=magister;Trusted_Connection=yes;",
        timeout=10)
    df = pd.read_sql(
        "SELECT metric, level_measure, project, b, [rank], cs_su, ig_su, rf_su, cs_cos, ig_cos, rf_cos "
        "FROM select_measure WHERE level_measure IN ('method','class','file')", conn)
    conn.close()
    for c in SCHEMES:
        df[c] = df[c].astype(bool)
    df.to_csv(SELECT_CACHE, index=False)
    return pd.read_csv(SELECT_CACHE, dtype=str)


def _gpu_available():
    try:
        import numpy as _np
        m = XGBClassifier(n_estimators=2, tree_method="hist", device="cuda", verbosity=0)
        m.fit(_np.random.rand(32, 4), _np.array([0, 1] * 16))
        return True
    except Exception:
        return False


USE_GPU = _gpu_available()


def make_clf(name):
    if name == "RF":
        return RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=1)
    if name == "XGB":
        kw = dict(device="cuda") if USE_GPU else {}
        return XGBClassifier(n_estimators=100, tree_method="hist", random_state=SEED,
                             n_jobs=1, eval_metric="logloss", verbosity=0, **kw)
    if name == "SVML":
        return make_pipeline(StandardScaler(),
                             LinearSVC(random_state=SEED, max_iter=5000))
    raise ValueError(name)


def balance_train(kind, Xtr, ytr):
    if kind == "NONE":
        return Xtr, ytr
    if kind == "ROS":
        return RandomOverSampler(random_state=SEED).fit_resample(Xtr, ytr)
    if kind == "RUS":
        return RandomUnderSampler(random_state=SEED).fit_resample(Xtr, ytr)
    if kind == "SMOTE":
        n_min = int(pd.Series(ytr).value_counts().min())
        if n_min < 2:
            raise ValueError("SMOTE: clase minoritaria con < 2 instancias")
        return SMOTE(random_state=SEED, k_neighbors=min(5, n_min - 1)).fit_resample(Xtr, ytr)
    raise ValueError(kind)


def eval_task(feat_key, feats, bal, clf_name, Xtr, Xte, ytr, yte):
    t0 = time.time()
    try:
        Xtr_f, Xte_f = Xtr[feats], Xte[feats]
        Xb, yb = balance_train(bal, Xtr_f, ytr)
        model = make_clf(clf_name)
        model.fit(Xb, yb)
        pred = model.predict(Xte_f)
        if hasattr(model, "predict_proba"):
            score = model.predict_proba(Xte_f)[:, 1]
        else:
            score = model.decision_function(Xte_f)
        res = dict(
            n_feats=len(feats), n_train=len(Xb), n_test=len(Xte_f),
            prec_w=metrics.precision_score(yte, pred, average="weighted", zero_division=0),
            rec_w=metrics.recall_score(yte, pred, average="weighted", zero_division=0),
            f1_w=metrics.f1_score(yte, pred, average="weighted", zero_division=0),
            acc=metrics.accuracy_score(yte, pred),
            prec_bug=metrics.precision_score(yte, pred, pos_label=1, zero_division=0),
            rec_bug=metrics.recall_score(yte, pred, pos_label=1, zero_division=0),
            f1_bug=metrics.f1_score(yte, pred, pos_label=1, zero_division=0),
            mcc=metrics.matthews_corrcoef(yte, pred),
            auc=metrics.roc_auc_score(yte, score),
            error="")
    except Exception as e:
        res = dict(n_feats=len(feats), n_train=-1, n_test=-1,
                   prec_w=-1, rec_w=-1, f1_w=-1, acc=-1, prec_bug=-1, rec_bug=-1,
                   f1_bug=-1, mcc=-1, auc=-1, error=str(e)[:120])
    res["_elapsed"] = time.time() - t0
    return (feat_key, bal, clf_name), res


def run_dataset(project, level, sel, done_keys):
    if (project, level) in done_keys:
        print(f"[skip] {project}/{level} ya procesado", flush=True)
        return

    path = os.path.join(DATA, project, level + ".csv")
    data = pd.read_csv(path)
    data = data.drop(columns=["Project", "Hash", "LongName", "Parent"], errors="ignore").dropna()
    y = (data["Number of Bugs"] > 0).astype(int)
    X = data.drop(columns=["Number of Bugs"]).astype(float).abs()

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.33, stratify=y, random_state=SEED)
    ytr = ytr.reset_index(drop=True)
    Xtr = Xtr.reset_index(drop=True)
    Xte = Xte.reset_index(drop=True)
    yte = yte.reset_index(drop=True)

    sub = sel[(sel["project"] == project) & (sel["level_measure"] == level)]

    # configuraciones: ALL + 6 esquemas x 3 ranks x 3 bs
    configs = [("ALL", "-", "-", tuple(X.columns))]
    for scheme in SCHEMES:
        for rank in RANKS:
            for b in BS:
                m = sub[(sub["rank"] == rank) & (sub["b"] == b) & (sub[scheme] == "True")]["metric"]
                feats = tuple(c for c in X.columns if c in set(m))
                if feats:
                    configs.append((scheme.upper(), rank, b, feats))

    # deduplicar subconjuntos identicos de caracteristicas
    uniq = {}
    for scheme, rank, b, feats in configs:
        uniq.setdefault(feats, []).append((scheme, rank, b))

    tasks = [(feats, bal, clf)
             for feats in uniq for bal in BALANCE for clf in CLFS]
    gpu_tasks = [t for t in tasks if t[2] == "XGB" and USE_GPU]
    cpu_tasks = [t for t in tasks if t not in gpu_tasks]
    print(f"[run ] {project}/{level}: {len(data)} inst, {len(configs)} configs, "
          f"{len(uniq)} subconjuntos unicos, {len(cpu_tasks)} tareas CPU + "
          f"{len(gpu_tasks)} tareas GPU (cuda={USE_GPU})", flush=True)

    t0 = time.time()
    # XGB en GPU: secuencial para no saturar la memoria de la tarjeta
    results = [eval_task(feats, list(feats), bal, clf, Xtr, Xte, ytr, yte)
               for feats, bal, clf in gpu_tasks]
    if gpu_tasks:
        print(f"[gpu ] {project}/{level}: {len(gpu_tasks)} tareas XGB en "
              f"{time.time()-t0:.1f}s", flush=True)
    # RF y SVM lineal en CPU, en paralelo
    results += Parallel(n_jobs=14, backend="threading")(
        delayed(eval_task)(feats, list(feats), bal, clf, Xtr, Xte, ytr, yte)
        for feats, bal, clf in cpu_tasks)
    cache = {k: v for k, v in results}

    rows = []
    for feats, combos in uniq.items():
        for scheme, rank, b in combos:
            for bal in BALANCE:
                for clf in CLFS:
                    r = cache[(feats, bal, clf)]
                    rows.append([project, level, scheme, rank, b, bal, clf,
                                 r["n_feats"], r["n_train"], r["n_test"],
                                 round(r["prec_w"], 4), round(r["rec_w"], 4),
                                 round(r["f1_w"], 4), round(r["acc"], 4),
                                 round(r["prec_bug"], 4), round(r["rec_bug"], 4),
                                 round(r["f1_bug"], 4), round(r["mcc"], 4),
                                 round(r["auc"], 4), r["error"]])

    df = pd.DataFrame(rows, columns=COLS)
    header = not os.path.exists(OUT)
    df.to_csv(OUT, mode="a", header=header, index=False)
    print(f"[done] {project}/{level}: {len(rows)} filas en {time.time()-t0:.1f}s", flush=True)


def main():
    sel = export_select_measure()
    print("select_measure:", len(sel), "filas", flush=True)

    done_keys = set()
    if os.path.exists(OUT):
        prev = pd.read_csv(OUT, usecols=["project", "level"])
        done_keys = set(map(tuple, prev.drop_duplicates().values))
        print("reanudando; datasets ya procesados:", len(done_keys), flush=True)

    sizes = []
    for proj in sorted(os.listdir(DATA)):
        for lvl in ["method", "class", "file"]:
            p = os.path.join(DATA, proj, lvl + ".csv")
            if os.path.exists(p):
                sizes.append((os.path.getsize(p), proj, lvl))
    sizes.sort()  # pequenos primero

    for _, proj, lvl in sizes:
        run_dataset(proj, lvl, sel, done_keys)

    print("EXPERIMENTO COMPLETO", flush=True)


if __name__ == "__main__":
    main()
