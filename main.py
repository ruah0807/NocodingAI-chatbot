from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from fastapi.responses import StreamingResponse
from init import client

app = FastAPI()
ASSISTANT_ID = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'


class CreateThreadResponse(BaseModel):
    thread_id: str

class DeleteThreadRequest(BaseModel):
    thread_id: str

class ChatRequest(BaseModel):
    thread_id: str
    prompt: str

class ChatResponse(BaseModel):
    reply: str

# 스레드와 메시지를 저장할 딕셔너리
threads = {}


@app.post("/create_thread", response_model=CreateThreadResponse)
def create_thread():
    thread = client.beta.threads.create()
    thread_id = thread.id
    threads[thread_id] = []
    return CreateThreadResponse(thread_id=thread_id)


@app.post("/delete_thread")
def delete_thread(request: DeleteThreadRequest):
    thread_id = request.thread_id
    if thread_id in threads:
        client.beta.threads.delete(thread_id)
        del threads[thread_id]
        return {"message": "Thread deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Thread not found.")
    


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    thread_id = request.thread_id
    prompt = request.prompt

    if thread_id not in threads:
        raise HTTPException(status_code=404, detail="Thread not found.")

    # 사용자 메시지 추가
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=prompt
    )

    # 어시스턴트 실행
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )
    run_id = run.id

    # 응답 대기
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        ).status
        if run_status == "completed":
            break
        time.sleep(2)

    # 어시스턴트 응답 가져오기
    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_msg = thread_messages.data[0].content[0].text.value
    if assistant_msg is None:
        raise HTTPException(status_code=500, detail="Assistant response not found.")

    # 스레드가 자동 삭제되는지 확인하기 위해 로그 출력
    print(f"Thread {thread_id} still exists with {len(thread_messages.data)} messages.")

    # 메시지 저장 (옵션)
    threads[thread_id].append({'role': 'user', 'content': prompt})
    threads[thread_id].append({'role': 'assistant', 'content': assistant_msg})

    # ChatResponse의 'reply' 필드에 어시스턴트 메시지를 포함하여 반환
    return ChatResponse(reply=assistant_msg)



@app.post("/stream_chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    thread_id = request.thread_id
    prompt = request.prompt

    if thread_id not in threads:
        raise HTTPException(status_code=404, detail="Thread not found.")

    # 사용자 메시지 추가
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=prompt
    )

    # 어시스턴트 실행
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
        stream=True,
        instructions="""
        [ there are two kind of answer options. you can answer the question follow the instructions. ]
                
        [ Option 1.]
        - If a user asks a question like this, you answer it in the same format.
            1. If user wants to get a direction to make there own website
            2. If user wants to create something(for example, create an image, etc.)
            3. If user wants to recieve the recommended models
        - You should suggest a model from the documents that suits the user, 
        - All information can be found in the documents which provide a 'NocodingAI link' with a sufficient description of the model. 

        - Option 1 answer format :

            (if it's help them, Put your answer and total instructions or whatever you want to say. It would be great also to give advice.)
            
            1. (model 1)
                - introduction : (why this model suits user) 
                - Link : [model's name](link)(only put 'NocodingAI Link' from the documents)
                
            // ... If there are more models you would like to reommend, please list them in order.


        [ Option 2. ]
        - If a user asks a general question rather than a model, there is no need to follow 'Option 1 answer format'. Give the answer you want. 
        - It should be a nocodingAI-related response.
        - All information can be found in the documents which provide a 'NocodingAI link' with a sufficient description of the model. 
        
        - Option 2 answer format :
            (whatever you can answer about relate 'NocodingAI' in order to help the user.) 
        """

    )
    async def event_generator():
        try:
            msg = ""
            for event in run:
                if hasattr(event, "data") and event.data.object =="thread.message.delta":
                    delta_content = event.data.delta.content
                    for item in delta_content:
                        if hasattr(item, "text") and hasattr(item.text, "value"):
                            msg += item.text.value
                            yield f" data: {msg}\n\n"
                elif hasattr(event, "data") and event.data.object == "thread.run.completed":
                    break
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"    

    return StreamingResponse(event_generator(), media_type="text/event-stream")                     
