export CLASSPATH=$CLASSPATH:/home/lu/eclipse-workspace/LabTool/weka-3-8-1/weka.jar

echo "inputfile": $1
echo "outputfolder": $2

java -Xmx2048M -Xms1024M weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.InfoGainAttributeEval -M" -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308" -i $1 -o $2/InformationGain.csv

java -Xmx2048M -Xms1024M weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.GainRatioAttributeEval -M" -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308" -i $1 -o $2/GainRatio.csv

java -Xmx2048M -Xms1024M weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.ReliefFAttributeEval -M -1 -D 1 -K 10" -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308" -i $1 -o $2/Relief.csv

java -Xmx2048M -Xms1024M weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.SymmetricalUncertAttributeEval " -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1" -i $1 -o $2/SymmetricalUncertainty.csv

java -Xmx2048M -Xms1024M weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.OneRAttributeEval -S 1 -F 10 -B 6 " -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1" -i $1 -o $2/OneVsRest.csv


