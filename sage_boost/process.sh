echo "Model,Identifier,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef" >> log/logs.csv

StringVal="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq n2v"
Identifiers="$@"

for model in $StringVal
do
    for id in $Identifiers
    do
        echo -n "${model},${id}," >> log/logs.csv
        emb_filename="${model}_${id}/emb.csv"
        es_filename="${model}_${id}/emb_out.csv"
        python sage_boost.py $emb_filename $es_filename >> log/logs.csv
    done
done       
