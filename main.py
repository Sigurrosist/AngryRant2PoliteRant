import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

# Template for prompt
template = """
    Below is an angry rant message.
    The writer wants to send this message to the recipient.
    The message can be very rough and messy, with curses and bad word choices.
    Turn it into a polite complaint message.

    Your goal is to:
    - Properly address the person's concerns
    - Adjust the tone to the requested level of politeness (0-10)
    - Convert the input into the requested language (English, Spanish, French)
    - Maintain the overall meaning of the input
    - Make it as long as the original input

    Here is the request:
    Message to convert: {angry_rant}
    Level of politeness: {level}
    Language: {language}

    Polite complaint message:
"""

prompt = PromptTemplate(
    input_variables=["angry_rant", "level", "language"],
    template=template,
)

# Setting page config
st.set_page_config(page_title="Polite Rant Generator", page_icon=":sunglasses:")

# Center-aligned header text using HTML and CSS
st.markdown(
    """
    <h2 style="text-align: center;">Angry Rant 😡 to Polite Rant 🙏</h1>
    """,
    unsafe_allow_html=True,
)

# Inserting an image / text using columns
co1, co2 = st.columns(2)
with co1:
    st.image(
        image="./images/angry-1294679.svg",
        width=200,
    )
with co2:
    st.write("### Let's fix this!")
    st.markdown(
        "Turn your Angry Rant 😡 into a Polite Rant 🙏 with just a few clicks. Express your frustrations, select the level of politeness, and let the app craft a more civilized version of your complaints. It's the perfect tool to maintain a positive tone wht\'s turn anger into understanding! 😊✨"
    )

st.write(
    "### This app uses OpenAI API key. You can get one [here](https://beta.openai.com/)."
)


def get_api_key():
    return st.text_input(label="Enter your OpenAI API key here")


openai_api_key = get_api_key()


def get_llm(openai_api_key):
    return OpenAI(
        temperature=0.5,
        openai_api_key=openai_api_key,
    )


def validate_input(openai_api_key, angry_rant):
    validated = True
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key", icon="🙏")
        validated = False
    if not angry_rant.strip():
        st.warning("Please enter a rant before generating", icon="🙏")
        validated = False
    if len(angry_rant.split()) > 400:
        st.warning("Please enter a rant of less than 400 words", icon="🙏")
        validated = False
    return validated


# Setting columns to divide the page
col1, col2 = st.columns(2)
with col1:
    st.write("## Vent your anger")
    angry_rant = st.text_area(label="Enter your angry rant here", height=300)

with col2:
    st.write("## Settings")
    st.write("Select the level of politeness:")
    level = st.slider(label="", min_value=0, max_value=10, value=5, step=1)
    st.write("Select the language:")
    language = st.selectbox(label="", options=["English", "Spanish", "French"])
    st.write()


if st.button(label="Generate!"):
    validated = validate_input(openai_api_key, angry_rant)
    if validated:
        ## Generate polite rant
        llm = get_llm(openai_api_key)
        st.write("## Result")
        st.write("This is the civilized version of your rant:")
        prompt_polite_rant = prompt.format(
            angry_rant=angry_rant, level=level, language=language
        )
        polite_rant = llm(prompt_polite_rant)

        st.write(polite_rant)
