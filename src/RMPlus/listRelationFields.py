import re

#Testing
if __name__ == '__main__' :
    # 读取SQL脚本文件
    with open(r'D:\Working\02WeeklyWorking\0ThisWeek\changed_tables_2024-05-29.txt', 'r', encoding='UTF-8') as file:
        sql_content = file.read()

    # 使用正则表达式匹配表名和字段定义
    table_defs = re.findall(r'CREATE TABLE (\w+)(?:\((.+?)\))?', sql_content, re.DOTALL)
    field_matches = re.findall(r'\s+(\w+)\s+(\w+)', sql_content)

    # 构建表名到字段的映射
    table_fields = {table: set(fields) for table, fields in table_defs for field in re.findall(r'\s+(\w+)\s+(\w+)', fields)}

    # 推测可能的关联
    possible_relations = []
    for table1, fields1 in table_fields.items():
        for table2, fields2 in table_fields.items():
            if table1 != table2:
                # 寻找相同的字段名或相似的字段名（这里简化处理，实际可以根据需要调整相似度判断）
                common_fields = fields1.intersection(fields2)
                if common_fields:
                    possible_relations.extend([(f"{table1}.{field}", f"{table2}.{field}") for field in common_fields])

    # 打印可能的关联
    for relation in possible_relations:
        print(relation)
