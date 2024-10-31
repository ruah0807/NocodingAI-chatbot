import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
from dotenv import load_dotenv
from init import client

load_dotenv()

ASSISTANT_ID = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'

instructions = """
[ Role ]
    당신은 'NocodingAI'를 모르는 사용자들을 위해 가이드 또는 모델을 추천하는 역할을 하는 챗봇입니다.

[ Documents ]
    1. overview_nocodingAI_models.md : 당사에서 지원하는 AI 모델과 설명 
    2. detail_models_nocodingai.md : 몇가지 모델의 좀더 디테일한 설명

[ What is the 'NocodingAI' ?]
    'NocodingAI'는 사용자가 빠르게 바뀌고 성장하는 AI 모델을 어렵지 않게 사용하도록 하기 위해, 모델들을 한곳에 모아놓고, 체험하기 쉽게 만들어주는 해주는 웹서비스 입니다.
    이것은 주로, 1인 개발자 혹은 코딩을 모르는 일반인들도 사용가능하게끔 설계되어 있습니다.

[ Introductions ]
    1. 사용자가 대화를 원하는 언어를 선택하게 합니다.
    2. Nocoidng AI의 모델을 어떻게 사용하면되는지 대답합니다.
   
[ Warning ]
    •	NocodingAI와 관련되지 않은 질문에는 절대 답변하지 마세요.
    •	반드시 vectorstore에 있는 업로드된 문서에 존재하는 모델들을 참고 후 대답하여야합니다.
"""


# [ Nocoding AI ] Chatbot
vector_store = client.beta.vector_stores.update(
    vector_store_id= 'vs_mqKG3tA390T6ZMFyRqBWGok2'
)



### 어시스턴트 업데이트
assistant = client.beta.assistants.update(
    assistant_id= ASSISTANT_ID,
    name= 'NoCoding AI ChatBot🤖',
    instructions = instructions,
    model ='gpt-4o-mini',
    tools =  [{'type': 'file_search'}],
    tool_resources={'file_search': {'vector_store_ids':[vector_store.id]}},
    temperature=0.86,
)

assistant_info = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
print(f"[현재 어시스턴트 정보]\n{assistant_info}")




###############################################################


### Create file store & Upload files embedding ####
# vector_store = client.beta.vector_stores.create(
#     name = '[ Nocoding AI ] Chatbot | update : 2024-10-29',
# )

# # file path to upload
# files_to_uploaded = [
#     '/Users/ainomis_dev/Desktop/ainomis/nocoding/chatbot-nocoding/.docs/detail_models_nocodingai.md',
#     '/Users/ainomis_dev/Desktop/ainomis/nocoding/chatbot-nocoding/.docs/overview_nocodingAI_models.md',
# ]

# file_streams = [open(path, 'rb') for path in files_to_uploaded]

# # upload and add to vectorstore
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#     vector_store_id=vector_store.id, files = file_streams
# )


###############################################################


# #### Searching Assistant List####
# assistant_list = client.beta.assistants.list()

# for assistant in assistant_list:
#     print(f"[Assistant Name]: {assistant.name}, [Assistant ID] : {assistant.id}")


###############################################################


# # Delete Vectorstore ###
# vector_store = client.beta.vector_stores.delete(
#     vector_store_id='vs_XOcvRLsWuHsNNh2WWVS7diBy'
# )


# ###############################################################


# ## Search Vectorstore List ###
# vector_store_list = client.beta.vector_stores.list()

# for vectorstore in vector_store_list:
#     print(f"Vectorstore Name: {vectorstore.name}, Vectorstore ID: {vectorstore.id}")

################################################################

# # ## Search the count of files in a vectorst ####
# vector_store_files = client.beta.vector_stores.retrieve(
#     vector_store_id='vs_XOcvRLsWuHsNNh2WWVS7diBy',
# )
# file_ids = vector_store_files.file_counts

# print('백터스토어에 저장된 파일 목록 : ')
# for file_id in file_ids:
#     print(file_id)