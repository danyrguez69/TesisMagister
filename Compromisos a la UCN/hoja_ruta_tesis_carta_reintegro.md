# Hoja de ruta de la tesis según la carta de reintegro

**Fuente de los compromisos:** `Carta_de_reintegro firmada.pdf` (20-jul-2026, firmada por el tesista y el tutor C. Meneses)
**Documentos revisados:** `main.tex` y todos los capítulos que incluye; `JCC2026/paper_jcc2026_extendida_completa.tex`; `references/papers.bib`
**Fecha del análisis:** 29-sep-2026. **Plazo final:** entrega para la defensa en noviembre de 2026.

---

## 0. Estado del cronograma comprometido

| Hito de la carta | Plazo | Estado real en el repositorio |
|---|---|---|
| Actualizar el estado del arte e integrar bibliografía sobre LLM | Jul–Ago 2026 | ❌ **No hecho en la tesis.** El trabajo está solo en el paper (Sec. II). El Cap. "Revisión del Estado del Arte" no cita ningún trabajo posterior a 2023 y no menciona los LLM. |
| Enviar el artículo a una conferencia internacional | Ago 2026 | ✅ Enviado a JCC 2026, con versión extendida por los revisores #3, #4 y #5. ❌ La tesis no lo menciona. |
| Redactar las conclusiones y la discusión final | Sep 2026 (**este mes**) | ❌ **Atrasado.** No existe una sección de discusión. `conclusion.tex` es la versión antigua: no valida H1–H5 ni recoge los hallazgos del paper. |
| Revisión final y validación por los profesores tutores | Oct 2026 | ⏳ Depende de los tres puntos anteriores |
| Entrega del documento final | Nov 2026 | ⏳ |

La carta también dice que queda pendiente **"la consolidación de los resultados finales y la actualización del marco teórico"**. Ninguna de las dos se ha reflejado todavía en la tesis.

---

## A. Lo que la carta exige y falta en la tesis

| ID | Compromiso de la carta | Qué falta concretamente | Prioridad |
|---|---|---|---|
| **C-1** | Incorporar estudios de vanguardia sobre **LLM** | En la tesis, el único rastro de los LLM es una frase en el trabajo futuro (`conclusion.tex`). Hay que agregar una sección nueva en el Cap. 4 (Estado del Arte), por ejemplo «Representaciones profundas y modelos de lenguaje de gran escala», que cite a hou2024, fan2023 y chen2026llm, y también a guo2023 y nam2026 (modelos preentrenados aplicados a JIT). | **P1** |
| **C-2** | **Analizar la relación directa** entre los LLM y el área de estudio | La carta pide un **análisis**, no solo citas. Falta un apartado que discuta: (a) métricas tabulares frente a representaciones de código (costo, interpretabilidad, acceso al código fuente); (b) el aporte de BugHunter y de la línea base de esta tesis como referencia para evaluar los LLM; (c) el efecto de la calidad de las etiquetas y del desbalance en los modelos preentrenados (guo2023, nam2026); (d) una propuesta concreta de integración en el trabajo futuro. El párrafo 3 de la Sec. II del paper es el punto de partida, pero en la tesis debe ocupar 2–3 páginas. | **P1** |
| **C-3** | **Actualizar el estado del arte** | El Cap. 4 (`chapters/chapter1/Sections/Related jobs/main.tex`) es metodológico: describe los criterios de búsqueda y las bases de datos, y solo analiza 4 trabajos en 3 líneas. Falta: (i) la revisión 2022–2026 (GNN/AST: sikic2022, zhou2022, liu2024sedpgk; DeepLineDP: pornprasit2023; CPDP: jiang2024, cheng2022, sharma2023far; revisiones sistemáticas: giray2023, stradowski2023); (ii) una tabla comparativa de trabajos (dataset, técnica, clasificador, métrica); (iii) actualizar el filtro de búsqueda («últimos diez años») y agregar términos de búsqueda como *LLM*, *deep learning* y *just-in-time*; (iv) eliminar el texto sobrante de la plantilla (L48: «Estos criterios adicionales pueden ayudar a asegurar que **tu** revisión…»). | **P1** |
| **C-4** | **Actualizar el marco teórico** | El comentario de `ChapterMarcoTeorico/main.tex` exige un punto 2.5, «Métricas de comparación de algoritmos», y una extensión de 15±3 páginas; hoy tiene unas 2.100 palabras (≈7–8 páginas). Falta: **(a)** una sección de métricas de evaluación (precisión, recall, F1 por clase y ponderado, **MCC**, **AUC-ROC**; hoy las fórmulas están en el Cap. 7); **(b)** XGBoost (boosting de gradiente, chen2016) y fundamentar la SVM lineal (cortes1995; la subsección actual no tiene ninguna cita); **(c)** pruebas estadísticas (Wilcoxon de rangos con signo, delta de Cliff, Scott-Knott ESD); **(d)** validación y sesgo de selección (holdout frente a CV, selección anidada: ambroise2002, cawley2010); **(e)** WPDP frente a CPDP. En la subsección de Random Forest falta citar shah2020 o breiman. | **P1** |
| **C-5** | **Consolidar los resultados finales** | El experimento con **28.440 ejecuciones (RF, XGBoost y SVM lineal)**, la línea base recalculada en sklearn, el desglose por clase, la tabla de desbalance y las pruebas de Wilcoxon y Cliff existen solo en el paper. Detalle en la Sección B. | **P1** |
| **C-6** | Redactar la **discusión final** | No existe una sección de discusión. La primera línea de `RQ1/main.tex` promete «una breve discusión… y amenazas a la validez», pero ninguna de las dos está escrita. | **P1** |
| **C-7** | Redactar las **conclusiones** | `conclusion.tex` no responde RQ1–RQ5, no dice si H1–H5 se aceptan o se rechazan y no incluye el hallazgo principal (el beneficio del balanceo depende de la métrica). La lista de trabajo futuro está desactualizada frente a los 7 puntos del paper. | **P1** |
| **C-8** | Difusión de resultados | Mencionar el artículo JCC 2026 en la introducción («Publicaciones derivadas») o en un anexo, y citarlo cuando se acepte. | P2 |

