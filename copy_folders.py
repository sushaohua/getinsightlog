from subprocess import PIPE, Popen
import os, sys
import glob


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


def copy_folders(log_dir, ip):
    for i in range(3):
        cmdline("adb devices")

    folderls = cmdline("adb -s " + ip + "  shell ls /sdcard/android/data")

    applist = str(folderls).split("\\r\\n")
    applist[0] = applist[0][applist[0].find("'") + 1:]
    applist.pop(-1)

    for i in applist:
        if i.find(".") != -1:
            applist.remove(i)

    total = len(applist)
    sel = []

    for i in range(total):
        sel.append(i)

    path = log_dir

    os.chdir(path)
    # print(os.getcwd())

    original = path
    sel.sort()

    for i in sel:
        try:
            path = log_dir + "/" + applist[i]
            os.mkdir(path)

        except:
            pass

        os.chdir(path)
        cmdline("adb -s " + ip + " pull /sdcard/android/data/" + applist[i])
        os.chdir(original)


if __name__ == '__main__':
    copy_folders(log_dir, ip)
