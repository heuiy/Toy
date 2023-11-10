# MBB 기본교육 시 설치한 패키지
install.packages("dplyr")       #데이터프레임 다루기
install.packages("tidyr")
install.packages("ggplot2")     #시각화용 패키지
install.packages("SixSigma")
install.packages("MASS")

# 추가 설치 패키지
install.packages("lattice")
install.packages("tigerstats")   #기초 통계학 교육용 패키지
install.packages("vioplot")      #violin plot 작성용
install.packages("fitdistrplus") # 적합한 분포 찾기
install.packages("qcc")          #관리도, 공정능력분석 등
install.packages("moments")      #적률(moment) 계산: 왜도, 첨도 등


#참고) "failed to lock directory..." Error로 패키지 설치 안될 때는 
# 아래 함수를 실행시켜 lock 해제 후 install.packages() 실행
options("install.lock"=FALSE) 


# 패키지 Loading
library("tigerstats")
library("dplyr")
library("tidyr")
library("lattice")
library("ggplot2")
library("vioplot")
library("SixSigma")
library("MASS")
library("fitdistrplus")
library("qcc")
library("moments")

# 9/16 : DX-LSS 교재 1-5항 복습 

#Read Exel
install.packages("readxl") # 인스톨 : 완료
library("readxl") # 불러오기 : 완료

ufdata = read_excel("ufdata.xlsx") # 데이터 불러오기
head(ufdata) # A tibble: 6 x 82 데이터 확인
str(ufdata) # tibble [117 x 82] 데이터 확인
dim(ufdata) # [1] 117  82 데이터 확인 



#내장함수연습 
B = seq(1,10)
B
sample(B,3)
A = sum(B)
A

colnames(ufdata)
ufdata
select(.,Yield)
ufdata_CIP %>% select(CIP Feed,"ufdata") #??? 안되는데??
ufdata %>% select(Yield)
ufdata %>% select(`CIP NWP`)

summary(ufdata) # 데이터 전체의 요약통계량 확인
boxplot(ufdata$Yield) # 수율의 이상치 확인 
hist(ufdata$Yield)
pairs(ufdata) # 상관행렬도


ufdata2 = read_excel("ufdatanum.xlsx")
boxplot(ufdata$`CIP NWP`)

#9/19
select%>%(Storage NWP, ufdata) # ??

#O-ring Groove Depth 문제 풀이 차용하여 M 단계 진행


# 현수준측정 ) 정규성 검정
qq1 =  qqnorm(ufdata$Yield, main = 'Q-Q Plot - 정규분포확인') #   #Q-Q Plot 확인
qqline(ufdata$Yield)

# 현수준측정 ) Shapiro-Wilk 검정
shapiro.test(ufdata$Yield)


# 공정 안정성 확인 ) 이상원인은 없는지 확인하기 위해 관리도를 그려 확인한다.
boxplot(ufdata$Yield) #  수율의 이상치 여부 확인 
install.packages("qcc")          #관리도, 공정능력분석 등
library("qcc")
I_MR = qcc.groups(data = ufdata$Yield, sample=ufdata$`batch No`)
I_MR
qcc(I_MR, type="xbar.one") # IMR 차트


abline(h = 1.5, lwd = 2, col="red") # 타켓표시 



# 9/19일의 하이라이트 공정능력 분석

# 공정능력분석

install.packages("SixSigma")
install.packages("qcc") 
library("SixSigma")
library("qcc")

ss.study.ca(ufdata$Yield, LSL=80.0,USL=90.0, T=84.0, 
            f.sub="UF yiled", alpha=0.05) 
# Pp=0.81, Ppk=0.74, 장기 공정능력

# 장기 시그마 수준 Z(LT) 산출
Z.lt = ss.ca.z(ufdata$Yield, LSL=80.0, USL=90.0, LT=FALSE) 
Z.lt# Z.lt=2.21                                                 


# 단기 시그마 수준 Z(ST) & Z(shift) 산출
Mean = 84.5         # 평균
StDev.st = 2.04     # 단기 표준편차
LSL = 80.0          # Lower Spec. Limit
USL=90.0            # Upper Spec. Limit
Z.st = qnorm(1-p.total, mean=0, sd=1)# 단기 시그마 수준
Z.st # 2.21
Z.shift = Z.st - Z.lt # Z(shift) = Z(ST)-Z(LT) = 0.0
Z.shift # 0.0

# 참고 
par(mfrow=c(1,1))


# 9/27

#Analyze 

#Read Excel
install.packages("readxl")
library("readxl")

# 데이터 불러오기
ufdata = read_excel("ufdata_raw.xlsx") 
str(ufdata)
head(ufdata)

# 결측치 제거 :  complete.case   
ufdata_comp <- ufdata[complete.cases(ufdata),]
dim(ufdata_comp)

# 정규성 검증
shapiro.test(ufdata_comp$Y)
qq1 =  qqnorm(ufdata_comp$Y, main = 'Q-Q Plot - 정규분포확인')
qqline(ufdata_comp$Y)
hist(ufdata_comp$Y)


# 이상치 확인 
boxplot(ufdata_comp$Y)
boxplot(ufdata_comp$Y)$stats
hist(ufdata_comp$Y)
dim(ufdata_comp)

# 79.2 이하의 값이 1개 있으며 이상치로 확인되어 제거가 필요하다.
#이상치 제거 : 필터 함수로 79.2 이하의 값을 제거한다.

install.packages("dplyr")
library(dplyr)

ufdata_outlier = ufdata_comp %>% filter(., Y>79.23)
dim(ufdata_outlier)
hist(ufdata_outlier$Y)
boxplot(ufdata_outlier$Y)$stats 


# NWP 값 추가 mutate 함수  

ufdata_nwp <- ufdata_outlier %>% mutate(nwp= C6/(((C1+C2)*0.5) - C4))

dim(ufdata_nwp)
str(ufdata_nwp)

# 배치번호제거(BSPXXXXX) Select 함수
ufdata_nwp <- ufdata_nwp %>% select(-A)
str(ufdata_nwp)

# 전처리 완료 함 

shapiro.test(ufdata_nwp$Y)
qq1 =  qqnorm(ufdata_nwp$Y, main = 'Q-Q Plot - 정규분포')
qqline(ufdata_nwp$Y)
hist(ufdata_nwp$Y)


https://jaaamj.tistory.com/44 참고

# 상관행렬도1
pairs(ufdata_nwp)
plot(ufdata_nwp)
 
# 상관행렬도2 
install.packages("corrplot")
library(corrplot)

ufdata_cor = cor(ufdata_nwp)
corrplot(ufdata_cor, method = "num")

# 데이터 set 구분 

set.seed(1214)
train = sample(nrow(ufdata_nwp),nrow(ufdata_nwp)*0.7)
test = (1:c(nrow(ufdata_nwp)))[-train]
length(train)
length(test)
ufdata_train = ufdata_nwp[train,]
ufdata_test = ufdata_nwp[test,]

head(ufdata_train)
head(ufdata_test)

dim(ufdata_train)
dim(ufdata_test)
str(ufdata_train)

  
install.packages("tree")
library(tree)

# 의사결정나무ver.1 
ufdata_tree <- tree(Y~. , data = ufdata_train) 
plot(ufdata_tree);text(ufdata_tree)
summary(ufdata_tree)

# 과적합 해결
ufdata_tree2<-cv.tree(ufdata_tree)
plot(ufdata_tree2);text(ufdata_tree2)

# 의사결정나무ver.2 
prune_tree<-prune.tree(ufdata_tree,best=5) 
plot(prune_tree);text(prune_tree)
summary(prune_tree)

# 예측 값  
predict(prune_tree, ufdata_test, type = "tree")

#  결론 배치수가늘어날수록 수율은 대체적으로 낮아진다.

install.packages("caret")
library(caret)

#(R)MSE
tree.Pred = predict(prune_tree, newdata = ufdata_test)
lm.test = ufdata_test$Y
MSE(tree.Pred ,lm.test)
RMSE(tree.Pred ,lm.test)
  

