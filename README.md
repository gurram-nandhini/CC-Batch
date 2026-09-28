# CC-Batch

## Integrated Biology and Geo Science Applications

This project contains two applications developed using modern web technologies, machine learning, and image processing.

---

## A) Biology: Gene Expression Data Analysis for Cancer Diagnosis

### Problem Statement

Cancer diagnosis using gene expression data involves analyzing thousands of gene features to identify patterns associated with different cancer types.

This application analyzes high-dimensional gene expression data and uses machine learning to classify cancer samples into different cancer types.

### Features

- User Registration and Login
- Gene Expression Dataset Processing
- Machine Learning Prediction
- Cancer Type Classification
- Prediction Probability
- Prediction History
- MySQL Database
- React Frontend
- FastAPI Backend

### Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- React
- MySQL
- Machine Learning

---

## B) Geo Science: Satellite Image Application

### Problem Statement

Satellite images contain useful information about the Earth's surface, but analyzing image properties manually can be difficult.

This application allows users to upload satellite images and analyze their properties using image processing techniques.

### Features

- User-friendly Dashboard
- Satellite Image Upload
- Image Preview
- Image Size Analysis
- RGB Analysis
- Brightness Analysis
- Image Enhancement
- Analysis History

### Technologies

- Python
- FastAPI
- React
- Pillow
- MySQL

---

## Project Architecture

```text
CC-Batch
│
├── backend/
│   └── Biology FastAPI Backend
│
├── frontend/
│   └── Biology React Frontend
│
└── satellite/
    ├── backend/
    │   └── Satellite FastAPI Backend
    │
    └── frontend/
        └── Satellite React Frontend
