\NeedsTeXFormat{LaTeX2e} % LaTeX 2.09 can't be used (nor non-LaTeX)
\ProvidesClass{rSIMONIN} % nom de la classe

\LoadClass[a4paper,11pt]{report} % On charge la classe report
% Il serait intéressant de regarder ce package un jour : https://ctan.org/pkg/memoir

\usepackage{emptypage} % Pour avoir des pages blanches

\usepackage[table]{xcolor}  % For color options
\usepackage{colortbl}       % For coloring table borders
\usepackage{tabularx}       % For tables that can stretch to the full width
\usepackage{array}          % For additional column formatting options
\usepackage{graphicx}       % For setting specific row heights


% pour avoir le même interligne que sur Word,
% car un "line skip" a un facteur de 1.2 donc 1.2*1.25=1.5
%\linespread{1.25}

\usepackage{packages/couleurs_SIMONIN} %Couleurs définies dans la charte graphique de Simonin
\usepackage[T1]{fontenc} % Pour les accents
\usepackage[utf8]{inputenc} % Pour les accents
\usepackage{censor} % Pour censurer du texte


% Package babel pour le français et l'anglais,
% main = language pour tout ce qui est titre etc
\usepackage[main=french,english]{babel} % Pour les langues
\usepackage{setspace} % Pour les interlignes

\singlespacing % interligne simple
% \onehalfspacing % interligne 1.5cm
\usepackage{indentfirst} % pour indenter en début de paragraphe suivant un début de section
\setlength{\parindent}{1.27cm} % espace d'indentation recommandé par la norme APA
\setlength{\parskip}{1em} % espacement entre les paragraphes


\usepackage{datetime2} % datetime2 replaces the datetime package
\usepackage{fancyhdr} % Pour les en-têtes et pieds de page
\usepackage{tikz} % Pour les dessins
\usetikzlibrary{backgrounds} % Provides page coordinates like current page.north west

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour les liens
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% \usepackage{hyperxmp} % hyperxmp charge les métadonées de base via \author etc.
\usepackage{bookmark} % charge hyperref

