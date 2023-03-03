import streamlit as st
import openai
from datetime import datetime
from streamlit.components.v1 import html
import pandas as pd
import csv
import pinecone

st.set_page_config(page_title="Rocking Chair")

pinecone.init(api_key='ad0771fd-9da6-4665-89de-feb647b17770', environment='us-east1-gcp')
index = pinecone.Index('agingparents') 


html_temp = """
                <div style="background-color:rgba(255, 255, 255, 0.16);padding:1px">
                
                </div>
                """

button = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="thehunter" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
"""


with st.sidebar:
    st.markdown("""
    # About 
    Rocking Chair is a Q&A service that suggest in tips, product recommendations, and services to adults who have aging parents. As our loved ones get older, it can be challenging to navigate the complex landscape of aging-related issues. That's where Rocking Chair comes in - we're here to help you find the answers you need to make informed decisions about your loved one's care and wellbeing. 


  """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # Example Prompts
    "My 78 year old mother has to undergo chemo, starting next week. 
    She seems to expect one of us to be there with her for every treatment and help care for her afterwards. 
    She lives with my 82 year old father who is capable of driving her to the appointments and shopping for them.
    Do you accompany your elderly parents to chemo? Did you hire in home help for them? How do you keep from resenting them for the care they need?"

    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work
    Using advanced scraping and analytics tools, we've combed through countless online forums, social media platforms, and other resources to identify the most pressing issues and concerns that individuals face when caring for aging parents. We've analyzed this data to develop a comprehensive database of insights, tips, and recommendations that can help you provide the best possible care for your loved ones.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    Made with ❤️ by [Lusenii Kromah](linkedin.com/in/luseniikromah/)
    """,
    unsafe_allow_html=True,
    )


input_text = None
if 'output' not in st.session_state:
    st.session_state['output'] = 0

if st.session_state['output'] <=2:
    st.markdown("""
    # Rocking Chair
    """)
    input_text = st.text_input("Community driven support for aging parent care needs - where compassion meets expertise. ", disabled=False, placeholder="What's on your mind? (Health, Finance, Wills, Venting, etc..)")
    st.session_state['output'] = st.session_state['output'] + 1


html(button, height=70, width=220)
st.markdown(
    """
    <style>
        iframe[width="220"] {
            position: fixed;
            bottom: 60px;
            right: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
if input_text:
     # build out prompt
    prompt_start = (
        "You are a Q&A service where people come to you for advice, product recommendations, service recommendations, and to just vent about their aging parents. Provide links to resources when necessary, but make sure to sound human and empathetic. Answer the question based on the context below.\n\n" +
        "Context:\n"
    )
    if prompt_start:
        # openai.api_key =  st.secrets["OPEN_AI_KEY"]
        openai.api_key =  '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'
        MODEL = 'text-embedding-ada-002'
        res = openai.Embedding.create(engine=MODEL, input=["My mother is getting dementia what should I do?"])

        # returned query vectort from Pinecon
        query_vector = res['data'][0]['embedding']
        res = index.query(query_vector, top_k=3, include_metadata=True)

        context = [
            x['metadata']['Top Comments'] for x in res['matches']
        ]

        limit = 5000

        prompt_end = (
            f"\n\nQuestion: {input_text}\nAnswer:"
        )

        for i in range(1, len(context)):
            if len("\n\n---\n\n".join(context[:i])) >= limit:
                input_text = (
                    prompt_start +
                    "\n\n---\n\n".join(context[:i-1]) +
                    prompt_end
                )
            elif i == len(context)-1:
                input_text = (
                    prompt_start +
                    "\n\n---\n\n".join(context) +
                    prompt_end
                )


        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=input_text, 
            temperature=0.1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        brainstorming_output = response['choices'][0]['text']
        
        st.info(brainstorming_output)
       
        st.write("[Need more help?](https://2lemvxpy32s.typeform.com/to/PSNhqoo1)")


        
        

        
