import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm

# 출력 옵션
pd.set_option('display.unicode.east_asian_width', True)
@@ -453,4 +455,54 @@ def bmi_category(bmi):
)

print('\n[위험점수]')
print(df[['환자ID', '위험점수']])
print(df[['환자ID', '위험점수']])


# =====================================
# [5] 시각화
# =====================================

print('=====================================')
print('[5] 시각화')
print('=====================================')

# ---------------------------------------------------
# 5-1) 혈압(SBP/DBP) 분포 히스토그램
# ---------------------------------------------------
'''
히스토그램
- 숫자 데이터가 어느 구간에 얼마나 많이 모여 있는지 보여주는 그래프
- bin이 크면 클 수록 나뉘는 구간이 촘촘함
- 구간 수에 따라 그래프 모양이 달라짐
'''

# 원하는 폰트 파일 경로 문자열로 입력
font_location = r'C:\Windows\Fonts\H2GTRM.TTF'

# 지정한 폰트 파일 경로에서 폰트 추출
fontname = fm.FontProperties(
    fname=font_location
).get_name()

# matplotlib의 전역 폰트 설정 변경
matplotlib.rc('font', family=fontname)

plt.figure() # 그래프 공간 생성
plt.hist(df['SBP(수축기)'], bins=8) # 구간 설정
plt.title('SBP DIST') # 그래프 위 제목(수축기 혈압(SBP) 분포)
plt.xlabel('SBP(mmHg)') # 가로축 의미 설명
plt.ylabel('frequency') # 세로축 의미 설명(빈도)
plt.tight_layout() # 글자가 잘리지 않게 자동 정렬
# plt.show()

plt.figure()
plt.hist(df['DBP(이완기)'], bins=8) # 구간 설정
plt.title('DBP DIST') # 그래프 위 제목(이완기 혈압(DBP) 분포)
plt.xlabel('DBP(mmHg)')
plt.ylabel('frequency')
plt.tight_layout()
# plt.show()

# ---------------------------------------------------
# 5-2) 혈압분류별 평균 SBP 막대그래프
# ---------------------------------------------------
plt.close('all')
bp_sbp_mean = df.groupby('혈압분류')['SBP(수축기)'].mean().sort_value(ascending=False)

plt.figure()
plt.bar(bp_sbp_mean.index, bp_sbp_mean.values)
plt.title('Avg SBP by Blood Category')
plt.xlabel('Blood Pressure Category')
plt.ylabel('Abverge SBP(mmHg)')
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# 5-3) 산점도 : BMI vs SBP
# ---------------------------------------------------
plt.close('all')

plt.figure()
plt.scatter(df['BMI'], df['SBP(수축기)'])
plt.title('BMI vs SBP Scatter plot')
plt.xlabel('BMI')
plt.ylabel('SBP(mmHg)')
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# 5-4) 측정일 기준 SBP 추이(날짜별 평균)
# ---------------------------------------------------
plt.close('all')

date_sbp = df.groupby('측정일')['SBP(수축기)'].mean()

