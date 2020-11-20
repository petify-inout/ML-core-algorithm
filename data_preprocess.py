import pandas as pd
from data_preprocess_util import symp_counter
import csv 
from data_preprocess_util import iniData 
import numpy as np
from data_preprocess_util import egGenerater
from data_preprocess_util import dataArrange 
from data_preprocess_util import del_duplicates
from data_preprocess_util import symp_process
import pickle

def data_preprocess() :
    with open('symptoms.csv' , 'r') as csv_file0:
        csv_reader0 = csv.reader(csv_file0)    
        del_duplicates(csv_reader0)


    with open('new_raw_data.csv' , 'r') as csv_file:
        csv_reader = csv.reader(csv_file) 
        with open('new_data.csv' , 'w',newline = '') as csv_file1:
            csv_writer = csv.writer(csv_file1)
            for line in csv_reader:
                new_row = []
                for i in line:
                    i = symp_process(i)
                    new_row.append(i)
                csv_writer.writerow(new_row) 


    with open('new_data.csv' , 'r') as csv_file:
        csv_reader = csv.reader(csv_file) 
        symp_list,counter_obj,disease_list,disease_obj = symp_counter(csv_reader)

            
        csv_file.seek(0)
        revised_iniData_matrix,disease_index  = iniData( symp_list, csv_reader)
        revised_iniData= pd.DataFrame(revised_iniData_matrix,columns =  symp_list,index = disease_index)
        with open('symp_model','wb') as model_file:
            pickle.dump(symp_list,model_file)

    for i in range(len(disease_obj)):
        for j in range(10):
            item = egGenerater(disease_obj[i].selectionPool,disease_obj[i].max_val)
            item_to_append  = dataArrange(symp_list,item) 
            item_df = pd.DataFrame([item_to_append],columns = symp_list,index = [disease_obj[i].name])
            revised_iniData = revised_iniData.append(item_df)
            


    return revised_iniData

