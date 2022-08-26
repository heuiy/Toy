
# 출처 : https://www.datalabs.co.kr/html/support/DataLibrary.php?mode=view&seq=264&page=1&bc_id=bbs_pds&num_per_page=20&page_per_block=10&search=&search_text=


###################################
#   쉽게 배우는 통계분석 with R   #
###################################

# 패키지 설치
install.packages("ggplot2")
install.packages("dplyr")
install.packages("patchwork")
install.packages("gganimate")
install.packages('gifski')
install.packages('av')
install.packages('png')

## R의 기본 원리(객체)
number <- c(1, 3, 5, 7, 9) # 다수 데이터 입력 시
number

## R의 기본 원리(함수)
x <- c(1, 2, 3, 4, 5)
y <- c(2, 4, 6, 8, 10)
plot(x,y, xlab = "x축", 
          ylab = "Y축", 
          main = "그래프실습")

## R 작업 경로 설정

setwd("c:/data/exam_r") # R 작업 디렉토리 설정
getwd() # 현재 작업 디렉토리 확인

## R 패키지 설치
install.packages()

## R 데이터세트 생성

a <- c(1, 2, 3, 4, 5) # 다중 데이터 입력
b <- c("A", "A", "A", "B", "B")
b <- rep(c("A","B"), c(3,2)) # 이와 같이 입력도 가능
c <- rep(c("A","B"), each = 10)
ab <- data.frame(score = a, class = b)
ls() # 생성된 변수 목록 확인
rm() # 특정 변수 삭제
rm(list =ls()) # 전체 변수 삭제

## R 데이터세트 생성(데이터 불러오기)
data <- read.csv('data handling_dplyr.csv', header = TRUE)
head(data) # 상위 6개 데이터세트 확인
head(data, n= 10) # 상위 10개 데이터세트 확인
tail(data) # 하위 6개 데이터세트 확인
dim(data) # 데이터의 차원 확인(행, 열 개수)

data() # R에 내장되어 있는 데이터세트 목록 확인
iris # R에 내장되어 있는 iris 데이터 확인

## 데이터 전처리(내장함수)

data[1,] # data 객체의 1번째 행만 출력
data[1:3,] # data 객체의 1~3번째 행만 출력
data[, 1] # data 객체의 1번째 열만 출력
data[,1:3] # data 객체의 1~3번째 열만 출력
data[,c(1, 4)] # data 객체의 1, 4번 열만 출력
str(data)
data[,c("직원ID", "직급")] # data 객체의 열 이름으로도 출력 가능
data[, -1] # data 객체의 1번째 열 삭제
data[-1,] # data 객체의 1번째 행 삭제
data[-c(1:10),] # data 객체의 1~10번째 행 삭제

## 데이터 전처리(dplyr 패키지)

exam <- read.csv('data handling_dplyr.csv') # 데이터불러오기

# select 함수 실습

a1_1 <- select(exam, 직원ID) # exam 객체에서 직원ID 열만 선택하여 새로운 객체 생성
nrow(a1_1)
head(a1_1)
a1_2 <- select(exam, c(직원ID,
                        지각횟수,
                        결근횟수,
                        업무성과,
                        토익점수))
head(a1_2)
a1_3 <- select(exam, 직원ID : 직급)
a1_3

# filter 함수 실습
a2_1 <- filter(exam, 지각횟수 == 0) # == 는 ~와 같은 조건이라는 것을 의미
a2_1
a2_2 <- filter(exam, 지각횟수 >= 1) # 지각횟수가 1 이상인 조건
a2_2
a3_3 <- filter(exam, 지각횟수 == 0 & 결근횟수 == 0) # 지각횟수와 결근 횟수가 모두 0회인 조건
a3_3
a3_4 <- filter(exam, 지각횟수 == 0 | 결근횟수 == 0) # 지각횟수 또는 결근횟수가 0회인 조건
a3_4

# 결측 데이터 추출 또는 제거
is.na(exam) # 결측값 확인
sum(is.na(exam)) # 모든 변수 결측값 개수 확인
colSums(is.na(exam)) # 열별 결측값 개수 확인
exam_na <- na.omit(exam) # 결측을 제외하고 새로운 데이터세트 생성

a4_1 <- filter(exam, is.na(토익점수)) # 토익 미응시자 직원 추출
a4_1
a4_2 <- filter(exam, !is.na(토익점수)) # 토익 미응시자 직원 제거
a4_2

