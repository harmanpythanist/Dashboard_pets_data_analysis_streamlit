import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


st.set_page_config(page_title='Dashboard', page_icon=':parrot:', layout="centered", initial_sidebar_state="auto", menu_items=None)


page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://cdn.elegantthemes.com/blog/wp-content/uploads/2013/09/bg-7-full.jpg");
    }}
    background: rgba(0,0,0,0);
    </style>
    """
#st.markdown(page_bg_img, unsafe_allow_html=True)

def display_text(text, text_color="white", background_color=None):
   st.write(f'<span style="color: {text_color}; background-color: {background_color}; padding: 5px;">{text}</span>', unsafe_allow_html=True)

def displaytextsize(text, text_color="white", background_color=None, size=14):
    st.write(f'<span style="color: {text_color}; background-color: {background_color}; padding: 5px; font-size: {size}px;">{text}</span>', unsafe_allow_html=True)

def display_text_shape(text, text_color='white', background_color=None, size=14, border_radius=0):
    st.write(f'<span style="color: {text_color}; background-color: {background_color}; padding: 5px; font-size: {size}px; border-radius: {border_radius}px;">{text}</span>', unsafe_allow_html=True)

def colored_subheader(text, color):
    st.markdown(f'<h3 style="color: {color};">{text}</h3>', unsafe_allow_html=True)

def display_underline(text, underline=False, color="white", size=14, bold=False):
    styles = f'color: {color}; text-decoration: {"underline" if underline else "none"};'
    styles += f'font-size: {size}px; font-weight: {"bold" if bold else "normal"};'
    styled_text = f'<span style="{styles}">{text}</span>'
    st.markdown(styled_text, unsafe_allow_html=True)




df = pd.read_csv('D://project/pet_food_customer_orders/pet_food_customer_orders.csv')

with st.sidebar:
    display_underline('Apply filter', bold=True, size=22, underline=True, color='black')
breed = st.sidebar.multiselect('Pick your breed', df['pet_breed_size'].unique())
if not breed:
    df2 = df.copy()
else:
    df2 = df[df["pet_breed_size"].isin(breed)]

gender = st.sidebar.multiselect('Pick a gender', df2['gender'].unique())
if not gender:
    df3 = df2.copy()
else:
    df3 = df2[df2['gender'].isin(gender)]

pet_st = st.sidebar.multiselect('Pick stage of pet', df3['pet_life_stage_at_order'].unique())
if not pet_st:
    df4 = df3.copy()
else:
    df4 = df3[df3['pet_life_stage_at_order'].isin(pet_st)]

if not gender and not breed and not pet_st:
    filter_df = df
elif not gender and not breed:
    filter_df = df[df['pet_life_stage_at_order'].isin(pet_st)]
elif not gender and not pet_st:
    filter_df = df[df['pet_breed_size'].isin(breed)]
elif breed and gender:
    filter_df = df4[df4['pet_breed_size'].isin(breed) & df4['gender'].isin(gender)]
elif gender and pet_st:
    filter_df = df4[df4['gender'].isin(gender) & df4['pet_life_stage_at_order'].isin(pet_st)]
elif breed and pet_st:
    filter_df = df4[df4['pet_breed_size'].isin(breed) & df4['pet_life_stage_at_order'].isin(pet_st)]

elif breed:
    filter_df = df4[df4['pet_breed_size'].isin(breed)]
elif gender:
    filter_df = df4[df4['gender'].isin(gender)]
elif gender and breed and pet_st:
    filter_df = df4[df4['pet_life_stage_at_order'].isin(pet_st) & df4['gender'].isin(gender) & df4['pet_breed_size'].isin(breed)]
a, b, c = st.columns(3)
with b:
    display_underline('Pet data analysis dashboard', color='black', underline=True, size=15, bold=True)
st.write('---')
col1, col2 = st.columns(2)

dfdf = filter_df.groupby(by= ['pet_has_active_subscription'], as_index=False)['premium_treat_packs'].sum()
filter_df['gender'] = filter_df['gender'].replace({'male': 1, 'female': 0})

with col1:
    display_underline('This pie graph gives concentration of pet with respect to their breed size', size=17, underline=True, color='black')
    figure_size = px.pie(filter_df, values='gender', names='pet_breed_size', hole=0.5)
    figure_size.update_traces(text=filter_df['pet_breed_size'], textposition='outside')
    st.plotly_chart(figure_size, use_container_width=True)



dfd = filter_df.groupby(by = 'pet_life_stage_at_order', as_index=False)['total_wet_food_updates'].sum()
with col2:
    display_underline(
        'This pie graph gives the food tier seperation of overall dataset (how many pets are there who have purchased a particular food tier)',
        size=17, underline=True, color='black')
    figure_size = px.pie(filter_df, values='gender', names='pet_food_tier', hole=0.5)
    figure_size.update_traces(text=filter_df['pet_food_tier'], textposition='outside')
    st.plotly_chart(figure_size, use_container_width=True)


st.write('---')
display_underline('This graph gives number of pets in term of diseases that they are suffering with', size=17, underline=True, color='black')

dfdfa = filter_df.groupby(by= ['pet_health_issue_list'], as_index=False)['gender'].sum()
fi = px.bar(dfdfa, x = 'pet_health_issue_list', y = 'gender', template='seaborn', color='pet_health_issue_list', color_discrete_map={'pet_life_issue_list':'blue'})
fi.update_layout(xaxis_title='Health issues', yaxis_title='total pets')
st.plotly_chart(fi, use_container_width=True)

st.write('---')
display_underline('This pie chart again gives number of pets with respect to the disease they are suffering with and the large blue region shown is the missing data from overall dataset.', size=17, underline=True, color='black')
figure_s = px.pie(filter_df, values = 'gender', names= 'pet_health_issue_list', hole = 0.5)
figure_s.update_traces(text = filter_df['pet_health_issue_list'], textposition='outside')
st.plotly_chart(figure_s, use_container_width=True)
st.write('---')
col3, col4 = st.columns(2)

with col3:
    display_underline('The interrelation between premiun treat packs and subscription status of pets', size=17,
                      underline=True, color='black')
    fig = px.bar(dfdf, x='pet_has_active_subscription', y='premium_treat_packs', template='seaborn')
    fig.update_layout(xaxis_title='Substription status (true=active)', yaxis_title='premium treats pack')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    display_underline('This graph is interrelation of pets life stage and wet food updated', color='black',
                      underline=True, size=17)
    figu = px.bar(dfd, x='pet_life_stage_at_order', y='total_wet_food_updates', template='seaborn',
                  color='pet_life_stage_at_order', color_discrete_map={'pet_life_stage_at_order': 'red'})
    figu.update_layout(xaxis_title='Life stage of pet', yaxis_title='Wet food updates')
    st.plotly_chart(figu, use_container_width=True)









