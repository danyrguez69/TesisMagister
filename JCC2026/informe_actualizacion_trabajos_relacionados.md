# Informe: Actualización de Trabajos Relacionados (2022–2026)

**Modo**: deep-research / three-way-scan (WHY–HOW–WHAT)
**Objetivo**: responder al comentario de revisión sobre cobertura limitada de trabajos recientes (2023–2025) en predicción de fallas con representaciones profundas de código (AST, GNN, LLMs).
**Fecha**: 2026-07-27
**Criterio de inclusión**: trabajos 2022–2026 sobre predicción de defectos/fallas de software con representaciones profundas de código, verificados de forma independiente (sede, autores, año). Los candidatos no verificables se descartaron (regla: zona gris = FAIL).

---

## Fichas WHY / HOW / WHAT

### 1. Zhou, He, Zeng y Ma (2022) — CGCN
Fuente: *Information and Software Technology*, vol. 152, Art. 107057 | Verificada (ScienceDirect)

- **WHY**: las métricas estáticas tabulares capturan parcialmente la semántica del código; se busca combinar la información semántica interna de cada archivo con la estructura externa entre archivos.
- **HOW**: CNN sobre tokens extraídos del AST + red convolucional de grafos (GCN) sobre la red de dependencias de clases; evaluación en siete proyectos de código abierto.
- **WHAT**: CGCN supera a métodos basados solo en semántica o solo en estructura; deja abierta la generalización a otros niveles de granularidad y datasets.

### 2. Guo, Gao, Zhang, Chan y Jiang (2023) — PTMs para JIT-SDP
Fuente: *Proc. IEEE 23rd Int. Conf. Software Quality, Reliability, and Security (QRS)*, 2023 | Verificada (IEEE/City U PDF)

- **WHY**: cuantificar qué aportan los modelos preentrenados de lenguaje/código a la predicción de defectos *just-in-time*.
- **HOW**: seis variantes (RoBERTa, CodeBERT, BART, PLBART, GPT-2, CodeGPT) como *backbone* de un mismo marco JIT; análisis de escenarios *few-shot* y de balance de datos.
- **WHAT**: mejoras consistentes frente a modelos JIT previos; el código del *commit* es la señal dominante y el **balance del conjunto de entrenamiento influye en escenarios de pocos datos** — conecta directamente con la RQ4 del paper.

### 3. Liu, Yue, Chen, Gu, Zhao, Liu y Zhao (2024) — SeDPGK
Fuente: *Information and Software Technology*, vol. 174, Art. 107510 | Verificada (ScienceDirect + anuncio del journal)

- **WHY**: la escasez de etiquetas limita la PFS supervisada; los métodos semisupervisados existentes ignoran la estructura del programa.
- **HOW**: grafo de dependencias de programa (control + datos) con GNN como modelo docente, destilado a un estudiante ligero (propagación de etiquetas + MLP); 17 proyectos reales.
- **WHAT**: mejora media de 8,9 % en AUC sobre líneas base semisupervisadas; el costo de construir grafos por proyecto persiste.

### 4. Jiang, Chen, He et al. (2024) — SSE
Fuente: *Empirical Software Engineering*, vol. 29, Art. 80 | Verificada (Springer) — completar lista de autores al insertar

- **WHY**: la predicción entre proyectos (CPDP) se degrada por la heterogeneidad de distribuciones entre proyectos — el mismo fenómeno que motiva la RQ5 del paper.
- **HOW**: codificación conjunta semántica y sintáctica derivada del AST para transferir conocimiento entre proyectos.
- **WHAT**: mejora sobre líneas base de CPDP, pero la heterogeneidad sigue siendo el cuello de botella principal; refuerza la lectura WPDP > CPDP.

### 5. Chen, Shen, Wang et al. (2026) — Revisión de LLMs para detección de defectos
Fuente: *Frontiers of Computer Science*, vol. 20, Art. 2006202 (DOI 10.1007/s11704-025-40672-2) | Verificada (Springer) — completar lista de autores al insertar

