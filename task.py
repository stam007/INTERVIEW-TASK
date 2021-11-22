import pandas as pd
import json
path_input_text="input_file.txt"
path_standard_definition_json="standard_definition.json"
path_error_codes="error_codes.json"


#REPORT DICT
report={"Section":[],"Sub-Section":[],"Given DataType":[],"Expected DataType":[],"Given Length":[],"Expected MaxLength":[],"Error Code":[]}


#LOAD THE STANDARD DEFINITION
f = open(path_standard_definition_json,)
standard = json.load(f)
print("STANDARD",standard) 
f.close()

#LOAD THE ERROR CODES
m = open(path_error_codes,)
errors = json.load(m)
print("ERRORS",errors) 
m.close()




#GET DATATYPE 
def get_data_type(val):
    
  if val.replace(" ", "").isalpha():
    return "word_characters"  
  elif val.isdigit():
    return "digits"  
  return "others"  



#GET THE ERROR CODE 
def get_error_code(given_dataype,given_lenth,sub_sec):

  cond_1=False
  cond_2=False

  if given_lenth!=0 and given_lenth<=sub_sec['max_length']:
    cond_1 = True

  if given_dataype==sub_sec['data_type']:
    cond_2 = True 

  if cond_1 == False and cond_2 == False:
    return "E04"
  elif cond_1==False:
    return "E03"
  elif cond_2==False:
    return "E02"       

  return "E01"


#FILL THE REPORT BY GIVEN DATA 
def make_report(index,ln,sec_name,sub_sec):

  val_sub_sec=''
  try:
    val_sub_sec=ln[index]
  except:
    val_sub_sec= None
    
  given_dataype =None if val_sub_sec==None else get_data_type(val_sub_sec)
  given_lenth = None if val_sub_sec==None else len(val_sub_sec)
  error_code = "E05" if val_sub_sec==None else get_error_code(given_dataype,given_lenth,sub_sec)
  report["Section"].append(sec_name)
  report["Sub-Section"].append(sub_sec['key'])
  report["Given DataType"].append(given_dataype)
  report["Expected DataType"].append(sub_sec['data_type'])
  report["Given Length"].append(None if given_lenth ==0 else given_lenth)
  report["Expected MaxLength"].append(sub_sec['max_length'])
  report["Error Code"].append(error_code)
     
  return



#EXPORT REPORT TO parsed/report.csv
def export_report(df):

  df.to_csv('parsed/report.csv',index=False,float_format='%.0f')


#EXPORT SUMMARY TO parsed/summary.text
def export_summary(df):
  file1 = open("parsed/summary.txt","w")

  for index, row in df.iterrows():
    err = [d for d in errors if d['code']==row['Error Code']][0]["message_template"].replace("LXY",row['Sub-Section']).replace("LX",row['Section']).replace("{data_type}",row['Expected DataType']).replace("{max_length}",str(row['Expected MaxLength']))
    file1.write(err+" \n")
    print(err)

  file1.close()
  return



#RUN TASK & LOAD INPUT TEXT
def Run_Task():
  f = open(path_input_text, "r")
  rs = f.read()
  rs=rs.split("\n")

  for x in rs:
    ln= x.split("&")
    if len(ln)>0:
      key=ln[0]
      stand= [d for d in standard if d['key']==key]
      if len(stand)>0:
        for k in stand[0]["sub_sections"]:
          index = int(k['key'].replace(key,''))
          make_report(index,ln,key,k)
  
  print("REPORT",report)
  df = pd.DataFrame(report)
  export_report(df)
  export_summary(df)



Run_Task()

  