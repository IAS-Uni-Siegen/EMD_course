\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{exerciseClass}[2024/04/16 EMD exercise LaTeX class]

\LoadClass[a4paper,12pt,notitlepage,oneside]{article}


\newif\ifsolution

\DeclareOption{solution}{\solutiontrue}
\ProcessOptions\relax


\RequirePackage{geometry}
\geometry{left=1.5cm, right=1.5cm, top=1.5cm, bottom=1.5cm}


%---Allgemeine Packages---
\RequirePackage{tabularx}
\RequirePackage{caption}
\RequirePackage{siunitx}
\RequirePackage[obeyspaces, spaces]{url}
\RequirePackage[utf8]{inputenc}
\RequirePackage[english]{babel}
\RequirePackage[babel]{csquotes}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{lmodern}
\RequirePackage[onehalfspacing]{setspace}
\RequirePackage{wrapfig}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{amsmath}
\RequirePackage{booktabs}
\RequirePackage{graphicx}
\RequirePackage{import}
\RequirePackage{epsfig}
\RequirePackage{upgreek}
\RequirePackage{subcaption}
\RequirePackage{titlesec}
\RequirePackage{siunitx}
\RequirePackage{bm}
\RequirePackage{tikz}
\RequirePackage{pgfplots}
\RequirePackage{standalone}
\RequirePackage{circuitikz}
\RequirePackage{multirow}
\RequirePackage{newfloat}
\RequirePackage{mathtools}
\RequirePackage{placeins}

%% Tikz
\pgfplotsset{compat=1.18}
\usetikzlibrary{shapes, arrows, positioning, fit, calc, patterns, decorations.pathmorphing,decorations.pathreplacing,decorations.shapes,decorations.text}
\usepgfplotslibrary{groupplots}

\RequirePackage{fancyhdr}
\pagestyle{fancy}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Caption
\DeclareCaptionFont{blue}{\color{blue}}


%---Grafiken---
\graphicspath{ {./fig/} }


% Setup page geometry
\setlength{\parindent}{0em}
\setlength{\parskip}{0pt}
\setlength{\headheight}{15mm}
\setlength{\headsep}{8mm}
%\setlength{\textheight}{674pt}
\setlength{\textheight}{250mm}


\fancyhead[L]{
    \textbf{\large{Electrical Machines and Drives}}\\
    Prof. Dr.-Ing. Oliver Wallscheid
}

\fancyhead[R]{
    \includegraphics[width=\textwidth,height=10mm, keepaspectratio]{fig/IAS.pdf}
}

\fancyfoot[C]{\thepage}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Solution block %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NewDocumentEnvironment{solutionblock}{+b}
{
    \ifsolution
    \color{blue}
    %\par
    \setlength{\parskip}{0pt}
    \noindent \ignorespaces 
    \underline{Answer:}\\
    #1
    \fi
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Solution table %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NewDocumentEnvironment{solutiontable}{+b}{
    \table[ht]
    \captionsetup{labelfont={color=blue},textfont={color=blue}}
    \color{blue}
    #1}
    {
        \endtabularx
        \endtable
    }


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Solution figure %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NewDocumentEnvironment{solutionfigure}{+b}{
    \figure[htb]
    \captionsetup{labelfont={color=blue},textfont={color=blue}}
    \color{blue}
    #1}
    {
        \endfigure
    }

\renewcommand{\figurename}{Fig.}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Counter and space %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% exercise %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcounter{exerciseCount}
\setcounter{exerciseCount}{0}

\newcommand{\ex}[1]{
    \stepcounter{exerciseCount}
    \large
    \ifnum\value{exerciseCount} < 10
        \textbf{Exercise~0\theexerciseCount:} #1
    \else
        \textbf{Exercise~\theexerciseCount:} #1
    \fi
    \normalsize
    \setlength{\parskip}{1em}
}

\titleformat*{\section}{\normalfont}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% task %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcounter{taskCount}[exerciseCount]
\setcounter{taskCount}{0}

\newcommand{\task}[1]{
    \stepcounter{taskCount}
        \ifnum\value{taskCount}=1
        \setlength{\parskip}{-12pt}
        \else
        \setlength{\parskip}{12pt}
        \fi
    \normalsize \section*{\textbf{Task~\thetaskCount:~#1}}
    \addcontentsline{toc}{section}{\protect\numberline{}Task~\thetaskCount:~#1}
    \setlength{\parskip}{-12pt}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% subtask %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcounter{subtaskCount}[taskCount]
\setcounter{subtaskCount}{0}

\newcommand{\subtask}[1]{
    {\stepcounter{subtaskCount}
        \normalsize
        \setlength{\parskip}{12pt}
        \thetaskCount.\thesubtaskCount \ #1
    }

}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Numbering of equations %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\numberwithin{equation}{exerciseCount}
\numberwithin{figure}{exerciseCount}
\numberwithin{table}{exerciseCount}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% SI units %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% one space between value and unit
\sisetup{number-unit-product=\ }

% no space between the units
\sisetup{inter-unit-product = }

% fraction for units
\sisetup{per-mode = fraction}

% allow fraction for values
\sisetup{parse-numbers = false}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Tabular %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% define specific tabular rules
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{L}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
