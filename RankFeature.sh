

export CLASSPATH="/home/lu/eclipse-workspace/LabTool1/weka-3-8-1/weka.jar"
echo $CLASSPATH
echo "inputfile": $1
echo "outputfolder": $2

java weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.InfoGainAttributeEval -M" -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308" -i $1 -o $2/InformationGain.csv

java weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.GainRatioAttributeEval -M" -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308" -i $1 -o $2/GainRatio.csv

java weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.ReliefFAttributeEval -M -1 -D 1 -K 10" -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308" -i $1 -o $2/Relief.csv

java weka.filters.supervised.attribute.AttributeSelection  -E "weka.attributeSelection.SymmetricalUncertAttributeEval " -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1" -i $1 -o $2/SymmeUncertain.csv



