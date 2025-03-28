from langchain_community.document_loaders import TextLoader
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

import os
import logging
import pathlib
import logging

from backend.gutenberg import GutenController

llm = init_chat_model("gemma2-9b-it", model_provider="groq")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

controller = GutenController()
prompt = (
    "You are a conversational bot that has read the book and knows everything about it. Be helpful and informative."
    "Help the user find information about the book if they have questions, otherwise be natural and let the conversation flow."
    "If the user's says their name is Amar - be very loving to them and share that they must be the most beautiful being on earth"
    "You will be provided with the full text of the book and can search for information within it."
    "To help you get started, here are some quick facts about the book:\n\n "
    "{metadata}"
    "Say OK and let's start the conversation."
)


class BookAgent:
    def __init__(self, book_id: int) -> None:
        self.book_id = book_id
        self.book_content_path = controller._get_content_path(
            book_id=book_id, cleaned=True
        )
        documents = self._load_document(self.book_content_path)
        self.vector_storage = self._setup_vector_storage(
            book_id=book_id, documents=documents
        )
        memory = MemorySaver()

        book_metadata = controller.fetch_book_metadata(book_id)
        agent_prompt = prompt.format(metadata=book_metadata.metadata)

        @tool(response_format="content_and_artifact")
        def _retrieve_func(query: str):
            """Retrieve information related to a query."""
            retrieved_docs = self.vector_storage.similarity_search(query)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized, retrieved_docs

        self.agent_executor = create_react_agent(
            llm,
            [_retrieve_func],
            # prompt=agent_prompt,
            checkpointer=memory,
        )
        self.chat(agent_prompt, role="system")
        # self.chat("Hello!")

    @staticmethod
    def _load_document(path: str | pathlib.Path):

        # Load and chunk contents of the book
        loader = TextLoader(path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(docs)
        logging.info(f"Split the document into {len(all_splits)} chunks")
        return all_splits

    @staticmethod
    def _setup_vector_storage(book_id: int, documents: list[Document]):
        directory = f"./cache/{book_id}/chroma"
        if not os.path.exists(directory):
            exists = False
            os.makedirs(directory, exist_ok=True)
        else:
            exists = True

        storage = Chroma(
            collection_name=f"book_{book_id}",
            embedding_function=embeddings,
            persist_directory=directory,
        )
        if not exists:
            storage.add_documents(documents)
        return storage

    def chat(self, input_message: str, role="user") -> str:
        config = RunnableConfig(configurable={"thread_id": "def234"})
        for event in self.agent_executor.stream(
            {"messages": [{"role": role, "content": input_message}]},
            stream_mode="values",
            config=config,
        ):
            pass
        return event["messages"][-1].content


class AgentsManager:
    def __init__(self) -> None:
        self.agents: dict[int, BookAgent] = {}

    def remove_agent(self, book_id: int):
        try:
            del self.agents[book_id]
        except KeyError:
            logging.warning(f"Agent for book {book_id} not found in cache")

    # Cache and reuse agents - one per book
    def get_agent(self, book_id: int, reset=False) -> BookAgent:
        if self.agents.get(book_id) and not reset:
            logging.info(f"Reusing agent for book {book_id}")
            return self.agents[book_id]
        else:
            self.remove_agent(book_id)
            logging.info(f"Creating new agent for book {book_id}")
            self.agents[book_id] = BookAgent(book_id)
            return self.agents[book_id]
