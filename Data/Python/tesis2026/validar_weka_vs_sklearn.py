# -*- coding: utf-8 -*-
"""
Validacion cruzada de los dos flujos experimentales de la tesis (solo lectura).

Flujo (a): Weka, "Supplied test set", sobre CSV train/test generados en Python
           (generar_dataset_weka.ipynb). Mejores configuraciones con/sin SMOTE a
           nivel de metodo -> chapters/chapter3/Tables/weka/train_test/weka_method_smote_b.tex
Flujo (b): scikit-learn, particion estratificada 67/33 (seed 42), mismas
           configuraciones de seleccion -> JCC2026/resultados_sensibilidad_clasificadores.csv
           (filas clf == RF).

Para cada fila de la tabla Weka se busca la misma configuracion (proyecto,
nivel=method, esquema, Rank, B, balanceo NONE/SMOTE) en el flujo (b) y se comparan:
  - F-measure ponderado y tamano del conjunto de prueba;
  - F1 de la clase bug y MCC, calculados desde la matriz de confusion de Weka.
No re-ejecuta ningun modelo.
"""
import math
import os
import re

import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
WEKA_TEX = os.path.join(BASE, "chapters", "chapter3", "Tables", "weka", "train_test", "weka_method_smote_b.tex")
SKL_CSV = os.path.join(BASE, "JCC2026", "resultados_sensibilidad_clasificadores.csv")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validacion_weka_sklearn.csv")


def num(s):
    return float(s.strip().replace(",", "."))


def leer_tabla_weka(path):
    filas, proyecto = [], None
    with open(path, encoding="utf-8") as f:
        for linea in f:
            if "&" not in linea or "textbf" in linea or "multicolumn" in linea:
                continue
            celdas = [c.strip() for c in re.sub(r"\\\\.*$", "", linea).split("&")]
            if len(celdas) != 13:
                continue
            if celdas[0]:
                proyecto = celdas[0]
            tp, tn, fn, fp = (int(celdas[i]) for i in (8, 9, 10, 11))
            filas.append(dict(
                project=proyecto, scheme=celdas[7].replace("\\_", "_"),
                rank=celdas[5], b=celdas[6],
                balance="SMOTE" if celdas[12].lower() in ("true", "sí", "si") else "NONE",
                weka_prec_w=num(celdas[1]), weka_rec_w=num(celdas[2]), weka_f1_w=num(celdas[3]),
                weka_tp=tp, weka_tn=tn, weka_fn=fn, weka_fp=fp))
    return pd.DataFrame(filas)


def metricas_confusion(tp, tn, fn, fp):
    """TP/FN corresponden a la clase bug (positiva) en la salida de Weka."""
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = (tp * tn - fp * fn) / den if den else 0.0
    return f1, mcc


def main():
    weka = leer_tabla_weka(WEKA_TEX)
    skl = pd.read_csv(SKL_CSV, dtype={"rank": str, "b": str})
    skl = skl[(skl.clf == "RF") & (skl.level == "method")]

    weka[["weka_f1_bug", "weka_mcc"]] = weka.apply(
        lambda r: pd.Series(metricas_confusion(r.weka_tp, r.weka_tn, r.weka_fn, r.weka_fp)), axis=1)
    weka["weka_n_test"] = weka[["weka_tp", "weka_tn", "weka_fn", "weka_fp"]].sum(axis=1)

    m = weka.merge(
        skl[["project", "scheme", "rank", "b", "balance", "n_test", "f1_w", "f1_bug", "mcc"]]
        .rename(columns={"n_test": "skl_n_test", "f1_w": "skl_f1_w", "f1_bug": "skl_f1_bug", "mcc": "skl_mcc"}),
        on=["project", "scheme", "rank", "b", "balance"], how="left")
    m["delta_f1_w"] = m.skl_f1_w - m.weka_f1_w
    m["delta_f1_bug"] = m.skl_f1_bug - m.weka_f1_bug
    m["delta_mcc"] = m.skl_mcc - m.weka_mcc
    m.round(4).to_csv(OUT, index=False)

    ok = m.dropna(subset=["skl_f1_w"])
    print(f"Filas Weka: {len(m)} | emparejadas con sklearn: {len(ok)}")
    print(f"n_test identico: {(ok.weka_n_test == ok.skl_n_test).sum()}/{len(ok)}")
    for col in ("delta_f1_w", "delta_f1_bug", "delta_mcc"):
        d = ok[col].abs()
        print(f"|{col}|: mediana={d.median():.4f}  max={d.max():.4f}  <=0,02: {(d <= 0.02).sum()}/{len(d)}")
    print("\nF1-bug y MCC (Weka) por balanceo, mediana:")
    print(m.groupby("balance")[["weka_f1_w", "weka_f1_bug", "weka_mcc"]].median().round(3))
    print(f"\nDetalle en {OUT}")


if __name__ == "__main__":
    main()
