evaluate () {
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $1 -m learn -a nivreeager 
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $2 -m parse -o $3_a
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $1 -m learn -a stackproj 
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $2 -m parse -o $3_s
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $1 -m learn -a covnonproj 
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $2 -m parse -o $3_c
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $1 -m learn -a stacklazy 
java -jar ../maltparser-1.9.2/maltparser-1.9.2.jar -c test -i $2 -m parse -o $3_l
python3 strip_comments.py $2 $4
python3 strip_comments.py $3_a $5_a
python3 strip_comments.py $3_s $5_s
python3 strip_comments.py $3_c $5_c
python3 strip_comments.py $3_l $5_l
java -jar ../dist-20141005/lib/MaltEval.jar -g $4 -s $5_a $5_s $5_c $5_l
}

for i in {1..10}
do
    evaluate xv/train$i.conll xv/test$i.conll xv/out$i.conll xv/teststripped$i.conll xv/outstripped$i.conll
done
