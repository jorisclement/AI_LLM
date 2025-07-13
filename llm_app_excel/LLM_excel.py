import lmstudio as lms
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import argparse

def ask_LLM (question: str):
    model = lms.llm("granite-3.2-8b-instruct")
    result = model.respond("Hello ?")
    print (result)
    return result

def Excel_management(excel_path, output_folder, template_dir, template_file):    
    excel_path = excel_path
    template_dir = template_dir
    template_file = template_file
    output_folder = output_folder

    env = Environment(loader=FileSystemLoader(template_dir), autoescape=False)
    template = env.get_template(template_file)

    # Load all sheets
    # sheets = pd.read_excel(excel_path, sheet_name=None)  # Returns a dict: {sheet_name: DataFrame}
    # for sheet_name, df1 in sheets.items():
    #     print(sheet_name,df1)

    with pd.ExcelFile(excel_path) as xls:
        sheet_names = xls.sheet_names
    print(sheet_names)

    df1 = pd.read_excel(excel_path, sheet_name=sheet_names[0])
    for index, element in enumerate(df1["client"]):
        excel_name = df1.loc[index,"Nom"]
        excel_surname = df1.loc[index,"Prénom"]
        excel_email = df1.loc[index,"email"]
        excel_fisc_num = df1.loc[index,"Numéro fiscal"]
        excel_addr = df1.loc[index,"Adresse"]

    df2 = pd.read_excel(excel_path, sheet_name=sheet_names[1])
    for index, element in enumerate(df2["Code"]):
        excel_code = df2.loc[index,"Code"]
        excel_libelle = df2.loc[index,"Libelle"]


        #if df1.loc[index,"Nom"]  == "Durand":
        context = {
        'name': excel_name,
        'surname': excel_surname,
        'email': excel_email,
        'fisc_num': excel_fisc_num,
        'address' : excel_addr
        }
        
        rendered_text = template.render(context)

        # Save the rendered text to a file
        with open(output_folder+'/'+excel_name+ '_' + excel_surname +'_output.txt', 'w', encoding='utf-8') as f:
            f.write(rendered_text)

def main():
    parser = argparse.ArgumentParser(description="Generate personalized emails from Excel and a Jinja2 template.")
    parser.add_argument('--excel', '-x', type=str, required=True, help='Path to the Excel input file')
    parser.add_argument('--outfolder', '-o', type=str, default='email_to_client', help='Output folder (default: email_to_client)')
    parser.add_argument('--template', '-t', type=str, default='email_template.j2', help='Jinja2 template filename (default: email_template.j2)')
    parser.add_argument('--templatedir', type=str, default='.', help='Directory containing the template (default: current directory)')

    args = parser.parse_args()

    Excel_management(args.excel, args.outfolder, args.templatedir, args.template)

def test():


    # Create a DataFrame to write
    new_data = pd.DataFrame({
        'Nom': ['Durand', 'Martin'],
        'Prénom': ['Jean', 'Claire'],
        'Prms': ['OP', 'Claire'],
        'email': ['jean.durand@email.com', 'claire.martin@email.com']
    })

    # File path to existing Excel
    excel_path = 'clients.xlsx'

    # Append new sheet
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a') as writer:
        new_data.to_excel(writer, sheet_name='sheet2', index=False)


    # # Create a DataFrame with an empty column named "test"
    # df1 = pd.DataFrame(columns=["client","Numéro fiscal","Nom","Prénom","Adresse", "email"])
    # df1["client"] = ["a", "b", "c"] 
    # # Save it to an Excel file
    # df1.to_excel("./output.xlsx", index=False)
    # #df1.to_csv("./output.csv", index=False)
    # print("Excel file created with an empty column named 'test'")

if __name__ == "__main__":
    main()
    #test()