\hypersetup{ % hyperref setup
    colorlinks=true, % colorise les liens
    linkcolor=bleuRoiUTT, % couleur des liens internes
    filecolor=magenta, % couleur des liens vers les fichiers
    urlcolor=bleuCielUTT, % couleur des liens externes
    pdfcenterwindow=true, % position the document window in the center of the screen
    pdfdisplaydoctitle=true, % display the document title in the pdf file
    pdfpagetransition=Dissolve, % use a "dissolve" transition for page transitions
    naturalnames=true, % use LATEX-computed names for links
    pdfcreator={Scrib'UTT}, % creator of the pdf file
}

\providecommand\phantomsection{} % To avoid the error "destination with the same identifier already exists"


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour avoir plusieurs langues dans le document
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\declarelanguage}{\@dblarg\@declarelanguage} % On déclare une langue
\def\@declarelanguage[#1]#2{% On définit la langue
    \long\@namedef{#2}{% On définit la commande
        \edef\@temp{\string#1}% On récupère le nom de la langue
        \ifx\@temp\languagename % Si la langue est la langue courante
            \expandafter\@firstofone % On affiche le texte
        \else
            \expandafter\@gobble % Sinon on ne fait rien
        \fi}%
}
\declarelanguage[english]{EN} % Utilisable avec \EN{English text}
\declarelanguage[french]{FR} % Utilisable avec \FR{French text}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour intégrer toutes les images d'un répertoire
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage{pgffor}    % For looping

% Define the directory and file extension of your images
\newcommand{\imagedir}{output_images/}  % Replace with your folder path
\newcommand{\imageext}{png}      % Set your image extension (e.g., png, jpg)
% Define a command to include images
\newcommand{\includeallimages}{
    \foreach \i in {1, 2, 3, 4, 5} {  % Replace 1,...,n with the expected image file names without extensions
            \includegraphics[width=\linewidth]{\imagedir \i.\imageext}
            \par\medskip  % Adds some space between images
        }
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour les citations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand*{\rom}[1]{\expandafter\@slowromancap\romannumeral #1@} % Pour les chiffres romains

% load the microtype package with the final package option
% to ensure that the microtypographic features are activated
% even when using the draft class option.
\usepackage[final]{microtype} % permet d'éviter le "overfull hbox" sur la bibliographie par exemple

\usepackage{floatrow} % pour minted, entre autre
\usepackage{url} % Pour les liens

\newcommand{\shortUrl}[1]{\href{#1}{(short.url)}} % Pour les liens courts

\usepackage{titling} %thetitle thedate etc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{afterpage} % Pour ajouter une page blanche

\newcommand\myemptypage{ % Pour ajouter une page blanche
    \null % Empty box
    \thispagestyle{empty} % Empty page style
    \addtocounter{page}{-1} % Decrease page counter
    \newpage % Add a new page
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour la table des matières
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand\myfinaltoc{ % Pour ajouter une page blanche
    \null % Empty box
    \fancyhead[R]{} % Empty page style
    \setlength{\cftbeforetoctitleskip}{-1em} % On réduit l'espace avant le titre
    \setlength{\cftaftertoctitleskip}{1em} % On réduit l'espace après le titre
    \pagenumbering{gobble} % on n'affiche pas les numéros de page
    \setcounter{tocdepth}{10} % On affiche tout
    \tableofcontents
    \addtocounter{page}{-1}
    \newpage
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour la liste des figures
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand\myILB{ 
    \null
    \thispagestyle{ILB} % Empty page style
    \addtocounter{page}{-1}
    \newpage
}

\usepackage{blindtext} % Pour générer des textes de test

\usepackage{graphicx} % pour les images
\graphicspath{{assets/img}} % chemin des images
\usepackage{placeins} % pour bien positionner lesdites images
\usepackage[export]{adjustbox} % pour le ratio
\usepackage{subfiles} % pour les sous fichiers
\usepackage{textcomp} % pour les symboles
\usepackage{lmodern} % Pour avoir de bonnes polices en pdf
\usepackage{graphicx, animate} % Indispensable pour les figures
\usepackage{wrapfig} % Pour les figures dans le texte
\usepackage{amsmath} % Environnement pour les maths, permet du mettre du texte dans les équations

\usepackage{xcolor} % pour colorer
\usepackage[normalem]{ulem} % pour surligner
% On charge "normalem" pour éviter de changer l'emphasize des bibliographies par exemple !

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour les surlignages
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand*\highlightdp{-.8ex} % Profondeur surlignage
\newcommand*\highlightwd{0.01ex} % Largeur surlignage
\newcommand*\highlightht{2.8ex} % Hauteur du surlignage

\newcommand\highlightcommon[1]{\bgroup\markoverwith{\textcolor{#1}{\smash{\rule[\highlightdp]{\highlightwd}{\highlightht}}}}\ULon} % Surlignage

\def\bluehl{\highlightcommon{bluelight}} % Surlignage bleu
\def\greenhl{\highlightcommon{greenlight}} % Surlignage vert
\def\pinkhl{\highlightcommon{pinklight}} % Surlignage rose
\def\yellowhl{\highlightcommon{yellow}} % Surlignage jaune


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour les tableaux
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage{multicol}		% Pour les colonnes
\usepackage{multirow}       % Pour des tableaux fun
\usepackage{longtable} % pour les longs tableaux
\usepackage{booktabs} % pour des jolis tableaux
\usepackage{siunitx} % pour le typage de tableaux

\usepackage{mathtools}  % Typographie pour les ensembles communs
\usepackage{amssymb}    % Typographie pour les ensembles communs
\usepackage{xspace}         % for including spaces at the end of latex macros

\usepackage{todonotes} % Pour les todos
\setlength {\marginparwidth }{2cm} % to loading the todonotes package

%%%% For custom itemize
\usepackage{enumitem} % pour les listes
\usepackage{pifont} % pour avoir d'autres caractères

% https://tex.stackexchange.com/questions/300340/topsep-itemsep-partopsep-parsep-what-do-they-each-mean-and-what-about

\setlist{ % Pour les listes
    itemsep=2pt, % Espace entre les items
    topsep=0pt, % Espace avant la liste
    parsep=0pt, % Espace entre les paragraphes
    partopsep=0pt, % Espace entre le paragraphe et la liste
    labelindent=1.27cm, % Indentation du label
    leftmargin=*, % Alignement à gauche
    align=left % Alignement à gauche
}

\setlist[itemize,1]{label=\color{bleuRoiUTT} $\bullet$} % Pour les listes à puce
\setlist[itemize,2]{label=\color{bleuRoiUTT}$\triangleright$} % Pour les listes à puce
\setlist[itemize,3]{label=\color{bleuRoiUTT}$\square$} % Pour les listes à puce
\setlist[enumerate,1]{label=(\roman{enumi})} % Pour les listes numérotées

\SetEnumitemKey{twocol}{ % Pour les listes en deux colonnes
    itemsep = 1\itemsep, % Espace entre les items
    parsep = 1\parsep, % Espace entre les paragraphes
    before = \raggedcolumns\begin{multicols}{2}, % Pour commencer les colonnes
        after = \end{multicols} % Pour finir les colonnes
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Pour les citations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% https://www.overleaf.com/learn/latex/Biblatex_citation_styles
\usepackage[
    backend=biber, % use the biber backend with the authoryear citation style
    dateera=secular, % pour avoir des Avant l'Ere Commune et plus av JC
    dateeraauto=100, % Si on le passe à 1000, 1969 deviendra 1970 EC
    maxnames=99, % Pour avoir tous les noms
    style=numeric, % Citation style
    citestyle=verbose, % Citation style
    sortlocale=auto, % Sort based on the locale of the bibliography
    seconds=true, % Pour avoir les secondes
    bibencoding=auto, % Auto-detect the input encoding
    sorting=nty % Sorting by name, title and years
]{biblatex} % Use biblatex to manage the bibliography

\addbibresource{latex-files/bibliography.bib} % The filename of the bibliography

%\usepackage[nottoc,numbib]{tocbibind} % pour inclure la biblio directement dans le sommaire

\usepackage{rotating} % pour tourner les figures
\usetikzlibrary{calc}		%Pour les figures et graphes
\usepackage{subcaption} % pour les sous figures

% Text pos to position texts in absolute coords for the first page.
\usepackage[absolute,overlay]{textpos} % Pour positionner des textes en coordonnées absolues

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Glossaire
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage[acronym, toc, xindy, ucmark]{glossaries} % Pour les glossaires
% Uncomment this if you want to make glossary
% \makeglossaries


%%%%%%%%%%%%%
% Si vous autorisez un étirement (ragged) arbitraire,
% vous pouvez obtenir un texte très irrégulier qui peut généralement être amélioré en limitant l'irrégularité.
\usepackage{ragged2e} % for justifying https://tex.stackexchange.com/questions/369549/justifying-text-in-overleaf-template
% https://fr.overleaf.com/learn/latex/Text_alignment#Using_the_package_ragged2e
%%%%%%%%%%%%

\usepackage{caption} % Pour les légendes
\usepackage{dialogue} % pour les dialogues

\usepackage[font=itshape]{quoting} % pour les citations
\usepackage{epigraph, varwidth} % pour les épigraphes


% Adjust epigraphs
\renewcommand{\epigraphsize}{\small\itshape} % Pour la taille
\renewcommand{\epigraphflush}{flushright} % Pour l'alignement
\renewcommand{\textflush}{justify} % Pour l'alignement
\setlength{\epigraphwidth}{0.5\textwidth} % Pour la largeur



% incorporer une citation dans une ligne
\newcommand{\inlinequote}[1]{\textit{``#1``}}  % Sans référence bibliographique
\newcommand{\inlinequoteRef}[2]{\textit{``#1``}\footnote{\cite{#2}}} % Avec référence bibliographique

% pour séparer les idées
\newcommand{\ideaEnd}{\[ \star \]} % Pour séparer les idées
\newcommand{\tripleS}{\[ \star \quad \star \quad \star \] \\} % Pour séparer les idées

% pour le code
% \usepackage[cache=false]{minted}        % Utilisé pour les scripts

% Box de couleur
\usepackage[skins,breakable, most]{tcolorbox} % Pour les boites de couleur

\tcbset{on line, 
    boxsep=4pt, left=0pt,right=0pt,top=0pt,bottom=0pt,colframe=white,colback=lightgray,highlight math style={enhanced} % Pour les boites de couleur
}

\newcommand{\code}[1]{\tcbox{\texttt{\textcolor{red}{#1}}}} % Pour le code

% "When using babel or polyglossia with biblatex, loading csquotes is recommended to ensure that quoted texts are typeset according to the rules of your main language.'
% load csquotes AFTER minted
\usepackage{csquotes} % Pour les guillemets

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%- verbatim input txt file beautifuly
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{fancyvrb} % for verbatim input

% redefine \VerbatimInput
\RecustomVerbatimCommand{\VerbatimInput}{VerbatimInput} % to redefine \VerbatimInput
{fontsize=\tiny, % font size
    %
    frame=lines,  % top and bottom rule only
    framesep=2em, % separation between frame and text
    rulecolor=\color{gray}, % color of frame
    %
    labelposition=topline, % above the frame
    %
    commandchars=\|\(\), % escape character and argument delimiters for
    % commands within the verbatim
    commentchar=*        % comment character
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%- lstlisting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{listings} % Pour les listings

\lstdefinestyle{codestyle}{ % Style pour les listings
    language=Python, % Langage
inputencoding=utf8, % Pour les accents
extendedchars=true, % Pour les accents
literate={é}{{\'e}}1 {è}{{\`e}}1 {ç}{{\c c}}1, % Pour les accents
backgroundcolor=\color{codebg!10},   % choose the background color
basicstyle=\ttfamily\scriptsize,        % size of fonts used for the code
breaklines=true,                 % automatic line breaking only at whitespace
captionpos=b,                    % sets the caption-position to bottom
commentstyle=\color{codecomment},    % comment style
escapeinside={\%*}{*)},          % if you want to add LaTeX within your code
moredelim=**[is][\color{red}]{@red}{@red}, % to set something in red, @red i'm in red @red
keywordstyle=\color{codekeyword},       % keyword style
stringstyle=\color{codepurple},     % string literal style,
breakatwhitespace=false,        % sets if automatic breaks should only happen at whitespace
keepspaces=true,                % keeps spaces in text, useful for keeping indentation of code (possibly needs columns=flexible)
columns=fullflexible,          % columns=flexible, keepspaces=true
title=\lstname,                % show the filename of files included with \lstinputlisting; also try caption instead of title
xleftmargin=0.8cm, % Pour l'indentation
rulecolor=\color{black!80}, % If not set, the frame-color may change on use
framesep=0.5em, % Pour l'espacement
frame=tlrb, % Pour le cadre
%frameshape={RYR}{Y}{Y}{RVR},
numberstyle=\tiny, % Pour la taille des numéros
numbersep=2em, % Pour l'espacement des numéros
numbers=left, % Pour les numéros à gauche
showspaces=false, % show spaces adding particular underscores
showstringspaces=true, % underline spaces within strings
morekeywords={None,} % Pour les mots clés
showtabs=false, % show tabs within strings adding particular underscores
tabsize=4, % Pour la taille des tabulations
belowskip=0em, % Pour l'espacement en dessous
aboveskip=1em, % Pour l'espacement au dessus
}

\lstset{style=codestyle} % On applique le style


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Import custom commands
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage{packages/commands} % Custom commands

\newcommand{\frontpagereports}{\import{packages/}{frontpage_reports.tex}} % Pour la page de garde des rapports
\newcommand{\frontpageSTB}{\import{packages/}{frontpage_STB.tex}} % Pour la page de garde des STB
\newcommand{\frontpageSTC}{\import{packages/}{frontpage_STC.tex}} % Pour la page de garde des STC

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newif\if@noUTTcolors\@noUTTcolorsfalse % Pour les couleurs UTT
\DeclareOption{noUTTcolors}{ % Pour les couleurs UTT
    \@noUTTcolorstrue % Pour les couleurs UTT
}
\ProcessOptions\relax % Pour les couleurs UTT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Variables pour le document
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% \newcommand{\UE}[1]{\def\theUE{#1}} %Passage de l'UE en variable
% \newcommand{\RPeda}[1]{\def\theRPeda{#1}} %Passage du respo peda en variable
% \newcommand{\Semestre}[1]{\def\theSemestre{#1}} %Passage du semestre en variable
\newcommand{\maitriseouvrage}[1]{\def\maitriseouvrage{#1}} %Passage du titre en variable
\newcommand{\architectes}[1]{\def\architectes{#1}} %Passage du titre en variable
\newcommand{\bureauetudescontrole}[1]{\def\bureauetudescontrole{#1}} %Passage du titre en variable
\newcommand{\titreprojet}[1]{\def\titreprojet{#1}} %Passage du titre en variable
\newcommand{\soustitreprojet}[1]{\def\soustitreprojet{#1}} %Passage du titre en variable
\newcommand{\redacteur}[1]{\def\redacteur{#1}} %Passage du titre en variable
\newcommand{\emailredacteur}[1]{\def\emailredacteur{#1}} %Passage du titre en variable
\newcommand{\verificateur}[1]{\def\verificateur{#1}} %Passage du titre en variable
\newcommand{\emailverificateur}[1]{\def\emailverificateur{#1}} %Passage du titre en variable
\newcommand{\numeroaffaire}[1]{\def\numeroaffaire{#1}} %Passage du titre en variable
\newcommand{\notehypotheses}[1]{\def\notehypotheses{#1}} %Passage du titre en variable
\newcommand{\adresseprojet}[1]{\def\adresseprojet{#1}} %Passage du titre en variable
\newcommand{\numeroreference}[1]{\def\numeroreference{#1}} %Passage du titre en variable
\newcommand{\numerodoc}[1]{\def\numerodoc{#1}} %Passage du titre en variable


% passage des mots clés en variables
\newcommand{\Kone}[1]{\def\theKone{#1}} %Passage des mots clés en variable
\newcommand{\Ktwo}[1]{\def\theKtwo{#1}} %Passage des mots clés en variable
\newcommand{\Kthree}[1]{\def\theKthree{#1}} %Passage des mots clés en variable
\newcommand{\Kfourth}[1]{\def\theKfourth{#1}}  %Passage des mots clés en variable

\newcommand{\Entreprise}[1]{\def\theEntreprise{#1}} %Passage de l'entreprise en variable
\newcommand{\Lieu}[1]{\def\theLieu{#1}} %Passage du lieu en variable
\newcommand{\REntre}[1]{\def\theREntre{#1}} % responsable entreprise

\newcommand{\DDate}[1]{\def\theDDate{#1}} % pour propager notre date dans tout le document

% On créé une variable redirigeant sur openstreetmap
\newcommand{\mapAddr}[1]{\href{https://www.openstreetmap.org/search?query=#1}{#1}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gestion des titres
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage[ % Pour les titres
    sf, % Serif text
    sl, % Slanted text
    outermarks, % Pour les marques extérieures
    explicit % Permet de choisir on l'on place l'argument
]{titlesec} % Pour les titres

%%% Chapter ( Niveau 1 )
% https://borntocode.fr/latex-personnaliser-les-titres-chapter/ => ?

% APA : Centré gras
\titleformat{\chapter} % command
[block] % shape (hang is normal shape, it was just for remember)
{\normalfont\LARGE\bfseries\centering\color{bleuRoiUTT}} % format
{\FR{Chapitre}\EN{Chapter} \thechapter} % label
{0.5em} % Spacing between label and title
{\\#1} % before code

\titlespacing{\chapter} % Set the spacing around the title
{0em}                  % Left
{0em}                  % Above
{1em}                  % Below\ŧit


%%% Section ( Niveau 2 )
% APA : Aligné à gauche, gras
\titleformat{\section} % command
[block] % shape (hang is normal shape, it was just for remember)
{\normalfont\Large\bfseries\raggedright\color{bleuRoiUTT}} % format
{\thesection} % label
{0.5em} % Spacing between label and title
{#1} % before code

%%% Subsection ( Niveau 3 )
\titleformat{\subsection} % command
[block] % shape
{\normalfont\large\bfseries\itshape\raggedright\color{bleuCielUTT}} % format
{\thesubsection} % label
{0.5em} % Spacing between label and title
{#1} % before code


%%% Subsubsection ( Niveau 4 )
\titleformat{\subsubsection} % command
[block]
{\hspace{1.27cm}\normalfont\large\bfseries\raggedright\color{grisUTT}} % format
{\thesubsubsection} % label
{0.5em} % Spacing between label and title
{#1} % before code

%%% paragraph ( Niveau 5 )
\titleformat{\paragraph} % command
[block]
{\hspace{1.27cm}\normalfont\large\bfseries\itshape\raggedright\color{bleuRoiUTT}} % format
{\theparagraph} % label
{0.5em} % Spacing between label and title
{#1} % before code

\titlespacing{\paragraph} % Set the spacing around the title
{0pt}                  % Left
{0pt}                 % Above
{0pt}                  % Below

%%% subparagraph
\titleformat{\subparagraph} % command
[block]
{\normalfont\bfseries\raggedright\color{bleuRoiUTT}} % format
{\thesubparagraph} % label
{0.5em} % Spacing between label and title
{#1} % before code

% Pour le titre de l'Abstract
\newenvironment{myabstract}{% Pour l'abstract
    \begin{center} % Pour centrer
        {\normalfont\Large\bfseries % Pour la taille et le gras
            \color{bleuRoiUTT}Abstract} % Pour la couleur
        \\
        \normalfont \normalsize \justify % Pour le texte normal
        \bfseries % Pour le gras
        }
        {
    \end{center}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gestion des TOC / LOF / LOT (Table Of Contents, List Of Figures, List Of Tables )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage[toc, page, header]{appendix} % Pour les annexes

\renewcommand{\appendixpagename}{Annexes} % Nom de la page des annexes
\renewcommand{\appendixtocname}{Annexes} % Nom des annex

%%
\usepackage{tocloft} % Pour les tables des matières

% On définit le style des titres
\renewcommand{\cfttoctitlefont}{\color{bleuRoiUTT}\Large\bfseries} % Pour le titre de la toc
\renewcommand{\cftloftitlefont}{\color{bleuRoiUTT}\Large\bfseries} % Pour le titre de la lof
\renewcommand{\cftlottitlefont}{\color{bleuRoiUTT}\Large\bfseries} % Pour le titre de la lot

% On paramètre ce qui se passe après
%\renewcommand{\cftaftertoctitle}{\markboth{TOC}{}}
%\renewcommand{\cftafterloftitle}{\markboth{LOT}{}}
%\renewcommand{\cftafterlottitle}{\markboth{LOF}{}}
%

\usepackage{etoc} % Pour avoir des tables de matières personnalisées

% Parametrer la profondeur de la numérotation des titres
\setcounter{secnumdepth}{3} % Pour les sections

% Espace entre numéro de section et titre dans la toc
\setlength\cftsecnumwidth{2em} % Pour les sections


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%En-tête et pied de page
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Marges de 2.54cm (norme APA)
\usepackage[
    a4paper, % Format de papier
    %showframe, % show the page layout
    %includeheadfoot, % la zone de texte inclut le header et le footer
    headsep=0.5cm, % Espace entre le header et le texte
    % top=2.54cm
    % bottom=2.54cm, % Marge
    % left=1.5cm, % Marge
    % right=1.5cm, % Marge
    headheight=6cm, % Hauteur du header
    margin=2cm, % Marge
    % margin=1.5cm, % Marges
    footskip=1.25cm % Espace entre le texte et le footer
]{geometry}   % Utilisé pour les marges

\usepackage{fancyhdr}		% Pour l'entête et les pieds de page
\renewcommand{\headrulewidth}{0pt} % pas de tiret en haut de page

% Permet d'éditer le header haut gauche afin de pouvoir regler le problème
% avec \chapter*{}, voir : https://stackoverflow.com/q/3684019
\newcommand{\markleft}[1]{\markboth{\MakeUppercase{#1}}{}} % Pour le header haut gauche

% \fancypagestyle{UTT}{
%     \renewcommand{\headrulewidth}{0.5pt} %Épaisseur de la ligne d'en-tête
%     \renewcommand{\footrulewidth}{1.5pt} %Épaisseur de la ligne de pied de page

%     \renewcommand{\footrule}{%
%         {\color{bleuRoiUTT} \hrule width\headwidth height\footrulewidth \vskip+0.5mm}
%     } %Changement de la couleur de la ligne de pied de page

%     \fancyhf{} % Clear header/footer

%     %Contenu de l'en-tête :
%     \fancyhead[L]{
%         \textsc{
%             \minipage[b]{.8\linewidth}
%             \footnotesize
%             \leftmark % Contient le nom du haut niveau (chapitre)
%             % \rightmark % Contient le nom du bas niveau (section)
%             \endminipage
%         }
%     } %Section actuelle à gauche de l'en-tête

%     % \fancyhead[C]{
%     %   \vspace{5cm}
%     %   \includegraphics[width=3cm]{ressources-graphiques/logos/UTT.eps}
%     %   \vspace{0.7cm}
%     % } %Sigle de l'UTT au centre de l'en-tête

%     \fancyhead[R]{ %en-tête droite
%         \small
%         \thedate
%     }

%     %Contenu du pied de page :
%     \fancyfoot[C]{
%         %\large
%         \textbf{\thepage}
%     } %Numéro de page au centre

%     \fancyfoot[L]{
%         \small
%         \textbf{\textcolor{bleuRoiUTT}{\theauthor}}
%     } %auteur(s) à gauche

%     \fancyfoot[R]{
%         \small
%         \textcolor{bleuRoiUTT}{\theUE}
%     }
% }

\fancypagestyle{rSIMONIN}{ % Pour le style de page
    \renewcommand{\headrulewidth}{0.4pt}  % Line thickness for header
    \renewcommand{\footrulewidth}{0.4pt}  % Line thickness for foot

    \fancyhf{} % Clear header/footer
    
    %Contenu de l'en-tête :
    \fancyhead[L]{ %en-tête gauche
        \includegraphics[width=2cm]{ressources-graphiques/logos/logo_simonin.png} % Include logo on the left header
    }
    \fancyhead[R]{ %en-tête droite
        \fontsize{8}{10}\selectfont SIMONIN S.A.S. \\ 
        22 ZA des épinottes 25500 MONTLEBON - France \\
        Tél. +33 (0)3 81 67 01 26 - E-mail simonin@simonin.com}

    \fancyfoot[L]{ % Pied de page gauche
        Projet: \titreprojet \\ %
        Reference: \numeroreference \\ %
        }
    \fancyfoot[R]{
        Page {\thepage}} % Numéro de page 

}
%Section actuelle à gauche de l'en-tête

% \fancyhead[C]{
%   \vspace{5cm}
%   \includegraphics[width=3cm]{ressources-graphiques/logos/UTT.eps}
%   \vspace{0.7cm}
% } %Sigle de l'UTT au centre de l'en-tête


% % % New fancy page style
% \fancypagestyle{noTitledHeader}{
%     \fancyhf{} % Clear header/footer
%     \pagestyle{rSIMONIN}% Duplicate plain page style
%     \fancyhead[L]{ ~ }
% }


% % New page style for ILB
% \fancypagestyle{ILB}{
%     \fancyhf{} % Clear header/footer
%     \fancyfoot[C]{
%         \bfseries
%         \FR{Page laissée intentionnellement vide}
%         \EN{Intentionnaly left blank}
%     }
% }

%% redéfinition des styles de pages
% Très important !
\fancypagestyle{plain}{} % Pour redéfinir le style de page "plain" comme celui de "fancy"
% Parce que parfois la première page d'un doc dans l'article si un \maketitle est utilisé change le style de page

%%%%%%%%%%%%%%%%%%%%

\usepackage[bottom]{footmisc} % Pour éviter que les notes de bas de page soient "collées" à notre texte
\addtolength{\skip\footins}{6pt} % pour ajouter un espace en bas
\interfootnotelinepenalty=10000 % Pour éviter que les notes de bas de pages se propagent
\renewcommand{\thefootnote}{\arabic{footnote}} % notes de bas de page en arabe

\usepackage{perpage} %the perpage package
\MakePerPage{footnote} %the perpage package command => pour avoir des notes de bas de page actualisé par page
