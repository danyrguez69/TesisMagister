# Hoja de Ruta de Revisión — `paper_jcc2026.tex`
**Destino:** JCC 2026 / CWPR (Workshop Chileno de Procesamiento y Reconocimiento de Patrones)
**Fecha del análisis:** 27 de julio de 2026 · **Cierre de envío:** 3 de agosto de 2026 (**quedan 7 días**)
**Base de la verificación:** `main.tex` (tesis), `chapters/chapter3/**` (tablas de resultados) y `Data/Python/**` (1.722.637 filas de resultados de selección de características)

---

## A. Comentarios de revisores externos recibidos (27-jul-2026) — estado de atención

> Sección añadida por `revision-coach`. Cuatro comentarios externos recibidos en sesión
> (RE-1/RE-2 sin numeración de origen; RE-3 = B.1.3, RE-4 = B.1.4 del informe), todos
> clasificados como **Mayores / P1 (must fix)**. La numeración B.1.x sugiere que existen
> B.1.1/B.1.2 (presumiblemente RE-1/RE-2) y una **Sección D con sugerencias de referencias
> que no fue entregada** — solicitarla al usuario.

| # | Resumen | Tipo | Sección | Estado |
|---|---------|------|---------|--------|
| RE-1 | El *F-measure* agregado ponderado queda dominado por la clase mayoritaria; pide F1-bug, AUC-ROC y MCC, o declarar la limitación de reproducibilidad como amenaza. Coincide con R5 (§7) y con la crítica del F agregado en C2/C4. | Mayor | III-D, RQ4, Amenazas | ✅ **Atendido** en `paper_jcc2026.tex`: nueva Tabla `tab:porclase` con el desglose por clase de la única salida completa conservada (línea base Weka ``All''/método: F1-bug 0,356, MCC 0,052, AUC-ROC 0,539); excepción documentada en III-D, RQ4, Amenazas y Disponibilidad de Datos. Se refuerza con RE-2: el experimento nuevo almacena F1-bug/MCC/AUC en todas sus ejecuciones. |
| RE-2 | Solo se emplea Random Forest; amenaza reconocida pero no mitigada. Pide ≥1 clasificador de otro paradigma (XGBoost o SVM). | Mayor | III-D, Resultados, Amenazas | ✅ **Atendido**: experimento completado (28.440 ejecuciones = 9.480 × {RF, XGBoost, SVM lineal}, 48 conjuntos, 0 errores; XGB acelerado en GPU RTX 3060). Integrado al paper: párrafo "Análisis de sensibilidad" en III-D, nueva subsección `sec:sensibilidad` con Tabla `tab:sensibilidad`, y actualización de resumen, introducción, RQ4, discusión, amenazas y conclusiones. Hallazgos: RQ1 y RQ5 se generalizan a los tres clasificadores; RQ4 depende de la métrica (el balanceo sí mejora F1-bug y MCC en los tres). Datos: `resultados_sensibilidad_clasificadores.csv` + scripts en `JCC2026/`. |
| RE-3 (B.1.3) | Inconsistencia de esquemas de validación: línea base con CV de 10 particiones en Weka vs. experimentos con holdout 67/33 en scikit-learn; factor de confusión. Pide recalcular la línea base bajo holdout 67/33 en scikit-learn, o precisar el impacto esperado. Coincide con la amenaza de validez interna ya declarada y con M3 (§5). | Mayor | III-D, Línea base, Amenazas | ✅ **Atendido**: línea base recalculada con RF bajo holdout 67/33 en scikit-learn para los 48 conjuntos: promedios 0,62/0,52/0,52 (método/clase/archivo) vs. 0,63/0,50/0,50 en Weka-CV — diferencias ≤ 0,02, el confusor no altera conclusiones. Además el desglose por clase de all/método en sklearn (F1-bug 0,360, MCC 0,069, AUC 0,546) corrobora el de Weka (0,356/0,052/0,539). Reportado en `sec:sensibilidad`; amenaza de validez interna reescrita como mitigada. |
| RE-4 (B.1.4) | Estado del arte desactualizado (2013–2022); faltan desarrollos 2023–2025 en representaciones profundas (AST, GNN, LLMs). Pide 5–8 referencias 2022–2025. | Mayor | Trabajos Relacionados | ✅ **Atendido** en `paper_jcc2026.tex`: nuevo párrafo de cierre en la Sección II con 6 referencias 2022–2024 (Šikić GNN 2022; Pornprasit DeepLineDP TSE 2023; Giray JSS 2023; Stradowski IST 2023; Hou TOSEM 2024; Fan ICSE-FoSE 2023), posicionando el enfoque de métricas tabulares frente a las representaciones profundas; cita de LLMs añadida también al trabajo futuro. ⚠️ Pendiente: verificar las 6 referencias con `/ars-citation-check` y contrastar con la «Sección D» del informe del revisor (no entregada). |

