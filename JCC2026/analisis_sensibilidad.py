# -*- coding: utf-8 -*-
"""Analisis del experimento de sensibilidad al clasificador para el paper JCC2026."""
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

BASE = r"c:\Users\danyr\OneDrive\Documents\Visual Studio 2022\Project\PaperJordanys"
IN = BASE + r"\JCC2026\resultados_sensibilidad_clasificadores.csv"

df = pd.read_csv(IN)
df = df[(df["error"].isna()) | (df["error"] == "")]
CLFS = ["RF", "XGB", "SVML"]
LEVELS = ["method", "class", "file"]


def rbc(x, y):
    """Correlacion biserial por rangos para Wilcoxon pareado (r_rb)."""
    d = np.asarray(x) - np.asarray(y)
    d = d[d != 0]
    if len(d) == 0:
        return 0.0
    ranks = pd.Series(np.abs(d)).rank().values
    wpos = ranks[d > 0].sum()
    wneg = ranks[d < 0].sum()
    return (wpos - wneg) / (wpos + wneg)


print("=" * 100)
print("1. LINEA BASE (ALL + NONE) POR CLASIFICADOR — mediana [min-max] de F ponderado por nivel")
print("   (16 conjuntos por nivel: 15 proyectos + all)")
print("=" * 100)
base = df[(df["scheme"] == "ALL") & (df["balance"] == "NONE")]
for lvl in LEVELS:
    row = []
    for clf in CLFS:
        s = base[(base["level"] == lvl) & (base["clf"] == clf)]["f1_w"]
        row.append(f"{clf}: {s.median():.3f} [{s.min():.3f}-{s.max():.3f}]")
    print(f"  {lvl:7s} " + " | ".join(row))

print()
print("=" * 100)
print("2. RQ1 — SELECCION DE CARACTERISTICAS por clasificador (sin balancear)")
print("   por dataset: F(ALL) vs mejor F con esquema de seleccion; reduccion de metricas")
print("=" * 100)
for clf in CLFS:
    for lvl in LEVELS:
        rows = []
        for proj in sorted(df["project"].unique()):
            d = df[(df["project"] == proj) & (df["level"] == lvl) & (df["clf"] == clf) & (df["balance"] == "NONE")]
            if d.empty:
                continue
            f_all = d[d["scheme"] == "ALL"]["f1_w"].iloc[0]
            n_all = d[d["scheme"] == "ALL"]["n_feats"].iloc[0]
            sel = d[d["scheme"] != "ALL"]
            if sel.empty:
                continue
            best = sel.loc[sel["f1_w"].idxmax()]
            rows.append((proj, f_all, best["f1_w"], best["f1_w"] - f_all, 1 - best["n_feats"] / n_all))
        r = pd.DataFrame(rows, columns=["proj", "f_all", "f_sel", "delta", "red"])
        r15 = r[r["proj"] != "all"]
        try:
            stat, p = wilcoxon(r15["f_sel"], r15["f_all"])
        except ValueError:
            p = float("nan")
        print(f"  {clf:5s} {lvl:7s}: dF mediana={r15['delta'].median():+.3f}  mejora en {(r15['delta']>0).sum()}/{len(r15)}  "
              f"p={p:.4f}  r_rb={rbc(r15['f_sel'], r15['f_all']):+.2f}  reduccion mediana={r15['red'].median()*100:.0f}%")

print()
print("=" * 100)
print("3. RQ4 — BALANCEO por clasificador: mejor F balanceado vs mejor F sin balancear por dataset")
print("   (pareado por conjunto; 15 proyectos individuales; tambien en F1-bug y MCC)")
print("=" * 100)
for metric in ["f1_w", "f1_bug", "mcc", "auc"]:
    print(f"  --- metrica: {metric}")
    for clf in CLFS:
        for lvl in LEVELS:
            rows = []
            for proj in sorted(df["project"].unique()):
                if proj == "all":
                    continue
                d = df[(df["project"] == proj) & (df["level"] == lvl) & (df["clf"] == clf)]
                if d.empty:
                    continue
                none_best = d[d["balance"] == "NONE"][metric].max()
                bal_best = d[d["balance"] != "NONE"][metric].max()
                rows.append((proj, none_best, bal_best))
            r = pd.DataFrame(rows, columns=["proj", "none", "bal"])
            delta = r["bal"] - r["none"]
            try:
                stat, p = wilcoxon(r["bal"], r["none"])
            except ValueError:
                p = float("nan")
            print(f"    {clf:5s} {lvl:7s}: d mediana={delta.median():+.4f}  balanceo mejora en {(delta>0).sum()}/{len(r)}  "
                  f"p={p:.4f}  r_rb={rbc(r['bal'], r['none']):+.2f}")

