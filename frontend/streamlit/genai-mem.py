from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import boto3

print("started...")
# Load document into memory
#document = """
#The blue whale is the largest animal on Earth. Blue whales can reach lengths of over 100 feet and weigh up to 150 tons. They live in all oceans around the world and often migrate long distances. Blue whales feed almost exclusively on krill. Though they once faced extinction from whaling, conservation efforts have helped blue whale populations slowly recover.
#"""
def load_context():
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='llm-playground-s3', Key='sample-c.txt')
    text = obj['Body'].read().decode('utf-8')
    #context = f"Article: {text}"    
    #full_prompt = f"{context}\n\nHuman: {prompt}"
    return text
document=load_context()
#print(document)
memory=ConversationBufferMemory(memories={"doc": document}) 

# Load Bedrock model and attach memory
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)
llm=Bedrock(client=bedrock_runtime, model_id="anthropic.claude-v2")
llm.store(document)
#llm.set_memory(memory)
conv_chain=ConversationChain(llm=llm, memory=memory)
print("******* MEMORY *************")
print(type(memory))
print("******* END MEMORY *************")

# Ask question based on document
#question="What is the largest animal on Earth?"
#question="What is XTCKURATO_2700?"
question="What is in the document?"
response=conv_chain(question)

print(response)
print("ended...")