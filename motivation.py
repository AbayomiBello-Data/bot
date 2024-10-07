import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from an environment variable
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
    personalized_bot_response = f"Hi Aima, {bot_response}"
    
    # Add the bot's response to the conversation history
    conversation_history.append({"role": "assistant", "content": personalized_bot_response})
    
    return personalized_bot_response

# Custom CSS for chat interface styling
def add_custom_css():
    st.markdown("""
    <style>
    body {
        background-color: #000000;  /* Black background */
        color: #FFFFFF;  /* White text */
    }
    .header {
        background-color: #1E1E1E;  /* Dark gray background for header */
        padding: 20px;  /* Padding around the header */
        border-radius: 10px;  /* Rounded corners */
        text-align: center;  /* Center the text */
        font-size: 24px;  /* Larger font size */
        color: #FFD700;  /* Gold color for header text */
    }
    .reminder {
        background-color: #FF69B4;  /* Hot pink for reminder */
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;  /* Medium font size */
        color: #FFFFFF;  /* White text */
        margin: 10px 0;  /* Margin around the reminder */
    }
    .bot-message {
        background-color: #007BFF;  /* Blue for bot messages */
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
        max-width: 70%;
    }
    .user-message {
        background-color: #28A745;  /* Green for user messages */
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        max-width: 70%;
        margin-left: auto;
    }
    .chat-input {
        position: fixed;
        bottom: 0;
        width: 100%;
        left: 0;
        background-color: #333333;  /* Dark grey input box */
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

    # Header with styled content
    st.markdown("<div class='header'>Hi Aima, Abayomi has created me to provide motivational quotes, Bible verses, and advice for job interviews and staying productive. Let’s chat 😊</div>", unsafe_allow_html=True)

    # Colorful reminder
    st.markdown("<div class='reminder'>A reminder that you are the best Software Engineer I know in the whole wide world 😊</div>", unsafe_allow_html=True)

    # Initialize conversation history for the session
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Display the chat history in a chat-like format
    with st.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for message in st.session_state.conversation:
            if message['role'] == 'user':
                st.markdown(f"<div class='user-message'>Aima: {message['content']}</div>", unsafe_allow_html=True)
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
