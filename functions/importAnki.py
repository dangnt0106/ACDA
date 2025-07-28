import csv

def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Ví dụ sử dụng
csv_file = "F:/studyingJapanese/csv/tuvung_0715.csv"
rows = read_csv(csv_file)
# for row in rows:
#     print(row)

my_list = list(rows)  # Đưa toàn bộ dữ liệu vào một list

# print(my_list)

# Lấy dữ liệu cột đầu tiên của từng dòng trong my_list
first_column = [row[0] for row in my_list if row]  # Kiểm tra row không rỗng

print(first_column)

def save_list_to_csv(data_list, file_path):
    with open(file_path, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data_list:
            writer.writerow(row)

# Ví dụ sử dụng
output_csv = "F:/studyingJapanese/csv/output.csv"
save_list_to_csv(my_list, output_csv)