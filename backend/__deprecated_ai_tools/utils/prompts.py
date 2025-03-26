from langchain_core.prompts import ChatPromptTemplate

map_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You will be provided with excerpts from a book retrieved legally via Project Gutenberg. "
            "Ignore anything related to Project Gutenberg in your answer. Only include information relevant "
            "to the text of the book itself. Write a summary of the following that does not leave out key "
            "details like theme, plot, key characters, etcetera:\n\n{context}",
        )
    ]
)


reduce_prompt = ChatPromptTemplate(
    [
        (
            "human",
            """
        The following is a set of summaries:
        {docs}
        Take these and consistently combine them without redundancy. They can be as long as 2000 tokens.
        Ommit any information related to Project Gutenberg. Only include information relevant to the text of the book itself.
        """,
        )
    ]
)


book_inquiry_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You will be provided with a summary of a book and some book metadata. 
            Your task is to answer any questions the user asks using only information present in the book's content and metadata. 
            Use information only from in the content you will be provided. 
            Here is the metadata:
            
            {metadata}
            
            Here is the summary:
            
            {summary} 
            
            """,
        ),
        (
            "human",
            "{human_input}",
        ),
    ]
)
