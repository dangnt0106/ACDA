import csv
def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')        
    return reader        

csv_file = "F:/Japanese/kaiwa/kaiwa_pv.csv"
ts=read_csv(csv_file)
print(ts)

def save_list_to_csv(data_list, file_path):
    with open(file_path, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data_list:
            writer.writerow(row)

# Ví dụ sử dụng
# output_csv = "F:/studyingJapanese/csv/output.csv"
# save_list_to_csv(my_list, output_csv)