plt.close('all')
plt.figure()
plt.plot(date_sbp.index, date_sbp.vlaue)
plt.title('Avg SBP Over Time')
plt.xlabel('measurement date')
plt.ylabel('Avg SBP(mmHg)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# 5-5) BMI분류 인원 수(파이차트)
# ---------------------------------------------------


bmi_count = df['BMI분류'].value_counts()

plt.close('all')
plt.figure()
plt.pie(
    bmi_count.values,
    labels=bmi_count.index,
    autopct='%1.1f%%'
)

plt.title('BMI Category DIST')
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# 5-6) 혈압분류별 BMI 분포(박스플롯)
# ---------------------------------------------------

plt.close('all')

plt.figure()
df.boxplot(column='BMI', by='혈압분류')
plt.title('BMI DIST by Blood Category')
plt.suptitle('')
plt.xlabel('Blood Pressure Category')
plt.ylabel('BMI')
plt.tight_layout()
plt.show()

# =====================================
# 5-7) 성별 BMI
# =====================================

plt.close('all')

plt.figure()

df[df['성별'] == 'M']['BMI'].hist(alpha=0.5, bins=8)
df[df['성별'] == 'F']['BMI'].hist(alpha=0.5, bins=8)


plt.title('BMI DIST by Gender')
plt.xlabel('BMI')
plt.ylabel('Frequency')
plt.legend('Male', 'Female')
plt.tight_layout()
plt.show()

# =====================================
# 5-8) 상관관계 히트맵
# =====================================
'''
히트맵
- 값의 크기를 색으로 표현하는 그래프
- 값이 클수록 진한 색
- 값이 작을수록 연한 색
'''

corr_cols = ['나이', '키_cm', '몸무게_kg', 'SBP(수축기)', 'SBP(이완기)', '공복혈당', 'BMI']

corr = df[corr_cols].corr()

plt.figure()
plt.imshow(corr)
plt.colorbar()
plt.xticks(range(len(corr_cols)), corr_cols, rotation=45)
plt.yticks(range(len(corr_cols)), corr_cols, rotation=45)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

print('==================================')
print('-1) 혈압분류 비율')
print('=====================================') 


# =====================================
# 6-1) 혈압분류 비율
# =====================================

plt.close('all')

bp_count = df['혈압분류'].vlaue_count()
bp_ratio = (bp_count)

print('\n[혈압분류 분포(비율%)]')
print(bp_ratio.round(1))

# =====================================
# 6-2) 위험 신호 : 공복혈당 평균과 126 이상 비율
# =====================================
mean_glu = df['공복혈당'].mean()
high_glu_ratio = (df['공복혈당'] >= 126).mean() * 100

print(f'\n[공복혈당 평균 : {mean_glu: .2f} mg/dL]')
print(f'[공복혈당 126 이상 비율 : {high_glu_ratio: .1f}%]')

# =====================================
# 6-3) 운동빈도와 주요 지표 관계
# =====================================

corr_exercise_sbp = df['운동빈도(주)'].corr(df['SBP(수축기)'])
corr_exercise_bmi = df['운동빈도(주)'].corr(df['BMI'])

print(f'\n[운동빈도 vs SBP 상관계수] : {corr_exercise_sbp: .2f}')
print(f'[운동빈도 vs BMI 상관계수] : {corr_exercise_sbp: .2f}')

# =====================================
# 6-4) 전략/제안 3줄
# =====================================
stratege = []

ht2_ratio = (df['혈압분류'] == '고혈압2기').mean()

if ht2_ratio >=30:
    stratege.append('고혈압2기 비율이 높은 편이라, ' \ '생활습관(운동/체중/염분)관련 교육 및 추적 관리가 필요합니다')

else:
    stratege.append('고혈압2기 비율이 과도하게 높진 않지만,' \ '고혈압1기 이상에 대한 예방 안내가 유효합니다.')

# BMI 비만 비율 코멘트
obesity_ratio = (df['BMI분류'] == '비만').mean() * 100
stratege.append(f'BMI 기준 비만 비율이 {obesity_ratio: .1f}%로 확인되어,
                체중관리(식습관+운동) 프로그램을 고려할 수 있습니다.')

if high_glu_ratio > 20:
    stratege.append('공복혈당 126 이상 비율이 꽤 있어,' \
                    '혈당 관련 추가 검사/상담 연계를 고려할 수 있습니다.')
else:
    stratege.append('공복혈당 고위험 비율이 높진 않지만,' \
                    '식급관/활동량 관련 기본 가이드를 제공하면 좋습니다.')

print('\n[제안 3줄]')
for s in stratege:
    print(f'- {s}')

# =====================================
# 6-5) 위험 점수 기반 위험군 요약
# =====================================

high_rist = df[df['위험점수'] >= 2]
high_rist_ratio = (len(high_rist) / len(df)) * 100

print(f'\n[고위험군 비율(위험점수 2 이상)] : {high_rist_ratio: .1f}%')
print('[고위험군 목록]')
print(high_rist[['환자ID', 'BMI', '공복혈당, '혈압분류', '위험점수']])

# =====================================
# 6-6) 최상위 위험 대상 Top 3
# =====================================

plt.close('all')

top_risk = df.sort_values(['위험점수', 'BMI'], ascending=True).head(3)
print('\n[최상위 위험 대상 Top 3]')
print(top_risk)[['환자ID', 'BMI', '공복혈당, '혈압분류', '위험점수']])

# =====================================
# 6-7) 전체 건강 상태 등급 평가
# =====================================

if (high_risk_ratio > 30) or (high_glu_ratio > 30):
    health_level = '위험'

else (high_risk_ratio > 15) or (high_glu_ratio > 15):
    health_level = '양호'

print(f'\n[전체 건강 상태 평가] => {health_level}')
