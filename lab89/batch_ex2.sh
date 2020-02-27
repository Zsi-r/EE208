#/bin/bash

command='hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -files mapper-ex2.py,reducer-ex2.py -mapper mapper-ex2.py -reducer reducer-ex2.py'
rm='hadoop fs -rm -r '
cp2local='hadoop fs -copyToLocal '
input='ex2_input'
for ((i=1;i<$1+1;i++));
do
    echo "Processing $i"
    output="ex2_output$i"
    eval "$command -input $input -output $output"
    input=$output
    eval "$rm $input/_SUCCESS"
done
mkdir /home/hduser/ex2_result
eval "$cp2local $output/* /home/hduser/ex2_result"
