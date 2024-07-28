import json

from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


Prompt_template =  """
你是一位数据分析助手，你的回应内容取决于用户的请求内容。

1. 对于文字回答的问题，按照这样的格式回答：
   {"answer": "<你的答案写在这里>"}
例如：
   {"answer": "订单量最高的产品ID是'MNWC3-067'"}

2. 如果用户需要一个表格，按照这样的格式回答：
   {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

3. 如果用户的请求适合返回条形图，按照这样的格式回答：
   {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

4. 如果用户的请求适合返回折线图，按照这样的格式回答：
   {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

5. 如果用户的请求适合返回散点图，按照这样的格式回答：
   {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
注意：我们只支持三种类型的图表："bar", "line" 和 "scatter"。


请将所有输出作为JSON字符串返回。请注意要将"columns"列表和数据列表中的所有字符串都用双引号包围。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

你要处理的用户请求如下： 
"""


def csv_tool(api, df, user_input):
    # 1、定义模型大脑
    model = ChatOpenAI(model="gpt-4", openai_api_key=api, temperature=0.5)
    # 2、开箱即用的agent
    agent = create_pandas_dataframe_agent(llm=model, df=df, agent_executor_kwargs={"handle_parsing_errors": True},
                                          verbose=True)
    # 3、提示词
    prompt = Prompt_template + user_input
    # 4、接受结果
    result = agent.invoke({"input": prompt})
    # print(result)  # {'input': '\n你是一位数据分析助手，。。。绘制出职业的条形图', 'output': 'Agent stopped due to iteration limit or time limit.'}
    # <class 'dict'>
    # print(type(result))  # <class 'dict'>
    # print(result["output"])  # Agent stopped due to iteration limit or time limit.
    # print(type(result["output"]))  # <class 'str'>
    result_dict = json.loads(result["output"])   # 期望中它解析出来是prompt_template的样子（但是output的值会把字典用引号包裹，所以要json解析），但是估计gpt3.5不行
    return result_dict


if __name__ == "__main__":
    import os
    import pandas as pd
    df = pd.read_csv("house_price.csv")
    run = csv_tool(os.getenv("OPENAI_API_KEY"), df, "绘制出职业的条形图")
    print(run)