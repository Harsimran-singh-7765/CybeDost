
# 🛡️ Cyber Dost - AI Cyber Safety Companion

**Cyber Dost** is an intelligent, interactive chatbot designed to educate students and internet users about Cyber Safety and Security. Built for the **Classes XI-XII Cyber Safety Competition**, it leverages Google's **Gemini 1.5 Flash** model to provide real-time, expert advice on topics ranging from password hygiene to preventing phishing attacks.

---

##  Tech Stack

`Python` | `Streamlit` | `Google Generative AI` | `LLM` | `Cyber Security` | `Prompt Engineering`

---

## 🚀 Key Features

* **⚡ Powered by Gemini 1.5 Flash:** Utilizes Google's latest lightweight model for lightning-fast responses.
* **🧠 Expert Persona:** Engineered via advanced System Prompting to act as a professional Cyber Security Consultant, not a generic AI.
* **🛡️ Comprehensive Coverage:** Trained to handle 25+ critical topics including Phishing, DDoS, SQL Injection, and Social Engineering.
* **💬 Interactive UI:** A clean, chat-interface built with Streamlit that mimics modern messaging apps.
* **🚫 Ethical Guardrails:** Programmed to refuse requests for malicious hacking instructions while pivoting to educational defense strategies.

---

## 📂 Project Structure

```bash
Cyber-Dost/
├── main.py               # Main application script
├── requirements.txt     # List of python dependencies
└── README.md            # Project documentation

```

---

## 🛠️ Installation & Setup

Follow these steps to set up the project locally.

### 1. Prerequisites

Ensure you have **Python** installed on your system.

### 2. Clone the Repository (or Download)

```bash
git clone https://github.com/your-username/cyber-dost.git
cd cyber-dost

```

### 3. Install Dependencies

It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt

```

*(If you don't have a requirements file, run: `pip install streamlit google-generativeai`)*

### 4. API Key Configuration

1. Get your free API Key from [Google AI Studio](https://aistudio.google.com/).
2. Open `app.py`.
3. Replace the placeholder with your key:
```python
GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"

```



---

##  How to Run

Execute the following command in your terminal:

```bash
streamlit run app.py

```

The application will automatically launch in your default web browser at `http://localhost:8501`.

---

##  Usage Examples

**User:** "How do I create a password that cannot be hacked?"
**Cyber Dost:** Provides a checklist (Length, Special Characters, avoiding dictionary words) and explains Entropy.

**User:** "I received a link saying I won a lottery."
**Cyber Dost:** Identifies this as a potential **Phishing attempt** and lists steps to verify the sender without clicking the link.

---

##  Rubric Compliance

This project meets the competition criteria by:

1. **Creativity:** Custom sidebar UI and typed-streaming effects.
2. **Originality:** Unique "Cyber Dost" persona defined via System Instructions.
3. **User Experience:** fast, error-free interaction using the Gemini Flash model.
4. **Coverage:** Capable of answering all 25+ mandated cyber safety questions.

---

##  Contribution

This is a solo project developed for the Cyber Safety Hackathon.

---

### Bonus Step: Create a `requirements.txt`

To make this look 100% professional, create a new file named `requirements.txt` in the same folder and paste these two lines inside it:

```text
streamlit
google-generativeai

```