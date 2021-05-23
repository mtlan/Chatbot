
heart <- read.csv("E:/project/AI/New/HeartDisease.csv", sep = ',', header = FALSE)
str(heart)
# dữ liệu heart có 304 dòng và 14 cột
dim(heart)

# lấy ra 6 dòng đầu
head(heart)













intrain <- createDataPartition(y = heart$V14, p=0.7, list = FALSE)
trainning <- heart[intrain,]
testing <- heart[-intrain,]

anyNA(heart)

summary(heart)
