import os
import win32security

def search_name():
    folder = os.getcwd()
    flag = True
    for root, dirs, files in os.walk(folder):
        for file in files:
            filename = os.path.join(root, file)

            if filename.endswith('.xml'):
                sd = win32security.GetFileSecurity(filename, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, domain, type = win32security.LookupAccountSid(None, owner_sid)
                flag = False
                break
        if not flag:
            break

    return name

owner_name = search_name()
filenames = []

def search_files(owner, list):
    folder = os.getcwd()

    for root, dirs, files in os.walk(folder):
        for file in files:
            filename = os.path.join(root, file)
            if (filename.endswith('doc') or filename.endswith('docx') or
            filename.endswith('ppt') or filename.endswith('pptx') or
            filename.endswith('xls') or filename.endswith('xlsx')):
                sd = win32security.GetFileSecurity(filename, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, domain, type = win32security.LookupAccountSid(None, owner_sid)

                if name == owner:
                    list.append(os.path.join(file))

    return list

filenames = search_files(owner_name, filenames)

def filing():
    file = open('filenames.txt', 'w')

    for i in filenames:
        file.write(i)
        file.write("\n")
    file.close()

filing()