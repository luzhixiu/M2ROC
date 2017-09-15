export CLASSPATH=$CLASSPATH:/home/lu/Downloads/weka-3-8-1/weka.jar
java -Xmx1024M -Xms512M weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.InfoGainAttributeEval -M" -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308" -i ../../Desktop/rawiris.csv -o out.csv

