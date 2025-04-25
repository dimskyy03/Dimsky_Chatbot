import streamlit as st
import google.generativeai as genai

# Initialize session state for API key and flag
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Streamlit app
st.title("💬 Google Gemini AI Chatbot")

# API key input section
if not st.session_state.api_key_set:
    st.subheader("Enter Gemini API Key")
    api_key_input = st.text_input("API Key", type="password", key="api_key_input")
    if st.button("Submit API Key"):
        if api_key_input:
            try:
                # Test the API key by configuring and listing models
                genai.configure(api_key=api_key_input)
                genai.list_models()  # This will raise an error if the key is invalid
                st.session_state.api_key = api_key_input
                st.session_state.api_key_set = True
                st.success("API key set successfully!")
                st.button("Click here to start")
            except Exception as e:
                st.error(f"Invalid API key: {str(e)}")
        else:
            st.error("Please enter a valid API key.")
else:
    # Configure the API (already validated)
    genai.configure(api_key=st.session_state.api_key)
    st.write("API key is set. Ready to chat!")

    # Sidebar for model selection
    st.sidebar.subheader("Model Selection")
    # Get model names and strip 'models/' prefix
    model_names = [model.name.replace('models/', '') for model in genai.list_models() if 'gemini' in model.name.lower()]
    choosen_model = st.sidebar.selectbox("Choose Gemini model", model_names)

    # Function to call Google AI API
    def call_google_ai(prompt, model_name=choosen_model):
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            text = response.text
            if text.startswith('\n'):
                text = text[1:]
            return text.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is up?"):
        # Store and display user prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display AI response
        with st.spinner("Generating response..."):
            response = call_google_ai(prompt, choosen_model)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

    # Optional: Reset API key
    if st.sidebar.button("Reset API Key"):
        st.session_state.api_key = None
        st.session_state.api_key_set = False
        st.session_state.messages = []
        st.experimental_rerun()  # Refresh to show input field