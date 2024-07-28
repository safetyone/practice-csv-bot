import streamlit as st
from model import csv_tool
import pandas as pd
import json

def create_chart(input_dict, chart_type):
    df = pd.DataFrame(data=input_dict["data"], columns=input_dict["columns"])
    if chart_type == "bar":
        st.bar_chart(df)
    elif chart_type == "line":
        st.line_chart(df)
    elif chart_type == "scatter":
        st.scatter_chart(df)
    else:
        st.error("请输入正确的指令。模型仅支持条形图、折线图、散点图。")



st.header("🔍csv辅助小助手")

with st.sidebar:
    api = st.text_input("请输入您的api密钥：", type="password", help="本模型使用Chatgpt，请输入GPT-4密钥")
    st.markdown("[获取api链接](https://platform.openai.com/account/api-keys)")

csv_file = st.file_uploader("请上传您的CSV文件", type="csv")
if csv_file:
    df = pd.read_csv(csv_file)
    with st.expander("原始数据"):
        st.dataframe(df)

user_input = st.text_area("请输入您的指令，包括相关问题询问、图表生成等(本程序仅支持条形图、散点图和折线图)", disabled=not csv_file)
button = st.button("点击生成")
if button and user_input:
    if not api:
        st.error("请输入您的api密钥")
        st.stop()
    else:
        with st.spinner("Ai正在思考..."):
            result = csv_tool(api, df, user_input)  # result是个字典

        if "answer" in result:
            st.write(result["answer"])
        if "table" in result:
            st.table(pd.DataFrame(data=result["table"]["data"], columns=result["table"]["columns"]))
        if "bar" in result:
            create_chart(input_dict=result["bar"], chart_type="bar")
        if "line" in result:
            create_chart(input_dict=result["line"], chart_type="line")
        if "scatter" in result:
            create_chart(input_dict=result["scatter"], chart_type="scatter")
        else:
            print("又啥也没解析出来，gpt-3.5就没办法")

# 格式是，

#  {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
#  {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
#  {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

# 所以传入create_chart函数的实际是 {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}