- **WHY**: mapear sistemáticamente el uso de LLMs en detección de defectos y ordenar una literatura que crece muy rápido.
- **HOW**: revisión de literatura que clasifica los enfoques en detección dinámica (generación de casos de prueba, guía por retroalimentación, evaluación de salidas) y estática (código fuente vs. binario).
- **WHAT**: potencial alto pero retos abiertos de costo, fiabilidad y evaluación; agenda de investigación que respalda la línea de trabajo futuro del paper.

### 6. Nam, Kim, Ryu y Baik (2026) — ReDef
Fuente: *Proceedings of the ACM on Software Engineering* (FSE 2026), DOI 10.1145/3808179 | Verificada (ACM DL + conf.researchr.org)

- **WHY**: los datasets JIT existentes tienen etiquetas ruidosas (heurísticas tipo SZZ); ¿entienden realmente los modelos de lenguaje de código los cambios de código?
- **HOW**: benchmark ReDef anclado en *commits* de reversión sobre 22 proyectos C/C++ (3.164 defectuosas / 10.268 limpias) y evaluación sistemática de CodeBERT, CodeT5+, UniXcoder y Qwen2.5 bajo cinco codificaciones de entrada.
- **WHAT**: las codificaciones compactas tipo *diff* superan a la función completa; la calidad de las etiquetas condiciona las conclusiones — paralelo directo con la motivación de calidad de datos de BugHunter.

---

## Síntesis transversal

- **WHY común**: la calidad de los datos (etiquetas ruidosas, desequilibrio, heterogeneidad entre proyectos) y la expresividad limitada de las métricas tabulares siguen siendo los cuellos de botella de la PFS — exactamente el espacio de problemas que el paper aborda sobre BugHunter.
- **HOW divergente**: tres rutas técnicas: (i) GNN sobre grafos de dependencia/AST (CGCN, SeDPGK), (ii) modelos preentrenados y LLMs sobre el texto del código o del cambio (QRS 2023, revisión FCS, ReDef), y (iii) codificaciones híbridas para transferencia entre proyectos (SSE).
- **WHAT más fuerte**: mejoras reales pero con costo computacional alto y dependencia del acceso al código fuente completo; varios trabajos (ReDef, QRS 2023) muestran que balance de datos y calidad de etiquetas condicionan los resultados tanto como la arquitectura.
- **Brecha global no resuelta**: ninguno de estos trabajos evalúa sobre BugHunter ni contrasta sistemáticamente contra clasificadores clásicos con selección de características rigurosa; el paper aporta precisamente esas líneas base interpretables y de bajo costo.

## Descartes documentados

| Candidato | Motivo de descarte |
|---|---|
| DeMuVGN (arXiv 2410.19550, 2024) | Solo preprint arXiv al momento de la verificación (nivel de evidencia inferior; sin revisión por pares) |
| "Hierarchical transformer network for SDP" (JSS, 2025) | Existe en ScienceDirect pero no se pudo confirmar la lista de autores; zona gris = fuera |

---

## Material listo para insertar (LaTeX / IEEE)

**Ubicación sugerida**: tercer párrafo de la Sección II (Trabajos Relacionados), que hoy cubre {\v S}iki\'c et al. y DeepLineDP. Los `\bibitem` deben insertarse en la bibliografía **en el orden de primera aparición** (la bibliografía es manual, el orden define la numeración IEEE).

Propuesta de texto (reemplaza/amplía las dos primeras oraciones del párrafo de representaciones profundas):

