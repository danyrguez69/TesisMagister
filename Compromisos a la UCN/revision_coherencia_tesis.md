# Revisión de completitud y coherencia de la tesis (`main.tex`)

**Fecha:** 29-sep-2026 · **Base:** plan aprobado (`realiza-un-plan-para-silly-fog.md`), carta de reintegro y lectura de todos los capítulos incluidos en `main.tex`.
**Estado de compilación:** compila con Tectonic, 147 páginas, sin citas ni referencias indefinidas.

---

## 1. ¿Se completó lo conversado?

| Compromiso / fase del plan | Estado | Observación |
|---|---|---|
| **Carta: estado del arte + integración bibliográfica de LLM** | ✅ | Cap. 3 reescrito: 6 estudios LLM 2023–2026 verificados, tabla comparativa y sección «Relación con esta tesis». |
| **Carta: discusión y conclusiones finales** | ✅ | `discusion.tex` (nuevo) y `conclusion.tex` reescrito. El contraste de H1–H5 está **pendiente de validar con el tutor**. |
| F0 Bibliografía (claves del JCC, `weka`, verificaciones) | ⚠️ | Hecho, pero quedan **5 pares de entradas duplicadas** (ver C-1). |
| F1 Validación Weka/scikit-learn | ✅ | Sección 7.12 y script; 32/32 particiones idénticas. |
| F2 Piloto LLM | ❌ | Script listo y probado sin llamadas a la API. **Falta ejecutarlo** (API key de OpenRouter + espacio en disco) y redactar la subsección «Resultados», que hoy está vacía. |
| F3 Estado del arte | ✅ | — |
| F4 Marco teórico | ✅ | Sección de evaluación nueva, XGBoost y citas de SVM/RF. |
| F5 Resultados | ⚠️ | Hecho, salvo la sección «Análisis utilizando Python», que quedó incoherente (ver C-2). |
| F6 Discusión y conclusiones | ✅ | — |
| F7 Estructura y coherencia | ⚠️ | Capítulos reordenados. Quedan tablas en inglés, el capítulo de Hipótesis en tiempo futuro y los agradecimientos vacíos. |
| Verificación: `/ars-citation-check` | ❌ | No ejecutado. |
| Verificación: actualizar la hoja de ruta de la carta | ❌ | No actualizada. |

---

## 2. Hoja de ruta de correcciones

Prioridad: **P0** = error visible o bloqueante · **P1** = incoherencia de contenido · **P2** = forma.

### P0 — Errores visibles en el PDF

| ID | Problema | Ubicación | Corrección |
|---|---|---|---|
| **C-0** | Los textos literales `{refs}` y `{ref}` se imprimen en el PDF. | `chapter2/Sections/Preprocesamientodedatos.tex:64-65` | SU → `\cite{yu2003feature}`; COS → `\cite{liu_empirical_2015}`. |
| **C-1** | Referencias duplicadas con dos claves: PROMISE (`sayyad_shirabad_promise_2005` / `Sayyad-Shirabad+Menzies:2005`), Rathi (`RATHI2023119806` / `rathi_empirical_2023`) y Singh (`SINGH2024101253` / `singh2024improved`). Como se citan ambas claves, **cada una aparece dos veces en la bibliografía**. Además hay duplicados sin citar: `WOS:000745605300002` = `cheng2022` y `zimmermann-promise-2007` = `zimmermann2007predicting`. | `papers.bib` y las citas en `BUGHUNTER.tex` y `SoftwareMetrics/main.tex` | Unificar las citas en una sola clave y borrar las entradas sobrantes. |
| **C-2** | «Análisis utilizando Python» afirma que «los resultados experimentales presentados en este capítulo fueron obtenidos utilizando Python» y que las tablas demuestran «la efectividad de las técnicas». Ambas afirmaciones **contradicen** la Sección 7.12 (el estudio principal clasificó en Weka) y la respuesta de RQ4. Los resultados de «balanceo sobre todo el conjunto» (F = 0,95) tienen fuga de datos y no se aclara qué conjunto ni qué métrica usan: la F de NB 0,54 con P = 0,37 y R = 0,97 parece la F de la clase *bug*. | `chapter3/Sections/PythonResult/main.tex` | Reencuadrarla como **experimento exploratorio preliminar** que motivó balancear solo el entrenamiento; declarar el conjunto y la métrica; eliminar «demostrando la efectividad»; dejar explícito que los resultados que responden las RQ son los de Weka. |