# 파생변수 생성

a5_1 <- mutate(a4_2, 근태점수 = 100 - (결근횟수 +(지각횟수/3))*5)
head(a5_1)
a5_2 <- mutate(a5_1, 근태평점 = case_when(근태점수 >=  0 & 근태점수 <= 20 ~ "1",
                                          근태점수 >= 20 & 근태점수 <= 40 ~ "2",
                                          근태점수 >= 40 & 근태점수 <= 60 ~ "3",
                                          근태점수 >= 60 & 근태점수 <= 80 ~ "4",
                                          근태점수 >= 80 & 근태점수 <= 100 ~ "5",
                                          TRUE ~ "NA"))
                                          
a5_2
head(a5_2)
a5_3 <- mutate(a5_2, 토익평점 = case_when(토익점수 <=600 ~ "1",
                                          토익점수 > 600 & 토익점수 <= 800 ~ "2",
                                          토익점수 > 800 ~ "3",
                                          TRUE ~ "NA"))
a5_3
str(a5_3) # 변수별 데이터 유형 확인

a5_3$근태평점 <- as.integer(a5_3$근태평점) # 정수형태로 변환
a5_3$토익평점 <- as.integer(a5_3$토익평점) # 정수형태로 변환

a5_4 <- mutate(a5_3, 총평가점수 = 업무성과 + 근태평점 + 토익평점)
str(a5_3)

head(a5_3)

# 기술통계량 
summary(a5_3$토익점수) # 토익점수의 기술통계량

str(a5_3)
a5_3 %>% # 그룹 별 토익 점수의 기술통계량
  group_by(부서) %>% 
  summarise(평균 = mean(토익점수),
              표준편차 = sd(토익점수),
              중위수 = median(토익점수),
              최대값 = max(토익점수)) %>%
  ggplot(aes(부서, 평균)) +
  geom_bar(stat='identity')

# 그래프 색상 변경을 위한 패키지 설치
install.packages('tidyverse')
library('tidyverse')
install.packages('colorspace')
library(colorspace)

hcl_palettes() # 색상표 확인
hcl_palettes(plot = TRUE) # 색상표 그림으로 확인
hcl_palettes('qualitative', plot = TRUE) # 데이터 유형별 색상표 그림으로 확인
qualitative_hcl(7, palette = 'Pastel 1') # Qualitative의 Paster 1에 있는 색상표 확인

