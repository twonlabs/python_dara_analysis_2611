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
