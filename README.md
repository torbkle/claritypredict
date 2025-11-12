# ClarityPredict

ClarityPredict is a lightweight, explainable health prediction app built with Streamlit and scikit-learn. It uses basic biomarkers (CRP, Albumin, Creatinine, BMI) to generate binary predictions and visualize feature importance using SHAP.

## 🔍 Purpose

The goal of ClarityPredict is to demonstrate how interpretable machine learning can support diagnostic decision-making. The app is designed for educational and prototyping purposes, with a focus on transparency, modularity, and clean UI.

## ⚙️ Features

- Upload CSV files with biomarker data
- Scaled logistic regression prediction
- SHAP-based feature importance (bar + beeswarm)
- Clean layout with branding and footer modules
- Modular codebase for easy extension

## 📦 Tech stack

- Python
- Streamlit
- scikit-learn
- SHAP
- pandas
- matplotlib
---

## 📚 Documentation

- `docs/project_definition.docx`  
- `docs/model_report.docx`  
- `docs/pitch_claritypredict.pptx`  

--- 

## Quick Test Mode (No Upload Needed)

ClarityPredict now includes a mobile-friendly test mode for users who don’t have a CSV file ready.

✅ How it works
Click the “Load and run example data” button on the front page

The app will automatically generate realistic test data (50 synthetic rows)

Predictions and visualizations will run instantly – no file upload required

## 📱 Designed for mobile users
This feature is especially helpful for:

First-time visitors

Mobile users who can’t easily download/upload files

Quick demos and testing without setup

---

## 👤 Author

**Torbjørn Kleiven**  
MSc in Artificial Intelligence and Machine Learning  
Noroff / UeCampus  

---

## 📬 Contact

For inquiries, collaborations, or feedback:  
📧 tk@infera.no  

---

## ⚖️ License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.


## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/claritypredict.git
cd claritypredict

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt