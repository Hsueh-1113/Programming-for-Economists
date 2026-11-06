# Programming for Economists

Coursework from **Programming for Economists** (7.5 ECTS),
Department of Economics, University of Copenhagen.

The course covers scientific programming in Python for economists: data types and
control flow, importing data from online databases (APIs), descriptive statistics and
visualisation, numerical optimisation and root-finding, simulation of economic models,
and collaborative development with Git.

Course description: [kurser.ku.dk/course/aøka08248u](https://kurser.ku.dk/course/a%C3%B8ka08248u)

---

## What is my own work

This repository contains both course material and my own work. To be explicit:

| | Folders |
| --- | --- |
| **My own work** | [`projects/`](projects) — data, model and exam projects, written in a group of three (my parts are listed below)<br>[`problem_sets/`](problem_sets) — my solutions to the weekly problem sets |
| **Course material** | [`lectures/`](lectures) — lecture notebooks, slides and walkthroughs |

Lecture notebooks and problem-set templates are teaching material from the Department
of Economics and are included here only so that my solutions are readable in context.
All rights to that material remain with the course.

### My parts of the group projects

The projects were written together with Tamanna Shabnam and Jie Zhou; the full split is in
[`projects/README.md`](projects/README.md).

| Project | My parts |
| --- | --- |
| [Data project](projects/01_data_project) | Core and disaggregated inflation in Denmark (with Tamanna Shabnam); international comparison of HICP inflation; extension on energy prices and a Taylor-rule policy rate |
| [Model project](projects/02_model_project) | Public good and optimal tax system (with Tamanna Shabnam); top tax; extension |
| [Exam project](projects/03_exam_project) | Exchange economy (with Tamanna Shabnam); AS-AD model |

---

## Structure

| Folder | Content |
| --- | --- |
| **`projects/`** | |
| `01_data_project` | **Data project** — inflation in Denmark and across countries, with data from the Statistics Denmark and FRED APIs |
| `02_model_project` | **Model project** — labour supply, public goods and optimal taxation, solved numerically |
| `03_exam_project` | **Exam project** — Danish house prices, an exchange economy and the AS-AD model |
| **`problem_sets/`** | |
| `Problem_set_0_Getting_started` | Setup exercise (course instructions) |
| `Problem_set_1_Printing_and_plotting` – `Problem_set_7_ASAD` | Weekly exercises — my solutions |
| **`lectures/`** | |
| `00_Intro_VSCode_Git_Anaconda` | Environment setup — VSCode, Git, Anaconda |
| `01_Introduction`, `02_03_Basics` | Python fundamentals — data types, containers, control flow, functions |
| `04_PrintingPlotting` | Printing, formatting and figures with `matplotlib` |
| `05_06_DescriptiveEconomics` | Descriptive statistics; importing, cleaning and merging data with `pandas` |
| `06_YourFirstProject` | Walkthrough and tips for the data project |
| `07_Optimization_RootFinding` | Numerical optimisers, root-finders, interpolation |
| `08_Seeds_and_RandomNumbers` | Pseudo-random numbers, seeds, simulation |
| `09_Solow_model`, `10_Walras`, `11_ASAD` | Solving and simulating micro- and macroeconomic models |
| `12_Calibration` | Calibrating models to data |
| `12_YourSecondProject` | Walkthrough for the model project |
| `13_DynamicProgramming` | Dynamic programming |
| `14_AI`, `14_ExamPrep` | Use of AI tools in the course; exam preparation |

---

## Skills demonstrated

- **Python fundamentals** — data types, containers (list / dict / array), conditionals,
  loops, functions and classes
- **Data handling** — import/export, API access to online databases, cleaning and merging
  with `pandas`
- **Visualisation** — descriptive statistics and figures with `matplotlib`, interactive
  plots with `ipywidgets`
- **Numerical methods** — optimisers, root-finders, linear interpolation, pseudo-random
  numbers and simulation
- **Economic modelling** — solving, simulating and calibrating micro- and macroeconomic
  models
- **Software practice** — structuring and documenting code, testing and debugging,
  version control with Git

---

## Data

All data come from public sources — Statistics Denmark and FRED — mostly downloaded
through their APIs (`dstapi`, `fredapi`); a few tables are included as Excel or CSV files.
No restricted or licensed data is included in this repository.

The data project needs a free FRED API key, which is not included. See
[`projects/README.md`](projects/README.md#how-to-run) for how to add your own.
