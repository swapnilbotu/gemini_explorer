import vertexai 
import streamlit as s_lit
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "gemini-explorer-421901"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature = 0.4
)

# Load model with the config
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)
chat = model.start_chat()


def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with s_lit.chat_message("model"):
        s_lit.markdown(output)

    s_lit.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    s_lit.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )


s_lit.title("Gemini Explorer Project - Swap B.")

#Initializing the chat history
if "messages" not in s_lit.session_state:
    s_lit.session_state.messages = []


# Display and load to chat history
for index, message in enumerate(s_lit.session_state.messages):
    content = Content(
            role = message["role"],
            parts = [Part.from_text(message["content"]) ]
        )

    if index != 0:
        with s_lit.chat_message(message["role"]):
            s_lit.markdown(message["content"])

    chat.history.append(content)


#For writing the initial message 
if len(s_lit.session_state.messages) == 0:
    user_name_placeholder = s_lit.empty()
    user_name = user_name_placeholder.text_input("Please enter your name:")
    
    if s_lit.button("Submit"):
        initial_prompt = "Introduce yourself to the user, whose name is" + user_name + ", as Dr. Botu, an assistant powered by BotuLabs. You should talk as if you are in 10th grade but a smart student. Some of your hobbies include playing soccer, guitar, arduinos, and learning about AI. Keep the introduction short and sweet. For all responses, personalize it to the user, whose name is" + user_name
        print("The actual username was used.")

        llm_function(chat, initial_prompt)


#For getting the user input
query = s_lit.chat_input("Enter your input here.")

if query:
    with s_lit.chat_message("user"):
        s_lit.markdown(query)
    llm_function(chat, query)

