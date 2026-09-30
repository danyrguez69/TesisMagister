# -*- coding: utf-8 -*-
"""
Piloto exploratorio: LLM como clasificador de defectos sobre metricas tabulares de BugHunter.

Pregunta: un LLM de proposito general, recibiendo las metricas de codigo de una
instancia como texto (sin codigo fuente), ¿clasifica bug / no-bug mejor o peor que
Random Forest entrenado con las mismas metricas?

Diseno (coherente con JCC2026/sensibilidad_clasificadores.py):
  - Particion estratificada 67/33 con semilla 42 sobre Data/Python/full/<proyecto>/<nivel>.csv.
  - Caracteristicas: top-K por Ganancia de Informacion (mutual_info_classif) calculada
    SOLO sobre el entrenamiento (sin fuga hacia la prueba).
  - Muestra de prueba: N instancias estratificadas por conjunto proyecto-nivel.
  - LLM: zero-shot y few-shot (k ejemplos balanceados del entrenamiento), temperatura 0,
    lotes de B instancias por solicitud con salida JSON.
  - Referencia: RF (100 arboles, semilla 42) entrenado con todo el entrenamiento y las
    mismas K metricas, evaluado sobre las mismas instancias muestreadas.
  - Metricas: F1 ponderado, F1 de la clase bug, MCC + IC bootstrap 95 %.

La API key se lee de la variable de entorno OPENROUTER_API_KEY (nunca se escribe en disco).

Uso:
  python piloto_llm.py --dry-run                       # estima tokens, no llama a la API
  python piloto_llm.py --models MODELO1 MODELO2 --n 20 # prueba corta
  python piloto_llm.py --models MODELO1 MODELO2        # corrida completa (reanudable)
  python piloto_llm.py --report                        # solo recalcula metricas desde el .jsonl
"""
import argparse
import json
import os
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.error
import urllib.request

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(BASE, "Data", "Python", "full")
RAW = os.path.join(HERE, "piloto_llm_respuestas.jsonl")
OUT_CSV = os.path.join(HERE, "piloto_llm_resultados.csv")
OUT_TEX = os.path.join(HERE, "piloto_llm_tabla.tex")

SEED = 42
PROJECTS = ["oryx", "antlr4", "netty"]
LEVELS = ["method", "class", "file"]
URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM = (
    "You are an expert software quality analyst. You receive static source-code metrics "
    "(computed by OpenStaticAnalyzer for Java code) of code elements and must predict whether "
    "each element is defective (bug) or not (no-bug). Answer ONLY with a JSON object of the form "
    '{"predictions": [{"id": <id>, "label": "bug" | "no-bug"}, ...]} covering every id.'
)


# ----------------------------------------------------------------------------- datos
def cargar(project, level):
    data = pd.read_csv(os.path.join(DATA, project, level + ".csv"))
    data = data.drop(columns=["Project", "Hash", "LongName", "Parent"], errors="ignore").dropna()
    y = (data["Number of Bugs"] > 0).astype(int)
    X = data.drop(columns=["Number of Bugs"]).astype(float).abs()
    return train_test_split(X, y, test_size=0.33, stratify=y, random_state=SEED)


def preparar(project, level, k_feats, n_test, k_shot):
    Xtr, Xte, ytr, yte = cargar(project, level)
    mi = mutual_info_classif(Xtr, ytr, random_state=SEED)
    feats = list(pd.Series(mi, index=Xtr.columns).sort_values(ascending=False).index[:k_feats])

    # muestra de prueba estratificada (misma proporcion de bug que la particion de prueba)
    if n_test < len(Xte):
        idx, _ = train_test_split(Xte.index, train_size=n_test, stratify=yte, random_state=SEED)
    else:
        idx = Xte.index
    Xs, ys = Xte.loc[idx, feats], yte.loc[idx]

    rng = random.Random(SEED)
    pos = [i for i in Xtr.index if ytr[i] == 1]
    neg = [i for i in Xtr.index if ytr[i] == 0]
    shots = rng.sample(pos, k_shot // 2) + rng.sample(neg, k_shot - k_shot // 2)
    rng.shuffle(shots)

    rf = RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1)
    rf.fit(Xtr[feats], ytr)
    return dict(feats=feats, Xs=Xs, ys=ys, shots=Xtr.loc[shots, feats], yshots=ytr.loc[shots],
                rf_pred=pd.Series(rf.predict(Xs), index=Xs.index),
                prop_bug_train=float(ytr.mean()))


def fila_texto(row):
    return ", ".join(f"{c}={v:g}" for c, v in row.items())


