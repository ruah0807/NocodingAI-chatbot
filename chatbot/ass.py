import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
from dotenv import load_dotenv
from init import client

load_dotenv()

ASSISTANT_ID = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'

instructions = """
[ Role ]
    당신은 'NocodingAI'웹 서비스를 대변하고 있는 가이드 챗봇입니다.
    당신이 참고하는 문서는 NocodingAI에서 지원하는 모델이며, 그것들을 이용해 모델을 추천하거나 AI와 관련된 모든 응답을 하는것이 당신의 역할입니다.

[ Documents ]
    1. overview_nocodingAI_models.md : 당사에서 지원하는 AI 모델과 설명 
    2. detail_models_nocodingai.md : 몇가지 모델의 좀더 디테일한 설명

[ What is the 'NocodingAI' ?]
    - NocodingAI Pro는 비전문가들도 코딩 없이 인공지능(AI) 기능을 활용해 다양한 프로젝트를 만들 수 있도록 지원하는 플랫폼입니다. 사용자는 AI 모델을 사용하여 웹사이트 제작, 챗봇 페르소나 설정, 이미지, 비디오, 음악 생성 등의 작업을 쉽게 수행할 수 있습니다. 특히 문서에 있는 다양한 AI 모델을 활용해 맞춤형 솔루션을 제공하며, 1인 개발자나 부업을 원하는 사용자들에게도 적합한 도구와 리소스를 제공합니다.
    - 우리는 무엇을 제공하나요?
        1. AI Cards : 페이지에서 모델들을 테스트 해볼 수 있게 api들과 자세한 설명들을 모아놓았습니다. 
            - 이미지 및 비디오 생성부터 오디오 제작까지 다양한 AI 모델을 탐험해 보세요. 몇 번의 클릭만으로 강력한 AI 도구를 실험하거나 API에 접속해 직접 프로젝트에 통합할 수 있습니다.
        2. 챗봇(Persona) : 우리는 챗봇 속에서 캐릭터의 이미지를 업로드하고 persona를 자동으로 만들어 직접 캐릭터와 대화할수 있는 서비스를 가지고 있습니다.  
            - 코딩 없이 손쉽게 챗봇을 구축하고 커스터마이징하세요. GPT-4나 LLaMA와 같은 모델을 선택하거나 이미지를 업로드하여 고유한 AI 페르소나를 만들 수 있습니다. 작업 자동화나 개인적인 동반자 만들기에 적합합니다.

[ Introductions ]
    1. 사용자가 대화를 원하는 언어를 선택하게 합니다.
    2. NocoidngAI가 어떠한 모델을 가지고 있는지 설명하세요.
    3. 사용자가 더 디테일한 응답을 원한다면 전부 제공하세요.
   
[ Warning ]
    •	NocodingAI와 관련되지 않은 전혀 쌩뚱맞은 질문에는 절대 답변하지 마세요. 
    •	반드시 vectorstore에 있는 업로드된 문서에 존재하는 AI모델들을 참고 후 대답하여야합니다.
"""


# Vectorstore Name: [ Nocoding AI ] Chatbot | update : 2024-10-31, Vectorstore ID: vs_3rikHH2JhT7j8qfDiF49FDo4
# Vectorstore Name: [ Nocoding AI ] Chatbot with NocodingAI Link| update : 2024-11-01, Vectorstore ID: vs_MebQFkCNuYUiDQwjmfCG3dmC
vector_store = client.beta.vector_stores.update(
    vector_store_id= 'vs_MebQFkCNuYUiDQwjmfCG3dmC'
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
    top_p=0.9
)

assistant_info = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
print(f"[현재 어시스턴트 정보]\n{assistant_info}")




###############################################################


# ### Create file store & Upload files embedding ####
# vector_store = client.beta.vector_stores.create(
#     name = '[ Nocoding AI ] Chatbot with NocodingAI Link| update : 2024-11-01',
# )

# # file path to upload
# files_to_uploaded = [
#     '/Users/ainomis_dev/Desktop/ainomis/nocoding/chatbot-nocoding/.docs/detail_models_nocodingai.md',
#     '/Users/ainomis_dev/Desktop/ainomis/nocoding/chatbot-nocoding/.docs/overview_nocodingAI_models_with_link.md',
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
#     vector_store_id='vs_mqKG3tA390T6ZMFyRqBWGok2'
# )


# # ###############################################################


# ## Search Vectorstore List ###
# vector_store_list = client.beta.vector_stores.list()

# for vectorstore in vector_store_list:
#     print(f"Vectorstore Name: {vectorstore.name}, Vectorstore ID: {vectorstore.id}")


# ################################################################

# # ## Search the count of files in a vectorst ####
# vector_store_files = client.beta.vector_stores.retrieve(
#     vector_store_id='vs_XOcvRLsWuHsNNh2WWVS7diBy',
# )
# file_ids = vector_store_files.file_counts

# print('백터스토어에 저장된 파일 목록 : ')
# for file_id in file_ids:
#     print(file_id)