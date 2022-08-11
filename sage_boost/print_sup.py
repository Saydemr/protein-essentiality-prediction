import os

models = ["gcn", "graphsage_maxpool", "graphsage_mean", "graphsage_meanpool", "graphsage_seq"]
organism = "hs"
with open('./log/logs_sup_new.csv', 'w+') as log_csv:
    log_csv.write('Option,Model,Accuracy,F1,ROC_AUC,Precision,Recall,TestorVal\n')
    for model in models:
        for option in range(5):
            base_dir = './supervised_old/org{}_id_opt{}/sup-example_data/{}_small_{}/'.format(organism,option,model)
            test_txt = base_dir + 'test_stats.txt'
            if os.path.isfile(test_txt):
                with open(test_txt, 'r') as test_txt:
                    test_line = test_txt.readline().strip().replace('=', ' ').split()
                    log_csv.write('{},{},{},{},{},{},{},{},Test\n'.format(option,model,test_line[3],test_line[5],test_line[7],test_line[9],test_line[11]))

            val_txt = base_dir + 'val_stats.txt'
            if os.path.isfile(val_txt):
                with open(val_txt, 'r') as val_txt:
                    val_line = val_txt.readline().strip().replace('=', ' ').split()
                    log_csv.write('{},{},{},{},{},{},{},{},Val\n'.format(option,model,test_line[3],test_line[5],test_line[7],test_line[9],test_line[11]))
    