from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage 


from dotenv import load_dotenv
import os

load_dotenv()

from agent.config import Configuration
from agent.states import overall_state
from agent.prompts import (
    Analyzer_prompt,
    Lecturer_prompt,
    Practitioner_prompt,
    assembler_prompt,
)
from agent.schema import analyzer_response

class Agent:
    def __init__(self, gemini_api_key):
        self._config = Configuration()
        self._gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self._builder = StateGraph(overall_state)
        self._builder.add_node("analyze", self.analyze)
        self._builder.add_node("lecture", self.lecture)
        self._builder.add_node("practice", self.practice)
        self._builder.add_node("user_response", self.user_response)
        self._builder.add_edge(START, "analyze")
        self._builder.add_edge("analyze", "lecture")
        self._builder.add_edge("analyze", "practice")
        self._builder.add_edge("lecture", "user_response")
        self._builder.add_edge("practice", "user_response")
        self._builder.add_edge("user_response", END)
        self.graph = self._builder.compile(name="eduflex")

    def analyze(self,state: overall_state) -> overall_state:
        llm = ChatOpenAI(
            model=self._config.model,
            base_url="https://generativelanguage.googleapis.com/v1beta/",
            api_key=os.getenv("GEMINI_API_KEY"),
            default_headers={
                "X-goog-api-key": os.getenv("GEMINI_API_KEY")
            }
        )
        structured_llm = llm.with_structured_output(analyzer_response)
        message = HumanMessage(
            content=f"{Analyzer_prompt}\n\nDữ liệu học tập:\n{state['messages']}"
        )
        response: analyzer_response = structured_llm.invoke([message])
        state['analytics'] = response.analysis.strip()
        state['plan'] = response.plan.strip()
        return state
    def lecture(self, state: overall_state) -> overall_state:
        llm = ChatOpenAI(
            model=self._config.model,
            base_url="https://generativelanguage.googleapis.com/v1beta/",
            api_key=os.getenv("GEMINI_API_KEY"),
            default_headers={
                "X-goog-api-key": os.getenv("GEMINI_API_KEY")
            }
        )
        message = HumanMessage(
            content=f"{Lecturer_prompt}\n\nBáo cáo phân tích:\n{state['analytics']}\n\nPLAN đồng bộ:\n{state['plan']}"
        )

        response = llm.invoke([message]).content
        return {"lesson": response}
    def practice(self, state: overall_state) -> overall_state:
        llm = ChatOpenAI(
            model=self._config.model,
            base_url="https://generativelanguage.googleapis.com/v1beta/",
            api_key=os.getenv("GEMINI_API_KEY"),
            default_headers={
                "X-goog-api-key": os.getenv("GEMINI_API_KEY")
            }
        )
        message = HumanMessage(
            content=f"{Practitioner_prompt}\n\nBáo cáo phân tích:\n{state['analytics']}\n\nPLAN đồng bộ:\n{state['plan']}"
        )
        response = llm.invoke([message]).content
        return {"practice": response}
    def user_response(self, state: overall_state) -> overall_state:
        llm = ChatOpenAI(
            model=self._config.model,
            base_url="https://generativelanguage.googleapis.com/v1beta/",
            api_key=os.getenv("GEMINI_API_KEY"),
            default_headers={
                "X-goog-api-key": os.getenv("GEMINI_API_KEY")
            }
        )
        message = HumanMessage(
            content=f"{assembler_prompt}\n\nBáo cáo phân tích:\n{state['analytics']}\n\nBài giảng:\n{state['lesson']}\n\nBài tập thực hành:\n{state['practice']}"
        )
        response = llm.invoke([message]).content
        state['user_response'] = response
        return state
    def get_graph_visualization(self, image_path: str = "./workflow.png") -> None:
        """Generate an .png image of the current graph workflow

        Args:
            image_path (str, optional): The path to save the image. Defaults to "./workflow.png".
        """
        try:
            png_bytes = self.graph.get_graph().draw_mermaid_png()

            # Display the image
            display(Image(png_bytes))

            # Save the image to a file
            with open(image_path, "wb") as f:
                f.write(png_bytes)

        except Exception as e:
            print(f"An error occurred: {e}")