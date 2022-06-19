import pyPath
import os

USER = os.getlogin()

# current file loc
file_ = str(__file__).split("/")
file_.pop()
while True:
    try:
        file_.remove("")
    except:
        break
cur_file = ""
for e in file_:
    cur_file+="/"+e
try:
    os.chdir(cur_file)
except:
    pass


target_paste = f"/home/{USER}/Glang"


def delete_Glang_dir():
    for e in os.listdir(target_paste):
        os.remove(f"{target_paste}/{e}")
    os.rmdir(target_paste)


def install():
    os.mkdir(target_paste)
    for e in ['pyTGR.py', 'pyPath.py', 'Parser.py', 'Module.py', 'main.py']:
        try:
            f_p = open(f"{target_paste}/{e}", "w")
            f_c = open(f"{e}", "r")
            f_p.write(f_c.read())
            f_p.close()
            f_c.close()
        except:
            pass
    my_path = pyPath.MYPATH()
    my_path.make_redirecting_bashfile(
        "Glang",
        target_pyfile=f"/home/{USER}/Glang/main.py",
        allow_args=True,
        max_num_args=1000
    )
    my_path.addfile_to_path(f"Glang",
                            "Glang",
                            exe=True)

def uninstall():
    delete_Glang_dir()
    os.remove("/usr/bin/Glang")

def update():
    uninstall()
    if os.path.exists("Glang_SRC"):
        if os.path.isdir("Glang_SRC"):
            for e in os.listdir("Glang_SRC"):
                os.remove(f"Glang_SRC/{e}")
            os.rmdir(f"Glang_SRC")
        else:
            os.remove("Glang_SRC")
    os.system("git clone https://github.com/mastercodermerwin/Glang.git Glang_SRC")
    os.system("cd Glang_SRC")
    os.system("sudo python3 Installer.py")

if os.path.exists(target_paste):
    cmd = input("Glang have been already installed. Do You want to Uninstall then enter `u` , if you want to make no change enter `n`  , if you want a update enter `t` [n/t/u] ?")

    if cmd == "n":
        pass
    elif cmd == "t":
        update()
    elif cmd == "u":
        uninstall()
else:
    install()

print("Thankyou for Installing , From Glang creators.")