def prompt(level, d, ids, few_shot):
    nivel = {"method": "method", "class": "class", "file": "file"}[level]
    partes = [f"Code elements are Java {nivel}s. In this project about "
              f"{d['prop_bug_train']*100:.0f}% of {nivel}s are defective."]
    if few_shot:
        partes.append("Labelled examples:")
        for i, (_, r) in enumerate(d["shots"].iterrows()):
            lab = "bug" if d["yshots"].iloc[i] == 1 else "no-bug"
            partes.append(f"- {fila_texto(r)} -> {lab}")
    partes.append("Classify these elements:")
    for i in ids:
        partes.append(f"id={i}: {fila_texto(d['Xs'].loc[i])}")
    return "\n".join(partes)


# ----------------------------------------------------------------------------- API
def llamar(model, user, key, max_retries=5):
    body = json.dumps({"model": model, "temperature": 0,
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": user}],
                       "response_format": {"type": "json_object"}}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "X-Title": "Tesis UCN - piloto LLM BugHunter"})
    for intento in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and intento < max_retries - 1:
                time.sleep(2 ** intento * 5)
                continue
            raise


def parsear(texto, ids):
    ini, fin = texto.find("{"), texto.rfind("}")
    preds = json.loads(texto[ini:fin + 1]).get("predictions", [])
    out = {}
    for p in preds:
        lab = str(p.get("label", "")).strip().lower()
        out[int(p["id"])] = 1 if lab == "bug" else 0 if lab in ("no-bug", "nobug", "no bug") else None
    return {i: out.get(i) for i in ids}


# ----------------------------------------------------------------------------- metricas
def puntuar(y, p):
    return dict(f1_w=metrics.f1_score(y, p, average="weighted", zero_division=0),
                f1_bug=metrics.f1_score(y, p, pos_label=1, zero_division=0),
                mcc=metrics.matthews_corrcoef(y, p))


def bootstrap(y, p, B=1000):
    rng = np.random.default_rng(SEED)
    y, p = np.asarray(y), np.asarray(p)
    vals = {k: [] for k in ("f1_w", "f1_bug", "mcc")}
    for _ in range(B):
        i = rng.integers(0, len(y), len(y))
        for k, v in puntuar(y[i], p[i]).items():
            vals[k].append(v)
    return {k: (np.percentile(v, 2.5), np.percentile(v, 97.5)) for k, v in vals.items()}


