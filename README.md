---
title: CASY
emoji: 🏆
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
short_description: survey bot
---

Check out the configuration reference at [Hugging Face Spaces Config](https://huggingface.co/docs/hub/spaces-config-reference)

# 🏆 CASY - Chatbot Survey Tool

<p align="center">
  <img src="logo.png" alt="CASY Logo" width="150"/>
</p>

**CASY** is a chatbot-based survey tool designed to collect insights from technical professionals like data scientists, software developers, and LLM developers. It focuses on gathering survey responses to identify and analyze technical challenges in software development projects.

## 📋 Project Overview

- **Purpose**: To enable dynamic and interactive data collection through a chatbot.  
- **Target Users**: Researchers, Master's and PhD students, and HR professionals.  
- **Participants**: Technical professionals (data scientists, developers, etc.).  
- **Tech Stack**:  
  - Streamlit (1.39.0)  
  - Python  
  - Google Cloud (Database Deployment)  

## 🛠️ Features

- **Interactive Chatbot**: Conversational survey experience for users.  
- **Cloud Integration**: All data is securely stored in Google Cloud Firestore.  
- **Dynamic Insights**: Collects responses to analyze technical challenges.
- **Dynamic Question Flow**: Adapts follow-up questions based on user responses to gather comprehensive data.  
- **Adversarial Resistance**: Maintains survey focus with up to 70% success rate.  

## 💻 Requirements

- **Python 3.x**  
- Required libraries listed in `requirements.txt`  


## 🚀 How to Run the Project

Install dependencies and run the app using the following commands:

1. Install the required libraries:  
   pip install -r requirements.txt  

2. Run the app:  
   streamlit run app.py

## 📜 License
This project is licensed under the **MIT License**.

## 👤 Contact

- **Owner**: Ahmet Bekcan  
- **Contributors**: Sıla Işık, Ceyda Suna  
- **Email**: ahmet.bekcan@metu.edu.tr, isik.sila@metu.edu.tr, ceyda.suna@metu.edu.tr