---

## B. Lo que falta traspasar del paper extendido a la tesis

### B.1 Contenido nuevo que no existe en la tesis

| # | Elemento del paper (`paper_jcc2026_extendida_completa.tex`) | Destino en la tesis | Acción |
|---|---|---|---|
| B1 | **Sec. II, párrafo 3**: representaciones profundas, GNN y LLM (13 referencias nuevas) | Cap. 4, Estado del Arte | Ampliar (ver C-1 a C-3) |
| B2 | **Sec. II, párrafo 2**: marco de dos etapas (liu2015, chen2013), la advertencia de que ambos seleccionan características antes de particionar, tantithamthavorn2020, rathi2023, hossen2020 y el hueco que cubre RQ5 | Cap. 4 | Agregar |
| B3 | **Tabla I (`tab:desbalance`)**: mediana y extremos del % de instancias bug por nivel, y comparación con NASA/PROMISE | Cap. 3 (BugHunter) o RQ4 | La tesis tiene `count_bug_nobug.tex` con conteos brutos; falta la tabla resumen y el argumento del «desbalance moderado» |
| B4 | **Párrafo sobre el orden de las etapas y el sesgo de selección** (Sec. III-B) | Cap. 3, `Preprocesamientodedatos.tex` / `ExperimentalDesign.tex` | Agregar |
| B5 | **Aclaración de lo que se almacenó** (solo métricas agregadas; excepción: Weka All/método) | Cap. 7, «La medida de rendimiento» | Agregar |
| B6 | **Análisis de sensibilidad**: diseño (RF, XGBoost, SVM lineal; semilla fija; 9.480 ejecuciones × 3) y justificación de la semilla | Cap. 3 (metodología) | Agregar una subsección |
| B7 | **Tabla III (`tab:porclase`)**: desglose por clase de la línea base (F1-bug 0,356; MCC 0,052; AUC 0,539) | Cap. 7, «Resultados con dataset original» | Agregar la tabla y su párrafo |
| B8 | **Tabla V (`tab:agg`)**: mediana del mejor F por proyecto; reducciones medianas de 40 %, 88 % y 50 % | Cap. 7, RQ1 | Agregar |
| B9 | **Advertencia sobre el sesgo de comparar el máximo contra una sola referencia** (RQ1) | Cap. 7, RQ1 | Agregar |
| B10 | **Advertencia sobre el artefacto de conteo** de CLOC/LOC/LLOC (RQ2) | Cap. 7, RQ2 | Agregar |
| B11 | **RQ3: estadísticos** (media 0,547; DE 0,104; correlaciones −0,021, 0,027 y 0,011) | Cap. 7, RQ3 | Comprobar que coincidan con la tesis y agregar lo que falte |
| B12 | **RQ4: prueba de Wilcoxon pareada y delta de Cliff** (p = 0,012 / 0,48 / 0,86 / 0,052; \|δ\| < 0,15), más la lectura condicionada a la métrica | Cap. 7, RQ4 | Agregar. **Es el hallazgo principal del paper y no aparece en la tesis.** |
| B13 | **RQ5: marco WPDP/CPDP** (cheng2022, sharma2023far) | Cap. 7, RQ5 | Agregar |
| B14 | **Sección IV-G y Tabla VII (`tab:sensibilidad`)**: línea base sklearn (0,62/0,52/0,52), generalización a XGB y SVM, ΔF1-bug y ΔMCC, puesto de «All» | Cap. 7, sección nueva | Agregar. Los datos están en `JCC2026/resultados_sensibilidad_clasificadores.csv` |
| B15 | **Sec. V, Discusión** | Capítulo o sección nueva de Discusión | Agregar y ampliar |
| B16 | **Sec. V-A, Amenazas a la validez** (constructo, conclusión, interna y externa; reproducibilidad; hiperparámetros) | Sección nueva | Agregar |
| B17 | **Sec. VI, Conclusiones y trabajo futuro** (7 líneas: selección anidada, CV repetida con Scott-Knott, RQ2 normalizado, hiperparámetros, versión de revista, otros lenguajes, LLM) | `conclusion.tex` | Reescribir |
| B18 | **Disponibilidad de datos y reproducibilidad** | Anexo (hoy `anexos.tex` solo tiene un título, sin contenido) | Agregar |
| B19 | **Agradecimientos al proyecto BIP 40067596-0 / GORE Antofagasta** | `agradecimientos.tex` (hoy tiene 8 palabras) | Agregar si corresponde |

