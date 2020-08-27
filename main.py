import time
from os import popen

import psutil
from pywinauto import application, WindowSpecification


def has_identifier(target: WindowSpecification, identifier: str) -> bool:
    ctrl_identifiers = target._ctrl_identifiers()
    result = False
    for ctrl in ctrl_identifiers.values():
        if identifier in ctrl:
            result = True
    return result


def start_9c() -> int:
    popen('NineChroniclesInstaller.exe')
    time.sleep(1)
    return get_pid("NineChroniclesInstaller.tmp")


def get_pid(process_name: str) -> int:
    pid = 0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if process_name == str(pinfo['name']):
                pid = pinfo['pid']
    return pid


if __name__ == '__main__':
    pid = start_9c()
    app = application.Application(backend='uia').connect(process=pid)
    window: WindowSpecification = app.window(class_name='TWizardForm')

    window["Next >"].click()
    print("Click Next")
    if has_identifier(window, "Next >"):
        window["Next >"].click()
        print("Click Next")
    window["Install"].click()
    print("Click Install")

    count = 0

    while count < 20:
        if has_identifier(window, "Finish"):
            window["Finish"].click()
            print("Click Finish")
            break
        else:
            count += 1
            time.sleep(5)

    if count >= 20:
        raise Exception('Cannot installed in 100 second.')

    time.sleep(1)
    if get_pid("Nine Chronicles.exe") == 0:
        raise Exception('Cannot run NineChronicles Launcher.')
    else:
        print("Successfully Launched.")

