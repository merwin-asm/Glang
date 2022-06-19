from rich import print
import platform
import time
import os


class Parser:
    def __init__(self,file):
        # Important Vars
        self.CONVERTIONSTARTTIME = time.time()
        self.FileLocation = os.path.abspath(file)
        self.PythonCode = ["import rich","from pyTGR import *","from Module import *","TGR = pyTGR()"]
        self.KEYWORDS = ["MAKE","CALL","FUN","UPDATE","PRINT","DRAW_PIXEL","DRAW_LINE","THREAD",
                         "SET_BG","GET_KEY","GET_MOUSE","PRINTLN","IMPORT","LOOP","BREAK"]
        # preparing out file destination
        self.SaveLocation = str(self.FileLocation).split("/")
        self.FileName = self.SaveLocation.pop()
        self.OutPutName = self.FileName.split(".")[0] + ".py"
        self.SaveLocation.remove("")
        self.SaveLocation.append(self.OutPutName)
        save_loc = ""
        for e in self.SaveLocation:
            save_loc += f"/{e}"
        self.SaveLocation = save_loc
        # Load File
        self.SrcFileObj = open(self.FileLocation,"r")
        self.SrcFileData = self.SrcFileObj.read()
        self.SrcFileObj.close()
        self.SrcFileData = self.SrcFileData.split("\n")
        try:
            self.SrcFileData.remove("")
        except:
            pass
        # Preprocess
        self.ProcessedInstructions = []
        multi = False
        for line in self.SrcFileData:
            if "#" in line:
                pass
            elif "`" in line:
                if multi:
                    multi = False
                    line = line.split("`")[1]
                else:
                    multi = True
                    line = line.split("`")[0]
                if line != "":
                    self.ProcessedInstructions.append(line)
            elif not multi:
                self.ProcessedInstructions.append(line)
        if self.ProcessedInstructions[0] in ["NOSUDO","SUDO"]:
            if self.ProcessedInstructions[0] == "NOSUDO":
                self.ProcessedInstructions.remove("NOSUDO")
            else:
                self.ProcessedInstructions.remove("SUDO")
                self.PythonCode.append("import os")
                self.PythonCode.append("os.system('sudo su -')")
        while True:
            try:
                self.ProcessedInstructions.remove("")
            except:
                break
        # Converting Instructions
        self.TAB_MAN = 0
        self.PY_CODE = False
        for INT in self.ProcessedInstructions:
            if INT[0] == "{":
                self.PY_CODE = True
            elif INT[0] == "}":
                self.PY_CODE = False
            elif self.PY_CODE:
                self.PythonCode.append(f"{'    '*self.TAB_MAN}{INT}")
            else:
                SUBINT = self.SplitINT(INT)
                if SUBINT[0] not in self.KEYWORDS and SUBINT[0] not in ["(",")","{","}"]:
                    print(f"[red]INT NOT FOUND `{SUBINT[0]}`[/red]")
                else:
                    if SUBINT[0] == "PRINT":
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}TGR.print({SUBINT[1]},end='')")
                    elif SUBINT[0] == "(":
                        self.TAB_MAN += 1
                    elif SUBINT[0] == ")" and self.TAB_MAN != 0:
                        self.TAB_MAN -= 1
                    elif SUBINT[0] == "PRINTLN":
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}TGR.print({SUBINT[1]})")
                    elif SUBINT[0] == "IMPORT":
                        if SUBINT[1].split(".")[1] == "ga":
                            Parser(SUBINT[1])
                            SUBINT[1] = str(SUBINT[1].split(".")[0])
                        else:
                            SUBINT[1] = str(SUBINT[1].split(".")[0])
                        PythonCode = [f"import {SUBINT[1]}"]
                        self.PythonCode = PythonCode + self.PythonCode
                    elif SUBINT[0] == "MAKE":
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}{SUBINT[1]} {self.MakeListStr(SUBINT[2:])}")
                    elif SUBINT[0] == "UPDATE":
                        OPERATION = ""
                        for e in range(0, len(SUBINT) - 2):
                            OPERATION += " " + SUBINT[e+2]
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}{SUBINT[1]} {OPERATION}")
                    elif SUBINT[0] == "LOOP":
                        OPERATION = ""
                        for e in range(0, len(SUBINT) - 1):
                            OPERATION += " " + SUBINT[e+1]
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}while {OPERATION}:")
                    elif SUBINT[0] == "FUN":
                        try:
                            SUBINT[2] = SUBINT[2].replace("[", "")
                            SUBINT[2] = SUBINT[2].replace("]", "")
                        except:
                            print("[red]Warning Params Not Provided![/red]")
                            SUBINT.append("")
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}def {SUBINT[1]}({SUBINT[2]}):")
                    elif SUBINT[0] == "BREAK":
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}break")
                    elif SUBINT[0] == "CALL":
                        try:
                            SUBINT[2] = SUBINT[2].replace("[", "")
                            SUBINT[2] = SUBINT[2].replace("]", "")
                        except:
                            SUBINT.append("")
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}{SUBINT[1]}({SUBINT[2]})")
                    elif SUBINT[0] == "SET_BG":
                        self.PythonCode.append(f"{'    '*self.TAB_MAN}TGR.set_bg({SUBINT[1]})")

        # Saving Python Code
        self.FinalCode = ""
        self.FinalCode += F"OS = '{platform.system()}'\n"
        self.FinalCode += F"STARTUPTIME = {time.time()-self.CONVERTIONSTARTTIME}\n"
        for e in self.PythonCode:
            self.FinalCode += e + "\n"
        self.SaveFileObj = open(self.SaveLocation,"w")
        self.SaveFileObj.write(self.FinalCode)
        self.SaveFileObj.close()

    def MakeListStr(self,lis):
        string = ""
        for e in lis:
            string += e
        return string

    def SplitINT(self,TEXT):
        TEXT_sp = TEXT.split('"')
        TEXT_final = []

        c = 1
        for e in TEXT_sp:
            if c % 2 == 0:
                TEXT_final.append(f'"{e}"')
            else:
                TEXT_final += e.split(" ")
            c += 1
        while True:
            try:
                TEXT_final.remove("")
            except:
                break
        F = False
        TEXT_FINAL_2 = []
        for e in TEXT_final:
            if e == "f":
                F = True
            elif F == True and e[0] == '"':
                F = False
                TEXT_FINAL_2.append(f"f{e}")
            elif F == True and e[0] != '"':
                F = False
                TEXT_FINAL_2.append("f")
                TEXT_FINAL_2.append(e)
            else:
                TEXT_FINAL_2.append(e)
        TEXT_FINAL_3 = []
        sqr = False
        ch = ""
        for e in TEXT_FINAL_2:
            if e[0] == "[":
                sqr = True
                ch += e
            elif e[-1] == "]":
                sqr = False
                ch += e
                TEXT_FINAL_3.append(ch)
                ch = ""
            elif sqr:
                ch += e
            else:
                TEXT_FINAL_3.append(e)

        return TEXT_FINAL_3


if __name__ == '__main__':
    Parser("test.ga")
