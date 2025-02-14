# ChatBot using Streamlit and Groq

## Overview
This project is a simple AI-powered chatbot built using **Streamlit** and **Groq**'s API. It allows users to have a conversation with an AI model in an interactive web-based interface. The chatbot uses **Llama 3.3-70B Versatile** as the model for generating responses.

## Features
- **Interactive Chat UI**: Users can input messages and receive AI-generated responses.
- **Session History**: Maintains chat history within a session.
- **Message Counter**: Tracks the number of messages exchanged during a session.
- **Customizable API Key Handling**: Loads the API key securely using **dotenv**.

## Technologies Used
- **Python**
- **Streamlit** (for building the web-based UI)
- **Groq API** (for AI-generated responses)
- **Dotenv** (for managing environment variables)

## Installation & Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/chatbot-streamlit.git
   cd chatbot-streamlit
   ```

2. **Install Dependencies**
   ```sh
   pip install streamlit groq python-dotenv
   ```

3. **Set Up Environment Variables**
   - Create a `.env` file in the project directory.
   - Add your Groq API key:
     ```sh
     GROQ_API_KEY=your_api_key_here
     ```
   - Update the script to correctly load this `.env` file.

4. **Run the Application**
   ```sh
   streamlit run chatbot.py
   ```

## How It Works
1. The app initializes chat history and displays a welcome message.
2. Users enter text into the chat input field.
3. The app sends the input and chat history to the **Groq API**.
4. The API generates a response, which is displayed in the chat.
5. The session stores chat messages to maintain context.

## Customization
- Modify the **temperature** parameter in the `get_response()` function to adjust response randomness.
- Change the **model** parameter to use a different AI model from Groq.
- Enhance UI elements using **Streamlit's** built-in components.
- Make sessions based on **Message Count** to avoid heavy tokenisation
