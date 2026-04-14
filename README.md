# 🌍 Village SaaS API

A production-style SaaS-based REST API built using FastAPI that manages hierarchical geographical data of India including States, Districts, Sub-Districts, and Villages. The system includes API Key authentication, search, autocomplete, and database-driven usage tracking.

---

# 🚀 Project Overview

This project simulates a real-world SaaS backend system where developers can access structured geographical data via secured APIs. It is designed with scalability, modularity, and production-level architecture in mind.


---


# ✨ Key Features

🔐 API Key-based Authentication system  
⚡ High-performance REST APIs using FastAPI  
🏗️ Hierarchical Data Structure (State → District → Sub-District → Village)  
🔎 Full search across all entities  
💡 Smart autocomplete suggestions  
📊 Database-driven API usage tracking  
🚦 Secure API key validation  
📘 Swagger UI for API testing  

---


# 🛠️ Tech Stack

Python  
FastAPI  
SQLAlchemy  
SQLite  
Uvicorn  

---


# 🔐 Authentication

All APIs require API key in headers:

x-api-key: YOUR_API_KEY  

---


# 📌 API Endpoints

## 🔑 Authentication
POST /generate-api-key → Generate API Key  

---


## 🏛️ States
GET /states → Get all states  
POST /states → Create state  
PUT /states/{id} → Update state  
DELETE /states/{id} → Delete state  

---


## 🏙️ Districts
POST /districts → Create district  
GET /districts → Get all districts  
GET /states/{state_id}/districts → Get districts by state  

---


## 🏘️ Sub-Districts
POST /subdistricts → Create sub-district  
GET /subdistricts → Get all sub-districts  

---


## 🌾 Villages
POST /villages → Create village  
GET /villages → Get all villages  

---

## 🔍 Search API
GET /search?query=keyword → Search across all entities  

---

## ⚡ Autocomplete API
GET /autocomplete?query=keyword → Get smart suggestions 

---

## 📊 Usage Tracking
GET /usage → View API usage statistics  

---

# 📈 Project Highlights

✔ Real-world SaaS backend architecture  
✔ Secure authentication system  
✔ Scalable hierarchical database structure  
✔ Search + autocomplete intelligence  
✔ Production-level FastAPI project  
✔ Internship-ready backend system  

---

# 🌐 API Documentation

http://127.0.0.1:8000/docs  

---

# ▶️ Installation & Setup

pip install -r requirements.txt  
uvicorn main:app --reload  

---

# 👩‍💻 Author

Deepika Gautam
