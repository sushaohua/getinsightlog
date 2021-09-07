#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, os, shutil, zipfile, time
from pathlib import Path
from copy_folders import copy_folders


def mkdir(log_dir):
    log_dir = log_dir.strip().rstrip("\\")
    isExists = os.path.exists(log_dir)
    if not isExists:
        os.makedirs(log_dir)
        return True
    else:
        shutil.rmtree(log_dir)
        os.makedirs(log_dir)
        print("路径已存在!")
        return True


def get_log(log_dir, ip):
    # 拷贝文件到本地
    copy_folders(log_dir, ip)
    # 通过命令本地生成文件
    os.popen('adb -s ' + ip + '  shell dmesg > ' + log_dir + '/dmesg.log')
    os.popen('adb -s ' + ip + '  shell dumpsys > ' + log_dir + '/dumpsys.log')
    os.popen('adb -s ' + ip + '  shell ifconfig > ' + log_dir + '/ifconfig.log')
    os.popen('adb -s ' + ip + '  shell cat /dev/kmsg > ' + log_dir + '/kmsg.log')
    os.popen('adb -s ' + ip + '  logcat > ' + log_dir + '/logcat.log')
    os.popen('adb -s ' + ip + ' shell getprop ro.serialno > ' + log_dir + '/getprop.log')
    time.sleep(15)
    os.system("taskkill /F /IM adb.exe")


def check_ip(ipAddr):
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:
        return False


def get_zip(input_path, result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            get_zip(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)


def zip_file_with(input_path, output_path, output_name):
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    get_zip(input_path, filelists)
    for file in filelists:
        f.write(file)
    f.close()
    return output_path + r"/" + output_name


def get_connected():
    log_dir = "c:/equipment_log"
    zip_dir = "c:/log_zip"
    flag = mkdir(zip_dir)
    if flag:
        zip_file = zip_dir + "/log.zip"
    flag = mkdir(log_dir)
    if flag:
        ip = input("请输入设备IP：")
        if check_ip(ip):
            pass
        else:
            print("输入错误，请重新执行脚本！")
        if len(ip)>0:
            result = os.popen("adb connect " + ip)
            res = result.read()
            for line in res.splitlines():
                if "connected to" in line:
                    get_log(log_dir, ip)
                    my_file = Path(zip_file)
                    if my_file.exists():
                        os.remove(zip_file)
                    zip_file_with(log_dir, 'c:/log_zip', "log.zip")
                else:
                    print("没连上设备，请重新执行脚本！")
    else:
        print("创建目录失败，请检查系统设置或手动在C盘创建文件夹名为equipment_log后再次执行脚本！")


if __name__ == '__main__':
    get_connected()
