import streamlit as st
import pandas as pd
import os

st.title("Hotel d'Or")
st.write("Welcome to our humble abode")

st.sidebar.title("Options")
st.sidebar.write("Something")

tab1, tab2 = st.tabs(["Agences", "Chambers"])

with tab1:
    st.title("Available agencies")
    st.image("static/img.jpeg")
    col1 ,col2, col3= st.columns(3)

    with col1:
        c1 = st.button("Column1")
        st.write("this is col1") if c1 else st.write("Kys")

    with col2:
        st.header("Column2")
        st.write("this col2")

    with col3:
        st.header("col3")
        st.write("this is col3")
    
with tab2:
    st.title("Available rooms")
    with st.expander("Types"):
        type_chosen = st.radio("", ["Simple", "Double"])
    match type_chosen:
        case "Simple":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("static/img.jpeg")
                st.write("A chambre with a jacozzi")
        case "Double":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("static/img.jpeg")
                st.write("A  simple double chambre")
        



      
      