import streamlit as st
import openai
from datetime import datetime
from streamlit.components.v1 import html
import pandas as pd
import csv

st.set_page_config(page_title="Rocking Chair")


html_temp = """
                <div style="background-color:{};padding:1px">
                
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
    Made by [Lusenii Kromah](linkedin.com/in/luseniikromah/)
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
else:
    # input_text = st.text_input("Brainstorm ideas for", disabled=True)
    st.info("Thank you! Refresh for more brainstorming💡")
    st.markdown('''
    <a target="_blank" style="color: black" href="https://twitter.com/intent/tweet?text=I%20just%20used%20the%20Rocking%20Chair%20helper%20tool%20by%20@boutique_lue!%0A%0Ahttps://urbanintell-rocking-chair-app-m5l2qq.streamlit.app/
    ">
        <button class="btn">
            Tweet about this!
        </button>
    </a>
    <style>
    .btn{
        display: inline-flex;
        -moz-box-align: center;
        align-items: center;
        -moz-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        margin: 0px;
        line-height: 1.6;
        color: #fff;
        background-color: #00acee;
        width: auto;
        user-select: none;
        border: 1px solid #00acee;
        }
    .btn:hover{
        color: #00acee;
        background-color: #fff;
    }
    </style>
    ''',
    unsafe_allow_html=True
    )

hide="""
<style>
footer{
	visibility: hidden;
    position: relative;
}
.viewerBadge_container__1QSob{
    visibility: hidden;
}
#MainMenu{
	visibility: hidden;
}
<style>
"""
st.markdown(hide, unsafe_allow_html=True)

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
    prompt = "You are a Q&A service where people come to you for advice, product recommendations, service recommendations, and to just vent about their aging parents. Provide links to resources when necessary, but make sure to sound empathetic. The prompt must actually make sense and be longer than 4 words, if it does not let the user know there was an issue with their request. This persons prompt is the following: "+str(input_text)
    if prompt:
        openai.api_key =  st.secrets["OPEN_AI_KEY"]
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150)
        brainstorming_output = response['choices'][0]['text']
        
        st.info(brainstorming_output)
       
        st.write("[Try Premium](https://2lemvxpy32s.typeform.com/to/PSNhqoo1)")

        fields = [input_text, brainstorming_output, str(today)]
        # read local csv file
        r = pd.read_csv('./data/prompts.csv')
        if len(fields)!=0:
            with open('./data/prompts.csv', 'a', encoding='utf-8', newline='') as f:
                # write to csv file (append mode)
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerow(fields)

        
        

        
