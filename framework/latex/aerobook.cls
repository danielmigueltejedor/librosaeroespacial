\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{aerobook}[2026/10/06 AeroBooks academic book class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass[11pt,a4paper,openany]{book}

\RequirePackage{aerobook-core}
