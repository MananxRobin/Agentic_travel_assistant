# 🧳 Travel Agent AI

An intelligent travel planning assistant built with Python.  
This AI-powered project helps users plan trips, find destinations, and organize travel itineraries.

---

## 📌 Features
- 🧠 AI-powered itinerary suggestions
- 🌍 Destination recommendations
- 📅 Activity scheduling
- 🗣️ Interactive Q&A travel assistant
- ✅ Fully tested with `pytest`

## 🛠️ Technologies Used

-   **Backend**: Python
-   **AI Framework**: LangChain
-   **Language Model**: OpenAI GPT-4o-mini
-   **Frontend**: Streamlit
-   **APIs**: Google Calendar API
-   **Dependencies**: `langchain`, `streamlit`, `google-api-python-client`, `google-auth-oauthlib`, `python-dotenv`, `openai`


---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/MananxRobin/Agentic_travel_assistant
cd Agentic_travel_assistant
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
You'll need to configure your API keys.

-   **OpenAI API Key**:
    -   Create a file named `.env` in the root of the project.
    -   Add your OpenAI API key to this file:
        ```
        OPENAI_API_KEY="your-openai-api-key"
        ```

-   **Google Calendar API Credentials**:
    1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    2.  Create a new project.
    3.  Enable the "Google Calendar API" for that project.
    4.  Go to "Credentials," click "Create Credentials," and choose "OAuth client ID."
    5.  Select "Desktop app" as the application type.
    6.  Download the JSON file and rename it to `credentials.json`.
    7.  Place this `credentials.json` file in the root directory of the project.

    *Note: The first time you run the application, you will be prompted to authorize access to your Google Calendar through a browser window.*

### 5. Run the App
```bash
streamlit run app.py
```

---

## 🧪 Running Tests
```bash
pytest test_code.py
```

---

## 📂 Project Structure
```
app.py             # Main application entry point
test_code.py       # Test cases for the travel agent
travel_agent.py    # Core travel agent logic
requirements.txt   # Python dependencies
README.md          # Project documentation
```

---

## 🛠 Tech Stack
- Python 3.10+
- OpenAI API (or other LLM provider)
- Pytest (for testing)

---

## 📸 Screenshots
<img width="1512" height="982" alt="Screenshot 2025-08-14 at 7 26 22 PM" src="https://github.com/user-attachments/assets/97b690f0-83eb-438a-a7bd-54141f884b93" />



---

## 📄 License
MIT 

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 🌟 Acknowledgements
- OpenAI for providing the AI APIs
- Python community for libraries and tools
