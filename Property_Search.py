import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.markdown('<p style="font-family:HGP創英角ﾎﾟｯﾌﾟ体; color:Salmon; font-size: 40px;">条件で絞り込む</p>',
            unsafe_allow_html=True)

# 選択された築年数でデータフレームをフィルタリング
df1 = pd.read_csv("muroran_data.csv")
number1 = st.multiselect('希望のエリアを選択してください', df1['エリア'].unique())
filtered_df1 = df1[df1['エリア'].isin(number1)]

number2 = st.multiselect('希望の築年数を選択してください', filtered_df1['築年数'].unique())
filtered_df2 = filtered_df1[filtered_df1['築年数'].isin(number2)]

number3 = st.multiselect('希望の階数を選択してください', filtered_df2['階数'].unique())
filtered_df3 = filtered_df2[filtered_df2['階数'].isin(number3)]

# 【追加】リンクに飛べるように表示
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter, NumberFormatter

cds = ColumnDataSource(filtered_df3)

columns = []
for c in filtered_df3.columns:
    if (c != "URL"):
        tc = TableColumn(field=c,title=c)
    else:
        tc = TableColumn(field=c,title=c, formatter=HTMLTemplateFormatter(template=f'<a href="<%= {c} %>"target="_blank"><%= value %></a>'))
    columns.append(tc)

p = DataTable(source=cds, columns=columns,css_classes=["my_table"])
st.bokeh_chart(p)

# 室蘭市の地図を表示
img = Image.open('muroran_map.png')
st.image(img, caption='', width=900)