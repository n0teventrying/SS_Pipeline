# Heart Rate Variability (HRV) Analysis Pipeline

## Overview
This project processes and analyzes heart rate variability data collected from multiple subjects in clinical trials.  
It includes:
- **Automated processing pipeline** for cleaned HRV data.
- **Interactive GUI** to streamline data cleaning (replacing slow Excel workflows).
- **Analysis notebooks** with statistical and visual results.

![Pipeline Diagram](images/pipeline_diagram.png)

---

## Data
The cleaned trial data is stored in [`data/data.zip`](data/data.zip).  
Each file contains HRV time series from one subject, pre-processed to remove obvious artifacts.

---

## Workflow
1. **Data Cleaning**
   - Performed using our custom [GUI tool](src/gui.py).
   - Speeds up artifact removal compared to manual Excel processing.
   - ![GUI Screenshot](images/gui_screenshot.png)

2. **Pipeline Execution**
   - Implemented in [`pipeline.py`](src/pipeline.py).
   - Steps include:
     1. Load cleaned data.
     2. Apply filtering and feature extraction.
     3. Output processed dataset for analysis.

3. **Analysis**
   - Conducted in [`notebooks/overview.ipynb`](notebooks/overview.ipynb).
   - Includes:
     - Time domain and frequency domain HRV metrics.
     - Visualization of variability trends.
     - Group comparisons across trial conditions.

---

## Example Results
![Results Plot](images/results_plot.png)

---

## How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
