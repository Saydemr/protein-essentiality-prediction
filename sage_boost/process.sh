echo "Model,Class,LR,Accuracy,F1_Score,Roc_Auc,Precision,Recall" > log/logs_unsup_new.csv

organism="$1"
Models="graphsage_maxpool graphsage_meanpool n2v"

for option in 0 1 2 3 4
do
    for identity_dim in 32
        do
            for lr in 0.005 0.001 0.0001
            do
                for epoch in 2
                do
                    for batch_size in 32
                    do
                        for model in $Models
                        do
                            emb_filename="./unsupervised/org${organism}_e${epoch}_b${batch_size}_id${identity_dim}_opt${option}/unsup-example_data/${model}_small_${lr}/emb.csv"
                            es_filename="./unsupervised/org${organism}_e${epoch}_b${batch_size}_id${identity_dim}_opt${option}/unsup-example_data/${model}_small_${lr}/emb_out.csv"

                            if [ -f $emb_filename ]; then
                                echo -n "${option},${model},${lr}," >> og/logs_unsup_new.csv
                                python3 sage_boost.py $emb_filename $es_filename >> log/logs_unsup_new.csv
                            fi
                        done
                    done
                done
            done
        done
    done
done
