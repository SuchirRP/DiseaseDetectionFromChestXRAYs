import os;
import PyPDF2;
import re;
import shutil;
import requests;
import sys;
import pandas as pd;

def sortfile(src_path, target_path, categories):
    """
            Function to sort study reports into folders after searching them for keywords each of which is indicative of a category.
            Study reports are expected to be pdfs.
            Arguments:
                src_path: Source directory, must be a string, containing the path for the source directory containing the studies. Please ensure it does not end with a "/"
                target_path: Target directory, must be a string, the directory where the sorted studies shall be stored. Please ensure it does bit end with a "/"
                categories: A dictionary with categories as keys and a list or corredponding search keywords as a value. Ex:- dict = {"category1" : ["keyword1", "keyword2"]}
    """

    #Function prechecks
    if(os.path.exists(src_path) == False):
        return "src_path doesn not exist";

    if(os.path.exists(target_path) == False):
        return "target_path doesn not exist";

    if(len(categories) == 0):
        return "categories is empty";

    src_dir_files = os.listdir(src_path);

    if(len(src_dir_files) == 0):
        return "src_path is empty: "+src_path;

    for cat in categories:
        if(os.path.exists(target_path+"/"+cat) == False):
            os.makedirs(target_path+"/"+cat);
    if(os.path.exists(target_path+"/"+"Others") == False):
        os.makedirs(target_path+"/"+"Others");

    #Core body
    for file in os.listdir(src_path):
        #print(dir+file);
        reader = PyPDF2.PdfReader(src_path+"/"+file);

        num_pages = len(reader.pages);

        search_flag = 0;
        for page in reader.pages:
            text = page.extract_text();

            for cat in categories.keys():
                for search_term in categories[cat]:
                    res_search = re.search(search_term, text, re.IGNORECASE);
                    if res_search != None:
                        print("src:", src_path+"/"+file);
                        print("des:",target_path+"/"+cat+"/"+file);
                        print("------");
                        search_flag = 1;
                        shutil.copy(src_path+"/"+file, target_path+"/"+cat+"/"+file);
        if(search_flag == 0):
                        shutil.copy(src_path+"/"+file, target_path+"/Others/"+file);

def print_impressions(target_path):
    start_search_terms = ["impression"];
    end_search_terms = ["dr"];

    for file in os.listdir(target_path+"/Others"):
        reader = PyPDF2.PdfReader(target_path+"/Others/"+file);
        num_pages = len(reader.pages);

        for page in reader.pages:
            start = -1;
            end = -1;
            text = page.extract_text();
            lines = text.splitlines();
            for i in range(len(lines)):

                for start_term in start_search_terms:
                    if(re.search(start_term, lines[i], re.IGNORECASE)):
                        start = i;
                        break;

                for end_term in end_search_terms:
                    if(re.search(end_term, lines[i], re.IGNORECASE)):
                        end = i;

            if(start != -1):
                if(end != -1):
                    #print("start = ", start, "end = ", end, "----------------");
                    for i in range(start, end):
                        #print("i = ", i)
                        print(lines[i]);
                else:
                    #print("start = ", start, "----------------");
                    for i in range(start, len(lines)):
                        #print("i = ", i)
                        print(lines[i]);

def csv_impressions(target_path):
    start_search_terms = ["impression"];
    end_search_terms = ["dr"];

    csv_ls = [];

    for file in os.listdir(target_path+"/Others"):
        reader = PyPDF2.PdfReader(target_path+"/Others/"+file);
        num_pages = len(reader.pages);

        index_str = "";
        for page in reader.pages:
            start = -1;
            end = -1;
            text = page.extract_text();
            lines = text.splitlines();
            for i in range(len(lines)):

                for start_term in start_search_terms:
                    if(re.search(start_term, lines[i], re.IGNORECASE)):
                        start = i;
                        break;

                for end_term in end_search_terms:
                    if(re.search(end_term, lines[i], re.IGNORECASE)):
                        end = i;

            if(start != -1):
                if(end != -1):
                    for i in range(start, end):
                        index_str = index_str + lines[i];
                        print(lines[i]);
                else:
                    for i in range(start, len(lines)):
                        index_str = index_str + lines[i];
                        print(lines[i]);
            if index_str != "":
                csv_ls.append(index_str);

    csf_df = pd.DataFrame(csv_ls);
    csf_df.to_csv("impressions.csv", index=False)

def num_of_studies(src_path, target_path, categories):
    print("Total number of studies", len(os.listdir(src_path)));
    print("---------------------");
    print("No of categories: ", len(categories.keys()));
    print(categories);
    print("---------------------");
    for folder in os.listdir(target_path):
        print("Category: ", folder, " - ", len(os.listdir(target_path+"/"+folder)));

def get_studies_list(target_path):
    folders = os.listdir(target_path);
    studies = {};
    for folder in folders:
        studies[folder] = os.listdir(target_path+"/"+folder);

def generate_request(url, category, paitent_id):
    dic = {"category" : category, "paitent_id":paitent_id};
    x = requests.post(url, json = dic);
    print(x);

def main():
    source = "/home/frzfishcustard/Projects/dicom/Reports/Studies";
    target = "/home/frzfishcustard/Projects/dicom/Reports/Sorted";
    categories = {"Atelectasis" : ["Atelectasis"],
                  "Cardiomegaly" : ["Cardiomegaly"],
                  "Effusion" : ["Effusion"],
                  "Infiltration" : ["Infiltration"],
                  "Mass" : ["Mass"],
                  "Nodule" : ["Nodule"],
                  "Pneumonia" : ["Pneumonia", "pneumonitis"],
                  "Pneumothorax" : ["Pneumothorax"],
                  "Consolidation" : ["Consolidation"],
                  "Edema" : ["Edema"],
                  "Emphysema" : ["Emphysema"],
                  "Fibrosis" : ["Fibrosis"],
                  "Pleural Thickening" : ["Pleural Thickening" ],
                  "Hernia" : ["Hernia"],
                  "Cavity" : ["Cavity"],
                  "Fracture" : ["Fracture"],
                  "Masectomy" : ["Masectomy"],
                  "Bronchitis" : ["Bronchitis"],
                  "Normal" : ["No Radiographic Abnormality", "No Significant  Radiographic Abnormality", "normal study", "study within normal limits",
                              "NO SIGNIFICANT RADIOLOGIC ABNORMALITY", "study is within normal limits", "No  Significant Radiographic Abnormality",
                              "NO SIGNIFICANT ABNORMALITY DETECTED IN CHEST RADIOGRAPH", "No  Significant  Radiographic Abnormality"
                              "NO SIGNIFICANT RADIOGRAPHIC ABNORMALITY DETECTED IN CHEST", "No Significant Radiographic Abnormality",
                              "No significant abnormality seen", "NORMAL CHEST RADIOGRAPH", "NO SIGNIFCANT RADIOGRAPHIC ABNORMALITY DETECTED INCHEST RADIOGRAPH",
                              "Essentially normal radiograph of the chest", "NO SIGNIFICANT LUNG FIELD CHANGES ISOLATED", "No significant abnormality seen",
                              "NO EVIDENCE OF BOWEL OBSTRUCTION OR FREE INTRAPERITONEAL GAS IS NOTED", "No abnormality detected in cervical spine"]};
    #sortfile(source, target, categories);
    num_of_studies(source, target, categories);
    #get_studies_list(target);
    #print_impressions(target);
    #csv_impressions(target);

if __name__=="__main__":
    main()
