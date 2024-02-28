import time
import boto3
import streamlit as st
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory

st.title("Personalized Bedrock Chat (using Claude-v2)")

# Setup bedrock
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

#@st.cache_resource
def load_llm(memory):
    llm = Bedrock(client=bedrock_runtime, model_id="anthropic.claude-v2")
    llm.model_kwargs = {"temperature": 0.7, "max_tokens_to_sample": 2048}
    model = ConversationChain(llm=llm, verbose=True, memory=memory)
    return model

def load_context():
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='llm-playground-s3', Key='sample-c.txt')
    text = obj['Body'].read().decode('utf-8')
    #context = f"Article: {text}"    
    #full_prompt = f"{context}\n\nHuman: {prompt}"
    return text

def create_memory(text):
    from langchain.memory import ConversationBufferMemory
    #memory = ConversationBufferMemory()
    memory = ConversationBufferMemory(
        memories={
            "document1": text
        }
    )
    #memory.add_memory("document1", text)
    #memory.add_memory("document2", "Text for document 2...")
    return memory

context=load_context()
memory=create_memory(context)
model = load_llm(memory)

if "messages" not in st.session_state:
    st.session_state.messages = []

#st.session_state.messages.append({"role": "user", "content": context})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # prompt = prompt_fixer(prompt)
        print(prompt)
        result = model.predict(input=prompt)

        # Simulate stream of response with milliseconds delay
        for chunk in result.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})