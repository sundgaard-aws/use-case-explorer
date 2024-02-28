import boto3
import json
import streamlit as st
from datetime import datetime
import base64

lambda_client = boto3.client('lambda', region_name='eu-north-1')
now = datetime.now()
print("************************************************************************************")
print(now)

def invoke_lambda(payload):
    response = lambda_client.invoke(
        FunctionName='get-all-use-cases-fn',
        Payload=json.dumps(payload) 
    )
    payload=response['Payload'].read()
    #print(payload)
    #return json.loads(response['Payload'].read())
    return payload

def extract_docs():
    responseBytes = invoke_lambda({}) # invoke Lambda, get list of docs
    responseDict=json.loads(responseBytes)
    docsBase64Str=responseDict["items"]
    print(type(docsBase64Str))
    print(docsBase64Str[:50])
    # Decode base64 string
    decoded_string = base64.b64decode(docsBase64Str).decode('utf-8')

    # Convert JSON string to DynamoDB result set
    docs = json.loads(decoded_string)
    print(type(docs[0]))
    print(docs[0]["technicalAbstract"])

    for doc in docs:
        #print(type(doc))
        for attr in doc:
            print(attr)
    return docs

def print_doc_attributes():
    for doc in docs:
        st.markdown(f"- {doc['url']}") 
        st.markdown(f"- {doc['abstract']}") 
        st.markdown(f"- {doc['why']}") 
        st.markdown(f"- {doc['how']}") 

def import_local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

docs=extract_docs()

st.set_page_config(layout="wide")
import_local_css("app.css")
st.header("Use cases")
selected_doc = st.selectbox("Select a document", options=[d['url'] for d in docs])
col1, col2 = st.columns(2)


selected_index = next((index for (index, d) in enumerate(docs) if d["url"] == selected_doc), None)

if selected_index is not None:
    doc = docs[selected_index]
    even=True
    for key, value in doc.items():        
        if even==True:
            col=col1
            even=False
        else:
            col=col2
            even=True
        with col:
            with st.expander(key, expanded=True):
                st.text_area(key="ta"+key, value=value, label=key, label_visibility="collapsed", height=200)
        #st.subheader(key)
        #st.text(str(value))