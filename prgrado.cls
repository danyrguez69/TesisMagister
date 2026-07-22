% Clase LaTeX para Informes de Proyectos de Grado de Computación
% InCo, Facultad de Ingeniería, Universidad de la República
% 12/2022


\def\filename{postgrado}
\def\fileversion{1.0}
\def\filedate{23/12/2022}

\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{postgrado}[\filedate\space\fileversion\space%
       Clase LaTeX Proyectos de Grado - InCo, FIng, UdelaR ]

\LoadClass[12pt]{book} % Cambia a una clase estándar con soporte de 12pt


%paquetes
\RequirePackage{newtxtext,newtxmath}
\RequirePackage[utf8]{inputenc} % para utilizar codificación utf8
\RequirePackage[english]{babel} % para documentos en ingles
\RequirePackage{hyperref}       % para seguir los hipervínculos
\RequirePackage{graphicx}       % para usar includegraphics
\RequirePackage{apacite}        % para citar en formato APA
\RequirePackage{ifthen}         % para comandos condicionales



%comandos
\renewcommand{\normalsize}{\fontsize{12pt}{16pt}\selectfont}
\renewcommand{\large}{\fontsize{16pt}{16pt}\selectfont}

\newcommand{\keywords}[1]{\textbf{Palabras clave:} #1}
\newcommand{\supervisor}[1]{\def\@supervisor{#1}}
\newcommand{\cosupervisor}[1]{\def\@cosupervisor{#1}}
\newcommand{\cclicense}[2]{\def\@cclicense{#1} \def\@ccversion{#2}}

\supervisor{}
\cosupervisor{}
\cclicense{by-nc-nd}{4.0}


%carátula

\renewcommand{\maketitle}[0]{%
\thispagestyle{empty}

\begin{center}
\includegraphics[height=3cm]{figs/logoUCN.png} 
\end{center}


\begin{center}
\textbf{\fontsize{18pt}{20pt}\selectfont\MakeUppercase {Universidad Católica del norte} }
\end{center}
\vspace{-10mm}
\begin{center}
\fontsize{14pt}{14pt}\selectfont \MakeUppercase {FACULTAD DE INGENIERÍA Y CIENCIAS GEOLÓGICAS } 
\end{center}
\vspace{-10mm}
\begin{center}
\large {Departamento de Ingeniería de Sistemas y Computación} 
\end{center}



\vfill

\begin{center}
 \textbf{\Huge \@title }\\[1.5cm]
\end{center}

\begin{center}
Trabajo de tesis para optar al grado de Magíster en Ingeniería Informática\\[1.5cm]

{\Large  \@author}\\[1.0cm]
\ifthenelse{\equal{\@cosupervisor}{}}{Supervisor}{Profesores Guía}\\[0.5cm]
{\large  \@supervisor}\\
{\large  \ifthenelse{\equal{\@cosupervisor}{}}{}{\@cosupervisor}}
\end{center}

\vfill 

\begin{center}
Antofagasta,  \@date
\end{center}
}

