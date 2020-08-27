import time
from os import popen

import psutil
from pywinauto import application, WindowSpecification


def has_identifier(target: WindowSpecification, identifier: str):
    ctrl_identifiers = target._ctrl_identifiers()
    result = False
    for ctrl in ctrl_identifiers.values():
        if identifier in ctrl:
            result = True
    return result


def start_process():
    popen('NineChroniclesInstaller.exe')
    time.sleep(1)
    PID = 0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if "NineChroniclesInstaller.tmp" == str(pinfo['name']):
                PID = pinfo['pid']
    return PID


if __name__ == '__main__':
    pid = start_process()
    app = application.Application(backend='uia').connect(process=pid)
    a = app.window(class_name='TWizardForm')

    a.print_control_identifiers()
    a["Next >"].click()
    print("Click Next")
    if has_identifier(a, "Next >"):
        a["Next >"].click()
        print("Click Next")
    a["Install"].click()
    print("Click Install")

    count = 0

    while count < 20:
        if has_identifier(a, "Finish"):
            a["Finish"].click()
            print("Click Finish")
            break;
        else:
            count += 1
            time.sleep(5)

    if count >= 20:
        raise Exception('Cannot installed in 100 second.')
