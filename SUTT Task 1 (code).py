import pandas as pd
import json

#reading the excel file
df = pd.read_excel('Timetable Workbook - SUTT Task 1.xlsx', sheet_name='S1',skiprows=1)

#renaming rows
column_mapping = {
    "COURSE NO.":"course_code",
    "COURSE TITLE":"course_title",
    "SEC":"sections",
    "INSTRUCTOR-IN-CHARGE \/ Instructor":"instructors",
    "ROOM":"room",
    "DAYS & HOURS":"day",
    "CREDIT":"L",
    "Unnamed: 4":"P",
    "Unnamed: 5":"U",
    "INSTRUCTOR-IN-CHARGE / Instructor" : "instructors",
}
df.rename(columns = column_mapping, inplace = True)

#removing unneccesary rows
coulumns_to_remove = ["COM COD","MIDSEM DATE & SESSION","COMPRE DATE & SESSION"]
df.drop(columns=coulumns_to_remove,inplace=True)
credit_edit = df.loc()

#converting to json file
df.to_json('SUTT Task 1 Output.json',orient='records',indent=4)

#removing nulls 
with open("SUTT Task 1 Output.json", "r") as file:
    data = json.load(file)
def remove_nulls(obj):
    if isinstance(obj, dict):
        return {k: remove_nulls(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_nulls(item) for item in obj if item is not None]
    else:
        return obj

cleaned_data = remove_nulls(data)

with open("SUTT Task 1 Output.json", "w") as file:
    json.dump(cleaned_data,file,indent=4)
    
# removing the credit row
with open("SUTT Task 1 Output.json", "r") as file:
    data = json.load(file)
remove_row = data[1:]
with open("SUTT Task 1 Output.json", "w") as file:
    json.dump(remove_row,file,indent=4)    

#making a credit list and moving L,P,U into it
with open("SUTT Task 1 Output.json", "r") as file:
    data = json.load(file)
credit_L = data[0]["L"]
credit_P = data[0]["P"]
credit_U = data[0]["U"]
credit =  {'lectures' : credit_L,'practicals' : credit_P,'units' : credit_U}
data[0]["credits"] = credit
del data[0]["L"]
del data[0]["P"]
del data[0]["U"]
with open("SUTT Task 1 Output.json", "w") as file:
    json.dump(data,file,indent=4)

#extracting section data
with open("SUTT Task 1 Output.json", "r") as file:
    data = json.load(file)
instructors = []
exists = False
for i in range (len(data)):
    if data[i]["sections"]:
        exists = True
        sections = data[i]["section"]
        data[1]["sections"].append(data[i]["intructors"])
with open("SUTT Task 1 Output.json", "w") as file:
    json.dump(data,file,indent=4)
