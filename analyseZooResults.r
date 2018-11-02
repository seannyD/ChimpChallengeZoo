try(setwd("~/Desktop/Stuff/FoxWolf/ZooResults"))
library(gplots)

d =read.table('results/05_13%H_40_39/results/rounds.csv',header=TRUE,sep=',')

d$selected = as.character(d$selected)
d$correct = as.character(d$correct)

d$all.correct = d$selected == d$correct


plotmeans(all.correct*100~latency,data=d[d$numerals==5,],ylab='Percentage Correct (%)', xlab='Latency (ms)',ylim=c(0,100),p=0.95,cex=2)
points(1,36,pch=17)
points(3.5,65,pch=17)
points(6,78.5,pch=17)

ind.mean.5nums.210ms = tapply(d[d$latency==210 & d$numerals==5,]$all.correct,d[d$latency==210 & d$numerals==5,]$name,mean,na.rm=TRUE)*100

hist(ind.mean.5nums.210ms,main = "Individuals' mean score on 5 numerals at 210ms")

ind.ntrials.5nums.210ms = tapply(d[d$latency==210 & d$numerals==5,]$all.correct,d[d$latency==210 & d$numerals==5,]$name,length)

# People getting 100% correct on 210 milliseconds for 5 numerals
ind.mean.5nums.210ms[ind.mean.5nums.210ms==100 & !is.na(ind.mean.5nums.210ms)]
# And the number of trials they did it for
ind.ntrials.5nums.210ms[ind.mean.5nums.210ms==100 & !is.na(ind.mean.5nums.210ms)]