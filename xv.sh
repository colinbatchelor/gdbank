evaluate () {
    ~/udpipe-1.2.0-bin/bin-linux64/udpipe --tokenizer=none --tagger=none --train xv_models/ud$6.model --parser=transition_system=projective < $1 
    ~/udpipe-1.2.0-bin/bin-linux64/udpipe --parse xv_models/ud$6.model < $2 > $3_a
    ~/udpipe-1.2.0-bin/bin-linux64/udpipe --tokenizer=none --tagger=none --train xv_models/uds$6.model --parser=transition_system=swap < $1 
    ~/udpipe-1.2.0-bin/bin-linux64/udpipe --parse xv_models/uds$6.model < $2 > $3_s
    ~/udpipe-1.2.0-bin/bin-linux64/udpipe --tokenizer=none --tagger=none --train xv_models/udl$6.model --parser=transition_system=link2  < $1 
    ~/udpipe-1.2.0-bin/bin-linux64/udpipe --parse xv_models/udl$6.model < $2 > $3_l

    python3 strip_comments.py $2 $4
    python3 strip_comments.py $3_a $5_a
    python3 strip_comments.py $3_s $5_s
    python3 strip_comments.py $3_l $5_l
    java -jar ../dist-20141005/lib/MaltEval.jar -g $4 -s $5_a $5_s $5_l >> xv_results.txt
}

touch xv_results.txt
mkdir xv_models
for i in {1..10}
do
    evaluate xv/train$i.conll xv/test$i.conll xv/out$i.conll xv/teststripped$i.conll xv/outstripped$i.conll $i
done
