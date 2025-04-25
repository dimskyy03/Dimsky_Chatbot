from google import generativeai as genai
import streamlit as st


API_KEY = st.text_input("OpenAI API Key", type="password")

# Check API key
if not API_KEY:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Setup Gemini Client
    client = genai.configure(api_key= API_KEY)

    # choose the model from sidebar
    choosen_model = st.sidebar.selectbox("Choose gemini model", [model.name for model in genai.list_models()])

    # Function to call Google AI API
    def call_google_ai(prompt, model_name=choosen_model):
        # Initialize the model
        model = genai.GenerativeModel(model_name)  # Use a valid model name
        # Generate content
        response = model.generate_content(prompt)
        # Strip leading newline if present
        if response.text.startswith('\n'):
            response.text = response.text[1:]
        return response.text

    # streamlit app
    st.title("💬Google Gemini AI Chatbot")

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    #generate a response from the AI model using the prompt.
        response = call_google_ai(prompt)

        # Store and display the AI's response.
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