print()
print("=" * 100)
print("4. RQ4-bis — media de F ponderado por tecnica (todas las ejecuciones, por clasificador)")
print("=" * 100)
for clf in CLFS:
    d = df[df["clf"] == clf]
    parts = []
    for bal in ["NONE", "ROS", "RUS", "SMOTE"]:
        parts.append(f"{bal}: {d[d['balance']==bal]['f1_w'].mean():.3f}")
    print(f"  {clf:5s} " + " | ".join(parts))
print("  -- lo mismo en F1-bug:")
for clf in CLFS:
    d = df[df["clf"] == clf]
    parts = []
    for bal in ["NONE", "ROS", "RUS", "SMOTE"]:
        parts.append(f"{bal}: {d[d['balance']==bal]['f1_bug'].mean():.3f}")
    print(f"  {clf:5s} " + " | ".join(parts))
print("  -- lo mismo en MCC:")
for clf in CLFS:
    d = df[df["clf"] == clf]
    parts = []
    for bal in ["NONE", "ROS", "RUS", "SMOTE"]:
        parts.append(f"{bal}: {d[d['balance']==bal]['mcc'].mean():.3f}")
    print(f"  {clf:5s} " + " | ".join(parts))

print()
print("=" * 100)
print("5. RQ5 — ranking del conjunto 'all' por nivel y clasificador (mejor F_w por dataset, y MCC)")
print("=" * 100)
for metric in ["f1_w", "mcc", "auc"]:
    print(f"  --- metrica: {metric}")
    for clf in CLFS:
        for lvl in LEVELS:
            best = df[(df["level"] == lvl) & (df["clf"] == clf)].groupby("project")[metric].max().sort_values(ascending=False)
            rank = list(best.index).index("all") + 1
            print(f"    {clf:5s} {lvl:7s}: 'all' puesto {rank}/{len(best)} ({metric}={best['all']:.3f}; "
                  f"mejor: {best.index[0]}={best.iloc[0]:.3f})")

print()
print("=" * 100)
print("6. METRICAS POR CLASE — mediana por clasificador y nivel (mejor configuracion sin balancear por dataset)")
print("=" * 100)
for clf in CLFS:
    for lvl in LEVELS:
        rows = []
        for proj in sorted(df["project"].unique()):
            d = df[(df["project"] == proj) & (df["level"] == lvl) & (df["clf"] == clf) & (df["balance"] == "NONE")]
            if d.empty:
                continue
            best = d.loc[d["f1_w"].idxmax()]
            rows.append(best[["f1_w", "f1_bug", "mcc", "auc"]])
        r = pd.DataFrame(rows)
        print(f"  {clf:5s} {lvl:7s}: F_w={r['f1_w'].median():.3f}  F1-bug={r['f1_bug'].median():.3f}  "
              f"MCC={r['mcc'].median():.3f}  AUC={r['auc'].median():.3f}")

print()
print("=" * 100)
print("7. COMPARACION GLOBAL ENTRE CLASIFICADORES (mejor F_w por dataset, pareado)")
print("=" * 100)
piv = df.groupby(["project", "level", "clf"])["f1_w"].max().unstack()
for a, b in [("RF", "XGB"), ("RF", "SVML"), ("XGB", "SVML")]:
    delta = piv[a] - piv[b]
    try:
        stat, p = wilcoxon(piv[a], piv[b])
    except ValueError:
        p = float("nan")
    print(f"  {a} vs {b}: d mediana={delta.median():+.4f}  {a} gana en {(delta>0).sum()}/{len(delta)}  p={p:.4f}  r_rb={rbc(piv[a], piv[b]):+.2f}")

print()
print("filas analizadas:", len(df), "| errores excluidos:", (pd.read_csv(IN)["error"].fillna("") != "").sum())
