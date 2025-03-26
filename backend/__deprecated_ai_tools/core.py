"""This entire module is based on the following article:
https://python.langchain.com/docs/tutorials/summarization/#orchestration-via-langgraph
"""

from langchain.chat_models import init_chat_model
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents.reduce import acollapse_docs, split_list_of_docs
from langchain_core.documents import Document
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send
from typing import List, Literal
import asyncio
from typing import TypedDict
from langchain_groq import ChatGroq
from .schemas import OverallState, SummaryState
from .utils.prompts import map_prompt, reduce_prompt, book_inquiry_prompt
from .utils.decorators import durable_ainvoke_decorator
import logging
import enum


logger = logging.getLogger(__name__)


class AICore:
    def __init__(self, model):
        self.llm: ChatGroq = init_chat_model(
            model,
            model_provider="groq",
            configurable_fields=["ainvoke"],
        )  # type: ignore

        # Wraps the llm.invoke function to wait on RateLimitErrors, working around
        # groq late limiting (free tier)
        self.llm.ainvoke = durable_ainvoke_decorator(self.llm.ainvoke)

    def split_documents(self, docs: List[Document], chunk_size: int = 3000):
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=0
        )
        return text_splitter.split_documents(docs)

    def length_function(self, documents: List[Document]) -> int:
        """Get number of tokens for input contents."""

        return sum(self.llm.get_num_tokens(doc.page_content) for doc in documents)


class AISummarizer(AICore):

    async def _reduce(self, input: dict) -> str:
        prompt = reduce_prompt.invoke(input)
        response = await self.llm.ainvoke(prompt)
        return response.content

    async def _generate_summary(self, state: SummaryState):
        prompt = map_prompt.invoke(state["content"])
        response = await self.llm.ainvoke(prompt)
        return {"summaries": [response.content]}

    @staticmethod
    def map_summaries(state: OverallState):
        return [
            Send("generate_summary", {"content": content})
            for content in state["contents"]
        ]

    @staticmethod
    def collect_summaries(state: OverallState):
        return {
            "collapsed_summaries": [Document(summary) for summary in state["summaries"]]
        }

    async def _generate_final_summary(self, state: OverallState):
        response = await self._reduce(state["collapsed_summaries"])
        return {"final_summary": response}

    async def generate_summary(
        self, docs: List[Document], chunk_size: int = 3000
    ) -> str:

        def should_collapse(
            state: OverallState,
        ) -> Literal["collapse_summaries", "generate_final_summary"]:
            """This represents a conditional edge in the graph that determines
            if we should collapse the summaries or not"""
            num_tokens = self.length_function(state["collapsed_summaries"])
            return (
                "collapse_summaries"
                if num_tokens > chunk_size
                else "generate_final_summary"
            )

        async def collapse_summaries(state: OverallState):
            doc_lists = split_list_of_docs(
                state["collapsed_summaries"], self.length_function, chunk_size
            )
            results = []
            for doc_list in doc_lists:
                results.append(await acollapse_docs(doc_list, self._reduce))
            return {"collapsed_summaries": results}

        # Split documents into chunks
        split_docs = self.split_documents(docs, chunk_size)
        logger.info(
            f"Split documents into {len(split_docs)} chunks of size {chunk_size}"
        )

        # Construct the graph
        # Nodes:
        graph = StateGraph(OverallState)
        graph.add_node("generate_summary", self._generate_summary)
        graph.add_node("collect_summaries", self.collect_summaries)
        graph.add_node("collapse_summaries", collapse_summaries)
        graph.add_node("generate_final_summary", self._generate_final_summary)

        # Edges:
        graph.add_conditional_edges(START, self.map_summaries, ["generate_summary"])
        graph.add_edge("generate_summary", "collect_summaries")
        graph.add_conditional_edges("collect_summaries", should_collapse)
        graph.add_conditional_edges("collapse_summaries", should_collapse)
        graph.add_edge("generate_final_summary", END)

        # Compile and execute the graph
        app = graph.compile()

        i = 0
        async for step in app.astream(
            {"contents": [doc.page_content for doc in split_docs]},
            {"recursion_limit": 10},
        ):
            logger.info(f"Step ({i}): {step.keys()}")
            i += 1

        return step["generate_final_summary"]["final_summary"]


class InquiryFormat(TypedDict):
    metadata: dict
    summary: str
    human_input: str


class AIChatAgent(AICore):

    async def chat(self, input: InquiryFormat) -> str:
        book_inquiry_prompt.invoke(input)
        response = await self.llm.ainvoke(input)
        return response.content
