# %%
import pandas as pd
import numpy as np

file_path = '/home/asd/projects/seoul_metro_congestion/seoul_metro_congestion.csv'

try:
    df = pd.read_csv(file_path, encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='utf-8')



# %%

# 데이터의 첫 5줄 확인
print("--- 원본 데이터 (처음 5줄) ---")
print(df.head())


# %%
# 데이터의 전체 구조 및 타입 확인
print("\n--- 원본 데이터 정보 ---")
df.info()

# %%
# 'id_vars'는 고정할 기준 컬럼들입니다. (데이터에 따라 '연번', '역번호' 등이 더 있을 수 있음)
# 실제 데이터의 컬럼명을 확인하고 정확히 지정해야 합니다.
id_columns = ['요일구분', '호선', '역번호', '출발역', '상하구분'] 

# id_vars에 포함되지 않은 나머지 컬럼 (즉, 시간대 컬럼들)을 모두 melt 대상으로 삼습니다.
# value_vars를 명시적으로 지정하지 않으면 id_vars를 제외한 모든 컬럼이 대상이 됩니다.
df_long = pd.melt(df, 
                  id_vars=id_columns, 
                  var_name='시간대', 
                  value_name='혼잡도')

print("\n--- Long Format으로 변경된 데이터 (처음 5줄) ---")
print(df_long.head())

# %%
df_long['혼잡도'] = df_long['혼잡도'].fillna(0)


print("\n--- '혼잡도' 컬럼 정제 후 (처음 5줄) ---")
print(df_long.head())

# %%
# (1) '시 ' 또는 '시' -> ':' (e.g., '05시 30분' -> '05:30분')
temp_time = df_long['시간대'].str.replace('시 ', ':', regex=False)
temp_time = temp_time.str.replace('시', ':', regex=False)

# (2) '분' -> '' (e.g., '05:30분' -> '05:30')
temp_time = temp_time.str.replace('분', '', regex=False)

# 2. '-'를 기준으로 분리하여 시작 시간(e.g., '05:30')만 추출
#    (e.g., '05:30-05:59' -> '05:30')
df_long['시간'] = temp_time.str.split('-').str[0]

# 3. (혹시 모를) 앞뒤 공백 제거
df_long['시간'] = df_long['시간'].str.strip()


# 4. '주중/주말' 컬럼 생성
df_long['주중주말'] = np.where(df_long['요일구분'] == '평일', '주중', '주말')


print("\n--- 파생 변수 생성 후 (시간 포맷 변경 확인) ---")
# '시간대'(원본), '시간'(변경 후)을 함께 출력하여 잘 바뀌었는지 확인
print(df_long[['시간대', '시간', '주중주말']].head())

print("\n--- 최종 데이터 정보 ---")
df_long.info()


# %%
# 1. (가장 중요) 현재 '호선' 컬럼에 어떤 값들이 있는지 확인합니다.
#    (출력된 리스트를 보고 2번 딕셔너리를 만드세요)
current_lines = df_long['호선'].unique()
print("--- 현재 호선 이름 ---")
print(current_lines)

# %%
# 2. 한글 이름을 영어 이름으로 바꾸는 '규칙' (Dictionary)을 만듭니다.
line_mapping = {
    '1호선': 'Line 1',
    '2호선': 'Line 2',
    '3호선': 'Line 3',
    '4호선': 'Line 4',
    '5호선': 'Line 5',
    '6호선': 'Line 6',
    '7호선': 'Line 7',
    '8호선': 'Line 8',
    '9호선': 'Line 9',
}

df_long['호선'] = df_long['호선'].replace(line_mapping)

print("\n--- 변경 후 호선 이름 ---")
print(df_long['호선'].unique())

print("\n'호선' 컬럼 영문 변경 완료!")

# %%
# 전처리 완료된 데이터를 새 파일로 저장
df_long.to_csv('preprocessed_congestion.csv', index=False, encoding='utf-8-sig')

print("\n--- 전처리 완료된 파일 저장 성공! ---")


