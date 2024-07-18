from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import RetrievalQA
from langchain_aws import ChatBedrock 
from langchain.embeddings import BedrockEmbeddings
import os
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def chatbedrock(user_input):
    #* 埋め込みモデルの読み込み
    embedding_model = BedrockEmbeddings(model_id="cohere.embed-multilingual-v3")

    # インデックスのパス
    index_path = "./storage"

    # インデックスの読み込み
    index = FAISS.load_local(
        allow_dangerous_deserialization = True,
        folder_path=index_path, 
        embeddings=embedding_model
    )

    #* プロンプトテンプレートの定義
    #* 中身を目的に沿った内容に編集してください
    question_prompt_template = """

    {context}
    
    Question: {question}
    Answer: """

    # プロンプトの設定
    QUESTION_PROMPT = PromptTemplate(
        template=question_prompt_template, # プロンプトテンプレートをセット
        input_variables=["context", "question"] # プロンプトに挿入する変数
    )

    #* モデルの設定
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    llm = ChatBedrock(
        model_id=model_id,
        model_kwargs={"temperature": 0.9}
    )

    # メモリーの設定
    memory = ConversationBufferMemory(memory_key="chat_history",output_key="result", return_messages=True)

    # （RAG用）質問回答chainの設定
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=index.as_retriever( 
            search_kwargs={'k': 2} # indexから上位いくつの検索結果を取得するか
        ), 
        chain_type_kwargs={"prompt": QUESTION_PROMPT}, # プロンプトをセット
        chain_type="map_reduce", #* 検索した文章の処理方法 [stuff:詰め込み方式、map_reduce:チャンクごとに実行、refine:純度を高める]
        memory=memory,
        return_source_documents=True # indexの検索結果を確認する場合はTrue
    )

    # 質問文
    question = user_input

    # LLMの回答生成
    response = chain.invoke(question)

    # indexの検索結果を確認
    for i, source in enumerate(response["source_documents"], 1):
            print(f"\nindex: {i}----------------------------------------------------")
            print(f"{source.page_content}")
            print("---------------------------------------------------------------")

    # 回答を確認
    response_result = response["result"]
    print(f"\nAnswer: {response_result}")

    return response_result