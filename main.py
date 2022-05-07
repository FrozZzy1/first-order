import os
import win32security

def search_name():
    folder = os.getcwd()
    flag = True
    for root, dirs, files in os.walk(folder):
        for file in files:
            filename = os.path.join(root, file)

            if filename.endswith('.xml') and filename != "workspace.xml":
                sd = win32security.GetFileSecurity(filename, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, domain, type = win32security.LookupAccountSid(None, owner_sid)
                flag = False
                break
        if not flag:
            break

    return name


def search_files(owner):
    folder = os.getcwd()
    lst = []
    extensions = ['.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']
    for root, dirs, files in os.walk(folder):
        for file in files:
            filename = os.path.join(root, file)
            ext = os.path.splitext(filename)[1]
            if ext in extensions:
                sd = win32security.GetFileSecurity(filename, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, domain, type = win32security.LookupAccountSid(None, owner_sid)

                if name == owner:
                    lst.append(os.path.join(file))

    return lst


def filing(file_names):
    file = open('filenames.txt', 'w')

    for i in file_names:
        file.write(i)
        file.write("\n")
    file.close()

def main():
    owner_name = search_name()
    filenames = search_files(owner_name)
    filing(filenames)

if __name__ == '__main__':
    main()