import streamlit as st;
st.title("MYbot")
s=st.text_input("enter message")
sub=st.button("submit")
if sub:
    st.markdown(s)
