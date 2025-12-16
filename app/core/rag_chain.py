"""RAG 체인 설정 및 관리."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import PGVector

from app.config import settings


def create_rag_chain(vectorstore: PGVector):
    """RAG (Retrieval-Augmented Generation) 체인 생성."""
    # 프롬프트 템플릿
    prompt = ChatPromptTemplate.from_template(
        """
다음 컨텍스트를 바탕으로 질문에 답해주세요:

컨텍스트: {context}

질문: {question}

답변:
"""
    )

    # 검색기 설정
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # LLM 설정 및 RAG 체인 구성
    if settings.openai_api_key:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        # 실제 RAG 체인 구성
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
    else:
        # 더미 RAG 함수 (OpenAI API 키가 없을 때)
        def dummy_rag_function(question: str) -> str:
            """OpenAI API 키가 없을 때 사용하는 더미 RAG 함수."""
            docs = retriever.invoke(question)
            context = "\n".join([f"- {doc.page_content}" for doc in docs])

            return f"""🔍 검색된 관련 문서들:
{context}

💡 더미 응답: 위의 문서들이 '{question}' 질문과 관련된 내용입니다.
실제 AI 응답을 받으려면 OpenAI API 키를 설정해주세요.
하지만 벡터 검색 기능은 정상적으로 작동하고 있습니다!"""

        # RunnableLambda로 래핑하여 체인과 호환되도록 함
        rag_chain = RunnableLambda(dummy_rag_function)

    return rag_chain

