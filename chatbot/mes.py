import os, sys, asyncio, concurrent.futures
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from init import client

ass_id = 'asst_t6EJ7fG2GebmCD7PNg3o8M5d'

async def submit_message_with_image(thread, user_message, image_path, image_url):
    content = [{'type': 'text', 'text': user_message}]

    #ThreadPoolExecutor를 사용하여 이미지 파일을 병렬로 업로드
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, upload_image, local_image_path, original_image_url)
            for local_image_path, original_image_url in zip(image_path, image_url)
        ]
  
        uploaded_files = await asyncio.gather(*tasks)

    #업로드 완료된 파일을 메시지에 추가
    for file, original_image_url in uploaded_files:
        if file:
            content.append({'type': 'image_file', 'image_file': {'file_id': file.id}})
            content.append({'type': 'text', 'text': f'등록하려는 상표 URL: {original_image_url}'})  # 원본 이미지 URL 라벨링

    if content:
        # 이미지 파일 전송
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=content)
    else:
        print(f"Error : 이미지 파일 전송 실패 ")
    print(f"이미지 업로드 완료 . thread_id : {thread.id}")


def upload_image(local_image_path, original_image_url):
    print(f"Opening image file: {local_image_path}")  # 각 이미지 경로를 출력하여 확인
    try:
        with open(local_image_path, 'rb') as image_file:
            file =  client.files.create(file=image_file, purpose='vision') # 이미지 분석을 위한 용도
            return file, original_image_url
    except FileNotFoundError as e:
        print(f"Error: 파일을 찾을 수 없습니다. 경로: {local_image_path}. 에러: {str(e)}")
        return None, original_image_url   
    

async def run_with_tools(ass_id, thread):

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ass_id,
        tools=  [{'type': 'file_search'}],
        instructions= """
        
        """
    )
    return run


# 새로운 스레드 생성 및 메시지 제출
async def similarity_create_thread_and_run(user_input, image_paths, image_urls):
    thread = await asyncio.to_thread(client.beta.threads.create)
    await submit_message_with_image(thread, user_input, image_paths, image_urls)
    run = await run_with_tools(ass_id, thread)
    return thread, run