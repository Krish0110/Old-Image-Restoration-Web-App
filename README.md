
#  Old Image Restoration Using AGAN

A **full-stack web application** that restores old and damaged images using **Attentive Generative Adversarial Networks (AGAN)**.  
The frontend is built with **React**, and the backend is powered by **Django**, featuring deep learning models for **automatic damage detection and restoration**.

---

##  Home Page

![Home Page](https://github.com/user-attachments/assets/f4779fc7-ab3a-49f4-b25a-b0b241f4c22b)

---

##  Main Page

![Main Page](https://github.com/user-attachments/assets/fbdf8630-7f83-469a-92a5-9447e17846d4)

_This is the main interface of our application, where users can upload, view, and restore old photographs._

---

##  Output Obtained

![Output](https://github.com/user-attachments/assets/cdff8c62-3fa2-4f7d-98ee-cb61f6949cd1)

---

##  Getting Started

Follow the steps below to set up and run the application locally.

###  Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- (Recommended) `virtualenv` or `conda` for backend environment isolation

---

## 🔧 Backend Setup (Django)

1. Open a terminal and navigate to the backend folder:
   ```bash
   cd DjangoBackend/
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Navigate into the Django project and run the server:
   ```bash
   cd majorBackend/
   python manage.py runserver
   ```

>  The backend will start at: `http://localhost:8000`

---

##  Frontend Setup (React)

1. Open another terminal and navigate to the frontend folder:
   ```bash
   cd major-web/
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

>  The frontend will be available at: `http://localhost:3000`

---

##  Model Inference

Ensure that your `.pth` model files are placed in the correct location inside the Django backend (e.g., `DjangoBackend/majorBackend/models/`).  
The backend will automatically use these models during image restoration.

---

## Team Members

- Aakrit Dongol
- Biraj Kumar Karanjit
- Krishala Prajapati

---
