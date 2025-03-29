import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Initialize API with caching
@st.cache_resource
def init_model():
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-2.0-flash')

# Condensed prompt with all key points
LOAN_ADVISOR_PROMPT = """You are a Loan Advisor AI expert in financial advising. Analyze the user's intent for these three categories:

1. LOAN ELIGIBILITY: Ask about income, employment, debts, credit score, age, and citizenship. Based on responses, analyze qualifying loan schemes with terms, rates, and repayment options. Request clarification if information is incomplete.

2. LOAN APPLICATION: If scheme specified, provide guidance for that scheme. If not, suggest suitable options. Include required documents, submission methods, timeline, and potential fees in step-by-step instructions.

3. FINANCIAL LITERACY: Assess financial situation and provide tailored advice on improving credit score, reducing debt, saving strategies, and emergency fund planning. Make advice actionable and easy to implement.

for abny question about insuarence, money saving, or any queries related to finance answer it in an short, effecient and understandable manner.

For other questions which are not related to money or finance, respond: "I'm a Loan Advisor AI designed for loan-related and financial guidance only."

Keep responses clear, structured, professional yet approachable. Prioritize accuracy from reputable sources."""

# Quick intent detection for optimization
def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["eligible", "qualify", "can i get", "approval"]):
        return "eligibility"
    elif any(word in text for word in ["apply", "application", "process", "document"]):
        return "application"
    elif any(word in text for word in ["advice", "tip", "improve", "financial", "credit score"]):
        return "financial_literacy"
    return "general"

def main():
    st.title("Loan Advisor AI")
    
    # Initialize states
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help with your loan needs today?"}]
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = init_model().start_chat(history=[])
    
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process user input
    prompt = st.chat_input("Ask about loans or financial advice...")
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            try:
                # Update context with detected intent
                intent = detect_intent(prompt)
                context = f"Current intent: {intent}. "
                
                # Extract basic financial info if present
                if any(word in prompt.lower() for word in ["income", "salary", "earn"]):
                    st.session_state.user_data["income_mentioned"] = True
                    context += "User mentioned income. "
                    
                if any(word in prompt.lower() for word in ["credit", "score", "debt"]):
                    st.session_state.user_data["credit_mentioned"] = True
                    context += "User mentioned credit or debt. "
                
                # Create enhanced prompt with context
                enhanced_prompt = f"{LOAN_ADVISOR_PROMPT}\n\nContext: {context}\n\nUser: {prompt}"
                
                # Stream response for better UX
                response = st.session_state.conversation.send_message(enhanced_prompt, stream=True)
                
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                message_placeholder.markdown(f"Error: {str(e)}")
                st.error("Please check your API key and connection.")

if __name__ == "__main__":
    main()