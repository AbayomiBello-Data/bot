import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to generate a conversational response using the OpenAI API
def generate_conversational_response(messages, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(  # Correct API method for chat completions
            model=model,
            messages=messages,
            temperature=0.7
        )
        # Extract the assistant's response from the API response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle chatbot responses
def chatbot_response(user_input, conversation_history):
    # Add the user input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Get the chatbot response
    bot_response = generate_conversational_response(conversation_history)
    
    # Personalize bot response
    personalized_bot_response = f"Hi Prosperous People, {bot_response}"
    
    # Add the bot's response to the conversation history
    conversation_history.append({"role": "assistant", "content": personalized_bot_response})
    
    return personalized_bot_response

# Custom CSS for chat interface styling
def add_custom_css():
    st.markdown("""
    <style>
    body {
        background-color: #FFFFFF;  /* White background */
        color: #000000;  /* Black text */
    }
    .header {
        padding: 20px;  /* Padding around the header */
        text-align: center;  /* Center the text */
        font-size: 24px;  /* Larger font size */
        color: #800080;  /* Simple purple for header text */
    }
    .logo {
        margin: 20px 0;  /* Margin for the logo space */
        height: auto;  /* Set height to auto for responsiveness */
        max-height: 80px;  /* Maximum height for the logo */
    }
    .reminder {
        background-color: #800080;  /* Simple purple for reminder */
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;  /* Medium font size */
        color: #FFFFFF;  /* White text */
        margin: 10px 0;  /* Margin around the reminder */
    }
    .bot-message {
        background-color: #FFFFFF;  /* White for bot messages */
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
        max-width: 70%;
        color: #000000;  /* Black text for bot messages */
    }
    .user-message {
        background-color: #DDA0DD;  /* Light purple for user messages */
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        max-width: 70%;
        margin-left: auto;
        color: #000000;  /* Black text for user messages */
    }
    .chat-input {
        position: fixed;
        bottom: 0;
        width: 100%;
        left: 0;
        background-color: #F5F5F5;  /* Light grey input box */
        padding: 10px;
        border-top: 1px solid #ccc;
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        margin-bottom: 80px; /* Space for the input box */
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit UI app code
def main():
    add_custom_css()

    # Display logo from a local file
    logo_path = "Frame 6_111720.png"  
    st.image(logo_path, use_column_width=True)  
    st.markdown("<div class='header'>We are Prosperous and we have good Success!</div>", unsafe_allow_html=True)

    # Declaration and uplifting scripture
    st.markdown("<div class='reminder'>I have been created to provide you with declaration, word of encouragement and scriptures to strengthen your faith! ✨</div>", unsafe_allow_html=True)


    # Initialize conversation history for the session
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Display the chat history in a chat-like format
    with st.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for message in st.session_state.conversation:
            if message['role'] == 'user':
                st.markdown(f"<div class='user-message'>You: {message['content']}</div>", unsafe_allow_html=True)
            elif message['role'] == 'assistant':
                st.markdown(f"<div class='bot-message'>Bot: {message['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Function to handle user input and generate bot response
    def handle_input():
        user_input = st.session_state.user_input
        if user_input:
            # Generate chatbot response
            bot_response = chatbot_response(user_input, st.session_state.conversation)
            # Clear input field after submission
            st.session_state.user_input = ""

    # User input box for chat
    st.text_input("Type your message here:", key='user_input', on_change=handle_input)

if __name__ == "__main__":
    main()
