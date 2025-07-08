# CRISPR Patents on Agricultural Plants

This Dash web application provides interactive visualizations of patent data related to the use of CRISPR technologies in agricultural plants. The aim is to offer insights into application trends and distributions of CRISPR-related patents in plant biotechnology.

## 🌱 Data Sources

- **Raw data** come from **PatStat Online**, the patent database maintained by the European Patent Office (EPO).
- Data were extracted using a custom SQL query, which is available in this repository (see `/data` folder).
- **Processed data** used to generate visualizations are also available in this repository (see `/data` folder).

## 📊 App Content

The app consists of several tabs:

- **Information**: Documentation of data sources, IPC/CPC codes, and jurisdiction-specific figures.
- **Publications per year**: Number of patent documents by year and authority (EP, US, WO).
- *(Add other tabs if applicable, e.g. "Applicants", "Technologies", etc.)*

## 📁 Folder Structure
- app.py # Main Dash app
- functions.py # Reusable functions for graph generation
- functions.py # For generating dynamic graph
- data/ # Pre-processed data used by the app and the sql script
- README.md # This file

## Online link to the App

https://patents-on-plant.onrender.com/

