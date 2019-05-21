evaluate () {
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $1 -m learn
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $2 -m parse -o $3
python3 strip_comments.py $2 $4
python3 strip_comments.py $3 $5
java -jar ../dist-20141005/lib/MaltEval.jar -g $4 -s $5
}

for i in {1..10}
do
    evaluate xv/train$i.conll xv/test$i.conll xv/out$i.conll xv/test$i_.conll xv/out$i_.conll
done