**Compromisos extraídos (ledger):**

- RE-1: «reportar F1-bug, AUC-ROC y MCC» — add_analysis — evidencia: new_table ✔ (`tab:porclase`); «declarar límite de reproducibilidad» — add_clarification — evidencia: discussion_paragraph ✔ (Amenazas).
- RE-2: «incluir clasificador adicional de otro paradigma» — add_experiment — evidencia: new_table (pendiente); «evaluar si los hallazgos se generalizan» — add_analysis — evidencia: discussion_paragraph (pendiente).
- RE-3: «recalcular línea base bajo holdout 67/33 sklearn» — add_experiment — evidencia: new_table (en curso, mismo experimento de RE-2); «precisar impacto de la diferencia metodológica» — add_clarification — evidencia: discussion_paragraph (pendiente).
- RE-4: «añadir 5–8 referencias 2022–2025» — add_citation — evidencia: new_citation ✔ (6 refs); «cubrir AST/GNN/LLM en discusión y trabajo futuro» — add_clarification — evidencia: prose_edit ✔.

**Patrón cruzado:** ambos comentarios atacan la robustez de las conclusiones de RQ4; el experimento de RE-2 resuelve también la carencia de RE-1 para los nuevos resultados (métricas por clase almacenadas por diseño). Nota: el experimento de RE-2 sustituye la opción "(b) inviable en 7 días" del hallazgo C2 (§2): al almacenar MCC y AUC por ejecución, permite reevaluar RQ5 con métricas insensibles al desbalance.

---

## 0. Veredicto

El paper está **bien construido y es publicable**, pero contiene **tres afirmaciones centrales que los datos del propio autor no sostienen** y que un revisor con acceso a la tabla de desbalance detectaría de inmediato. Al mismo tiempo, el paper **subvende su resultado más fuerte**, que sí es estadísticamente significativo.

| | |
|---|---|
| Cumplimiento formal JCC | ✅ Correcto, con 6 ajustes menores |
| Exactitud de los números reportados | ✅ Verificados uno a uno — **todos correctos** |
| Validez de las *interpretaciones* | ❌ **3 problemas críticos** (§2) |
| Suficiencia de los resultados | ⚠️ Suficientes en volumen, **insuficientes en profundidad analítica** (§3) |

**Recomendación:** revisión mayor antes de enviar. El trabajo necesario son ~2 días y **mejora** el paper: los análisis nuevos que propongo se calculan con datos que ya existen en el repositorio y convierten un resultado nulo débil en una contribución positiva y defendible.

---

## 1. Cumplimiento de los requisitos del JCC 2026

