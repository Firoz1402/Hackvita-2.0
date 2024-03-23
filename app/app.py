import streamlit as st
import product_page
def home_page():
    st.title("SnapSpot")
    st.write("Tired of scrubbing through endless video to find that specific scene?")
    st.write("Our innovative video search tool takes the hassle out of finding what you're looking for..")
    

def about_page():
    st.title("About Us")
    st.write("Meet our team:")


    st.markdown("---")
    st.header("Firoz Anjum Chowdhury")
    st.image("assets/firoz.jpeg", width=150)
    st.write("The Data Scientist & MLOPs engineer with some expertise in web development.")

    st.markdown("---")
    st.header("Hillol Pratim Kalita")
    st.image("assets/hillol.jpeg", width=150)
    st.write("The data scientist with a passion for machine learning.")
 
    st.markdown("---")
    st.header("Koyal Borbora")
    st.image("assets/koyal.png", width=150)
    st.write("The UX/UI designer with a focus on user-centric design.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["HOME", "Product", "About Us"])

    if page == "HOME":
        home_page()
    elif page == "Product":
        product_page.main()
    elif page == "About Us":
        about_page()

if __name__ == "__main__":
    main()
