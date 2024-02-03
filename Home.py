import streamlit as st

st.set_page_config(
    page_title="Home Page",
    page_icon="Images/ai-icon.jpg",
)
st.image("Images/ai.jpg")
st.write("""<h1 style='text-align: center; color: white;'> Welcome 👋</h1> 
         <h3 style='text-align: center; color: white;'> You can chat with the BOT and also preview your Data</h3>""", unsafe_allow_html=True)

st.sidebar.success("Select above one")
