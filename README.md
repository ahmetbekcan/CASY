# 🏆 CASY - Chatbot Survey Tool

<p align="center">
  <img src="ui_components/logo.PNG" alt="CASY Logo" width="150"/>
</p>

**CASY** is a chatbot-based survey tool designed to collect insights from technical professionals like data scientists, software developers, and LLM developers. It focuses on gathering survey responses to identify and analyze technical challenges in software development projects.

## 📋 Project Overview

- **Purpose**: To enable dynamic and interactive data collection through a chatbot.  
- **Target Users**: Researchers, Master's and PhD students, and HR professionals.  
- **Participants**: Technical professionals (data scientists, developers, etc.).  
- **Tech Stack**:  
  - Streamlit (1.39.0)  
  - Python  
  - Google Cloud

## 🛠️ Features

- **Interactive Chatbot**: Conversational survey experience for users.  
- **Dynamic Insights**: Collects responses to analyze technical challenges.
- **Dynamic Question Flow**: Adapts follow-up questions based on user responses to gather comprehensive data.  
- **Adversarial Resistance**: Maintains survey focus with up to 90% success rate.  

## 💻 Requirements

- **Python 3.x**  
- Required libraries listed in `requirements.txt`  


## 🚀 How to Run the Project

Install dependencies and run the app using the following commands:
1. Clone the project.
2. Install the required libraries:  
   pip install -r requirements.txt
3. Create an access token in Hugging Face.
4. Authenitcate with Hugging Face using "huggingface-cli login" command, and enter your Hugging Face token.
5. Run the app:  
   streamlit run app.py

## 🧩 Core Features
### **Create a survey session**
![msedge_eW7cbZiyeE](https://github.com/user-attachments/assets/e57de93b-bcbc-46bc-a547-e9647a12bdaf)

### **Join a created survey session**
![msedge_L56G8ijmhS](https://github.com/user-attachments/assets/47c988fb-6ca6-4d44-914e-453c7e89489e)

### **Complete the survey**
![msedge_uM5vL0xPVk](https://github.com/user-attachments/assets/e772fa51-4bfd-4f1b-a44c-786d3e3abca8)

### **View details of completed survey sessions**
![msedge_nP6GRiqCU8](https://github.com/user-attachments/assets/3148378b-61c7-44b7-83a0-f455caa98f00)

### **Resume surveys from where you left off**
![explorer_9LPqjuXiZW](https://github.com/user-attachments/assets/97261457-9b12-41c2-8d31-4dc144b88427)


## 🛠️ Trial Features
### Try CASY right away!

![explorer_P8kOl9Ciuf](https://github.com/user-attachments/assets/18501fde-9755-4e49-837e-ff5ff99a4909)

### Simulate a survey
Due to the nature of our application, it is not possible to create a testing environment using predefined question-answer pairs to measure the chatbot's accuracy. Therefore, we developed a simulation environment that allows us to evaluate the chatbot's performance by generating survey participant agents using real data from technical debt surveys.

In this environment, you can select a participant profile and specify the number of questions the chatbot should ask, then run the survey simulation. To make the testing environment more realistic, we introduced two parameters: Offtopic Answer Weight and Uninformative Answer Weight. Based on these weights, additional agents may take over the survey, producing off-topic or uninformative answers, enabling us to observe how the chatbot handles such situations.

"Log Data" checkbox can be checked to save the simulation data and parameters in your Weights And Biases account (requires authentication).

Further details about the implementation can be found in tests/survey_test.py.

![msedge_9ZFWTTueS2](https://github.com/user-attachments/assets/f341dadc-d54d-474c-8ac1-4f8d949d2d77)

### Change chatbot parameters

![msedge_5CYtTrj16D](https://github.com/user-attachments/assets/174bbfb9-0c55-4747-94d8-0ebedb6f0abc)

## 📜 License
This project is licensed under the **MIT License**.

## 👤 Contact

- **Owner**: Ahmet Bekcan  
- **Contributors**: Sıla Işık, Ceyda Suna  
- **Email**: ahmet.bekcan@metu.edu.tr, isik.sila@metu.edu.tr, ceyda.suna@metu.edu.tr
