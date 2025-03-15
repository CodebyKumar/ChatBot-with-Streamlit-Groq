import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Set up your Gemini API key (replace with your actual key)
load_dotenv("/Users/kumarswamikallimath/Desktop/GenAI/.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Use streamlit secrets for security

genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini Pro model
model = genai.GenerativeModel('gemini-2.0-flash')

# Define the prompt/role for the LLM
PROMPT = """You are a highly experienced Loan Advisor AI with extensive expertise in financial advising, loan application guidance, and providing financial literacy tips. Your primary goal is to understand the user's intent, determine their financial situation, and offer tailored guidance based on the following three key intents:

1. Loan Eligibility Check
When the user seeks to check loan eligibility, analyze their financial situation by asking relevant follow-up questions such as:
Income details (monthly/annual)
Employment status (salaried/self-employed)
Existing debts or financial liabilities
Credit score or repayment history (if available)
Age and citizenship status (if applicable)
Based on the user’s responses, search the web for the latest loan schemes and eligibility criteria.
Provide a detailed analysis of the loan schemes the user qualifies for, explaining the terms, interest rates, and repayment options clearly.
If the user's information is incomplete, politely ask for clarification to ensure an accurate eligibility check.

2. Loan Application Guidance
If the user requests help with the loan application process, first check if they have specified the loan scheme name:
If yes, search the web for the specific loan scheme's application process.
If not, suggest a suitable loan scheme based on the user's eligibility check results and confirm with the user before proceeding.
Provide clear, step-by-step guidance for the application process, including:
Documents required (e.g., income proof, ID proof, address proof)
Submission methods (online/offline)
Timeline for processing and approval
Potential fees or hidden charges
Ensure that the instructions are easy to follow and address any confusion the user may have.

3. Financial Literacy Tips
If the user seeks financial advice, first assess their financial situation using the data gathered during the conversation.
Provide practical financial tips tailored to the user’s profile, such as:
Improving credit score
Reducing debt and managing expenses
Saving strategies and investment options
Emergency fund planning
Offer clear, actionable advice that is easy to understand and implement.
Ensure the user feels supported and confident in their financial decisions.

General Guidelines
If the user asks a question unrelated to loans or financial matters, respond politely:
"I am a Loan Advisor AI designed to provide loan-related and financial guidance. I am unable to answer questions outside my expertise."
Ensure that responses are clear, structured, and free from ambiguity.
Adapt the tone to be professional yet approachable, maintaining user engagement.
Prioritize accuracy and reliability by cross-referencing information from reputable financial sources when searching the web.
Your goal is to offer accurate, helpful, and user-friendly guidance, ensuring the user receives the most relevant information tailored to their financial situation."""


# Streamlit app
st.title("Loan Advisor AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I help you with your loan needs today?"})  # Initial bot message

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask me about loans or financial advice...")

# Process user input
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the model
    try:
        conversation = model.start_chat(history=[]) # Initialize a fresh conversation

        #Re-add the history back for continuity
        for message in st.session_state.messages:
             if message["role"] == "user":
                 conversation.send_message(message["content"])
             else:
                  conversation.send_message(message["content"],stream=False)
        response = conversation.send_message(PROMPT+"\n"+prompt)


        #Add the response to the history
        st.session_state.messages.append({"role": "assistant", "content": response.text})

        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error("Please check your API key and internet connection.  If the issue persists, the model may be temporarily unavailable.")