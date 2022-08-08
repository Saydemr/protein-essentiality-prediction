import os

models = ['graphsage_maxpool', 'graphsage_meanpool']
identity_dim = 32
epoch = 2
batch_size = 32
with open('./log/logs_sup_new.csv', 'w+') as log_csv:
    log_csv.write('Model,Class,LR,Accuracy,F1,ROC_AUC,Precision,Recall,Loss,TestorVal\n')
    for model in models:
        for learning_rate in [0.01, 0.001, 0.0001]:
            for option in range(5):
                base_dir = './supervised/org{}_e{}_b{}_id{}_opt{}/sup-example_data/{}_small_{}/'.format(organism,epoch,batch_size,identity_dim,option,model,learning_rate)
                test_txt = base_dir + 'test_stats.txt'
                if os.path.isfile(test_txt):
                    with open(test_txt, 'r') as test_txt:
                        test_line = test_txt.readline().strip().replace('=', ' ').split()
                        log_csv.write('{},{},{},{},{},{},{},{},Test\n'.format(option,model,learning_rate,test_line[3],test_line[5],test_line[7],test_line[9],test_line[11]]))