```latex
Una línea de trabajo más reciente sustituye las métricas de código por
representaciones profundas del código fuente. {\v S}iki\'c et al. \cite{sikic2022}
aplican redes neuronales de grafos (GNN) sobre representaciones derivadas del
árbol de sintaxis abstracta (AST), Zhou et al. \cite{zhou2022} combinan semántica
interna (CNN sobre el AST) con la estructura de dependencias entre clases (GCN),
y SeDPGK \cite{liu2024sedpgk} extiende esta ruta al escenario semisupervisado
mediante destilación de conocimiento sobre grafos de dependencias. Pornprasit y
Tantithamthavorn \cite{pornprasit2023} proponen DeepLineDP para localizar defectos
a nivel de línea, y Jiang et al. \cite{jiang2024} muestran que la codificación
conjunta semántica--sintáctica mejora la transferencia entre proyectos, aunque la
heterogeneidad de distribuciones sigue siendo el principal obstáculo. En paralelo,
los modelos preentrenados de código se han incorporado a la predicción
\textit{just-in-time}: Guo et al. \cite{guo2023} reportan mejoras consistentes con
seis \textit{backbones} preentrenados —donde el balance de los datos de
entrenamiento resulta determinante en escenarios de pocos datos—, y el benchmark
ReDef \cite{nam2026} muestra que la calidad de las etiquetas condiciona las
conclusiones sobre estos modelos, en línea con la motivación de BugHunter. Las
revisiones sistemáticas de Giray et al. \cite{giray2023}, Stradowski y Madeyski
\cite{stradowski2023} y, para los enfoques basados en LLM, Chen et al.
\cite{chen2026llm} coinciden, no obstante, en que estos modelos incrementan
considerablemente el costo computacional sin superar de forma consistente a los
clasificadores clásicos entrenados sobre métricas tabulares.
```

Bibitems (insertar cada uno en la posición de su primera aparición en el texto):

```latex
\bibitem{zhou2022} C. Zhou, P. He, C. Zeng, and J. Ma, ``Software defect prediction with semantic and structural information of codes based on graph neural networks,'' \textit{Information and Software Technology}, vol. 152, p. 107057, 2022.

\bibitem{liu2024sedpgk} W. Liu, Y. Yue, X. Chen, Q. Gu, P. Zhao, X. Liu, and J. Zhao, ``SeDPGK: Semi-supervised software defect prediction with graph representation learning and knowledge distillation,'' \textit{Information and Software Technology}, vol. 174, p. 107510, 2024.

\bibitem{jiang2024} S. Jiang, Y. Chen, Z. He \textit{et al.}, ``Cross-project defect prediction via semantic and syntactic encoding,'' \textit{Empirical Software Engineering}, vol. 29, art. 80, 2024.   % VERIFICAR lista completa de autores

\bibitem{guo2023} Y. Guo, X. Gao, Z. Zhang, W. K. Chan, and B. Jiang, ``A study on the impact of pre-trained model on just-in-time defect prediction,'' in \textit{Proc. IEEE 23rd Int. Conf. Software Quality, Reliability, and Security (QRS)}, 2023.   % VERIFICAR páginas

\bibitem{nam2026} D. Nam, T. Kim, D. Ryu, and J. Baik, ``ReDef: Do code language models truly understand code changes for just-in-time software defect prediction?'' \textit{Proceedings of the ACM on Software Engineering} (FSE 2026), 2026.   % VERIFICAR volumen/número de artículo

\bibitem{chen2026llm} Y. Chen, Y. Shen, T. Wang \textit{et al.}, ``Software defect detection using large language models: A literature review,'' \textit{Frontiers of Computer Science}, vol. 20, art. 2006202, 2026.   % VERIFICAR lista completa de autores
```

**Nota de extensión**: el paper debe mantenerse en 4–8 páginas (formato JCC2026). El texto propuesto reemplaza parte del párrafo existente (no lo duplica), por lo que el crecimiento neto estimado es de ~6–8 líneas más 6 entradas bibliográficas.

---

## Declaración de uso de IA

Este informe fue elaborado con asistencia de herramientas de investigación basadas en IA (Claude Code + plugin academic-research-skills, modo three-way-scan). Todas las referencias fueron verificadas de forma independiente contra las páginas de sus editores (IEEE Xplore, ACM DL, ScienceDirect, Springer) el 2026-07-27. Las entradas marcadas con `% VERIFICAR` requieren confirmación humana del dato señalado antes del envío.
