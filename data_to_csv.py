import json

csv_string = ""
with open("data.json", "r") as read_file:
    json_data = json.load(read_file)
    csv_string = json_data["data"].replace("\n", "\n")

with open("data.csv", "w") as text_file:
    text_file.write(csv_string)

