import os
import mlflow
from uuid import uuid4
from typing import Any, List, Dict

from mlflow.pyfunc import ResponsesAgent
from mlflow.entities import SpanType
from mlflow.types.responses import (
    ResponsesAgentRequest,
    ResponsesAgentResponse,
    ResponsesAgentStreamEvent,
)

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from databricks_langchain import ChatDatabricks, VectorSearchRetrieverTool


def build_agent() -> AgentExecutor:
    # Read env for VS index (set this in your logging/serving env)
    vs_index_name = os.environ.get("VS_INDEX_NAME")
    if not vs_index_name:
        raise RuntimeError("VS_INDEX_NAME is not set in environment")

    # LLM endpoint
    llm = ChatDatabricks(
        endpoint=os.environ.get("LLM_ENDPOINT_NAME", "databricks-llama-4-maverick"),
        max_tokens=500,
        temperature=0.5,
    )

    # Tools
    retriever_tool = VectorSearchRetrieverTool(
        name="product_details_tool",
        index_name=vs_index_name,
        description=(
            "Use to find relevant passages about products, materials, features, and examples. "
            "Input should be a natural-language question or keywords."
        ),
    )
    uc_tools: List[Any] = []  # add UC tools here if you use them

    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system",
            """You are a hand-crafted product design expert and your task is to create products that are very good and can be sold online.Write a product title and description that is similar to the following product title and item details. Maximum 300 words.When helpful, call tools (UC functions or vector search) to ground your answers. Cite retrieved facts from search results in your response.Return ONLY the final deliverable. Do not describe your steps or tools. No code blocks, no brackets, no function names.
            Format exactly:
            Title: <one-line title>

            Description: <~250 words>"""
            ),
            MessagesPlaceholder("chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent_chain = create_tool_calling_agent(
        llm=llm, tools=[retriever_tool, *uc_tools], prompt=prompt
    )
    return AgentExecutor(agent=agent_chain, tools=[retriever_tool, *uc_tools], verbose=False)


class LangChainResponsesAgent(ResponsesAgent):
    """
    Wraps your LangChain AgentExecutor in an MLflow ResponsesAgent so it can be
    logged/served via MLflow 3.4+ Models-from-Code.
    """

    def __init__(self):
        # Build and cache the LangChain agent once per model load
        self.agent = build_agent()

    def _last_user_text(self, messages: List[Dict[str, Any]]) -> str:
        user_msgs = [m for m in messages if m.get("role") == "user"]
        if user_msgs:
            return str(user_msgs[-1].get("content", ""))
        return str(messages[-1].get("content", "")) if messages else ""

    def predict(self, request: ResponsesAgentRequest) -> ResponsesAgentResponse:
        # Convert Responses messages -> LangChain payload
        msgs = [m.model_dump() for m in request.input]
        input_text = self._last_user_text(msgs)

        # If you want to thread history, transform msgs -> your prompt's "chat_history"
        chat_history: List[Any] = []  # keep simple; extend if you want multi-turn memory

        result = self.agent.invoke({"input": input_text, "chat_history": chat_history})
        text = result["output"] if isinstance(result, dict) and "output" in result else str(result)

        # Return a single text output item (keeps UI clean, no “plan”/tool narration)
        return ResponsesAgentResponse(
            output=[self.create_text_output_item(text, str(uuid4()))],
            custom_outputs=request.custom_inputs,
        )

    # Optional: stream a single final item (compatible with Responses interface)
    def predict_stream(self, request: ResponsesAgentRequest):
        resp = self.predict(request)
        yield ResponsesAgentStreamEvent(
            type="response.output_item.done",
            item=resp.output[0],
        )


# Register model object for MLflow Models-from-Code
# Build a single instance for local/testing use…
AGENT = LangChainResponsesAgent()
mlflow.models.set_model(AGENT)
