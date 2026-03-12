  🌾 Rice Leaf Disease Detection using Deep Learning (DenseNet121)

   📌 Project Overview

Rice is one of the most important staple crops worldwide, and plant diseases significantly affect crop yield and food security. Early detection of rice leaf diseases can help farmers take timely preventive measures.

This project presents a **deep learning–based image classification system** that detects rice leaf diseases using a **DenseNet121 transfer learning model**. The system is integrated with a **Flask-based web application** that allows users to upload images of rice leaves and receive real-time disease predictions.

The model was trained on a labeled dataset containing multiple rice leaf disease categories and achieved high classification accuracy.

---

   🎯 Objectives

* Detect rice leaf diseases automatically using deep learning.
* Reduce dependency on manual inspection by agricultural experts.
* Provide a **user-friendly web interface** for disease prediction.
* Assist farmers and agricultural researchers in early disease identification.

---

   🧠 Model Architecture

The system uses **DenseNet121 (Transfer Learning)** with fine-tuning to classify rice leaf diseases.

**Workflow:**

Dataset → Image Preprocessing → Data Augmentation → DenseNet121 Model → Disease Prediction

Key techniques used:

* Transfer Learning
* Data Augmentation
* Image Classification
* Deep Convolutional Neural Networks

---

   🦠 Disease Classes

The model classifies the following rice leaf conditions:

* Bacterial Leaf Blight
* Brown Spot
* Leaf Blast
* Leaf Scald
* Narrow Brown Spot
* Healthy Leaf

---

   📊 Model Performance

The trained DenseNet121 model achieved strong performance on the test dataset.

**Evaluation Metrics**

* High classification accuracy
* Robust feature extraction
* Good generalization on unseen images

Visualizations included in the project:

* Training Accuracy Graph
* Training Loss Graph
* Confusion Matrix

---

   🖥️ Web Application

A **Flask-based web interface** allows users to:

1. Register/Login
2. Upload rice leaf images
3. Get disease predictions
4. View prediction history
5. Visualize model performance

    Web Pages

* Home
* Register
* Login
* Predict
* Result
* History
* Charts

---

   ⚙️ Technologies Used

    Programming Language

* Python

    Machine Learning / Deep Learning

* TensorFlow
* Keras
* NumPy
* Pandas
* Scikit-learn

    Visualization

* Matplotlib

    Web Framework

* Flask

    Frontend

* HTML
* CSS
* JavaScript

---

   📂 Project Structure

```
VTPDL01
│
├── CODE
│   ├── app.py
│   ├── requirements.txt
│   ├── best_densenet_model.keras
│   ├── rice_leaf_densenet121_final_model.keras
│   ├── prediction_history.json
│   │
│   ├── templates
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── predict.html
│   │   ├── result.html
│   │   ├── history.html
│   │   └── chart.html
│   │
│   ├── static
│   │   ├── accuracy.png
│   │   ├── loss.png
│   │   └── Confusion Matrix.png
│   │
│   └── uploads
│
├── README.md
└── howtorun.txt
```

---

   🚀 How to Run the Project

    1️⃣ Clone the repository

```
git clone https://github.com/RUTHVIKRAO04/VTPDL01.git
```

    2️⃣ Navigate to the project folder

```
cd VTPDL01/CODE
```

    3️⃣ Create virtual environment

```
python3 -m venv venv
```

    4️⃣ Activate virtual environment

Mac/Linux:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

    5️⃣ Install dependencies

```
pip install -r requirements.txt
```

    6️⃣ Run the Flask application

```
python app.py
```

    7️⃣ Open in browser

```
http://127.0.0.1:5001

```

---

   📈 Future Improvements

* Deploy the model on cloud platforms
* Convert to a mobile application for farmers
* Improve dataset diversity
* Implement real-time field detection
* Integrate IoT-based crop monitoring

---

   👨‍💻 Author

**Ruthvik Makloor**

B.Tech Computer Science Engineering
Deep Learning | Machine Learning | AI Applications in Agriculture

---

   📜 License

This project is developed for **academic and research purposes**.
