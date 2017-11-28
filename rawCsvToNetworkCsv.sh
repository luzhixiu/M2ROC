name="rawiris.csv"

line1=$(head -n 1 $name)
arr1=(${line1//,/ })
echo -n ''>out1.csv
for ((i=0;i<${#arr1[@]};i++));
do
    echo -n attribute$i>>out1.csv
    echo -ne "\t">>out1.csv
done

cnt=0
while read line ;
do
    let cnt+=1
    echo ''>>out1.csv
    echo -n "sample"$cnt>>out1.csv
    arr=(${line//,/ })
    unset 'arr[${#arr[@]}-1]'
    for i in "${arr[@]}";
    do
        echo -ne '\t'$i>>out1.csv
    done
done <$name
echo ''>>out1.csv
sed 's/.$//' out1.csv>out.csv
rm out1.csv
