import openai
import streamlit as st

st.title("Virtual FriendGPT")

# ----- SESSION STATES

if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
    
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
 
# ----- OPEN API KEY ENTRY 
with st.expander('Additional Information'):
    st.write('This is a simple ChatBot build around the OpenAI API. \
    It requires that you provide your own personal OpenAI API key. \
    You can find or create your OpenAI API key here https://platform.openai.com/account/api-keys')
    
st.session_state.api_key = st.text_input('Enter your openai api key', type = 'password')
openai.api_key = st.session_state.api_key

# ----- SETUP EMPTY MESSAGE HISTORY

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----- SETUP A PROMPT AND RESPONSE

if st.session_state.api_key != '':
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar = 'https://github.com/1901Analytics/GeneralGPT/blob/main/bot.png?raw=true'):
            st.markdown(prompt)

        # ----- GET RESPONSE FROM OPENAI AND STORE CHAT HISTORY
        try:
            with st.chat_message("assistant", avatar = 'https://github.com/1901Analytics/GeneralGPT/blob/main/bot.png'):
                message_placeholder = st.empty()
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except:
            st.error('Please enter a valid openai api key.')
        
else:
    st.error('Please enter your openai api key to start chatting.')
