from typing import List

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langserve import add_routes
from langchain.chains import LLMMathChain
from langchain.llms import OpenAI
from langchain.schema import StrOutputParser

# 1. Chain definition
llm_math = LLMMathChain.from_llm(OpenAI(), verbose=True)

template_1 = """
You are given five cards from a standard deck of 52 cards. 
Please write a math expression that calculates the probability of getting that hand.
I don't want any explanation. Just the math expression.
"""
human_template_1 = "{text}"

template_2 = """
You are given a probability: {answer}
Your task is to write a paragraph that helps the reader understand how big this probability is in a real-world context.
"""


prompt_1 = ChatPromptTemplate.from_messages([
    ("system", template_1),
    ("human", human_template_1),
])
prompt_2 = ChatPromptTemplate.from_messages([
    ("system", template_2),
])

prompt = ChatPromptTemplate.from_messages([
    ("human", '{text}')
])
# | CommaSeparatedListOutputParser()
chain = (
    prompt | ChatOpenAI()
    # (prompt_1 | ChatOpenAI() | StrOutputParser())
    # | llm_math
    # | prompt_2
    # | ChatOpenAI()
    # | StrOutputParser()
)


# 2. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# 3. Adding chain route
add_routes(
    app,
    chain,
    path="/test",
)