Requisitos oficiales (https://jcc2026.utalca.cl/wscwpr.html):

| Requisito | Estado | Nota |
|---|---|---|
| Formato *proceedings* IEEE-CS | ✅ | `\documentclass[conference,a4paper]{IEEEtran}` correcto |
| Español o inglés | ✅ | Español, permitido explícitamente |
| 4–8 páginas incl. figuras y referencias | ✅ ~5,8 pág. estimadas | Margen de ~2 pág. para los añadidos de §3 |
| Envío por CMT3 | ⏳ | https://cmt3.research.microsoft.com/jcc2026 |
| Al menos un autor inscrito | ⏳ | Requisito para presentar |
| Revisión ciega | ❓ | **La convocatoria no la menciona.** El paper lleva nombres y afiliación. Confirmar en CMT antes de enviar |

### Ajustes de formato a aplicar

1. **`[H]` en todos los *floats*** (líneas 139, 158, 174, 196, 212). Con `IEEEtran` a dos columnas, `[H]` del paquete `float` provoca huecos grandes y desbordes. Cambiar a `[t]` o `[!t]`.
2. **`\IEEEoverridecommandlockouts`** (línea 2). Solo debe usarse si hay un error real de márgenes; IEEE lo desaconseja en *camera-ready*. Quitar y recompilar.
3. **Correo personal** `jordanys.wong@gmail.com` (línea 36). Usar el institucional de la UCN.
4. **Referencias sin fecha de acceso**: `uci1987` y `osa2004` son URLs. IEEE exige `[Online]. Available: … [Accessed: DD-Mmm-YYYY]`.
5. **Orden de citas**: `cheng2022`, `sharma2023far` y `radjenovic2013` aparecen en el texto en orden 17-18-19 pero están en la bibliografía como 18-19-17. IEEE numera por orden de primera cita. Reordenar los tres `\bibitem`.
6. **7 ecuaciones numeradas y ninguna referenciada en el texto.** Si necesita espacio para §3, las ecuaciones (1)–(5) pueden ir en línea o eliminarse: son definiciones estándar (entropía, χ², ReliefF, SU, SMOTE) que no aportan al argumento. Ahorro: ~0,25 pág.

### Verificaciones automáticas superadas
- 19 citas / 19 entradas bibliográficas — **sin citas huérfanas ni entradas sin citar**
- Todos los `\ref` resuelven a un `\label` existente
- La figura `frec_all.png` existe en la ruta del `\graphicspath`

> ⚠️ **No se pudo compilar**: no hay LaTeX instalado en este equipo (`IEEEtran.cls` no encontrado). La estimación de 5,8 páginas es analítica. **Compile antes de enviar** para confirmar el rango 4–8.

---

## 2. Problemas críticos de validez

### 🔴 C1 — La premisa del desbalance de clases es falsa para BugHunter

**Dónde:** Resumen (l. 42), Introducción (l. 54), toda la motivación de RQ4.

El paper afirma: *"el desequilibrio de clases, dado que las instancias sin errores superan ampliamente a las instancias con errores"*.

Calculé el ratio de desbalance (IR = mayoritaria/minoritaria) desde la tabla `count_bug_nobug` de la tesis:

| Nivel | IR mediana | Rango | Severo (IR>5) | Casi balanceado (IR<1,5) |
|---|---|---|---|---|
| Método | 2,56 | 1,37–7,56 | 2/15 | 1/15 |
| Clase | **1,43** | 1,01–6,98 | 1/15 | **8/15** |
| Archivo | **1,34** | 1,05–6,60 | 1/15 | **12/15** |

Casos concretos: `elasticsearch` a nivel de clase tiene 15.769 *bug* vs 15.875 *sin bug* (**49,8 % minoritaria**). `hazelcast` a nivel de clase tiene **más** instancias con error que sin error.

**Por qué ocurre:** es una consecuencia del diseño de BugHunter, que solo incluye elementos *tocados por un error* y captura su estado antes y después de la corrección — descartando los elementos nunca afectados. Ferenc et al. lo construyeron así a propósito. **BugHunter no está desbalanceado.**

**Consecuencia:** RQ4 pregunta si el balanceo mejora un conjunto que ya está balanceado. El resultado nulo no es sorprendente, es **esperado**. La explicación actual del paper (*"porque el conjunto de prueba conserva la distribución original"*) es correcta pero secundaria; la explicación real y mucho más fuerte es que **no había nada que balancear**.

**Acción:**
- Reescribir la motivación: BugHunter *no* sufre desbalance severo, a diferencia de PROMISE/NASA. Esto es una diferencia notable respecto de la literatura previa (`rathi2023`, `hossen2020`), que trabaja sobre conjuntos con IR de 5–20.
- Añadir la tabla de IR (o al menos las medianas por nivel) — cabe en 6 líneas.
- Reformular la conclusión de RQ4: *"el balanceo no aporta en BugHunter porque el conjunto ya es aproximadamente balanceado por construcción; esto acota el alcance de las recomendaciones de la literatura, que asumen desbalance severo."* Esto es una contribución **positiva**, no un resultado nulo.

Evidencia de apoyo que calculé: la correlación entre IR y la ganancia por balanceo (ΔF) es prácticamente nula (Spearman global ρ = −0,31, n = 45); ni siquiera en el cuartil más desbalanceado el balanceo ayuda (ΔF medio = **−0,0087**).

---

### 🔴 C2 — La conclusión de RQ5 está confundida por el desbalance

**Dónde:** Resumen (l. 42), RQ5 (l. 235), Discusión (l. 239), Conclusiones (l. 248).

El paper afirma: *"entrenar modelos por proyecto individual supera consistentemente a unificar las métricas de los 15 proyectos"*.

El problema: **el F-measure reportado es el agregado ponderado, que crece mecánicamente con el desbalance.** Un conjunto más desbalanceado obtiene un F ponderado más alto sin ser un mejor modelo.

Regresión sobre los 15 proyectos individuales (nivel método):

```
F_base = 0,472 + 0,0565 · IR        R² = 0,72
corr(IR, F_base): Pearson +0,85 · Spearman +0,87
corr(log N, F_base): Pearson −0,35   (el tamaño NO explica nada)
```

**El 72 % de la variación del F entre proyectos se explica solo por su ratio de desbalance.**

Ahora bien, `all` tiene IR = 1,70 — está entre los **menos** desbalanceados. Al controlar por IR:

| Nivel | IR de `all` | F esperado | F real | Residuo | Proyectos de IR comparable que lo superan |
|---|---|---|---|---|---|
| Método | 1,70 | 0,569 | 0,579 | **+0,010** | **0 de 7** |
| Clase | 1,06 | — | 0,484 | — | 2 de 7 |
| Archivo | 1,03 | — | 0,482 | — | 1 de 9 |

A nivel de método, `all` **supera a los 7 proyectos con desbalance comparable** (`elasticsearch` 0,561, `mcMMO` 0,561, `orientdb` 0,560, `neo4j` 0,545, `hazelcast` 0,542, `MapDB` 0,520, `Android-UIL` 0,486).

**La conclusión de RQ5 se invierte una vez controlado el confusor.** `all` no aparece a media tabla por heterogeneidad entre proyectos, sino porque los proyectos que lo superan (`oryx` IR=7,56, `antlr4` IR=5,82, `junit` IR=3,57) son simplemente los más desbalanceados.

**Acción (elija una):**
- **(a) Recomendada** — Reformular RQ5 honestamente: *"la aparente superioridad del entrenamiento por proyecto se explica en gran medida por el ratio de desbalance de cada proyecto (R²=0,72); tras controlarlo, el conjunto unificado rinde a la par o mejor. Esto sugiere que comparar F-measure agregado entre conjuntos con distinta distribución de clases no es válido."* **Esto es un hallazgo metodológico más valioso que la conclusión original.**
- **(b)** Recalcular RQ5 con una métrica insensible al desbalance (MCC o AUC). Requiere reejecutar; probablemente inviable en 7 días.
- **(c)** Eliminar RQ5 del paper y dejarlo para la versión extendida.

> No mantenga la redacción actual. La afirmación *"supera consistentemente"* es la más vulnerable del paper.

---

### 🟠 C3 — RQ2: la afirmación sobre CLOC/LOC/LLOC es incorrecta a nivel de archivo

**Dónde:** Resumen (l. 42), RQ2 (l. 194), Discusión (l. 239), Conclusiones (l. 248).

El paper afirma que CLOC, LOC y LLOC *"son las predictoras más consistentes"* y *"aportan un valor predictivo consistente independientemente del nivel de granularidad"*.

Calculé la tasa de selección real sobre las 1,72 M de filas de `metricData.csv`:

**Nivel archivo (las 6 métricas disponibles):**

| Métrica | Tasa de selección |
|---|---|
| McCC | 51,1 % |
| PDA | 49,6 % |
| CLOC | 47,3 % |
| **LOC** | **5,0 %** |
| **LLOC** | **5,0 %** |
| PUA | 1,0 % |

**A nivel de archivo, LOC y LLOC son seleccionadas el 5 % de las veces — son de las métricas menos elegidas, no de las más.**

**Nivel método (72 métricas):** el top está dominado por el Índice de Mantenibilidad y Halstead, no por métricas de tamaño:

| # | Métrica | Tasa |
|---|---|---|
| 1–4 | MISEI, MI, MIMS, MISM | 86,1–86,3 % |
| 5–12 | HTRP, HEFF, HNDB, HVOL, HCPL, HPL, HDIF, HPV | 84,1–85,8 % |
| **15** | **LOC** | 80,7 % |
| **16** | **LLOC** | 80,6 % |
| **25** | **CLOC** | 63,4 % |

**Nivel clase (95 métricas):** aquí sí se cumple — LOC #2 (93,2 %), LLOC #4 (92,7 %), CLOC #8 (83,6 %). ✅

La afirmación proviene de ordenar por **frecuencia absoluta agregada** (criterio de la Fig. `frec_all`), donde LOC sale #1 y LLOC #2. Pero ese criterio está sesgado: las métricas presentes en los tres niveles acumulan conteos de los tres, y el nivel de método aporta 72 métricas frente a 6 del nivel de archivo. **Es un artefacto del método de conteo, no un hallazgo.**

**Acción:**
- Sustituir la frecuencia absoluta por la **tasa de selección normalizada por nivel** (`seleccionada / oportunidades`). Es un cambio de una línea en el análisis y elimina el sesgo.
- Corregir la afirmación: *"las métricas de tamaño son predictoras fuertes a nivel de clase y método, pero a nivel de archivo solo CLOC se mantiene; allí McCC y PDA dominan."*
- **Reportar el hallazgo real que se está perdiendo:** a nivel de método, las métricas de mantenibilidad (MI y variantes) y de Halstead superan sistemáticamente a las de tamaño. El paper no las menciona ni una vez, y contradicen parcialmente a `radjenovic2013`, que se cita como apoyo.

---

### 🟠 C4 — La prueba de Wilcoxon: correcta en el cálculo, mal etiquetada en el efecto

**Dónde:** Resumen (l. 42), RQ4 (l. 229), Amenazas (l. 244), Conclusiones (l. 248).

**Origen:** este análisis **no existe en la tesis**. Búsqueda en todo `chapters/`: cero coincidencias de `wilcoxon`, `cliff`, `p =`, `significancia`, `tamaño de efecto`. La tesis solo aporta estadística descriptiva en RQ4. La prueba se calculó *ex novo* para el paper, sobre los 16 pares (mejor F sin balancear, mejor F balanceado) de las tablas `b_u_c_m`/`b_u_c_c`/`b_u_c_f`.

**Reproducción:** los valores-p son correctos.

| Nivel | p reportado | p recalculado | n declarado | n efectivo |
|---|---|---|---|---|
| Método | 0,012 | 0,0125 | 16 | **15** |
| Clase | 0,48 | 0,4802 | 16 | **12** |
| Archivo | 0,86 | 0,8647 | 16 | **15** |
| Global | 0,052 | 0,0526 | 48 | **42** |

**Cuatro correcciones necesarias:**

1. **Signo de Cliff's δ invertido.** Reportado +0,07; el cálculo da −0,074. El texto afirma "a favor de la versión sin balancear", que corresponde al signo negativo. Declarar la convención (¿balanceado − sin balancear?).

2. **Estadístico de efecto equivocado.** Cliff's δ es para muestras independientes; con datos pareados corresponde la correlación biserial-por-rangos `r_rb = (W⁺−W⁻)/(n(n+1)/2)`:

   | Nivel | Cliff δ (mal aplicado) | **r_rb (correcto)** | Magnitud |
   |---|---|---|---|
   | Método | −0,074 *insignif.* | **−0,742** | **GRANDE** |
   | Clase | −0,043 | −0,244 | pequeño |
   | Archivo | +0,043 | −0,058 | insignificante |
   | Global | −0,007 | −0,344 | mediano |

   A nivel de método, **13 de 15 proyectos empeoran al balancear y solo 2 mejoran**. El efecto es grande y consistente. Lo despreciable es la *magnitud en F* (mediana ΔF = −0,003), no el tamaño de efecto. El paper confunde ambos conceptos.

   **Redacción sugerida:** *"el balanceo degrada el rendimiento de forma consistente (13/15 proyectos) y estadísticamente significativa (p = 0,012; r_rb = −0,74), pero con una magnitud despreciable (mediana ΔF = −0,003), por lo que carece de relevancia práctica."*

3. **n declarado ≠ n usado.** Wilcoxon descarta los empates exactos. A nivel de clase se descartan 4 de 16 pares (25 %) sin mencionarlo. Reportar n efectivo por nivel.

4. **La prueba no es reproducible desde el paper.** El texto remite a las Tablas II y III, pero la Tabla II solo muestra `oryx` y la Tabla III solo mediana/mín/máx. Los 16 pares por nivel **solo existen en la tesis**. Añadir los valores por proyecto como tabla en anexo o material suplementario.

> **Nota técnica adicional:** hay empates en |d| en los tres niveles, por lo que la prueba exacta no es aplicable y se usó la aproximación normal. Con n = 12–15 esto es marginal; declarar la variante empleada y, preferiblemente, aplicar la corrección por empates en la varianza.

---

## 3. El paper subvende su resultado más fuerte

**Dónde:** RQ1 (l. 156), Resumen, Discusión, Conclusiones.

El paper describe la selección de características como *"pérdida marginal de F-measure (inferior a 0,02)"* — es decir, la vende como *no dañina*. Los datos dicen algo mucho mejor.

Wilcoxon pareado, línea base vs. mejor esquema de FS, sobre los 15 proyectos individuales:

| Nivel | ΔF mediana | Mejora en | p | Cliff's δ | Reducción mediana de características |
|---|---|---|---|---|---|
| Método | +0,009 | 9/15 | 0,61 | +0,08 (insignificante) | 65,3 % |
| **Clase** | **+0,075** | **14/15** | **0,0009** | **+0,44 (mediano)** | **88,0 %** |
| **Archivo** | **+0,043** | **14/15** | **0,0009** | **+0,46 (mediano)** | **50,0 %** |

**A nivel de clase y archivo, la selección de características MEJORA el rendimiento de forma estadísticamente significativa y con tamaño de efecto mediano, usando 88 % y 50 % menos características.** Eso es un resultado positivo, robusto y perfectamente publicable — y el paper lo describe como "no perder nada".

⚠️ **Salvedad obligatoria:** esta comparación cruza herramientas y esquemas de validación (línea base = Weka + CV 10 *folds*; FS = scikit-learn + *holdout* 67/33). El paper ya reconoce esto en Amenazas a la Validez (l. 244). **Debe declararse junto al resultado, no solo en la sección de amenazas.** Redacción sugerida: *"la comparación cruza herramienta y esquema de validación, por lo que la magnitud debe tomarse como indicativa; la consistencia del signo en 14 de 15 proyectos es el hallazgo robusto."*

**Acción:** reescribir el resumen y RQ1 para liderar con este resultado. Es la contribución más defendible del paper.

---

## 4. Análisis nuevos disponibles con los datos actuales

Todos calculables **sin reejecutar experimentos**. Ordenados por relación valor/esfuerzo.

| # | Análisis | Esfuerzo | Aporte |
|---|---|---|---|
| 1 | Tabla de ratio de desbalance por proyecto/nivel | Trivial (ya está en la tesis) | Sostiene C1, C2 |
| 2 | Wilcoxon línea base vs FS (§3) | 1 h | Convierte el resultado nulo en positivo |
| 3 | Regresión F ~ IR y control del confusor en RQ5 | 2 h | Resuelve C2 |
| 4 | Tasa de selección normalizada por nivel | 1 h | Resuelve C3 |
| 5 | **SU vs COS: comportamiento del umbral** | 1 h | Hallazgo metodológico nuevo |
| 6 | **Irrelevancia del algoritmo de relevancia** | 1 h | Respuesta mucho mejor a RQ3 |
| 7 | Clasificador trivial como referencia | 1 h | Refuerza amenazas a la validez |

### 4.5 — SU y COS no son comparables como medidas de redundancia

Tasas de retención calculadas sobre los datos completos:

| Nivel | SU retiene | COS retiene |
|---|---|---|
| Método | 22,4 % | 49,9 % |
| Clase | 26,4 % | 48,7 % |
| Archivo | 3,3 % | 49,7 % |

**COS retiene casi exactamente el 50 % en los tres niveles y para los tres valores de β.** Ese comportamiento sugiere que, con la implementación usada, el umbral de Semejanza de Coseno actúa como un **corte fijo a la mediana**, insensible a β. SU, en cambio, sí responde al nivel (3,3 % a nivel de archivo frente a 26,4 % a nivel de clase).

Esto es relevante porque el paper afirma en RQ1 que *"COS predominó a nivel de método y archivo"*. Si COS simplemente conserva la mitad de las características por construcción, "predominar" puede significar solo que entrega subconjuntos mayores, no mejores. **Merece una comprobación antes de enviar.**

### 4.6 — El algoritmo de relevancia casi no influye (mejor respuesta a RQ3)

| Esquema | Tasa de retención (método) |
|---|---|
| cs_su | 22,7 % |
| ig_su | 22,7 % |
| rf_su | 21,9 % |
| cs_cos | 49,9 % |
| ig_cos | 49,9 % |
| rf_cos | 49,9 % |

Ganancia de Información, Chi-Cuadrado y ReliefF producen tasas de selección **prácticamente idénticas**; toda la variación proviene de la medida de redundancia (SU vs COS). Actualmente RQ3 solo reporta tres correlaciones cercanas a cero (−0,021 / +0,027 / +0,011), lo cual es poco informativo. Este resultado —*la elección del algoritmo de relevancia es indiferente; lo que importa es el control de redundancia*— es una respuesta concreta y accionable para el profesional.

### 4.7 — Referencia del clasificador trivial

Comparando el F reportado contra la proporción de la clase mayoritaria (nivel método):

| Proyecto | F reportado | Clase mayoritaria |
|---|---|---|
| oryx | 0,852 | **0,883** |
| antlr4 | 0,781 | **0,853** |
| junit | 0,695 | **0,781** |
| netty | 0,676 | **0,733** |
| ceylon-ide-eclipse | 0,644 | **0,724** |
| titan | 0,584 | **0,719** |

En los proyectos con "mejor" rendimiento, el F-measure agregado queda por debajo de lo que obtendría un clasificador que siempre predice la clase mayoritaria. Aunque F y *accuracy* no son directamente comparables, la yuxtaposición es un argumento contundente para la sección de Amenazas y **refuerza la crítica que el propio paper ya se hace** sobre el F agregado.

---

## 5. Observaciones menores a corregir

| # | Ubicación | Problema |
|---|---|---|
| M1 | l. 156 | *"diferencias de entre −0,014 y +0,036"*. El valor balanceado a nivel método es 0,837 − 0,852 = **−0,015**. Corregir el extremo inferior. |
| M2 | l. 122 | *"La línea base … se estableció con 2.592 ejecuciones"*. **2.592 = 16 conjuntos × 3 niveles × 3 *Rank* × 3 β × 6 esquemas**, que es el número de configuraciones de *selección de características*, no de ejecuciones de línea base (sin FS no hay *Rank* ni β que variar). Verificar y corregir. |
| M3 | l. 120 vs tesis | El paper dice que RF se ejecuta en **scikit-learn** para los experimentos de FS; la tesis (`RQ1/main.tex`) dice *"dentro de la plataforma Weka"* y menciona **solo SMOTE**, no ROS/RUS. Reconciliar: es una contradicción entre documentos que un revisor podría detectar. |
| M4 | l. 253 | *"disponibles a solicitud de los autores"*. Está cada vez peor visto y **aquí los datos ya existen** (`Data/Python/`). Suba a Zenodo y cite el DOI — mejora la evaluación de reproducibilidad a coste casi nulo. |
| M5 | l. 137 | *"el proyecto oryx obtuvo el mejor desempeño"*. Contextualícelo: `oryx` es el proyecto **más desbalanceado** (IR = 7,56). Relacionado con C2. |
| M6 | l. 231 | El párrafo de cautela sobre el sesgo de selección optimista es correcto y honesto. **Consérvelo.** |

### ✅ Verificado como correcto (no tocar)

Comprobé cada cifra contra las tablas de la tesis:

- **Tabla III** (`tab:agg`): los 6 valores de mediana/mín/máx son **exactos** en los tres niveles y en ambas condiciones.
- **Tabla II** (`tab:oryx`): conteos de métricas, F-measures y los seis porcentajes de reducción son correctos.
- **Reducciones medianas** 40 % / 88 % / 50 %: recalculadas sobre los 15 proyectos, **correctas**.
- **Tabla I** (línea base) y **Tabla IV** (balanceo): coinciden con la tesis.
- **Estadísticos de RQ3** (media 0,547; DE 0,104; mín 0,274; máx 0,844; las 3 correlaciones): correctos.
- El paper **corrige** un error de la tesis: `RQ1/main.tex` dice que a nivel de archivo se reduce "de 92 a 46 características"; el nivel de archivo solo tiene 6 métricas. El paper reporta correctamente 6 → 3.

---

## 6. Plan de ejecución sugerido (7 días)

| Día | Tarea |
|---|---|
| 1 | Instalar LaTeX + IEEEtran, compilar, confirmar páginas. Aplicar ajustes de formato §1 (1–6). |
| 2 | Recalcular tasas de selección normalizadas (C3) y tabla de IR (C1). |
| 3 | Reescribir Resumen + RQ1 liderando con el resultado significativo (§3). |
| 4 | Reescribir RQ4 con la premisa corregida (C1) y RQ5 con el control del confusor (C2). |
| 5 | Añadir §4.5 y §4.6 a RQ3. Corregir M1–M3, M5. Subir datos a Zenodo (M4). |
| 6 | Recorte a 8 páginas (candidatas: ecuaciones 1–5, §II condensada). Revisión de estilo. |
| 7 | Compilación final, verificación de figuras/tablas, envío por CMT3. |

---

## 7. Esqueleto de carta de respuesta

> Reutilizable si el paper recibe revisión mayor. Cada entrada corresponde a un hallazgo de este informe; el revisor real muy probablemente planteará C1, C2 o C3.

**R1 — Sobre la caracterización del desbalance de clases en BugHunter (→ C1)**
> Agradecemos la observación. Hemos verificado que BugHunter presenta un ratio de desbalance mediano de 1,43 (clase) y 1,34 (archivo), sustancialmente menor que el de conjuntos como PROMISE o NASA. Esto es consecuencia de su diseño, que solo incluye elementos afectados por errores. Hemos reescrito la Sección [X] para reflejarlo y reformulado la conclusión de RQ4: el balanceo no aporta *porque el conjunto ya es aproximadamente balanceado*, lo que acota el alcance de las recomendaciones previas de la literatura. Se añadió la Tabla [Y] con los ratios por proyecto y nivel.

**R2 — Sobre la comparación entre proyecto unificado e individuales (→ C2)**
> Tiene razón. Al analizar el F-measure agregado en función del ratio de desbalance encontramos R² = 0,72, lo que indica que la mayor parte de la variación entre proyectos se explica por su distribución de clases y no por su predictibilidad. Controlando ese factor, el conjunto unificado no rinde por debajo de proyectos de desbalance comparable. Hemos reformulado RQ5 [o: lo hemos retirado del alcance de este trabajo] y añadido este punto como amenaza a la validez de constructo.

**R3 — Sobre las métricas de tamaño de código (→ C3)**
> Corregido. El ordenamiento original usaba frecuencia absoluta agregada, sesgada a favor de las métricas presentes en varios niveles. Con tasas normalizadas por nivel, LOC y LLOC se seleccionan solo el 5 % de las veces a nivel de archivo, donde dominan McCC y PDA. Hemos matizado la afirmación y añadido el hallazgo, previamente no reportado, de que las métricas de mantenibilidad (MI) y de Halstead dominan la selección a nivel de método.

**R4 — Sobre la significancia estadística de la selección de características (→ §3)**
> Hemos añadido pruebas de Wilcoxon pareadas sobre los 15 proyectos: a nivel de clase y archivo la selección de características mejora el F-measure de forma significativa (p = 0,0009; Cliff's δ = 0,44 y 0,46) reduciendo un 88 % y un 50 % las características. Señalamos explícitamente que esta comparación cruza herramienta y esquema de validación, por lo que la magnitud es indicativa y el hallazgo robusto es la consistencia del signo (14/15 proyectos).

**R5 — Sobre la métrica de evaluación (→ RE-1) [ACTUALIZADO — atendido en el manuscrito]**
> Coincidimos en que el F-measure agregado es una limitación en este contexto. Los resultados almacenados de las 13.916 ejecuciones no permiten desagregarlo por clase sin reejecutarlas, y así lo declaramos ahora explícitamente en la Sección de Amenazas. No obstante: (i) añadimos la Tabla [tab:porclase] con el desglose por clase de la única salida completa conservada (línea base Weka del conjunto "All" a nivel de método: F1-bug = 0,356 frente a un F ponderado de 0,565; MCC = 0,052; AUC-ROC = 0,539), que cuantifica empíricamente la magnitud del sesgo señalado; (ii) acotamos el sesgo con la distribución de clases de BugHunter (desbalance moderado, Tabla [tab:desbalance]); y (iii) el nuevo experimento de sensibilidad al clasificador (véase R7) almacena F1-bug, MCC y AUC-ROC en la totalidad de sus ejecuciones, por lo que sus conclusiones no dependen de la métrica agregada.

**R7 — Sobre el uso exclusivo de Random Forest (→ RE-2)**
> Agradecemos la sugerencia. Ejecutamos un análisis de sensibilidad con dos clasificadores adicionales de paradigmas distintos: XGBoost (boosting de gradiente) y SVM lineal con estandarización, sobre los 48 conjuntos proyecto-nivel, replicando el diseño del estudio (partición estratificada 67/33, los mismos subconjuntos de características de la selección en dos etapas, y balanceo ROS/RUS/SMOTE aplicado solo al entrenamiento), con particiones idénticas entre clasificadores para permitir comparaciones pareadas: 28.440 ejecuciones en total (9.480 por clasificador). Los resultados se reportan en la nueva Sección IV-G (Tabla de sensibilidad). Los hallazgos principales se generalizan: la selección de características mejora el F-measure ponderado en los tres clasificadores (mediana +0,001 a +0,041; mejora en 14–15 de 15 proyectos; p<0,01), y el conjunto unificado «All» no es superior en ningún clasificador ni métrica (puestos 7–15/16 en F ponderado, 6–13/16 en MCC). El efecto del balanceo resultó dependiente del clasificador y de la métrica —tal como el revisor anticipaba—: no mejora el F ponderado en RF, mejora marginalmente en XGBoost y significativamente en SVM lineal, y mejora la detección de la clase bug (F1-bug, MCC) de forma consistente en los tres. Los resultados por ejecución, incluidas las métricas por clase, se distribuyen en `resultados_sensibilidad_clasificadores.csv` junto con los scripts.

**R8 — Sobre la inconsistencia de esquemas de validación (→ RE-3 / B.1.3)**
> Coincidimos en que la diferencia de herramienta y esquema de validación entre la línea base (Weka, CV de 10 particiones) y los experimentos (scikit-learn, holdout 67/33) constituía un factor de confusión. Siguiendo la sugerencia, recalculamos la línea base —todas las características, sin balanceo— bajo el mismo esquema holdout estratificado 67/33 en scikit-learn para los 48 conjuntos proyecto-nivel, como parte del análisis de sensibilidad (Sección IV-G). Los promedios de F-measure resultan 0,62 (método), 0,52 (clase) y 0,52 (archivo), frente a 0,63, 0,50 y 0,50 de la versión Weka: diferencias de a lo sumo 0,02 que indican que el factor de confusión no altera las conclusiones. Adicionalmente, el desglose por clase de la línea base del conjunto «All» a nivel de método coincide estrechamente entre ambas herramientas (F1-bug 0,360 vs. 0,356; MCC 0,069 vs. 0,052; AUC-ROC 0,546 vs. 0,539), lo que corrobora ambas mediciones de forma independiente. La amenaza de validez interna se reescribió en consecuencia: las comparaciones sustantivas del nuevo experimento comparten herramienta, particiones y esquema de validación.

**R9 — Sobre la actualización del estado del arte (→ RE-4 / B.1.4)**
> Actualizamos la Sección de Trabajos Relacionados con un párrafo dedicado a las líneas recientes de predicción de fallas basadas en representaciones profundas del código: GNN sobre representaciones derivadas del AST [Šikić et al., IEEE Access 2022], predicción a nivel de línea con aprendizaje profundo [Pornprasit y Tantithamthavorn, IEEE TSE 2023], las revisiones sistemáticas de [Giray et al., JSS 2023] y [Stradowski y Madeyski, IST 2023], y la agenda emergente de LLMs para ingeniería de software [Hou et al., ACM TOSEM 2024; Fan et al., ICSE-FoSE 2023]. El párrafo posiciona nuestro enfoque de métricas tabulares como línea base interpretable y de bajo costo frente a dichas representaciones, y el trabajo futuro incorpora ahora las referencias de LLMs. [Si la Sección D del informe sugiere referencias específicas distintas, indicarlas para incorporarlas.]

**R6 — Sobre reproducibilidad**
> Los conjuntos procesados, los *scripts* y los resultados agregados están ahora disponibles públicamente en [DOI de Zenodo].
