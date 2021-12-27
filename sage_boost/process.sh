echo "Model,Class,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/logs_last.csv

StringVal="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq n2v"


for model in $StringVal
do
    for i in 1 2 3 4 5 6 7
    do
        emb_filename="./runs/${i}/unsup-example_data/${model}_small_0.000010/emb.csv"
        es_filename="./runs/${i}/unsup-example_data/${model}_small_0.000010/emb_out.csv"

        if [ -f $emb_filename ]; then
            echo -n "${i},${model}," >> log/logs_last.csv
            python3 sage_boost.py $emb_filename $es_filename >> log/logs_last.csv
        fi
    done
done