%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                         Resume Template                            %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2025/01/01 Resume]

%-----------------------------------------
% Base Class
%-----------------------------------------
\LoadClass[a4paper,11pt]{article}

%-----------------------------------------
% Packages
%-----------------------------------------
\RequirePackage{verbatim}
\RequirePackage{titlesec}
\RequirePackage{color}
\RequirePackage{enumitem}
\RequirePackage{fancyhdr}
\RequirePackage{tabularx}
\RequirePackage{latexsym}
\RequirePackage{marvosym}
\RequirePackage[empty]{fullpage}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[normalem]{ulem}
\RequirePackage[english]{babel}
\RequirePackage[default]{sourcesanspro}

%-----------------------------------------
% PDF Unicode
%-----------------------------------------
\input glyphtounicode
\pdfgentounicode=1
\urlstyle{same}

%-----------------------------------------
% Page Layout
%-----------------------------------------
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0in}
\renewcommand{\footrulewidth}{0in}
\setlength{\tabcolsep}{0in}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\topmargin}{-0.7in}
\addtolength{\textwidth}{1.0in}
\addtolength{\textheight}{1.0in}

\raggedbottom{}
\raggedright{}

%-----------------------------------------
% Section Formatting
%-----------------------------------------
\titleformat{\section}
  {\scshape\large}{}
    {0em}{\color{blue}}[\color{black}\titlerule\vspace{0pt}]

%-----------------------------------------
% Redefinitions
%-----------------------------------------
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\renewcommand{\ULdepth}{2pt}

%-----------------------------------------
% Custom Commands
%-----------------------------------------
\newcommand{\resumeItem}[1]{%
  \item\small{#1}%
}

\newcommand{\resumeItemListStart}{%
  \begin{itemize}[rightmargin=0.11in]%
}
\newcommand{\resumeItemListEnd}{\end{itemize}}

\newcommand{\resumeSectionType}[3]{%
  \item\begin{tabular*}{0.96\textwidth}[t]{p{0.15\linewidth}p{0.02\linewidth}p{0.81\linewidth}}%
    \textbf{#1} & #2 & #3%
  \end{tabular*}\vspace{-2pt}%
}

\newcommand{\resumeTrioHeading}[3]{%
  \item\small{%
    \begin{tabular*}{0.96\textwidth}[t]{l@{\extracolsep{\fill}}c@{\extracolsep{\fill}}r}%
      \textbf{#1} & \textit{#2} & #3%
    \end{tabular*}%
  }%
}

\newcommand{\resumeQuadHeading}[4]{%
  \item%
  \begin{tabular*}{0.96\textwidth}[t]{l@{\extracolsep{\fill}}r}%
    \textbf{#1} & #2 \\%
    \textit{\small#3} & \textit{\small #4}%
  \end{tabular*}%
}

\newcommand{\resumeQuadHeadingChild}[2]{%
  \item%
  \begin{tabular*}{0.96\textwidth}[t]{l@{\extracolsep{\fill}}r}%
    \textbf{\small#1} & {\small#2}%
  \end{tabular*}%
}

\newcommand{\resumeHeadingListStart}{%
  \begin{itemize}[leftmargin=0.15in, label={}]%
}
\newcommand{\resumeHeadingListEnd}{\end{itemize}}

%-----------------------------------------
% End of Class
%-----------------------------------------
\endinput
