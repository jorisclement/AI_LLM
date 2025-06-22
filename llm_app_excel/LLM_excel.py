import lmstudio as lms
import pandas as pd
from jinja2 import Environment, FileSystemLoader

def ask_LLM (question: str):
    model = lms.llm("granite-3.2-8b-instruct")
    result = model.respond("Hello ?")
    print (result)
    return result

def Excel_management():
    
    excel_path = './llm_app_excel/output.xlsx'
    template_dir = './llm_app_excel'
    template_file = './email_template.j2'
    output_folder = './llm_app_excel/email_to_client'

    env = Environment(loader=FileSystemLoader(template_dir), autoescape=False)
    template = env.get_template(template_file)


    df = pd.read_excel(excel_path)
    for index, element in enumerate(df["client"]):
        excel_name = df.loc[index,"Nom"]
        excel_surname = df.loc[index,"Prénom"]
        excel_email = df.loc[index,"email"]
        excel_fisc_num = df.loc[index,"Numéro fiscal"]
        excel_addr = df.loc[index,"Adresse"]


        #if df.loc[index,"Nom"]  == "Durand":
        context = {
        'name': excel_name,
        'surname': excel_surname,
        'email': excel_email,
        'fisc_num': excel_fisc_num,
        'address' : excel_addr
        }
        
        rendered_text = template.render(context)

        # Save the rendered text to a file
        with open(output_folder+'/'+excel_name+ '_' + excel_surname +'_output.txt', 'w') as f:
            f.write(rendered_text)

def main():
    Excel_management()



if __name__ == "__main__":
    main()
















    # # Create a DataFrame with an empty column named "test"
    # df = pd.DataFrame(columns=["client","Numéro fiscal","Nom","Prénom","Adresse", "email"])
    # df["client"] = ["a", "b", "c"] 
    # # Save it to an Excel file
    # df.to_excel("./output.xlsx", index=False)
    # #df.to_csv("./output.csv", index=False)
    # print("Excel file created with an empty column named 'test'")