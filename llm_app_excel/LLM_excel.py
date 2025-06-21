import lmstudio as lms
import pandas as pd
from jinja2 import Environment, FileSystemLoader

def ask_LLM (question: str):
    model = lms.llm("granite-3.2-8b-instruct")
    result = model.respond("Hello ?")
    print (result)
    return result

def Excel_management():
    
    excel_path = 'output.xlsx'
    template_dir = './'
    template_file = 'email_template.j2'


    # # Create a DataFrame with an empty column named "test"
    # df = pd.DataFrame(columns=["client","Numéro fiscal","Nom","Prénom","Adresse", "email"])
    # df["client"] = ["a", "b", "c"] 
    # # Save it to an Excel file
    # df.to_excel("./output.xlsx", index=False)
    # #df.to_csv("./output.csv", index=False)
    # print("Excel file created with an empty column named 'test'")
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=False)
    template = env.get_template(template_file)


    df = pd.read_excel(excel_path)
    for index, element in enumerate(df["client"]):
        #if df.loc[index,"Nom"]  == "Durand":
        print(df.loc[index,"email"])

def main():
    Excel_management()



if __name__ == "__main__":
    main()