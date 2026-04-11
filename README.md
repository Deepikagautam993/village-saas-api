# 🌍 Village SaaS API

A production-style SaaS-based REST API built using FastAPI that manages hierarchical geographical data of India including States, Districts, Sub-Districts, and Villages. The system includes API Key authentication, rate limiting, and database-driven usage tracking.

---

## 🚀 Project Overview

This project simulates a real-world SaaS backend system where developers can access structured geographical data via secured APIs. It is designed with scalability, modularity, and production-level architecture in mind.

---

## ✨ Key Features

- 🔐 API Key-based Authentication system
- ⚡ High-performance REST APIs using FastAPI
- 🏗️ Hierarchical Data Structure (State → District → Sub-District → Village)
- 📊 Database-driven API usage tracking
- 🚦 Rate limiting support for API protection
- 🔎 Full-text search functionality
- 💡 Smart autocomplete feature
- 📘 Interactive API documentation using Swagger UI

---

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

---

## 🔐 Authentication

All protected endpoints require an API key to be passed in headers:

```
x-api-key: YOUR_API_KEY
```

---

## 📌 API Endpoints

### 🔑 Authentication
- POST /generate-api-key → Generate new API key

---

### 🏛️ States
- GET /states → Fetch all states  
- POST /states → Create new state  
- PUT /states/{id} → Update state  
- DELETE /states/{id} → Delete state  

---

### 🏙️ Districts
- GET /districts → Fetch all districts  
- POST /districts → Create district  
- GET /states/{state_id}/districts → Get districts by state  

---

### 🏘️ Sub-Districts
- POST /subdistricts → Create sub-district  
- GET /subdistricts → Fetch sub-districts  

---

### 🌾 Villages
- POST /villages → Create village  
- GET /villages → Fetch villages  

---

### 🔍 Search API
- GET /search?query=keyword → Search across all entities  

---

### ⚡ Autocomplete API
- GET /autocomplete?query=keyword → Get intelligent suggestions  

---

### 📊 Usage Tracking
- GET /usage → View API usage statistics  

---

## ▶️ Installation & Setup

Clone the repository and install dependencies:

pip install -r requirements.txt  
uvicorn main:app --reload

---

## 🌐 API Documentation

Once the server is running, access interactive Swagger UI:

http://127.0.0.1:8000/docs

---

## 📈 Project Highlights

- Real-world SaaS backend architecture
- Secure API design with authentication layer
- Scalable relational database structure
- Production-style API development
- Internship-ready backend project

---

## 👩‍💻 Author

Deepika Gautam