### B.2 Resumen, abstract e introducción desactualizados

- **`resumen.tex` y `abstract.tex`:** no mencionan XGBoost, SVM, las 42.356 ejecuciones, las reducciones medianas, Wilcoxon/Cliff ni el hallazgo sobre MCC y F1-bug. Además, dicen que el enfoque logra «mejoras» en la precisión, algo que los datos de RQ4 no sostienen: hay que alinearlos con el abstract del paper. Las palabras clave del resumen en español están en inglés.
- **`intro.tex`:**
  - Dice que la línea base usa «RandomForest en Weka», pero no menciona el análisis de sensibilidad.
  - La hoja de ruta del documento (último párrafo) dice que el Cap. II son trabajos relacionados y el Cap. V las conclusiones. En `main.tex`, en cambio, el orden es: Introducción, Marco teórico, Materiales y métodos, Estado del arte, Hipótesis, Objetivos, Resultados y Conclusión (**8 capítulos**).
  - Agregar el párrafo de contribuciones del paper y la mención de la publicación (C-8).
- **Título** (`portada.tex`): «Clasificación de fallas de software basadas en métricas…». Conviene evaluarlo con el tutor frente al título del paper.

### B.3 Referencias: faltan unas 22 en `papers.bib`

Hay que agregarlas con formato BibTeX (verificadas): sikic2022, zhou2022, liu2024sedpgk, pornprasit2023, jiang2024, guo2023, nam2026, giray2023, stradowski2023, hou2024, fan2023, chen2026llm, chen2016 (XGBoost), cortes1995 (SVM), cheng2022, ambroise2002, cawley2010, singh2021survey, además de las de Wilcoxon, Cliff y Scott-Knott ESD si se explican en el marco teórico. Algunas ya existen con otra clave (tantithamthavorn2020 = `8494821`, rathi2023 = `rathi_empirical_2023`, hossen2020 = `hossen_hybrid_2020`, junsomboon2017, shah2020, yu2003 = `yu2003feature`, radjenovic2013 = `RADJENOVIC20131397`): **hay que mapear esas claves, no duplicarlas.**

⚠️ Tres referencias heredan la marca `% VERIFICAR` del paper: los autores de jiang2024 y chen2026llm, y el volumen o artículo de nam2026. Hay que resolverlas antes de la entrega. Se sugiere `/ars-citation-check`.

