import streamlit as st
import task1
import task2
import task3
import task4
import task5
import task6
import task7

st.sidebar.title("GOOGLE PLAY STORE DATA ANALYSIS")
option = st.sidebar.selectbox(
    "Select Task",
    ("5-Star Review Keywords – Health & Fitness", "Free vs Paid Apps: Installs & Revenue (Top Categories)", "Top 10 Categories: Ratings vs Review Count", "Global Installs by App Category (Filtered View)", "Games Category: Size vs Rating vs Installs", "Install Growth Trends by Category (Teen Content)", "Rating Distribution by Category (Filtered Insights)"),
)
if option == "5-Star Review Keywords – Health & Fitness":
    st.title("5-Star Review Keywords – Health & Fitness")
   # st.write("This task analyzes the most common keywords in 5-star reviews for Health & Fitness apps.")
    task1.main()
elif option == "Free vs Paid Apps: Installs & Revenue (Top Categories)":
    st.title("Free vs Paid Apps: Installs & Revenue (Top Categories)")
   # st.write("This task compares the installs and revenue of free and paid apps in the top categories.")
    task2.main()
elif option == "Top 10 Categories: Ratings vs Review Count":    
    st.title("Top 10 Categories: Ratings vs Review Count")
  #  st.write("This task analyzes the ratings and review count of the top 10 app categories.")
    task3.main()
elif option == "Global Installs by App Category (Filtered View)":
    st.title("Global Installs by App Category (Filtered View)")
   # st.write("This task provides a filtered view of global installs by app category.")
    task4.main()
elif option == "Games Category: Size vs Rating vs Installs":
    st.title("Games Category: Size vs Rating vs Installs")
  #  st.write("This task analyzes the relationship between app size, rating, and installs in the Games category.")
    task5.main()
elif option == "Install Growth Trends by Category (Teen Content)":
    st.title("Install Growth Trends by Category (Teen Content)")
   # st.write("This task analyzes the install growth trends by category for apps with Teen content.")
    task6.main()
elif option == "Rating Distribution by Category (Filtered Insights)":
    st.title("Rating Distribution by Category (Filtered Insights)")
   # st.write("This task provides filtered insights into the rating distribution by app category.")
    task7.main()

