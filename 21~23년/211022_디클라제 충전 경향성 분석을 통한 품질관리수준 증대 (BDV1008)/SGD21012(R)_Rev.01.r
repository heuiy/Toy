library(dplyr)

number = c(0:57)

sample(45, 6)

rty = c(87.0,
74.6,
70.9,
61.0,
68.9,
59.2,
72.9,
71.0,
79.9,
76.1,
68.8,
81.0,
81.6,
81.7,
84.6,
81.4,
75.6,
77.6,
77.4,
69.7,
86.8,
76.4,
69.5,
79.4,
83.6,
81.9,
76.0,
83.5,
82.7,
74.8,
80.8,
82.1,
83.0,
81.6,
88.3,
79.3,
87.2,
86.1,
75.7,
72.3,
78.9,
79.1,
83.2,
77.8,
65.4,
72.7,
71.8,
71.8,
72.1,
77.7,
83.8,
86.4,
84.1,
79.5,
76.9,
68.0,
70.3,
59.3)

df = data.frame(number, rty)
head(df, 3)

df_raw = df

df <- df_raw

boxplot(df$rty)

summary(df$rty)

dim(df)

boxplot.stats(df$rty)$stats[5]

df <- df %>% filter(df$rty>boxplot.stats(df$rty)$stats[1], # Y 최소값 (Q1 - 1.5 * IQR) 이하 제거
                    df$rty<boxplot.stats(df$rty)$stats[5]) # Y 최대값 (Q3 + 1.5 * IQR) 이상 제거
dim(df)

mean(df$rty)

sd(df$rty)

mean(df$rty) - sd(df$rty)

mean(df$rty) - 2*sd(df$rty)

mean(df$rty) - 3*sd(df$rty)

# End



