import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
from dotenv import load_dotenv
from init import client

load_dotenv()

ass_id = ''



instructions = '''
[ Role ]
    당신은 사용자가 업로드하는 이미지 속 주인공의 성격, 
[ Context ]
   
[ dialog flow ]
    1.	대상 상표 이미지 업로드 1개 :
        - 사용자가 등록하고자 하는 1개의 이미지를 분석합니다. 
    2.	유사한 10개의 상표 이미지 업로드 : 
        - 유사성이 있는 10개의 이미지들을 사용자가 처음으로 올린 이미지와 대조해가며 유사성을 분석합니다.

    3.	상표심사기준 적용:
        - 사용자가 등록하고자 하는 상표 이미지와 브랜드명, 두번째로 올린 유사한 상표의 이미지와 브랜드명들을 비교 분석합니다.
    각각의 상표 이미지를 사용자가 등록하고자하는 이미지와 비교하여 [상표유사여부보고서형식(예시).md]형식으로 대답하세요

[ Constraints ]
    •	반드시 vectorstore에 참고문서를 참고하여 대답하여야합니다.

'''



vector_store = client.beta.vector_stores.update(
    vector_store_id= 'vs_rLXYrSoCNE7aNpLI6cBGPseN'
)



### 어시스턴트 업데이트
assistant = client.beta.assistants.create(
    # assistant_id= ass_id,
    name= 'MY AI-Friend',
    instructions = instructions,
    model ='gpt-4o',
    tools =  [{'type': 'file_search'}],
    # tool_resources={'file_search': },
    temperature=0,
)

assistant_info = client.beta.assistants.retrieve(assistant_id=ass_id)
print(f"[현재 어시스턴트 정보]\n{assistant_info}")






###############################################################


#### 백터스토어 생성및 파일 임베딩 업로드 ####
# vector_store = client.beta.vector_stores.create(
#     name = '상표 식별 documents',
# )


# # #업로드할 파일들의 경로를 지정
# files_to_uploaded = [
#     '../_docs/example/상표심사기준202405.pdf',
#     '../_docs/example/상표유사여부보고서(예시).md',
# ]

# file_streams = [open(path, 'rb') for path in files_to_uploaded]

# # 파일 업로드 및 백터 스토어에 추가
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#     vector_store_id=vector_store.id, files = file_streams
# )


###############################################################


### 어시스턴트 리스트 검색 ####
# print(client.beta.assistants.list())

# for assistant in assistant_list:
#     print(f"[Assistant Name]: {assistant.name}, [Assistant ID] : {assistant.id}")


###############################################################


## vectorstore 삭제 ###
# vector_store = client.beta.vector_stores.delete(
#     vector_store_id='vs_iuSR8xFYdZML64ycdt8TC6BW'
# )


###############################################################


# ## 벡터스토어 리스트 검색 ###
# vector_store_list = client.beta.vector_stores.list()

# for vectorstore in vector_store_list:
#     print(f"Vectorstore Name: {vectorstore.name}, Vectorstore ID: {vectorstore.id}")


