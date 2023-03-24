import streamlit as st
import pandas as pd
import requests
import altair as alt
from bokeh.plotting import figure, show
import json

st.set_page_config(page_title="Volume Kalman", page_icon="📊")
st.markdown("# Volume Kalman")
st.sidebar.header("Volume Kalman")

def transform(dataframe):
    print(dataframe)
    volumeData = dataframe['vol']
    response = requests.get("http://127.0.0.1:9938/kalman", params={
        "internal": volumeData})
    if response.status_code == 200:
        # newData = json.loads(response.content)
        newData = response.json()
        vol = newData["volume"]
        volkal = newData["kalmanised"]
        date = dataframe["date"]
        data = pd.DataFrame({'Date': date,
                             'Volume': vol,
                             'Kalmanised Volume': volkal})
        # data.set_index('Date', inplace= True)
        print(data.head())
        # data = date.to_frame().merge(vol).merge(volkal)
        print(data.columns)
        # pd.to_datetime(data['Date'])
        # groupLabels = ['Volume', 'Kalmanised Volume']
        # colors = ['blue','orange']
        # fig = ff.create_distplot(group, groupLabels, curve_type='kde', colors=colors)
        # fig.update_layout(title_text='Volume Distribution')
        # st.plotly_chart(fig, use_container_width=True)
        # st.line_chart(data, x = data['Date'], y=data['Volume'], use_container_width=1)
        data.set_index('Date', inplace=True)
        st.line_chart(data)
        st.dataframe(data, use_container_width=1)
        # st.line_chart(data.rename(columns={'Date': 'index'}).set_index('index'))
        # chart = alt.Chart(data.rename(columns={'Date': 'index'}).set_index('index')).mark_line(point=True).encode(
        #     x='index',
        #     y='Volume',
        #     color="Volume"
        # )
        # st.altair_chart(chart)
        # p = figure(title = "VOLKAL", x_axis_label ='Date', y_axis_label ='Volume')
        # p.line(data['Date'], data['Volume'], legend_label="Volume", color="red")
        # p.line(data['Date'], data['Volume Kalman'], legend_label="Kalmanised Volume", color="black")
        # data.plot(x='Date', y = ['Volume','Volume Kalman'], kind ='line')
        # show(p)
        # st.bokeh_chart(p)
        # fig, ax = plt.subplots()
        # ax.plot(x='Date', y=['Volume','Volume Kalman'])
        # st.pyplot(data)

        # st.dataframe(, use_container_width=1)

    else:
        return "Internal Server Error! Contact tech@cogitaas.com"



uploaded_file = st.file_uploader("Choose a file", type=['csv'])
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.dataframe(dataframe, use_container_width=1)
    rows = len(dataframe.axes[0])
    columns = len(dataframe.axes[1])
    st.write("Rows: " +str(rows))
    st.write("Columns: " + str(columns))
    transform(dataframe)

