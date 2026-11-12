# 의료 기초 데이터 분석 미니 프로젝트
# Numpy + Pandas + Matplotlib

# ============================
# [0] 라이브러리 import, 출력 옵션(선택)
# ============================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 줄 정렬 옵션
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.width', 140)
pd.set_option('display.max_columns', 60)
pd.set_option('display.max_rows', 200)

# ============================
# [1] 데이터 준비
# ============================

data = {
    '측정일': [
        '2026-02-01','2026-02-01','2026-02-02',
        '2026-02-02','2026-02-03','2026-02-03',
        '2026-02-04','2026-02-04','2026-02-05',
        '2026-02-05','2026-02-06','2026-02-06',
        '2026-02-07','2026-02-07','2026-02-08'
    ],
    '환자ID': [
        'P001','P002','P003','P004','P005',
        'P006','P007','P008','P009','P010',
        'P011','P012','P013','P014','P015'
    ],
    '성별': [
        'F','M','M','F','F','M','M','F',
        'F','M','F','M','M','F','F'
    ],
    '나이': [
        25,31,44,np.nan,52,39,28,33,
        47,61,29,42,np.nan,36,55
    ],
    '키': [
        '162cm','175cm','168cm','160cm','158cm',
        '180cm','172cm','165cm','170cm','177cm',
        '159cm','174cm','169cm','163cm','157cm'
    ],
    '몸무게': [
        '54kg','78kg','70kg','52kg','60kg',
        '90kg','68kg','58kg','73kg','82kg',
        '50kg','76kg','71kg','57kg','66kg'
    ],
    'SBP(수축기)': [
        108,135,142,118,150,130,125,112,
        140,160,105,138,145,120,155
    ],
    'DBP(이완기)': [
        70,88,92,75,95,85,80,72,
        90,100,68,89,96,78,97
    ],
    '심박수': [
        72,84,90,68,95,78,70,75,
        88,92,66,80,86,73,89
    ],
    '공복혈당': [
        92,110,125,98,130,np.nan,105,90,
        118,140,88,112,128,100,np.nan
    ],
    '흡연': [
        'N','Y','Y','N','N','Y','N','N',
        'Y','Y','N','Y','Y','N','N'
    ],
    '운동빈도(주)': [
        3,1,0,2,np.nan,1,4,2,
        1,0,5,1,0,3,np.nan
    ],
}

df = pd.DataFrame(data)


# ============================
# [2] 데이터 탐색
# ============================

print('===============================')
print('[2] 데이터 탐색')
print('===============================')

print('\n[head()]')
print(df.head())

print('\n[info()] / 데이터 구조 확인')
print(df.info())

print('\n[describe] / 숫자 칼럼 요약')
num_cols = ['나이', 'SBP(수축기)', 'DBP(이완기)', '심박수', '공복혈당','운동빈도(주)']
print(df[num_cols].describe)


# ============================
# [3] 데이터 정제 및 변환
# ============================

print('===============================')
print('[3] 데이터 정제 및 변환')
print('===============================')

# pd.to_datetime():
print(df['측정일'].dtype) # 변환 전
df['측정일'] = pd.to_datetime(df['측정일'])

print(df['측정일'].dtype)

# ============================
# 3-2) 단위 제거:  
# ============================

# str.replace() : 문자열 치환(여기서는 단위 제거)

print(df['키'].dtype)
print(df['몸무게'].dtype)

# df['키_cm'] = df['키'].str.replace('cm', '', regex=Flase).astype(int)
df['뭄무게_kg'] = df['몸무게'].str.replace('cm', '', regex=Flase).astype(int)

print(df['키_cm'].dtype)
print(df['몸무게'].dtype)

# ============================
# 3-3) 결측치 확인:   
# ============================

print('3-3) 결측치 확인')
print('[결측치 개수 확인]')
print(df.isnull().sum())

# ============================
# 3-4) 결측치 처리(예시)   
# ============================

df['나이'] = df['나이'].fillna(df['나이'].mean())
df['공복혈당'] = df['공복혈당'].fillna(df['공복혈당'].median())
df['운동빈도(주)'] = df['운동빈도(주)'].fillna(0)

print('[결측치 처리 후 개수 확인]')
print(df.isnull().sum())

# ============================
# 3-5) 파생 컬럼 생성(변환)   
# ============================

# BMI = 몸무게(kg) / 키(m)^2
print('== cm -> m 변환 ==')
df['키_m'] = df['키_m'] / 100
df['BMI'] = df['몸무게_kg'] / (df['키_m'] ** 2)

print('== BMI ==')
print(df[['키_cm', '키_m']].head())
print(df['BMI'].head())

print('== 맥박압(PP) ==')
df['맥박압_pp'] = df['SBP(수축기)'] - df['DBP(이완기)']
print(df['맥박압_PP'].head)

print('== 평균동맥압(MAP) ==')

df['평균동맥압_MAP'] = (df['SBP(수축기)'] + 2 * df['DBP(이완기)']) / 3
print(df['평균동맥압_MAP'].head())

# ============================
# 3-6) 범주화(카테고리 만들기) : 혈압 단계 분류  
# ============================


def bp_category(sbp, dbp):
    if(sbp >= 140) or (dbp >= 90):
        return '고혈압2기'
    elif(130 <= sbp <= 139) or (80 <= dbp <= 89):
        return '고혈압1기'
    elif(120 <= sbp <= 129) and (dbp < 80):
        return '주위(상승)'
    elif(sbp < 120) and (dbp < 80):
        return '정상'
    else:
        return '기타'
'''
# 일반 함수
def test(row):
    return 'hi'

# lambda : 이름 없이 간단하게 작성하는 함수(익명함수)
# lambda 매개변수: 반환할_표현식
lambda row: 'hi'
'''

# apply() : 행 단위로 함수를 적용할 때 자주 사용
df['혈압분류'] = df.apply(lambda row: bp_category(
    row['SBP(수축기)'],
    row['DBP(이완기)']
), axis=1
)

print('[혈압 분류 결과]')
print(df[['SBP(수축기)', 'DBP(이완기)', '혈압분류']].head)

# ============================
# 3-7) 범주화 : BMI 단계 분류(간단 예시)  
# ============================
'''
BMI 분류
- 저체중 : < 18.5
- 정상 : 18.5 ~ 22.9
- 과체중 : 23.0 ~ 24.9
- 비만 : 
'''

def bmi_category(bmi):
    if bmi < 18.5:
        return '저체중'
    elif bmi < 22.9:
        return '정상'
    elif bmi < 24.9:
        return '과체중'
    else bmi <