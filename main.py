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


def start_process() -> int:
    popen('NineChroniclesInstaller.exe')
    time.sleep(1)
    pid = 0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if "NineChroniclesInstaller.tmp" == str(pinfo['name']):
                pid = pinfo['pid']
    return pid


if __name__ == '__main__':
    pid = start_process()
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
