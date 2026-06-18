# KPI-Tech — Support-Ticket Analytics

ETL pipeline and interactive dashboard analysing a support-ticket system ("Comptel System") for an SME, focused on support-agent performance and resolution-time KPIs.

## What it does
- **ETL** on the raw ticket export (`salida.json` / `fuente.csv`) with Pandas: cleaning, date parsing, outlier filtering and agent-name normalisation.
- Computes support KPIs:
  - **TPR** — average resolution time (*Tiempo Promedio de Resolución*).
  - **TPPR** — average time to first response (*Tiempo Promedio de Primera Respuesta*).
  - Resolution time and ticket volume **per agent**.
  - Monthly trends (year/month aggregation).
- **Interactive dashboard** built with **Dash + Plotly**, plus a **Power BI** report (`.pbix` in `FILES/`).

## Tech
Python · Pandas · NumPy · Plotly · Dash · Power BI

## Run
```bash
pip install pandas numpy matplotlib plotly dash
python KPI_TECH-PY.py
```
Then open the local Dash server in your browser. The Power BI report lives in `FILES/`.