---

## C. Defectos de la tesis que no dependen del paper pero bloquean la entrega

| # | Problema | Ubicación |
|---|---|---|
| D1 | `\cite{weka}` no tiene entrada en el `.bib`, así que la cita sale como «?» en el PDF | `intro.tex:16` |
| D2 | `sharma2023far` aparece **dos veces** en el `.bib` (L133 y L432), y hay una entrada con la clave vacía | `references/papers.bib` |
| D3 | `RQ1/main.tex` abre con `\chapter{Análisis de resultados}` dentro del capítulo «Resultados Experimentales», lo que crea un capítulo extra en el índice | `chapters/chapter3/Sections/Research Questions/sections/RQ1/main.tex:1` |
| D4 | Notas de trabajo visibles en el PDF: «analizar el final del anterior», «buscar analisis a nivel de proyecto en las metricas» y una frase truncada («pueden  la predicción») | `chapters/chapter5/main.tex` |
| D5 | **Contradicción metodológica:** RQ1 dice que el entrenamiento se hizo «dentro de la plataforma Weka», mientras que el Cap. 3 y el paper dicen scikit-learn con holdout 67/33 | `RQ1/main.tex:16` frente a `ExperimentalDesign.tex:43` |
| D6 | Las hipótesis y las RQ están duplicadas: en la introducción y en los Caps. 5 y 7. Además, las redacciones de las RQ difieren entre sí | `intro.tex`, `chapter4/main.tex`, `chapter3/main.tex` |
| D7 | Mezcla de inglés en el texto: «Step 1: Features Selection», «Without Bug», «FALSO/VERDADERO» en tablas, «RamdonForest» | Cap. 3 y Cap. 7 |
| D8 | El Cap. 4 (Estado del Arte) va **después** de Materiales y métodos; lo habitual es ponerlo antes. Revisar el orden con el tutor | `main.tex:172-179` |
| D9 | 10 entradas del `.bib` no se citan (en `unsrt` no aparecen, pero hay que revisar si se quería citarlas) | `papers.bib` |

---

## D. Orden de trabajo propuesto (Oct 2026, antes de la validación de los tutores)

1. **Semana 1:** B.3 (bibliografía) y D1/D2. Luego el Cap. 4 completo (C-1, C-2, C-3, B1, B2).
2. **Semana 2:** Marco teórico (C-4) y metodología (B3–B6).
3. **Semana 3:** Resultados: B7–B14 (la sección de sensibilidad es la más larga).
4. **Semana 4:** Discusión, amenazas y conclusiones (B15–B17, C-6, C-7, validación de H1–H5); después el resumen, el abstract y la introducción (B.2); al final D3–D9 y los anexos.

**Validación de hipótesis sugerida (a confirmar por el tutor), según la evidencia del paper:**
- H1: aceptada (reducciones medianas de 40–88 % con ΔF < 0,02).
- H2: **rechazada con el F ponderado y aceptada con F1-bug y MCC**.
- H3: parcial.
- H4: parcial (hay que considerar el artefacto de conteo).
- H5: **rechazada**, porque «All» nunca es el mejor.

---

## E. Borrador del informe de cumplimiento al Comité de Programa

> Antofagasta, __ de ______ de 2026
> **A:** Comité de Programa del Magíster, UCN
> **REF:** Informe de avance del plan de trabajo comprometido en la solicitud de reincorporación del 20 de julio de 2026
>
> | Compromiso | Estado | Evidencia en la tesis |
> |---|---|---|
> | Actualización del estado del arte y de la bibliografía sobre LLM | [completado / en curso] | Cap. [4], secciones [x.y]; [N] referencias 2022–2026 |
> | Análisis de la relación entre los LLM y el área de estudio | [ ] | Sección [x.y] |
> | Envío del artículo a una conferencia internacional | Completado | JCC 2026 (Talca), artículo N.º 270; versión extendida presentada tras la revisión |
> | Conclusiones y discusión final | [ ] | Caps. [x] y [y] |
> | Revisión por los profesores tutores | [ ] | Fecha: [ ] |
> | Entrega para la defensa | [ ] | Fecha: [ ] |
>
> [Firma del tesista] — [Visto bueno del tutor]
