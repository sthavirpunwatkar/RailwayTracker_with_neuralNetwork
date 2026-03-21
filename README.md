# 🚆 Railway Gate Closing Time Predictor (AI System)

A full-stack Machine Learning system that predicts railway gate closing time using a **Neural Network built from scratch (NumPy only)** — without using frameworks like TensorFlow or PyTorch.

This project simulates a **real-world ML pipeline** with continuous learning, API integration, database storage, and a user interface.

---

## 🧠 Project Overview

This system predicts how long a railway gate will remain closed based on:

* Time of day
* Train delay
* Speed of train
* Distance to gate
* Day of week

It continuously improves by:

* Storing predictions
* Updating actual values
* Retraining the model

---

## ⚙️ Tech Stack

* **Python**
* **NumPy** – Neural Network from scratch
* **FastAPI** – Backend API
* **PostgreSQL** – Database
* **SQLAlchemy** – ORM
* **Streamlit** – UI Dashboard
* **Uvicorn** – ASGI Server

---

## 🏗️ Project Structure

```
NeuralNetwork_RailwayProject/
│
├── app/                # FastAPI backend
│   └── api.py
│
├── model/              # Neural network implementation
│   └── model.py
│
├── training/           # Training & feedback loop
│   ├── train.py
│   └── update_actuals.py
│
├── db/                 # Database layer
│   ├── database.py
│   ├── models.py
│   ├── init_db.py
│   └── insert_data.py
│
├── ui/                 # Streamlit frontend
│   └── ui.py
│
├── model_weights.npz   # Trained model weights
├── requirements.txt
└── README.md
```

---

## 🔁 System Workflow

```
User Input → API → Prediction → Database
                        ↓
                Update Actual Values
                        ↓
                  Retrain Model
                        ↓
                Improved Predictions
```

---

## 🚀 Features

### 🤖 Machine Learning

* Neural Network built from scratch (NumPy)
* Forward propagation + backpropagation
* Gradient descent optimization

### 🧩 Feature Engineering

* `is_peak_hour` (rush hour detection)
* `travel_time = distance / speed`

### 🔄 Continuous Learning

* Stores predictions in DB
* Updates actual values
* Retrains model periodically

### 🌐 Backend API

* FastAPI-based prediction service
* Input validation
* JSON-based interaction

### 📊 UI Dashboard

* Built using Streamlit
* Interactive inputs
* Real-time predictions
* Error visualization

---

## ▶️ How to Run

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd NeuralNetwork_RailwayProject
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup Database

Make sure PostgreSQL is running and update credentials in:

```
db/database.py
```

Then create tables:

```bash
python db/init_db.py
```

---

### 4. Run API Server

```bash
uvicorn app.api:app --reload
```

API will run at:

```
http://127.0.0.1:8000/docs
```

---

### 5. Run UI

```bash
streamlit run ui/ui.py
```

---

### 6. Train Model

```bash
python -m training.train
```

---

### 7. Update Actual Values (Feedback Loop)

```bash
python -m training.update_actuals
```

---

## 📊 Example Input

```json
{
  "time": 14,
  "delay": 10,
  "speed": 60,
  "distance": 5,
  "day": 2
}
```

---

## 🧠 Key Learning Concepts

* Neural networks from scratch
* Feature engineering impact
* Data consistency in ML pipelines
* Feedback-based learning systems
* Real-world ML architecture

---

## ⚠️ Important Notes

* Custom normalization is used instead of StandardScaler for consistency
* Model improves gradually with more data
* Small datasets may initially cause unstable predictions

---

## 🔮 Future Improvements

* Integration with real railway APIs
* Automated retraining (cron jobs)
* Advanced features (weather, congestion)
* Model optimization
* Deployment (Render / Railway / AWS)

---

## 📌 Highlights

✔ Full-stack ML system
✔ Neural network from scratch
✔ Real-time API + UI
✔ Self-learning pipeline
✔ Clean modular architecture

---

## 👨‍💻 Author

**Sthavir Punwatkar**

---

## ⭐ Support

If you found this project useful:

* ⭐ Star the repo
* 🍴 Fork it
* 📢 Share it

---
