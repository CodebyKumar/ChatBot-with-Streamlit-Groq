import streamlit as st
from groq import Client


# streamlit app
st.set_page_config(page_title="ChatBot")
st.title("ChatBot")

# create a sidebar with an input box named enter your groq api key
st.sidebar.title("Enter your Groq API Key")
GROQ_API_KEY = st.sidebar.text_input("Enter your Groq API Key", type="password", key="api_key")
st.sidebar.write("Please enter your Groq API Key to use the chatbot.")
client = Client(api_key=GROQ_API_KEY)

if GROQ_API_KEY=="":
    st.warning("Please enter your Groq API Key to use the chatbot.")
else:
    # function to get response with user input
    def get_response(prompt, chat_history):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
            temperature=0.8
        )
        return response.choices[0].message.content

    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    if "message_count" not in st.session_state:
        st.session_state["message_count"] = 0


    # Display previous chat
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])


    if user_input := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        bot_response = get_response(user_input, st.session_state["messages"])

        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        st.chat_message("assistant").write(bot_response)
        st.session_state["message_count"] += 1
    st.write(f"Message Count: {st.session_state["message_count"]}")
