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



if __name__ == "__main__":
    main()
















    # # Create a DataFrame with an empty column named "test"
    # df = pd.DataFrame(columns=["client","Numéro fiscal","Nom","Prénom","Adresse", "email"])
    # df["client"] = ["a", "b", "c"] 
    # # Save it to an Excel file
    # df.to_excel("./output.xlsx", index=False)
    # #df.to_csv("./output.csv", index=False)
    # print("Excel file created with an empty column named 'test'")