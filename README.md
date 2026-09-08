# 🪐 TESS Exoplanet Explorer

An interactive **Python and Streamlit application** for analyzing NASA TESS
(Transiting Exoplanet Survey Satellite) light-curve data and identifying
potential exoplanet transit signals.

The application processes stellar brightness measurements, searches for
periodic decreases in brightness using the **Box Least Squares (BLS)**
algorithm, and visualizes candidate transit signals through periodograms
and phase-folded light curves.

---

## 🔭 Overview

When an exoplanet passes between its host star and an observer, it can cause
a small, periodic decrease in the star's observed brightness. This is known
as the **transit method**.

TESS Exoplanet Explorer provides an interactive workflow for analyzing
public TESS observations and searching for these repeating transit-like signals.

Users can select a target star, retrieve observations from multiple TESS
sectors, configure an orbital-period search range, and inspect potential
planet candidates through an interactive Streamlit interface.

---

## ✨ Features

- 🔎 Search TESS observations by target identifier
- 📡 Retrieve publicly available TESS light-curve data
- 🧹 Clean, normalize, flatten, and combine observations from multiple sectors
- 📉 Remove missing values and statistical outliers
- 🪐 Detect periodic transit-like signals using **Box Least Squares (BLS)**
- 📊 Generate BLS periodograms to identify strong candidate periods
- 🔁 Phase-fold light curves around detected orbital periods
- 🌌 Search for multiple potential candidates within the same system
- 🎛️ Configure period ranges and analysis parameters
- 💻 Explore results through an interactive **Streamlit dashboard**

---

## ⚙️ How It Works

### 1. Retrieve TESS Data

The user enters a target star and selects the observations to analyze.

The application retrieves available TESS light-curve data for the target.

### 2. Preprocess the Light Curve

The observations are processed before transit detection.

The preprocessing pipeline includes:

1. Removing missing values
2. Normalizing stellar flux
3. Removing statistical outliers
4. Flattening long-term brightness trends
5. Combining observations for analysis

This produces a cleaner light curve for detecting small periodic changes
in stellar brightness.

### 3. Search for Periodic Signals

The processed light curve is analyzed using the **Box Least Squares (BLS)**
algorithm.

BLS searches across possible orbital periods for repeating, approximately
box-shaped decreases in stellar brightness that may represent planetary
transits.

Candidate signals can be characterized using values such as:

- Orbital period
- Transit duration
- Transit epoch
- BLS power

### 4. Phase-Fold the Light Curve

The light curve can be folded around a detected candidate period.

If the brightness decrease is periodic, observations from multiple orbital
cycles should align around a similar phase. This makes potential transit
patterns easier to inspect.

### 5. Search for Additional Candidates

After identifying a strong candidate signal, detected transit regions can
be excluded from subsequent analysis.

The BLS search can then be repeated on the remaining observations to
investigate additional periodic signals.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and data-processing logic |
| **Streamlit** | Interactive web application |
| **Lightkurve** | TESS light-curve retrieval and processing |
| **NumPy** | Numerical computation |
| **Astropy** | Astronomical analysis and units |
| **Matplotlib** | Scientific visualization |
| **NASA TESS Data** | Photometric observations |

---

## 📁 Project Structure

```text
TESS-Exoplanet-Explorer/
│
├── App.py
│   └── Main Streamlit application
│
├── analysis.py
│   └── Light-curve preprocessing and transit analysis
│
├── plotting.py
│   └── Scientific plotting and visualization
│
├── results.py
│   └── Analysis results and candidate presentation
│
├── sidebar.py
│   └── Streamlit sidebar controls and user inputs
│
├── nasa_eyes.py
│   └── NASA visualization functionality
│
├── pages/
│   └── Additional Streamlit application pages
│
├── requirements.txt
│   └── Python dependencies
│
├── environment_windows.yml
│   └── Windows environment configuration
│
├── images/
│   └── README screenshots
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/kovanhassan/TESS-Exoplanet-Explorer.git
cd TESS-Exoplanet-Explorer
```

### 2. Install Dependencies

It is recommended to create a virtual environment first.

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run App.py
```

Streamlit will start the application and provide a local address that can
be opened in your browser.

---

## 📊 Box Least Squares (BLS)

The **Box Least Squares** algorithm is commonly used to search astronomical
time-series data for periodic transit-like signals.

Planetary transits produce temporary decreases in the measured brightness
of a star. If a planet repeatedly crosses its host star, these decreases
occur periodically.

BLS searches a range of possible orbital periods and determines which
periods best match a repeating box-shaped transit model.

A strong BLS peak can therefore indicate a potentially interesting
periodic signal for further investigation.

---

## 🔬 Transit Detection Workflow

```text
TESS Target
     │
     ▼
Retrieve Light-Curve Data
     │
     ▼
Clean & Normalize Data
     │
     ▼
Remove Outliers
     │
     ▼
Flatten Light Curve
     │
     ▼
Box Least Squares Search
     │
     ▼
Identify Candidate Period
     │
     ▼
Phase-Fold Light Curve
     │
     ▼
Inspect Transit Candidate
```

---

## 🎯 Project Goals

TESS Exoplanet Explorer was developed to explore the intersection of:

- Astronomical data analysis
- Scientific Python programming
- Time-series signal processing
- Algorithmic detection
- Data visualization
- Interactive application development

The project demonstrates an **end-to-end scientific data-analysis pipeline**,
from retrieving astronomical observations to preprocessing, signal detection,
and interactive visualization.

---

## ⚠️ Scientific Disclaimer

Signals identified by this application should be treated as **potential
exoplanet candidates, not confirmed planets**.

Periodic changes in stellar brightness can also be produced by:

- Eclipsing binary stars
- Stellar activity
- Instrumental artifacts
- Background objects
- Other astrophysical phenomena

Confirmation of an exoplanet requires additional validation and
observational analysis.

---

## 👤 Author

**Kovan Hassan**  
Mechatronics Engineering  
University of Waterloo

GitHub: **@kovanhassan**

---

## 📄 License

This project was developed for educational, research, and portfolio purposes.
