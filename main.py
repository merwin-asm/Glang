"""
Glang (Extension `.ga`) ver. 1.0.0

A simple lang for game dev.
Author : Merwin

Compiler Commands:
    Glang run <path>
    Glang help-cmd
    Glang help-lang
    Glang version


Info:
    - > The files are located in /home/user/Glang

Docs:

    Making Vars:
        MAKE NAME = VALUE

    Operators:
        +
        -
        /
        *
        **
        etc
        (Uses PEMDAS rule)
        When redefining a var:
            UPDATE var = var + 1 
    Function:
        Call <function name> [<args>] (calling a function)

        Func <function name> [var1,var2(Params-which-are-required)]
        (
        sum =  var1 + var2
        return sum
        )

    Internal Vars:
        STARTUPTIME , contains how long the program took to start.
        OS , contains the OS you are on.
    
    Loop:
        Loop 
        (
        PRINT "hello"
        )
        use BREAK to end
        
    InBuild Functions:
        SET_BG [ 0,0,0]        
        PRINT "TEXT"
        PRINTLN "TEXT"
        for colored printing:
        PRINTLN "[red]TEXT[/red]" or  PRINT "[red]TEXT[/red]"

    Note:
        - > Only 2D InBuild support
        - > Installer only for linux

    Extras:
        - > Internal Python Code execution (
            Put the code in {}.
            eg:
                {
                print("Hello World")
                }
                Make sure you don't write code in the same line in which "{" or "}" is present.
            )
"""

import os
import sys
import Converter
from rich import print
from rich.panel import Panel
from rich.table import Table


Short_Docs = """
Glang (Extension `.ga`) ver. 1.0.0

A simple lang for game dev.
Author : Merwin

Compiler Commands:
    Glang run <path>
    Glang help-cmd
    Glang help-lang
    Glang version


Info:
    - > The files are located in /home/user/Glang

Docs:

    Making Vars:
        MAKE NAME = VALUE

    Operators:
        +
        -
        /
        *
        **
        etc
        (Uses PEMDAS rule)
        When redefining a var:
            UPDATE var = var + 1 
    Function:
        Call <function name> [<args>] (calling a function)

        Func <function name> [var1,var2(Params-which-are-required)]
        (
        sum =  var1 + var2
        return sum
        )

    Internal Vars:
        STARTUPTIME , contains how long the program took to start.
        OS , contains the OS you are on.
    
    Loop:
        Loop 
        (
        PRINT "hello"
        )
        use BREAK to end
        
    InBuild Functions:
        SET_BG [ 0,0,0]        
        PRINT "TEXT"
        PRINTLN "TEXT"
        for colored printing:
        PRINTLN "[red]TEXT[/red]" or  PRINT "[red]TEXT[/red]"

    Note:
        - > Only 2D InBuild support
        - > Installer only for linux

    Extras:
        - > Internal Python Code execution (
            Put the code in {}.
            eg:
                {
                print("Hello World")
                }
                Make sure you don't write code in the same line in which "{" or "}" is present.
            )
"""


VERSION  = "1.0.0"


def Run_Glang(path,args):
    Converter.Parser(path)
    file_ =str(path).split("/")
    file_org = file_.pop()
    while True:
        try:
            file_.remove("")
        except:
            break
    file = ""
    for e in file_:
        file += "/" + e
    file += str(file_org.split(".")[0])+".py"
    os.system(f"python3 {file} {args}")



table_commands = Table(title="Glang Commands")

table_commands.add_column("Command", style="cyan", no_wrap=True)
table_commands.add_column("Use", style="magenta")
table_commands.add_column("No", justify="right", style="green")
table_commands.add_row("help-cmd", "Get info about the commands.", "1")
table_commands.add_row("help-lang", "Displays a short Doc.", "2")
table_commands.add_row("run <path>", "Runs a Glang file.", "3")
table_commands.add_row("Version", "Shows the current version of Glang.", "4")

args = sys.argv

main_cmd = ""
DONE = False
try:
    main_cmd = args[1].lower()
except:
    print(table_commands)
    DONE = True

if not DONE:
    if main_cmd == "help-cmd":
        print(table_commands)
    elif main_cmd == "help-lang":
        print(Panel(f"[green][bold]{Short_Docs}[/bold][/green]", title="Short Docs"))
    elif main_cmd == "run":
        DONE_2 = False
        code_file = ""
        try:
            code_file = args[2]
        except:
            print(f"[red]File Not Passed In.")
            DONE_2 = True
        if not DONE_2:
            if os.path.exists(code_file):
                if os.path.isfile(code_file):
                    Run_Glang(code_file,args[2:])
                else:
                    print(f"[red]Make sure '{code_file}' is a file.")
            else:
                print(f"[red]Make sure '{code_file}' exists.")

    elif main_cmd == "version":
        print(f"[blue]{VERSION}")
    else:
        print("[red]Command not found.")
