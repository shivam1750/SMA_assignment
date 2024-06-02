import xml.etree.ElementTree as ET
import csv
import os
from collections import defaultdict

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    test_cases = defaultdict(float)
    for testcase in root.findall(".//testcase"):
        classname = testcase.get("classname")
        time = float(testcase.get("time"))
        test_cases[classname] += time
    return test_cases

def group_testcases(test_cases):
    sorted_testcases = sorted(test_cases.items(), key=lambda item: item[1], reverse=True)
    group_size = len(sorted_testcases) // 5
    groups = {}
    for i in range(5):
        start = i * group_size
        end = (i + 1) * group_size if i < 4 else len(sorted_testcases)
        groups[i + 1] = sorted_testcases[start:end]
    return groups

def write_csv(groups, output_file):
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["classname", "time", "groupNo"])
        for group_no, testcases in groups.items():
            for testcase in testcases:
                writer.writerow([testcase[0], testcase[1], group_no])

if __name__ == "__main__":
    data_dir = "programming/assignment-1/data/"
    output_file = "programming/assignment-1/output.csv"
    test_cases = defaultdict(float)
    for filename in os.listdir(data_dir):
        if filename.endswith(".xml"):
            file_path = os.path.join(data_dir, filename)
            test_cases.update(parse_xml(file_path))
    groups = group_testcases(test_cases)
    write_csv(groups, output_file)