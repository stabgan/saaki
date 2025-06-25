# SA-AKI ML Experiment Log

This document summarizes all major experiments conducted for survival analysis and binary classification on the SA-AKI (Sepsis-Associated Acute Kidney Injury) project.

---

## 1. Survival Analysis Experiments

### **A. Models Tried**

| Model                        | Features Used         | GPU | C-index (Test) | Notes |
|------------------------------|----------------------|-----|----------------|-------|
| DeepSurv (Neural Cox)        | Clean/original       | Yes | ~0.73          | Best performer; no data leakage |
| Random Survival Forest       | Engineered (107)     | No  | ~0.63          | Memory issues, no improvement |
| XGBoost AFT                  | Engineered (107)     | Yes | ~0.49          | Below random; label encoding issues |
| Compact SurvTRACE (Transformer) | Engineered (107) | Yes | ~0.53          | Feature-as-token, poor learning |
| Time Transformer (Transformer)   | Engineered (107) | Yes | ~0.64          | Time-as-sequence, best transformer |

### **B. Feature Engineering**
- Created polynomial, interaction, and clinical ratio features (total 107 features)
- One-hot encoded categorical variables
- Calculated Charlson Comorbidity Index
- **Result:** More features did not improve performance; simpler feature sets worked better

### **C. Key Insights**
- DeepSurv with original features consistently outperformed all advanced models
- Transformers and XGBoost did not surpass neural Cox regression
- Feature engineering beyond clinical basics often hurt performance
- Data quality and feature selection are likely the limiting factors

---

## 2. Binary Classification Experiments

### **A. Models Tried**

| Model                        | Features Used         | GPU | AUROC (Test)   | Notes |
|------------------------------|----------------------|-----|----------------|-------|
| XGBoost (GPU)                | Clean/original       | Yes | ~0.81          | Initial run, after fixing leakage |
| XGBoost (GPU)                | Wrong features/table | Yes | 1.00 (leakage) | Data leakage, fixed later |
| Logistic Regression          | Clean/original       | No  | ~0.78          | Baseline, no GPU |
| Deep Neural Net (PyTorch)    | Clean/original       | Yes | ~0.81          | Overfit with leakage, fixed |

### **B. Data Issues & Fixes**
- Initial runs used wrong target (`mortality_28d` instead of `event_observed`)
- Data leakage from survival/event columns; fixed by excluding them
- Corrected to use `postgres.dataset.mimic_saaki_final` with proper targets

### **C. Key Insights**
- Data leakage can inflate AUROC to 1.0; must carefully exclude outcome-related features
- XGBoost and neural nets perform similarly when leakage is fixed
- Simpler models (logistic regression) are competitive with advanced models

---

## 3. General Lessons Learned

- **Model complexity does not guarantee better results**; data quality and correct feature selection are more important
- **GPU acceleration** is helpful for large models but not a substitute for good data
- **Transformers** are not always superior for tabular clinical data
- **Careful validation** (no leakage, correct targets) is essential

---

_Last updated: 2025-06-25_ 