import streamlit as st
import requests

import pickle
import pandas as pd
from streamlit_lottie import st_lottie

restros_dict = pickle.load(open('restros.pkl','rb'))
restros = pd.DataFrame(restros_dict)
df_percent = pd.DataFrame(restros_dict)
df_percent.set_index('name', inplace=True)
indices = pd.Series(df_percent.index)
similarity = pickle.load(open('similarity.pkl','rb'))
show_df = False

# --------- Functions ---------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def recommend(name, cosine_similarities = similarity):
    
    # Create a list to put top restaurants
    recommend_restaurant = []
    
    # Find the index of the hotel entered
    idx = indices[indices == name].index[0]
    
    # Find the restaurants with a similar cosine-sim value and order them from bigges number
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
    
    # Extract top 30 restaurant indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)
    
    # Names of the top 30 restaurants
    for each in top30_indexes:
        recommend_restaurant.append(list(df_percent.index)[each])
    
    # Creating the new data set to show similar restaurants
    df_new = pd.DataFrame(columns=['cuisines', 'Mean Rating', 'cost'])
    
    # Create the top 30 similar restaurants with some of their columns
    for each in recommend_restaurant:
        df_new = df_new.append(pd.DataFrame(df_percent[['cuisines','Mean Rating', 'cost']][df_percent.index == each].sample()))
    
    # Drop the same named restaurants and sort only the top 10 by the highest rating
    df_new = df_new.drop_duplicates(subset=['cuisines','Mean Rating', 'cost'], keep=False)
    df_new = df_new.sort_values(by='Mean Rating', ascending=False).head(10)
    
    print('TOP %s RESTAURANTS LIKE %s WITH SIMILAR REVIEWS: ' % (str(len(df_new)), name))
    #df_new = df_new.style.set_properties(**{'text-align': 'left'})
    
    return df_new



# --------- Assets ---------------------


# ---------Title and Header --------------
st.set_page_config(page_title="RPS One", layout = "wide")

with st.container():
    st.title("Restaurant Prediction System")
    st.header("Create a customized list of restaurants curated for you!")
    #st.write("Providing the best in business Restaurant recommandations in Bangalore")


# ---- Paragraph ----
with st.container():
  left_column, right_column = st.columns(2)
  with left_column:
    selected_movie_name = st.selectbox(
      "Type or select a movie from the dropdown",
      restros['name'].values
    )
  if st.button('Show Recommendation'):
    answer = recommend(selected_movie_name)
    show_df = True
    st.dataframe(answer)

st.header("How it works")
    
