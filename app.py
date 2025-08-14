import streamlit as st
from travel_agent import agent_executor
from langchain_core.messages import HumanMessage, AIMessage

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Travel Concierge",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- Page Title and Introduction ---
st.title("✈️ AI Travel Concierge")
st.write("I'm your personal AI assistant for planning and booking trips. Ask me anything!")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="How can I help you plan your next trip?")
    ]

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

# --- Chat Input ---
if prompt := st.chat_input("Ask me about flights, hotels, and more..."):
    # Add user's message to history and display it
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Generate and display assistant's response ---
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # THE CRITICAL CHANGE IS HERE:
            # We now pass the 'chat_history' to the agent.
            # We also ensure the history doesn't include the latest prompt, which is passed as 'input'.
            response = agent_executor.invoke({
                "input": prompt,
                "chat_history": st.session_state.messages[:-1] # Pass all messages except the last one
            })

            assistant_response = response['output']
            st.markdown(assistant_response)

    # Add assistant's response to history
    st.session_state.messages.append(AIMessage(content=assistant_response))
