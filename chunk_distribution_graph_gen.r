
library(ggplot2)
library(foreach)

tsv_dir <- 'H:\\work_images\\tsvs'

files <- list.files(tsv_dir, pattern = "*.tsv", full.names=TRUE)

res <- foreach(i=files, .combine=rbind) %dopar% {
  df <- read.csv(i, sep="\t", header=TRUE)
  df
}

ggplot() + geom_bar(data = res, aes(Phone, fill = Category), width = 0.5, position = "fill") + ylab("Chunk distribution") + theme(axis.text.x = element_text(angle = 45, hjust = 1));