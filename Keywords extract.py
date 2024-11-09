import pytesseract
import os
import fitz
import re
from PIL import Image
import tkinter as tk
from tkinter import filedialog
def pdf2Imgs(PDF_path):
    File_name = os.path.basename(PDF_path)
    File_basename = os.path.splitext(File_name)[0]
    if(Check_all_operation(File_basename)):
        return True
    MakeDir(File_basename)
    PDF_FILE = fitz.open(PDF_path)
    for page in range(5):
        NUM_page = PDF_FILE[page]
        rotate = 0
        coordinate_x = 2
        coordinate_y = 2
        Matrix = fitz.Matrix(coordinate_x,coordinate_y).prerotate(rotate)
        Pix = NUM_page.get_pixmap(matrix=Matrix,alpha=False)
        Pix.save(File_basename+'/'+'IMG'+'/'+File_basename+'_%s.png'%page)
        IMG2Text(page,File_basename)
    MatchKeyWords(File_basename)
    Complete_previous_operation(File_basename)

def Complete_previous_operation(File_basename):
    with open("./check",'a') as File:
        File.write(File_basename+'_document'+'='+'True'+'\n')

def Check_all_operation(File_basename):
    Search_String = File_basename+'_document'+'='+'True'
    try:
        with open("./check",'r') as File:
            for line in File:
                if Search_String in line:
                    print(File_basename+"-----Succeeded")
                    return True
                    break
    except FileNotFoundError:
        print('')
    return False
def IMG2Text(page,File_basename):
    Text = pytesseract.image_to_string(Image.open(File_basename+'/'+'IMG'+'/'+File_basename+'_%s.png'%page), lang='eng')
    with open(File_basename+'/'+File_basename+'.txt', 'a', encoding='utf-8') as File:
        File.write(Text)
def MakeDir(File_basename):
    if not os.path.exists(File_basename):
        os.makedirs(File_basename+'/'+'IMG')

def MatchKeyWords(File_basename):
    with open(File_basename+'/'+File_basename+'.txt', 'r', encoding='utf-8') as File:
        Text = File.read()
    pattern = r"Keywords\s*(.*?)\n\n"
    matches = re.findall(pattern, Text,re.DOTALL)
    with open('./result.txt', 'a', encoding='utf-8') as File:
        for match in matches:
            print(match.strip().replace(':','').replace('\n',''))
            File.write(File_basename+'-----'+'Keywords---'+match.strip().replace(':','').replace('\n','')+'\n\n')

def Read_PDF(FILE_BASE_PATH):
    try:
        if isinstance(FILE_BASE_PATH, tuple):
            for file in FILE_BASE_PATH:
                if os.path.isfile(file):
                    pdf2Imgs(file)
    except Exception as e:
        print('')
def Confirm_Window(FILE_Base_PATHS):
    Confirm_root = tk.Toplevel()
    Confirm_root.title('OK')
    File_list = tk.Listbox(Confirm_root)
    for File in FILE_Base_PATHS:
        File_list.insert(tk.END, File)
    File_list.pack()
    def Confirm_action():
        Read_PDF(FILE_Base_PATHS)
        Confirm_root.quit()
    Confirm_button = tk.Button(Confirm_root, text='Confirm', command=Confirm_action)
    Confirm_button.pack()
    Confirm_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    FILE_BASE_PATHS = filedialog.askopenfilenames(
        title='Select PDF files',
        filetypes = (("PDF FILES","*.pdf"),("ALL FILES",".*"))
    )
    if FILE_BASE_PATHS:
        Confirm_Window(FILE_BASE_PATHS)

