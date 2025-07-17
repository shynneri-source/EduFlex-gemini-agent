
from agent.agent import Agent


agent = Agent(gemini_api_key=None)
agent.get_graph_visualization("./eduflex_workflow.png")



with open('mock_data.txt', 'r', encoding='utf-8') as file:
    data_text = file.read()

from dotenv import load_dotenv
import os
load_dotenv()

result = agent.graph.invoke({
    "messages": data_text,
})

print(result["user_response"])