def reporte(conjuntos):
    rows, preds_global = [], {}
    registros = [json.loads(l) for l in open(RAW, encoding="utf-8")] if os.path.exists(RAW) else []
    llm = {}
    for r in registros:
        for i, lab in r["pred"].items():
            llm[(r["model"], r["mode"], r["project"], r["level"], int(i))] = lab
    for (project, level), d in conjuntos.items():
        y = d["ys"]
        pares = [("RF", "-", d["rf_pred"])]
        for (m, mode) in sorted({(k[0], k[1]) for k in llm if k[2] == project and k[3] == level}):
            p = pd.Series({i: llm.get((m, mode, project, level, i)) for i in y.index})
            pares.append((m, mode, p))
        for m, mode, p in pares:
            validos = p.notna()
            yy, pp = y[validos], p[validos].astype(int)
            rows.append(dict(model=m, mode=mode, project=project, level=level, n=int(validos.sum()),
                             invalidas=int((~validos).sum()), **puntuar(yy, pp)))
            g = preds_global.setdefault((m, mode), ([], []))
            g[0].extend(yy.tolist()); g[1].extend(pp.tolist())
    df = pd.DataFrame(rows)
    df.round(4).to_csv(OUT_CSV, index=False)

    lineas = []
    for (m, mode), (yy, pp) in preds_global.items():
        s, ci = puntuar(yy, pp), bootstrap(yy, pp)
        lineas.append((m, mode, len(yy), s, ci))
        print(f"{m:45} {mode:9} n={len(yy):4}  F1w={s['f1_w']:.3f} "
              f"F1bug={s['f1_bug']:.3f} [{ci['f1_bug'][0]:.3f},{ci['f1_bug'][1]:.3f}]  "
              f"MCC={s['mcc']:.3f} [{ci['mcc'][0]:.3f},{ci['mcc'][1]:.3f}]")
    with open(OUT_TEX, "w", encoding="utf-8") as f:
        f.write("% Generado por piloto_llm.py\n\\begin{tabular}{llcccc}\n\\toprule\n"
                "Modelo & Modo & $n$ & F1 pond. & F1 bug [IC 95\\,\\%] & MCC [IC 95\\,\\%] \\\\\n\\midrule\n")
        for m, mode, n, s, ci in lineas:
            fmt = lambda v: f"{v:.3f}".replace(".", ",")
            f.write(f"{m.split('/')[-1].replace('_', '-')} & {mode} & {n} & {fmt(s['f1_w'])} & "
                    f"{fmt(s['f1_bug'])} [{fmt(ci['f1_bug'][0])}; {fmt(ci['f1_bug'][1])}] & "
                    f"{fmt(s['mcc'])} [{fmt(ci['mcc'][0])}; {fmt(ci['mcc'][1])}] \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}\n")
    print(f"\nDetalle por conjunto: {OUT_CSV}\nTabla LaTeX: {OUT_TEX}")


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=[])
    ap.add_argument("--n", type=int, default=150, help="instancias de prueba por conjunto proyecto-nivel")
    ap.add_argument("--k-feats", type=int, default=10)
    ap.add_argument("--k-shot", type=int, default=8)
    ap.add_argument("--batch", type=int, default=10)
    ap.add_argument("--modes", nargs="*", default=["zero-shot", "few-shot"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--workers", type=int, default=1, help="solicitudes simultaneas a la API")
    ap.add_argument("--max-cost", type=float, default=None,
                    help="tope de gasto en USD para esta invocacion (segun el costo informado por OpenRouter)")
    a = ap.parse_args()

    conjuntos = {}
    for project in PROJECTS:
        for level in LEVELS:
            conjuntos[(project, level)] = preparar(project, level, min(a.k_feats, 99), a.n, a.k_shot)
            d = conjuntos[(project, level)]
            print(f"[datos] {project}/{level}: n={len(d['ys'])} (bug={int(d['ys'].sum())}) feats={d['feats']}")

    if a.report:
        return reporte(conjuntos)

    hechos = set()
    if os.path.exists(RAW):
        for l in open(RAW, encoding="utf-8"):
            r = json.loads(l)
            hechos.add((r["model"], r["mode"], r["project"], r["level"], tuple(r["ids"])))

    trabajos = []
    for (project, level), d in conjuntos.items():
        ids = list(d["Xs"].index)
        for j in range(0, len(ids), a.batch):
            for mode in a.modes:
                trabajos.append((project, level, mode, ids[j:j + a.batch]))

    if a.dry_run:
        chars = sum(len(prompt(lv, conjuntos[(pr, lv)], ids, mo == "few-shot")) for pr, lv, mo, ids in trabajos)
        print(f"{len(trabajos)} solicitudes por modelo, ~{chars/4/1e3:.0f}k tokens de entrada por modelo")
        return

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key or not a.models:
        raise SystemExit("Defina OPENROUTER_API_KEY y --models")

    pendientes = [(model, project, level, mode, ids)
                  for model in a.models for project, level, mode, ids in trabajos
                  if (model, mode, project, level, tuple(ids)) not in hechos]
    print(f"{len(pendientes)} solicitudes pendientes, {a.workers} en paralelo", flush=True)

    estado = {"gastado": 0.0, "hechas": 0, "detenido": False}
    lock = threading.Lock()

    def ejecutar(out, model, project, level, mode, ids):
        with lock:
            if a.max_cost is not None and estado["gastado"] >= a.max_cost:
                if not estado["detenido"]:
                    print(f"Tope de gasto alcanzado ({estado['gastado']:.4f} USD >= {a.max_cost} USD); "
                          f"no se envían más solicitudes.", flush=True)
                    estado["detenido"] = True
                return
        user = prompt(level, conjuntos[(project, level)], ids, mode == "few-shot")
        try:
            resp = llamar(model, user, key)
            texto = resp["choices"][0]["message"]["content"]
            pred = parsear(texto, ids)
            uso = resp.get("usage", {})
        except Exception as e:
            # no se registra: al reanudar, la solicitud se reintenta
            with lock:
                print(f"ERROR {model} {mode} {project}/{level} ids {ids[0]}..: {e}", flush=True)
            return
        with lock:
            out.write(json.dumps(dict(model=model, mode=mode, project=project, level=level,
                                      ids=ids, pred=pred, raw=texto, usage=uso)) + "\n")
            out.flush()
            estado["gastado"] += float(uso.get("cost", 0) or 0)
            estado["hechas"] += 1
            print(f"[{estado['hechas']}/{len(pendientes)}] {model} {mode} {project}/{level} ids {ids[0]}..: "
                  f"{sum(v is not None for v in pred.values())}/{len(ids)} validas | "
                  f"gasto acumulado {estado['gastado']:.4f} USD", flush=True)

    with open(RAW, "a", encoding="utf-8") as out:
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            for t in pendientes:
                pool.submit(ejecutar, out, *t)
    reporte(conjuntos)


if __name__ == "__main__":
    main()