# 다중회귀분석ver.1
lm.result = lm( Y ~.-C1-UF4-UF6, data = ufdata_train)
lm.result
summary(lm.result)
step(lm.result)

# 다중회귀분석ver.2
lm.fit = lm( Y ~ BC + C6 + CD1 + TM1 + UF2 ,  data = ufdata_train)
lm.fit
summary(lm.fit)

#lm.fit로 다중회귀분석 완료 

install.packages("car")
library(car)

vif(lm.fit)

lm.fit2  = lm(Y ~ BC + CD1 + TM1 + UF2, data = ufdata_train)
vif(lm.fit2)
summary(lm.fit2) 

par(mfrow=c(2,2))
plot(lm.fit2)

par(mfrow=c(1,1))

install.packages("DescTools")
library(DescTools)

#(R)MSE
lm.Pred = predict(lm.fit2, newdata = ufdata_test)
lm.test = ufdata_test$Y
MSE(lm.Pred,lm.test)
RMSE(lm.Pred,lm.test)


# 랜덤 포레스트
install.packages("MASS")
library(MASS)

install.packages("randomForest")
library(randomForest)

RF.1 = randomForest(Y ~ ., data =ufdata_train, importance = TRUE) 
RF.1 

varImpPlot(RF.1)


RF.fit = randomForest(Y~BC +UF1+UF2+UF3+nwp, data =ufdata_train, importance = TRUE)
RF.fit
varImpPlot(RF.fit) 


lm.Pred2 = predict(RF.fit, newdata = ufdata_test) # 예측값
lm.test = ufdata_test$Y
MSE(lm.Pred2,lm.test)
RMSE(lm.Pred2,lm.test) 

# RF.fit로 랜덤포레스트 완료 

#Lasso-----------------------------------
library(dplyr)
train_x <- as.matrix(ufdata_train %>% select(-Y))
train_y <- as.matrix(ufdata_train %>% select(Y))
test_x <- as.matrix(ufdata_test %>% select(-Y))
test_y <- as.matrix(ufdata_test %>% select(Y))

install.packages("glmnet")
library(glmnet)

cv_model <- cv.glmnet(train_x, train_y, alpha = 1 )
best_lambda <- cv_model$lambda.min
best_lambda
plot(best_lambda)


lasso.fit <- glmnet(train_x,train_y, alpha = 1, lambda = best_lambda)
lasso.pred <- predict(lasso.fit, s = best_lambda, newx = test_x)
lasso.pred


coef(lasso.fit)



library(DescTools)
RMSE(lasso.pred,test_y)


#Ridge-----------------------------------
cv_model <- cv.glmnet(train_x, train_y, alpha = 0 )
best_lambda <- cv_model$lambda.min
best_lambda



ridge.fit <- glmnet(train_x,train_y, alpha = 0, lambda = best_lambda)
ridge.pred <- predict(ridge.fit, s = best_lambda, newx = test_x)



coef(ridge.fit)



library(DescTools)
RMSE(ridge.pred,test_y)


# IMmprove _> 10/4일 문의 

# 각 인자별 최소, 최대값 구하기 -> 최적 조건 도출 
# 다중회귀 분석 BC , CD1 , TM1 , UF2를 유의한 인자로 선택 

## 도움이 필요합니다. 

colnames(ufdata_test)
# [1] "IB"   "BC"   "Y"    "C1"   "C2"   "C4"   "C6"   "A5"   "B5"   "PH1"  "CD1"  "TM1"  "UF1" 
# [14] "UF2"  "UF3"  "UF4"  "UF5"  "UF6"  "UF12" "nwp"
length(ufdata_test) # 20
> for(i in 1:20) #????? 
  +  A = ufdata_test[ ,i]
  +  B = A[A>boxplot(A)$stats[1]&A<boxplot(A)$stats[5]]%>%range()
  + print(data.frame(names = colnames(ufdata_test)[i], lower=B[1], Upper = B[2]))