### P1 — Incoherencias de contenido

| ID | Problema | Ubicación | Corrección |
|---|---|---|---|
| **C-3** | El Objetivo 4 pide «identificar la estrategia de balanceo **más efectiva**», pero ni RQ4 ni las Conclusiones lo responden. Los datos sí lo permiten. Medianas sobre los 15 proyectos: con RF y XGB, **RUS** da el mayor F1-bug (0,417 y 0,427, frente a 0,325 y 0,318 sin balanceo) y el menor F ponderado (0,513 y 0,524). Con la SVM lineal, las tres técnicas quedan en torno a 0,42–0,43 de F1-bug. | RQ4, `conclusion.tex` | Agregar: «la técnica más efectiva depende del objetivo: RUS maximiza la detección de defectos a costa del F ponderado; ROS y SMOTE ofrecen un compromiso». |
| **C-4** | El capítulo de Hipótesis, en «Validación de la hipótesis», está en futuro («adoptaremos», «utilizaremos», «se espera») y solo menciona RF y P/R/F1; no incluye el análisis de sensibilidad, el MCC ni las pruebas estadísticas. | `chapter4/main.tex` | Redactar en presente o pasado y agregar la sensibilidad (XGB, SVM), las métricas por clase y Wilcoxon/Cliff; remitir a la Tabla 8.1 (contraste). |
| **C-5** | Las contribuciones de la Introducción (5) no coinciden con las de las Conclusiones (6): faltan la validación Weka/scikit-learn, las métricas por clase / análisis de sensibilidad y el estado del arte con LLM. | `intro.tex:39-47` | Alinear con las Conclusiones. |
| **C-6** | Las hipótesis H2, H3 y H5 hablan de «precisión» en sentido amplio, pero la tesis mide F ponderado, F1-bug y MCC. El contraste de la Discusión funciona, pero un evaluador puede leer «precisión» como la métrica *precision*. | `intro.tex`, `chapter4/main.tex` | Agregar una nota: «en estas hipótesis, *precisión* se entiende como desempeño predictivo, medido con las métricas de la Sección 2.6.1». No cambiar la redacción original de las hipótesis. |
| **C-7** | La hipótesis general y las H1–H5 están duplicadas textualmente en la Introducción y en el Cap. 4. | `intro.tex`, `chapter4/main.tex` | Dejarlas solo en el Cap. 4 y referenciarlas desde la Introducción (o aceptar la duplicación si la pauta UCN la exige). |
| **C-8** | Resumen y Abstract mencionan el piloto LLM «evaluado», pero todavía no tiene resultados. | `resumen.tex`, `abstract.tex` | Completar después de ejecutar el piloto (F2) o quitar la frase. |
| **C-9** | La descripción de ROS dice «generación aleatoria de nuevas muestras»; ROS **duplica** instancias existentes y no genera nuevas (eso es SMOTE). | `Preprocesamientodedatos.tex` (ROS) | Corregir. |
| **C-10** | En «Modelos de clasificación» solo se menciona RF en Weka. | `Preprocesamientodedatos.tex` (`sub:modelos`) | Agregar que el análisis de sensibilidad usa RF, XGBoost y SVM lineal en scikit-learn (Sección 2.5). |
| **C-11** | La respuesta de RQ2 no recoge la advertencia del artefacto de conteo, que sí aparece en el texto, la Discusión y las Conclusiones. | `RQ2/main.tex` (recuadro) | Agregar media frase. |

