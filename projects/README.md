# Ultrasonic

**Group members:**

- Tamanna Shabnam (vfc208)
- Jie Zhou (zlh638)
- Shih-Hsueh Lee (vxp299)

**This repository contains:**

1. **Data project** — [`01_data_project/`](01_data_project)
   - 1 Aggregate inflation in Denmark
     - 1.1 Basics (Tamanna Shabnam)
     - 1.2 Instantaneous inflation (Tamanna Shabnam)
     - 1.3 Core inflation (Tamanna Shabnam and Shih-Hsueh Lee)
     - 1.4 Disaggregated inflation in Denmark (Tamanna Shabnam and Shih-Hsueh Lee)
   - 2 International Comparison (Shih-Hsueh Lee)
   - 3 Extension (Shih-Hsueh Lee)
2. **Model project** — [`02_model_project/`](02_model_project)
   - 1 Labor supply (Tamanna Shabnam)
   - 2 Public good (Tamanna Shabnam and Shih-Hsueh Lee)
   - 3 Top tax (Shih-Hsueh Lee)
   - 4 Extension (Shih-Hsueh Lee)
3. **Exam project** — [`03_exam_project/`](03_exam_project)
   - 1 Danish House Prices (Tamanna Shabnam)
   - 2 Exchange economy (Tamanna Shabnam and Shih-Hsueh Lee)
   - 3 The AS-AD Model (Shih-Hsueh Lee)

## How to run

All code can be run with a standard Anaconda Distribution for Python 3.13.

The data and exam projects download data through APIs, so they need a few extras:

1. Install the API packages:
   `pip install git+https://github.com/alemartinello/dstapi` (Statistics Denmark, both
   projects) and `pip install fredapi` (FRED, data project).
2. For the data project, get a free FRED API key at
   <https://fredaccount.stlouisfed.org/apikeys> and save it in
   `01_data_project/fredapi.txt`. The file is listed in `.gitignore`, so the key is never
   committed.
