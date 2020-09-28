library(lubridate)
library(tidyverse)
library(udpipe)

today = today()
fn <- function(sentence, old_sentence_id) udpipe_annotate(ud_gd, sentence) %>% 
  as.data.frame() %>% mutate(sentence_id = old_sentence_id)

m <- udpipe_train(file = str_glue("{today}.udpipe"), 
                  files_conllu_training = "gd_arcosg-ud-train.conllu", 
                  files_conllu_holdout = "gd_arcosg-ud-dev.conllu")
ud_gd <- udpipe_load_model(str_glue("{today}.udpipe"))
gold <- udpipe_read_conllu('gd_arcosg-ud-test.conllu')
text <- gold %>% select(sentence, sentence_id) %>% unique()
result <- pmap_dfr(text %>% rename(old_sentence_id = sentence_id), fn)

las <- gold %>% 
  inner_join(result, by=c("sentence_id", "token_id", "head_token_id", "dep_rel")) %>% 
  nrow()/nrow(gold)
ulas <- gold %>% 
  inner_join(result, by=c("sentence_id", "token_id", "head_token_id")) %>% 
  nrow()/nrow(gold)
accuracy <- udpipe_accuracy(ud_gd, 'gd_arcosg-ud-test.conllu')