### P2 — Forma y estilo

| ID | Problema | Ubicación |
|---|---|---|
| **C-12** | Tablas con encabezados en inglés (Project, Level, Method, Our/Paper, Without Bug…). | `Original results Weka/tables/*.tex`, `RQ4/tables/count_bug_nobug.tex`, `RQ5/tables/min_max_all.tex`, `RQ2/tables/selected_metrics.tex`, `chapter2/Tables/metricsTable.tex` |
| **C-13** | Primera persona tomada de las fuentes traducidas: «Según nuestra evidencia empírica» (es la evidencia de Pandey et al.), «Utilizamos», «podemos identificar». | `ChapterMarcoTeorico/sections/Datasets/main.tex:3`, `chapter2/Sections/BUGHUNTER.tex` |
| **C-14** | Términos en inglés en el diseño experimental: «Features Selection», «Classification Models», «Discretize Class», «Relevance Analysis», «fichero». | `ExperimentalDesign.tex:33-41` |
| **C-15** | `agradecimientos.tex` solo contiene un comando de fuente, así que la página sale vacía. | `agradecimientos.tex` (incluir el proyecto BIP 40067596-0 / GORE si el tutor lo confirma) |
| **C-16** | `\citep` en el Cap. 4 frente a `\cite` en el resto (mismo resultado numérico; es solo consistencia). | `chapter4/main.tex:19` |

---

## 3. Observación que excede la tesis (informar al tutor)

El paper JCC (`paper_jcc2026*.tex`) atribuye la clasificación del estudio principal a scikit-learn, pero los valores de la tabla RQ1 coinciden dígito a dígito con Weka. Además, dice que la selección mejora el F «en 14 o 15 de 15 proyectos», cuando con SVM a nivel de archivo son 9/15. Por la regla del usuario, el paper no se modificó.

---

## 4. Borrador de respuesta al tutor / Comité

> **Estado del plan de trabajo comprometido (carta del 20-jul-2026)**
>
> 1. *Actualización del estado del arte e integración bibliográfica de LLM* — **Completado.** Cap. 3, Secciones 3.4–3.8: [N] referencias 2022–2026 y análisis de la relación LLM–métricas tabulares. Piloto exploratorio en la Sección 7.14 ([completado / pendiente]).
> 2. *Envío de artículo a conferencia* — **Completado.** JCC 2026, artículo 270; versión extendida entregada tras la revisión.
> 3. *Redacción de conclusiones y discusión final* — **Completado.** Cap. 8 (Discusión, contraste de H1–H5 y amenazas a la validez) y Cap. 9 (Conclusiones). Se solicita validar el contraste de hipótesis (Tabla 8.1).
> 4. *Revisión final por profesores tutores* — [fecha].
> 5. *Entrega del documento final* — [fecha].

---

## 5. Estado tras aplicar las correcciones (29-sep-2026)

Se aplicaron todas las correcciones C-0 a C-16. La tesis compila sin errores (151 páginas, sin citas ni referencias indefinidas, sin marcadores `{ref}`).

**Piloto LLM completado:** 1.296 instancias × {zero-shot, few-shot} con GPT-4.1 mini, DeepSeek-V3.2 y GPT-5. Costo total: 6,35 USD, incluida la prueba corta. Ningún LLM supera a RF en MCC (0,063–0,105 frente a 0,081, con intervalos de confianza superpuestos); los LLM muestran más F1-bug y menos F ponderado, el mismo patrón de RQ4. Los resultados quedaron en la Sección 7.14, la Discusión, las Conclusiones, el Resumen y el Abstract.

**Pendiente para el tutor:** validar el contraste de hipótesis (Tabla 8.1) y los agradecimientos; informar las dos discrepancias del paper JCC (Sección 3 de este informe).
