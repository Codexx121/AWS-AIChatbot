#Calling all imports
from langchain.chains import LLMChain
from langchain.llms import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import os
import streamlit as stl


#Calling the AWS user (pre-configured)
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")



#Intiating the client by specifing the aws service and region
bed_client= boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

#Model to used
modelID = "anthropic.claude-v2"


#Bridging Langchain with the bedrock client
llm = Bedrock(
    model_id=modelID,
    client=bed_client,
    model_kwargs={"max_tokens_to_sample":200,"temperature":0.5} #Tokens set for 100 (to minimize costs) and temperature to maintain reasonable predictablity
)


#Defining your chatbot
def Chatbot(language,freeform_text,tone,complexity):
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text","tone","complexity"],
        template="You are a chatbot. Respond directly in {language}.Answer in a {tone} tone. Make the answer {complexity}. \n\n{freeform_text}"
    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    response = bedrock_chain.invoke({'language': language,'tone': tone,'freeform_text': freeform_text,'complexity':complexity})
    return response






## UI Using Streamlit 
stl.title("AI Man Chatbot")

# Input form
stl.sidebar.header("Chat Options")
language = stl.sidebar.selectbox("Choose language:", ["English", "Spanish","French"])
tone = stl.sidebar.selectbox("Choose a tone:", ["Formal", "Informal", "Neutral"])
tone = stl.sidebar.selectbox("Choose the Complexity:", ["Like I'm 5 years old", "in Simple English", " A Bit Complex","Very Detailed"])


freeform_text = stl.text_area(
    "Type your question here:", 
    placeholder="Ask me anything...", 
    max_chars=100
)


# Chatbot response
if stl.button("Ask!"):
    if freeform_text:
        response = Chatbot(language, tone, freeform_text)
        stl.markdown("### Chatbot Response:")
        stl.write(response['text'])
    else:
        stl.error("Please type a question before submitting.")