a5_3 %>%
  group_by(부서) %>%
  summarize(mean = (mean(토익점수)) %>%

# ggplot 샘플

x <- c(1, 2, 3, 4, 5)
y <- c(2, 4, 6, 8, 10)

test <- data.frame(x = x, y = y)

ggplot(test, aes(x = x, y = y)) + 

    geom_point() +

  labs(title = "산점도")


# 그래프(히스토그램)
cap <- read.csv('cap.csv')
head(cap)
a1_1 <- ggplot(cap, 
               aes(x = rotate.power)) + 
  geom_histogram(fill = 'skyblue',
                 color = 'black')
a1_1

a1_3 <- ggplot(cap, aes(x = rotate.power)) + 
  geom_histogram(fill = 'skyblue',
                 color = 'black',
                 bins = 15,
                 binwidth = 2)
a1_3

a1_4 <- a1_3 + 
  labs(x = '회전력', # x축 이름 설정
       y = '빈도', # y축 이름 설정
       title = '회전력 히스토그램',) + # 그래프 제목 이름 설정
  theme_bw() + # 배경화면 흰색으로
  theme(plot.title = element_text(hjust = 0.5, size = 15, face = "bold"),
        axis.title = element_text(size = 15), # 축값 변경
        axis.text = element_text(size = 15)) # 축 제목 변경

a1_4

a2_1 <- a1_4 + geom_vline(xintercept = 12,
                          linetype = 'dashed', color = 'red') +
               geom_vline(xintercept = 33,
                          linetype = 'dashed', color = 'red')
a2_1

a2_2 <- a2_1 + annotate('text', x = 11, y = 13, label = '12', col = "red") +
               annotate('text', x = 34, y = 13, label = '33', col = 'red')
a2_2

# 데이터 레이블 표시
a3_1 <- a2_2 + 
  stat_bin(aes(label = ..count..), # ..count.. : 빈도
           geom = "text", # 텍스트 형태로 추가
           vjust = -0.5, # 막대 기준 수직 위치 이동
           hjust = 0.5, # 막대 기준 수평 위치 이동
           bins = 15, # 막대 개수
           binwidth = 2) # 막대 너비
a3_1

cap$machine <- as.character(cap$machine)
str(cap)
a4_2 <- ggplot(cap, aes(x = rotate.power, fill = machine)) +
        geom_histogram(aes(y = ..density..),
                       position = 'identity',
                       alpha = 0.5,
                       bins = 15,
                       binwidth = 2) +
        geom_density(alpha = 0.3)
a4_2

# 상자 그림(1)

shop <- read.csv('상점별 판매량.csv') # 데이터 불러오기 
head(shop)

b1_1 <- ggplot(shop, aes(y=Sales)) +
  geom_boxplot(fill = 'orange',
               color = 'blue')
b1_1

b1_2 <- ggplot(shop, aes(x = Location, y=Sales, fill = Location)) +
  geom_boxplot()
b1_2

b2_1 <- b1_2 + 
          stat_summary(fun = "mean", # function = 평균
                       geom = "point", # 형태 = 점
                       shape = 21, # 모양 유형
                       size = 2, # 모양 크기
                       fill = "red") # 모양 색상
b2_1
?stat_summary

# 상자 그림(2)

pipe <- read.csv('파이프2.csv')
head(pipe)
View(pipe)
str(pipe)

# 주 별로 상자 그림 그리기
pipe$week <- as.factor(pipe$week) # 데이터 유형 변경
c1_1 <- ggplot(pipe, aes(x = week,
                         y = diameter,
                         fill = week)) +
        geom_boxplot()
c1_1

# 기계별로 주에 따라 상자그림 그리기
pipe$machine <- as.factor(pipe$machine) # 데이터 유형 변경
c2_1 <- ggplot(pipe, aes(x = week,
                         y = diameter,
                         fill = machine)) +
  geom_boxplot() +
  facet_wrap(~machine) # 분할해서 그릴 때 사용하는 함수
c2_1

# 상관분석과 산점도
scatter.plot <- read.csv('작업속도와 결함률.csv')
head(scatter.plot)
a1 <- ggplot(scatter.plot, aes(x = Work.Velocity,
                               y = Error.Rate)) +
      geom_point()
a1
# 상관분석
a2 <- cor.test(scatter.plot$Work.Velocity, scatter.plot$Error.Rate)
a2

a3 <- ggplot(scatter.plot, aes(x = Work.Velocity,
                               y = Error.Rate)) +
  geom_point() +
  stat_smooth(method = 'lm') # 회귀직선 추가
a3

# 그룹 별 산점도 그리기
scatter.plot2 <- read.csv('작업속도와 결함률_방법.csv')

a4 <- ggplot(scatter.plot2, aes(x = Work.Velocity,
                                y = Error.Rate,
                                color = Method)) + # color로 구분
      geom_point()
a4

a5 <- ggplot(scatter.plot2, aes(x = Work.Velocity,
                                y = Error.Rate,
                                color = Method)) + # color로 구분
  geom_point() + 
  geom_smooth(method = 'lm', se = FALSE)
a5

scatter.plot3 <- scatter.plot2[-c(101:105), ] # 101-105번째 행까지 삭제
tail(scatter.plot3)

a6 <- ggplot(scatter.plot3, aes(x = Work.Velocity,
                                y = Error.Rate,
                                color = Method)) + # color로 구분
  geom_point() + 
  geom_smooth(method = 'lm', se = FALSE)
a6

# 막대 그래프

cate <- read.csv('categorical.csv') # cate라는 객체로 데이터 불러오기
head(cate) # 데이터 확인 
ggplot(cate, aes(x = sex)) + # 성별 막대 그래프
	geom_bar() # 막대 그래프 함수

ggplot(cate, aes(x = sex, fill = disease) +
	geom_bar(position = 'dodge') + 
	theme_bw() + # 배경색을 흰 바탕으로 변경
	ggtitle('성별에 따른 질병 수') + # 그래프 제목
	theme(plot.title = element_text(family = 'notosanskr', # 제목 폰트
				    face = 'bold', #제목 폰트 형태
				    hjust = 0.5)) + # 정렬(가운데)
	labs(x = '성별', y = '빈도', fill = '질병명') + # 축 이름 변경, fill은 범례
	geom_text(stat = "count", aes(label = ..count..), # 레이블 표시 및 위치 설정
		position = position_dodge(width = 1), vjust = -0.5)
	

# 정규성 검정

tile <- read.csv('타일.csv')
qqnorm(tile$warp, col = 'red') # 점
qqline(tile$warp) # 선

shapiro.test(tile$warp) # Shapiro-Wilk test
install.packages('nortest') # Anderson-Darling test를 위한 패키지 설치 'nortest'
library(nortest)
ad.test(tile$warp) # Anderson-Darling test

# 1표본 t 검정(정규성 검정)

Tuna.Can <- read.csv('참치캔.csv') # 데이터 불러오기
head(Tuna.Can)
Tuna.Can <- rename(Tuna.Can, tuna = 참치캔) # dplyr 함수 이용 변수명 변경(앞:신규, 뒤:기존)

ad.test(Tuna.Can$tuna) # 정규성 검정

# 1표본 t 검정
t.test(Tuna.Can, mu = 150) # 단측검정 시 alternative = 'greater' 또는 'less' 추가
# 예: t.test(Tuna.Can, mu = 150, alternative = 'less')

# 검정력
power.t.test(n = 15, delta = 2.5, sd = 5.09, sig.level = 0.05, type = "one.sample")
            
# 표본 크기 결정
power.t.test(delta = 2.5, sd = 5.09, sig.level = 0.05, power = 0.8, type = "one.sample")
      
energy <- read.csv('에너지 소비량.csv')
            Energy.Elec <- filter(energy, Ventilation.Machine == 1) # 데이터 분할 
            Energy.Heat <- filter(energy, Ventilation.Machine == 2)
head(Energy.Elec)
head(Energy.Heat)            
ad.test(Energy.Elec$Energy.Consume) # AD 검정 결과
ad.test(Energy.Heat$Energy.Consume)

# 등분산 검정

var.test(Energy.Elec$Energy.Consume, Energy.Heat$Energy.Consume)

# 2 표본 t 검정
t.test(Energy.Elec$Energy.Consume, Energy.Heat$Energy.Consume, var.equal = TRUE)

# 쌍체 t-검정

shoes <- read.csv('shoes.csv') # 데이터 불러오기

t.test(shoes$materials.A, shoes$materials.B, paired = TRUE)

# diff 라는 파생변수를 생성하여 n_shoes로 저장 
n_shoes <- mutate(shoes, diff = materials.A - materials.B)
# 평균을 0으로 하는 1-표본 t 검정 결과와 비교
t.test(n_shoes$diff, mu = 0)

# 카이제곱 검정

bp.freq.table = table(cate$sex, cate$disease) # 이원표 생성
bp.freq.table

chisq.test(cate$sex, cate$disease, correct = FALSE)


# 분산분석(One-way)

pro_rate1 <- read.csv('기계1.csv')
pro_rate2 <- read.csv('기계2.csv')
str(pro_rate1)
str(pro_rate2)

# 정규성 검정
shapiro.test(pro_rate2$Company.A)
shapiro.test(pro_rate2$Company.B)
shapiro.test(pro_rate2$Company.C)

# 등분산 검정
# 세 집단 이상일 경우 Levene 검정 사용
# car 패키지 활용
install.packages('car')
library(car)
# Levene 등분산 검정
leveneTest(Product ~ Company, data = pro_rate1)

# 일원분산분석
oneway <- aov(Product ~ Company, data = pro_rate1)
summary(oneway)

# 내장함수를 이용한 잔차 그림 그리기
par(mfrow = c(1, 1))
plot(oneway, 1)
plot(oneway, 2)

# 사후검정(Tukey)
tukey.result <- TukeyHSD(oneway)
tukey.result

# 이원분산분석
twoway <- read.csv('twowayanova.csv')
head(twoway)
str(twoway)
twoway$근로자 <- as.character(twoway$근로자)
twoway_model <- aov(data = twoway, 생산량 ~ 회사명+근로자)
summary(twoway_model)
print(model.tables(twoway_model, "mean"), digits = 2)


# 사이트 소개
https://www.datanovia.com/en/blog/gganimate-how-to-create-plots-with-beautiful-animation-in-r/
http://ds.sumeun.org/?p=1089