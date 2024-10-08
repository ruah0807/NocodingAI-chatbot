import pandas as pd
import os

# 엑셀 파일을 읽어온다
df = pd.read_csv('/Users/ainomis_dev/Desktop/ainomis/chatbot-nocoding/.docs/노코딩AI_모델 설명.csv')

# markdown 형식으로 변환
markdown_table = df.to_markdown(index=False)

# 저장할 폴더 경로 설정
save_folder = '/Users/ainomis_dev/Desktop/ainomis/chatbot-nocoding/.docs/'  # 원하는 폴더 경로
save_path = os.path.join(save_folder, '노코딩AI_모델 설명.md')

# 해당 폴더가 없는 경우 폴더를 생성
os.makedirs(save_folder, exist_ok=True)

# 마크다운 파일로 저장
with open(save_path, 'w') as f:
    f.write(markdown_table)
    print(f"파일이 {save_path}에 저장되었습니다.")




##################################################################################################################

# # 엑셀 파일을 읽어온다
# df = pd.read_csv('/Users/ainomis_dev/Desktop/ainomis/ai_assistant/_docs/similarity_code/35-판매알선업-표1.csv')

# # markdown 형식으로 변환
# markdown_table = df.to_markdown(index=False)

# # 한 파일에 저장할 행 수 설정 (청킹크기)
# chunk_size = 1000

# # 저장할 폴더 경로 설정
# save_folder = '/Users/ainomis_dev/Desktop/ainomis/ai_assistant/_docs/similarity_code/35-판매알선업-표1/'  # 원하는 폴더 경로
# os.makedirs(save_folder, exist_ok=True)

# # 청킹하여 파일로 저장
# for i in range(0, len(df), chunk_size):
#     # 데이터 프레임을 청킹 
#     chunk_df = df[i:i+chunk_size]

#     # 마크다운 형식으로 변환
#     markdown_table = chunk_df.to_markdown(index=False)

#     #파일명 설정 (청킹 번호로 구분)
#     file_name = f'35-판매알선업_chunk_{i//chunk_size + 1}.md'
#     file_path = os.path.join(save_folder, file_name)

#     #마크다운 파일로 저장
#     with open(file_path, 'w', encoding='utf-8') as f :
#         f.write(markdown_table)

#     print(f"{file_name} 저장 완료")