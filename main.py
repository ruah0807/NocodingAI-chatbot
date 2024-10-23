from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from init import client

app = FastAPI()
assistant_id = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'


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
        assistant_id=assistant_id,
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