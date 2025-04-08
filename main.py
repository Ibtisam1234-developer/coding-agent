import streamlit as st
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

# API setup
gemini_api = "AIzaSyBWOH8VTt5dgEs6WD124soShBAnRQh9vkk"
provider = AsyncOpenAI(
    api_key=gemini_api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)

agent = Agent(
    name="Ibtisam's Agent",
    instructions=" You are a highly intelligent coding assistant that is designed to provide detailed explanations, solutions, and guidance for all programming-related questions. 
    You are specialized in answering questions about various programming languages (like Python, JavaScript, Java, etc.), libraries, frameworks, algorithms, data structures, coding best practices, and debugging code. 
    You should explain code snippets, solve coding problems, clarify programming concepts, and assist with any coding task. 
    
    However, **you must refuse to answer any questions that are not related to coding**. 
    If the user asks about anything non-coding (e.g., personal questions, unrelated topics, or general knowledge outside of programming), respond with:
    
    "I'm sorry, I am only capable of answering coding-related questions. Please ask something related to programming."
    
    Your responses should always be clear, concise, and educational, with the goal of helping the user improve their coding skills.",
    model=model,
)

# Async call to agent
async def get_agent_response(prompt):
    return await Runner.run(agent, prompt)

# Streamlit UI
st.set_page_config(page_title="Ibtisam's AI Chatbot")
st.title("🤖 Ibtisam's AI Chatbot")
st.markdown("**Note:** This agent is strictly for coding-related questions only. Non-coding queries will not be answered.", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask me a coding question...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(get_agent_response(prompt))
            st.markdown(response.final_output)

    st.session_state.chat_history.append({"role": "assistant", "content": response.final_output})
