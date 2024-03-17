### Author: Schvis ###
### Helpers: crossxzone
### Jomok: rekiihype, _.chl._
import importlib, subprocess
### Installing missing imports ###
def getlibs():
    requiredLibs = ['customtkinter', 'configparser', 'packaging', 'Pillow', 'requests', 'zipfile', 'tqdm', 'CTkListbox', 'patool', 'tkinter']
    for lib in requiredLibs:
        try:
            importlib.import_module(lib)
        except ImportError:
            print(f"Library {lib} not found. Installing...")
            subprocess.run(['pip', 'install', lib])
getlibs()
### Imports ###
from difflib import SequenceMatcher
from datetime import datetime
from CTkListbox import *
from PIL import Image
import glob
import customtkinter
import os, sys, shutil, time, threading, requests, io, urllib, webbrowser, json
from customtkinter import filedialog as fd
from configparser import ConfigParser
import zipfile
from tqdm import tqdm
import patoolib
from tkinter import StringVar

if not os.path.exists('./backup'):
    os.makedirs('./backup')
if not os.path.exists('./backup/cfg'):
    os.makedirs('./backup/cfg')
if not os.path.exists('./backup/files'):
    os.makedirs('./backup/files')
urllib.request.urlretrieve("https://raw.githubusercontent.com/Schvis/account_manager/main/image.ico", "./backup/image.ico")
root = customtkinter.CTk()
root.geometry('900x480')
root.iconbitmap('./backup/image.ico')
root.title('Account Manager')
root.resizable(False, False)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2,3), weight=1)
root.grid_rowconfigure((0,1,2), weight=1)
customtkinter.set_appearance_mode('Dark')
### Variables ###
GOwner = 'Cotton-Buds'
GLocal = 'calculator'
Settings = ConfigParser()
AccountList = ConfigParser()
Backup = ConfigParser()
regions = [
    'Default', 'EU', 'NA', 'Asia', 'TW/HK/MO',
]
SettingsPath = './backup/settings.ini'
AccountPath = './backup/accounts.ini'
InjectorTxT = './backup/injectors.txt'
Settings.read(SettingsPath)
InjPath = []
Ignore = 'injector.exe'
own = sys.argv[0]
own_name = os.path.basename(own)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
try:
    url = f'https://api.github.com/repos/{GOwner}/{GLocal}/releases/latest'
    response = requests.get(url)
    response.raise_for_status()

    # Get the download URL of the latest injector release
    asset_url = response.json()['assets'][0]['browser_download_url']
    original_name = response.json()['assets'][0]['name']
except Exception as e:
    print(f'{bcolors.WARNING}[Warning] Failed to fetch latest version: {e}{bcolors.ENDC}')
    original_name = 'Exceded'

### Creating files/folders if doesnt exist ###
try:
    os.remove(AccountPath)
except FileNotFoundError:
    pass

if not os.path.isfile(AccountPath):
    with open(AccountPath, 'w') as f:
        print(f'{bcolors.OKGREEN}[Success] Created accounts.ini file{bcolors.ENDC}')
        AccountList.read(AccountPath)

if not os.path.isfile(SettingsPath):
    with open(SettingsPath, 'w') as f:
        print(f'{bcolors.OKGREEN}[Success] Created settings.ini file{bcolors.ENDC}')
        Settings.read(SettingsPath)

if not os.path.isfile(InjectorTxT):
    with open(InjectorTxT, 'w') as f:
        print(f'{bcolors.OKGREEN}[Success] Created injectors.txt file{bcolors.ENDC}')

if not os.path.isfile('./backup/files/config.txt'):
    with open(InjectorTxT, 'w') as f:
        print(f'{f}')

korepi_folder = [FolderValue for folder in Settings for FolderUsed, FolderValue in Settings[folder].items()]

def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
### Refreshing Injector List and Account List on boot ###
def retrieve_info():
    accountF = glob.glob(f'{korepi_folder[0]}*/accounts.ini')
    accountFile = ''.join(str(x) for x in accountF)
    InjectorList = glob.glob(f'{korepi_folder[0]}*/*.exe')
    configjson = glob.glob(f'{korepi_folder[0]}*/cfg.json')
    configFile = ''.join(str(x) for x in configjson)
    saveFile = time.strftime("%Y-%m-%d-%H-%M-cfg.json")

    try:
        shutil.copy(configFile, f'./backup/cfg/{saveFile}')
    except Exception as e:
        print(f'{bcolors.WARNING}[Error] Failed to backup cfg.json: {e}{bcolors.ENDC}')

    with open(InjectorTxT, 'w') as InjectorWrite:
        for Injectors in InjectorList:
            Injector_filename = os.path.basename(Injectors)
            if not Injector_filename == own_name:
                InjectorWrite.write(Injectors + '\n')

    if accountFile == '':
        print(f'{bcolors.HEADER}[i] Account file not found, please export at least 1 account first.{bcolors.ENDC}')
        return

    shutil.copy(accountFile, './backup/accounts.txt')

    try:
        AccountList.add_section('Accounts')
    except:
        print(f'{bcolors.OKCYAN}[i] Account file ready{bcolors.ENDC}')

    with open(AccountPath, 'w') as AccWrite:
        AccountList.write(AccWrite)

    os.rename(AccountPath, './backup/accounts2.txt')

    with open('./backup/accounts.txt', 'r') as firstfile, open('./backup/accounts2.txt', 'a') as secondfile:
        for line in firstfile:
            secondfile.write(line)

    # Deleting bugged line (if possible)
    try:
        with open('./backup/accounts2.txt', 'r') as fr2:
            lines2 = fr2.readlines()
            ptr = 1
            with open('./backup/accounts2.txt', 'w') as fw2:
                for line2 in lines2:
                    if ptr != 3:
                        fw2.write(line2)
                    ptr += 1
                print('')
    except:
        print(f'{bcolors.WARNING}[Error] Oops! Failed to delete bugged line{bcolors.ENDC}')

    try:
        os.rename('./backup/accounts2.txt', AccountPath)
        os.remove('./backup/accounts.txt')
    except:
        print(f'{bcolors.WARNING}[Error] Woops coding issue :waduh:{bcolors.ENDC}')

try:
    retrieve_info()
except Exception as e:
    print(e)
try:
    AccountList.read(AccountPath)
    acc = [AccountKey for section2 in AccountList for AccountKey, AccountValue in AccountList[section2].items()]
    acc.append('Default')
    LastUsed = [UsedValue for Used in Settings for UsedAcc, UsedValue in Settings[Used].items()]
    if len(LastUsed[2]) >= 3:
        print(f'{bcolors.OKGREEN}[i] Last used account: {LastUsed[2]}\n[i] Last used region: {LastUsed[1]}{bcolors.ENDC}')
    else:
        print('[i] No used accounts found')
except:
    print('')
print(f'{bcolors.OKCYAN}[i] Accounts: {str(acc)}{bcolors.ENDC}')

### Get Injectors ###
try:
    with open('./backup/injectors.txt', 'r') as injRead:
        savedInjector = injRead.readlines()
    savedInjector = [path.strip() for path in savedInjector]
    InjPath.extend(savedInjector)
    available_injectors = []
    for injectors in InjPath:
        injector_available = os.path.basename(injectors)
        available_injectors.append(injector_available)
    print(f'{bcolors.OKCYAN}[i] Available injectors: {str(available_injectors)}{bcolors.ENDC}')
except FileNotFoundError:
    print(f'{bcolors.WARNING}[i] No injectors.txt file found{bcolors.ENDC}')

### Defining Functions ###
### Kill and Reopen App ###
def reopen():
    print(f'{bcolors.OKGREEN}[i] Reloading Launcher...{bcolors.ENDC}')
    fileis = sys.argv[0]
    time.sleep(1)
    os.system(f'"{os.path.realpath(fileis)}"')

def select_folder():

    selected_folder = fd.askdirectory(
        title='Select Korepi Folder'
    )

    if not selected_folder:
        print(f'{bcolors.FAIL}[Warning] No folder selected{bcolors.ENDC}')
        return
    
    try:
        Settings.add_section('Settings')

    except Exception:
        pass
    Settings.set('Settings', 'folder', selected_folder)
    Settings.set('Settings', 'SelReg', '')
    Settings.set('Settings', 'SelAcc', '')
    Settings.set('Settings', 'lastInjector', '')
    Settings.set('Settings', 'SkinFolder', '')
    Settings.set('Settings', 'Disabled', '')
    with open('./backup/settings.ini', 'w') as f:
        Settings.write(f)
    threading.Thread(target=reopen).start()

try:
    if korepi_folder and korepi_folder[0]:

        if os.path.isdir(korepi_folder[0]):
            print(f'{bcolors.OKCYAN}[i] Selected folder: {korepi_folder[0]}{bcolors.ENDC}')

        else:
            print(f'{bcolors.WARNING}[Warning] No folder selected, please select your korepi folder.{bcolors.ENDC}')
            select_folder()
            try:
                root.destroy()
            except:
                pass

    else:
        print(f'{bcolors.FAIL}[Error] Failed to retrieve Korepi folder. Selecting folder...{bcolors.ENDC}')

        try: 
            select_folder()
            try:
                root.destroy()
            except:
                pass
        except:
            pass

except OSError as e:
    print(f'{bcolors.FAIL}[Error] Failed to load selected folder: {e}{bcolors.ENDC}')
    
### Download function ###

def downloadInjector():
    try:
        try:
            injector_old = glob.glob('*.zip')
            for old in injector_old:
                os.remove(old)
            injector_file = glob.glob(f'{korepi_folder[0]}*/*.exe')
            for file in injector_file:
                filename = os.path.basename(file)
                if filename not in Ignore:
                        os.remove(file)
                        print(f'Uninstalling {filename}. Reason: Outdated') 
        except:
            pass    

        url = f'https://api.github.com/repos/{GOwner}/{GLocal}/releases/latest'
        response = requests.get(url)
        response.raise_for_status()

        # Get the download URL of the latest injector release
        asset_url = response.json()['assets'][0]['browser_download_url']
        original_name = response.json()['assets'][0]['name']

        # Download the zip file with a progress bar
        print('[i] Starting the download...')
        response = requests.get(asset_url, stream=True)  # Use stream=True for streaming content
        response.raise_for_status()

        # Save the asset to a file
        file_name = f'{original_name}'
        total_size = int(response.headers.get('content-length', 0))  # Get total file size
        block_size = 1024 # Chunk size for updating progress

        with open(file_name, 'wb') as f:
            for data in tqdm(response.iter_content(block_size), total=total_size, unit='B', unit_scale=True, desc='Downloading'):
                f.write(data)

        print(f'{bcolors.OKGREEN}[i] Downloaded Korepi and saved in {korepi_folder[0]}.{bcolors.ENDC}')
        with zipfile.ZipFile(f'./{original_name}', 'r') as zip_ref:
            zip_ref.extractall(f'{korepi_folder[0]}/backup/files')
        threading.Thread(target=reopen).start()
        root.destroy()
    except requests.RequestException as e:
        print(f'{bcolors.FAIL}[!] Error during download: {e}{bcolors.ENDC}')
        return None

def ThreadLocal():
    threading.Thread(target=downloadInjector).start()

### Launch function ###
def ThreadLaunch():
    threading.Thread(target=launch).start()

def launch():
    acco = accSel.get()
    reg = regSel.get()
    LInj = injectorSel.get()

    Settings.set('Settings', 'selacc', acco)
    Settings.set('Settings', 'selreg', reg)
    Settings.set('Settings', 'lastInjector', LInj)

    with open(os.path.join(SettingsPath), 'w') as last:
        Settings.write(last)

    REGION_MAPPING = {
        'EU': 'eu',
        'NA': 'usa',
        'Asia': 'asia',
        'TW/HK/MO': 'thm'
    }
    reg = REGION_MAPPING.get(reg, reg.lower())

    injector_realpath = os.path.dirname(own)
    injector_backup = os.path.abspath(injector_realpath)
    target_injector = LInj
    injector_dir = os.path.dirname(LInj)

    # Get the full path to the executable file that the shortcut points to
    executable = os.path.realpath(os.path.join(injector_dir, os.path.basename(target_injector)))

    if acco == 'Default' and reg == 'default':
        args = [executable]
        print(f'{bcolors.OKGREEN}[i] Selected account: {acco}\n[i] Selected region: {reg}{bcolors.ENDC}')
        subprocess.run(args, cwd=injector_backup)
    if acco == 'Default' and reg != 'default':
        args = [executable,'-region', reg]
        print(f'{bcolors.OKGREEN}[i] Selected account: {acco}\n[i] Selected region: {reg}{bcolors.ENDC}')
        subprocess.run(args, cwd=injector_backup)
    if acco != 'Default' and reg == 'default':
        args = [executable, '-account', acco]
        print(f'{bcolors.OKGREEN}[i] Selected account: {acco}\n[i] Selected region: {reg}{bcolors.ENDC}')
        subprocess.run(args, cwd=injector_backup)
    if acco != 'Default' and reg != 'default':
        args = [executable, '-account', acco, '-region', reg]
        print(f'{bcolors.OKGREEN}[i] Selected account: {acco}\n[i] Selected region: {reg}{bcolors.ENDC}')
        subprocess.run(args, cwd=injector_backup)
try:
    first_folder = LastUsed[4]
    second_folder = LastUsed[5]
except Exception as e:
    print(e)
def enable_skin():
    skin_folder = fd.askdirectory(
        title='Select Skin Folder'
    )
    if skin_folder == '':
        return
    backup_folder = fd.askdirectory(
        title='Select Backup Folder'
    )
    if backup_folder == '':
        return
    Settings.set('Settings', 'SkinFolder', skin_folder)
    Settings.set('Settings', 'Disabled', backup_folder)
    with open('./backup/settings.ini', 'w') as selected:
        Settings.write(selected)
    threading.Thread(target=reopen).start()
    root.destroy()
listbox2 = ''
listbox = ''
selection = ''
selected1 = ''
lastselected = ''
lastfolder = ''
def show_value(selected_option: str):
    global selection, selected1, lastselected, lastfolder
    selected1 = selected_option
    selection = f'{first_folder}/{selected_option}'
    lastselected = selected_option
    lastfolder = f'{first_folder}/{selected_option}'

selection2 = ''
selected2 = ''
def show_value2(selected_option: str):
    global selection2, selected2, lastselected, lastfolder
    selected2 = selected_option
    selection2 = f'{second_folder}/{selected_option}'
    lastselected = selected_option
    lastfolder = f'{second_folder}/{selected_option}'
skin_dirs = []
disabled_dirs = []
def transfer_right():
    if selection == '':
        return print(f'{bcolors.WARNING}[i] No selected folder.{bcolors.ENDC}')
    shutil.move(selection, second_folder)
    global listbox, listbox2
    selected_int = [i for i,x in enumerate(skin_dirs) if x == f'{selected1}']
    for deletion in selected_int:
        named = os.path.basename(selection)
        listbox.delete(deletion)
        listbox2.insert('END', named)
        disabled_dirs.append(selected1)
        skin_dirs.remove(selected1)

def transfer_left():
    if selection2 == '':
        return print(f'{bcolors.WARNING}[i] No selected folder.{bcolors.ENDC}')
    shutil.move(selection2, first_folder)
    global listbox, listbox2
    selected_int = [i for i,x in enumerate(disabled_dirs) if x == f'{selected2}']
    for deletion2 in selected_int:
        named = os.path.basename(selection2)
        listbox2.delete(deletion2)
        listbox.insert('END', named)
        skin_dirs.append(selected2)
        disabled_dirs.remove(selected2)

def download_json():
    webbrowser.open('https://mega.nz/folder/bkwXHTzK#W4gQLg_7CpPPegSfGAj2IA')

def threading_skins(method):
    if method == 'extract':
        threading.Thread(target=extract_skins).start()
    if method == 'left':
        threading.Thread(target=transfer_left).start()
    if method == 'right':
        threading.Thread(target=transfer_right).start()
def extract_skins():
    global listbox2
    selected_rar = fd.askopenfilename(
        title='Select file to extract.',
        filetypes=[('Compressed Files', '.rar .zip')]
    )
    print(selected_rar)
    if selected_rar == None:
        return print('No file selected.')
    try:
        print(f'{bcolors.HEADER}[i] Extracting files...{bcolors.ENDC}')
        with zipfile.ZipFile(selected_rar, 'r') as zipskin:
            zipskin.extractall(second_folder)
            try:
                disabled_dirs = [f.name for f in os.scandir(second_folder) if f.is_dir()]
                disabled_int = 0
                for disable in disabled_dirs:
                    listbox2.insert(disabled_int, disable)
                    disabled_int = disabled_int + 1
                print(f'{bcolors.OKGREEN}[i] Extraction succesful.')
            except:
                pass
    except:
        try:
            print(f'{bcolors.HEADER}[i] Extracting files...{bcolors.ENDC}')
            patoolib.extract_archive(selected_rar, outdir=second_folder)
            try:
                disabled_dirs = [f.name for f in os.scandir(second_folder) if f.is_dir()]
                disabled_int = 0
                for disable in disabled_dirs:
                    listbox2.insert(disabled_int, disable)
                    disabled_int = disabled_int + 1
                print(f'{bcolors.OKGREEN}[i] Extraction succesful.')
            except:
                pass
        except Exception as e:
                print(f'{bcolors.FAIL}[Error] Cannot extract the files. Check if you got an existing folder already.{bcolors.ENDC}')
def edit_inis():
    global lastselected, lastfolder
    ini_files = glob.glob(f'{lastfolder}*/*.ini')
    try:
        for files in ini_files:
            subprocess.Popen(["notepad", files])
    except:
        print('No valid .ini files found.')
def edit_keys():
    saved_keys = []
    saved_headers = []
    lines_to_write = []
    global lastfolder
    ini_files = glob.glob(f'{lastfolder}*/*.ini')
    for ini in ini_files:
        shutil.copy(ini, './backup/files/config.txt')
        with open("./backup/files/config.txt", "r") as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines):
                if 'key' in line:
                    saved_keys.append(line.strip())
                    lines_to_write.append(line_num)
                    prev_line_num = max(0, line_num - 1)
                    while prev_line_num >= 0:
                        prev_line = lines[prev_line_num]
                        if prev_line.startswith("["):
                            saved_headers.append(prev_line.strip())
                            break
                        prev_line_num -= 1
    try:
        if len(line.strip()) >= 3:
            try:
                if prev_line.strip() and line.strip() != '':
                    kd = customtkinter.CTkToplevel()
                    kd.title("Edit Hotkeys")
                    size = len(saved_keys)
                    size_to_set = 105 * size
                    if size_to_set <= 300:
                        size_to_set = 280
                    kd.geometry(f"250x{size_to_set}")
                    kd.iconbitmap('./backup/image.ico')
                    kd.grid_columnconfigure(1, weight=1)
                    kd.grid_columnconfigure((2,3), weight=1)
                    kd.grid_rowconfigure((0,1,2), weight=1)
                    
                    frame = customtkinter.CTkFrame(kd, width= 250,corner_radius=0)
                    frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
                    doubles = {}
                    num = 0
                    rows = 0
                    values_to_save = {}
                    values_to_check = []
                    for value in saved_keys:
                        input_string = value
                        parts = input_string.split("=")
                        if len(parts) == 2:
                            next_part = parts[1].strip()
                            if next_part:
                                next_char = next_part[0]
                        else:
                            print("Failed to get key.")
                        doubles[f'header{num}'] = customtkinter.CTkLabel(frame, text=saved_headers[num], font=('Helvetica', 18, 'bold'))
                        doubles[f'header{num}'].grid(row=rows, column=1, padx=15, pady=(10,10))
                        doubles[f'label{num}']= customtkinter.CTkLabel(frame, text='Key = ', font=('Helvetica', 18, 'bold'))
                        doubles[f'label{num}'].grid(row=rows + 1, column=0, padx=15, pady=(10,10))
                        doubles[f'keys{num}']= customtkinter.CTkEntry(frame, placeholder_text=next_char)
                        doubles[f'keys{num}'].grid(row=rows + 1, column=1, padx=15, pady=(10,10))
                        values_to_check.append(num)
                        num = num + 1
                        rows = rows + 2
                        values_to_save[f'key{num}'] = next_char
                    def save_values():
                        values_to_change = []
                        for_number = 0
                        for num in values_to_check:
                            current_value = doubles[f'keys{num}'].get()[:1]
                            values_to_change.append(current_value)
                        with open('./backup/files/config.txt', 'r') as f:
                                write_line = f.readlines()
                        for line in lines_to_write:
                            if for_number < len(values_to_change):
                                new_value = values_to_change[for_number]
                                write_line.insert(line, f'key = {new_value}\n')
                                line_to_del = line +1
                                del write_line[line_to_del]
                                for_number = for_number + 1
                        with open('./backup/files/config.txt', 'w') as lol:
                            lol.writelines(write_line)
                        for old_ini in ini_files:
                            shutil.copy('./backup/files/config.txt', old_ini)
                        time.sleep(0.1)
                        kd.destroy()
                    save_button = customtkinter.CTkButton(frame, text='Save', command= lambda: save_values())
                    save_button.grid(row=rows + 1, column=1, padx=10, pady=10)
            except Exception as e:
                print('No Keys Found.')
    except:
        pass
def remove_folder():
    global lastfolder, listbox, listbox2
    try:
        selected_int = [i for i,x in enumerate(disabled_dirs) if x == f'{selected2}']
        for deletion2 in selected_int:
            listbox2.delete(deletion2)
            disabled_dirs.remove(selected2)
    except:
        print('Error Removing Folder')
    try:
        selected_int = [i for i,x in enumerate(skin_dirs) if x == f'{selected1}']
        for deletion in selected_int:
            listbox.delete(deletion)
            skin_dirs.remove(selected1)
    except:
        print('Error Removing Folder')
    os.rmdir(lastfolder)
    print(f'Deleted {lastfolder}')
tabview = ''
korek_api = 'https://agent.korepi.com/api/v1'
def enable_key():
    global key_enter, hwid_enter
    key = key_enter.get()[:41]
    hwid = hwid_enter.get()[:32]
    if key == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input a key.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    if hwid == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input the new HWID.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    info = {
        "cardKey": key,
        "hwid": hwid,
    }
    response = requests.post(f'{korek_api}/sign', json=info)
    response_data = response.json()
    try:
        response_message = response_data['message']
        if response_message == 'hwid格式错误(hwid format error)':
            response_message = '=====================================================================\n         HWID format is wrong, please check your HWID.\n=====================================================================\n'
        if response_message == '卡密不存在(card not exist)':
            response_message = '=====================================================================\n         Card does not exist.\n=====================================================================\n'
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text=response_message, font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
    except:
        try:
            f = open(f'{korepi_folder[0]}/enc.json', 'w')
            f.close()
            with open(f'{korepi_folder[0]}/enc.json', 'w') as f:
                json.dump(response_data, f)
            key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Succesfully generated enc.json\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
            key_label.grid(row=5, column=1, padx=0, pady=(10,10))
            time.sleep(5)
            key_label.destroy()
        except Exception as e:
            key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text=f'=====================================================================\n         Unknown Error Has Occured: {e}\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
            key_label.grid(row=5, column=1, padx=0, pady=(10,10))
            time.sleep(5)
            key_label.destroy()
def combine_keys():
    global key_enter, hwid_enter
    oldkey = key_enter.get()[:41]
    newkey = hwid_enter.get()[:41]
    if oldkey == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input your current key.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    if newkey == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input a new key to stack.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    info = {
        "newCardKey": newkey,
        "oldCardKey": oldkey
    }
    response = requests.post(f'{korek_api}/stack', json=info)
    response_data = response.json()
    response_message = response_data['message']
    if response_message == '要叠加的卡密已使用,无法进行叠加处理(The card secret to be stacked has been used and cannot be stacked)':
        response_message = '=====================================================================\n         Card has been already used.\n=====================================================================\n'
    if response_message == '老卡密订阅数据不存在。(Old card subscription data does not exist)':
        response_message = '=====================================================================\n         Old card subscription data does not exist.\n=====================================================================\n'
    if response_message == '卡密不存在或已被删除。(Card does not exist or has been deleted)':
        response_message == '=====================================================================\n         Subscription data does not exist.\n=====================================================================\n'
    key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text=response_message, font=('Helvetica', 10, 'bold'))
    key_label.grid(row=5, column=1, padx=0, pady=(10,10))
    time.sleep(5)
    key_label.destroy()
def unpause_license():
    global key_enter
    key = key_enter.get()[:41]
    if key == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input a key.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    info = {
        "cardKey": key
    }
    response = requests.post(f'{korek_api}/unpause', json=info)
    response_data = response.json()
    response_message = response_data['message']
    if response_message == '当前卡密状态无需取消暂停。(No need to unpause for the current card status)':
        response_message = '=====================================================================\n         Key doesn\'t need to be unpaused.\n=====================================================================\n'
    if response_message == '卡密不存在或已被删除。(Card does not exist or has been deleted)':
        response_message = '=====================================================================\n         Key doesn\'t exist or has been deleted.\n=====================================================================\n'
    key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text=response_message, font=('Helvetica', 10, 'bold'))
    key_label.grid(row=5, column=1, padx=0, pady=(10,10))
    time.sleep(5)
    key_label.destroy()
def pause_license():
    global key_enter
    key = key_enter.get()[:41]
    if key == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input a key.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    info = {
        "cardKey": key
    }
    response = requests.post(f'{korek_api}/pause', json=info)
    response_data = response.json()
    response_message = response_data['message']
    if response_message == '卡密类型不允许暂停。(Card type does not allow pause)':
        response_message = '=====================================================================\n         This key can\'t be paused.\n=====================================================================\n'
    if response_message == '暂停过程中出现错误: null':
        response_message = '=====================================================================\n         An error occured during pause.\n=====================================================================\n'
    if response_message == '卡密不存在或已被删除。(Card does not exist or has been deleted)':
        response_message = '=====================================================================\n         Key doesn\'t exist or has been deleted.\n=====================================================================\n'
    if response_message == 'Успешно поставлено на паузу':
        response_message = '=====================================================================\n         Succesfully Paused\n=====================================================================\n'
    if response_message == '卡密已被暂停。(Card has been paused)':
        response_message = '=====================================================================\n         Card is already paused.\n=====================================================================\n'
    key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text=response_message, font=('Helvetica', 10, 'bold'))
    key_label.grid(row=5, column=1, padx=0, pady=(10,10))
    time.sleep(5)
    key_label.destroy()
def reset_hwid():
    global key_enter, hwid_enter
    key = key_enter.get()[:41]
    hwid = hwid_enter.get()[:32]
    if key == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input a key.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    if hwid == '':
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Please input the new HWID.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
        return
    info = {
        "cardKey": key,
        "newHwid": hwid
    }
    response = requests.post(f'{korek_api}/change-hwid', json=info)
    response_data = response.json()
    response_message = response_data['message']
    if response_message == 'HWID успешно изменен':
        response_message = '=====================================================================\n         Succesfuly Changed HWID\n=====================================================================\n'
    if response_message == '7天内已经重置过HWID,无法再次重置。(HWID has been reset within 7 days, cannot be reset again)':
        response_message = '=====================================================================\n         HWID has been changed within 7 days, wait before changing again.\n=====================================================================\n'
    if response_message == 'hwid格式错误(hwid format error)':
        response_message = '=====================================================================\n         HWID format is wrong, please check your HWID.\n=====================================================================\n'
    key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text=response_message, font=('Helvetica', 10, 'bold'))
    key_label.grid(row=5, column=1, padx=0, pady=(10,10))
    time.sleep(5)
    key_label.destroy()
def get_info():
    global key_enter
    used_key = key_enter.get()[:41]
    info = {
        "cardKey": used_key
    }
    try:
        response = requests.post(f'{korek_api}/get-info', json=info)
        response_data = response.json()
        expiration = response_data['data']['expiry_time']
        timestamp_dt = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S.%f%z")
        readable_time = timestamp_dt.strftime("%B %d, %Y, %I:%M:%S %p")
        current_hwid = response_data['data']['hwid']
        current_status = response_data['data']['statusLabel']
        if current_status == '正常':
            current_status = 'Active'
        if current_status == '过期':
            current_status = 'Expired'
        if current_status == '暂停中':
            current_status = 'Paused'
        if current_status == '封禁':
            current_status = 'Banned'
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text=f'=====================================================================\n         Key Expiration Time (UTC+8): {readable_time}\n         Key Status: {current_status}\n         HWID: {current_hwid}\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
    except Exception as e:
        key_label = customtkinter.CTkLabel(tabview.tab('Key Manager'), text='=====================================================================\n         Suscription does not exist/server error.\n=====================================================================\n', font=('Helvetica', 10, 'bold'))
        key_label.grid(row=5, column=1, padx=0, pady=(10,10))
        time.sleep(5)
        key_label.destroy()
key_enter = ''
hwid_enter = ''
def threading_key(method: str):
    if method == 'info':
        threading.Thread(target=get_info).start()
    if method == 'activation':
        threading.Thread(target=enable_key).start()
    if method == 'reset':
        threading.Thread(target=reset_hwid).start()
    if method == 'pause':
        threading.Thread(target=pause_license).start()
    if method == 'unpause':
        threading.Thread(target=unpause_license).start()
    if method == 'combine':
        threading.Thread(target=combine_keys).start()
def open_folders():
    global lastfolder
    if lastfolder == '':
        print('Please select a folder first.')
    os.startfile(lastfolder)
def similar(a, b: str):
    return SequenceMatcher(None, a, b).ratio()
def similar2(a, b):
    return SequenceMatcher(None, a, b).ratio()
sv = ''
def search_bar(*args: str):
    global skin_dirs, disabled_dirs, sv, listbox2, listbox
    body = sv.get()
    if body == '':
        listbox.delete('all')
        try:
            skin_dirs = [f.name for f in os.scandir(first_folder) if f.is_dir()]
            skin_int = 0
            for skins in skin_dirs:
                listbox.insert(skin_int, skins)
                skin_int = skin_int + 1
        except:
            pass
        listbox2.delete('all')
        try:
            disabled_dirs = [f.name for f in os.scandir(second_folder) if f.is_dir()]
            disabled_int = 0
            for disable in disabled_dirs:
                listbox2.insert(disabled_int, disable)
                disabled_int = disabled_int + 1
        except:
            pass
    else:
        if len(body) <= 3:
            return
        listbox.delete('all')
        listbox2.delete('all')
        position = 0
        position2 = 0
        for folder in skin_dirs:
            similarity = similar(body, folder)
            if body[:len(body)].lower() == folder[:len(body)].lower():
                if similarity <= 0.39:
                    listbox.insert('END', folder)
            if similarity >= 0.4:
                listbox.insert('END', folder)
            position = position + 1
        for folder in disabled_dirs:
            similarity = similar(body, folder)
            if body[:len(body)].lower() == folder[:len(body)].lower():
                if similarity <= 0.39:
                    listbox2.insert('END', folder)
            if similarity >= 0.4:
                listbox2.insert('END', folder)
            position2 = position2 + 1
### Creating GUI ###
try:
    InjectorList = glob.glob(f'*.zip')
    Name = ''.join(InjectorList)

    left_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
    left_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')

    regSel = customtkinter.StringVar(root)
    regSel.set('0')
    Region = customtkinter.CTkOptionMenu(left_frame, values=regions, variable=regSel)
    Region.grid(row=0, column=0, padx=20, pady=(10,10))

    accSel = customtkinter.StringVar(root)
    accSel.set('0')
    Account = customtkinter.CTkOptionMenu(left_frame, values=acc, variable=accSel)
    Account.grid(row=1, column=0, padx=20, pady=(10,10))

    blank1 = customtkinter.CTkLabel(left_frame, text='')
    blank1.grid(row=4, column=0, padx=20, pady=(10,10))

    blank2 = customtkinter.CTkLabel(left_frame, text='')
    blank2.grid(row=5, column=0, padx=20, pady=(10,10))

    blank3 = customtkinter.CTkLabel(left_frame, text='')
    blank3.grid(row=6, column=0, padx=20, pady=(10,10))
    
    blank4 = customtkinter.CTkLabel(left_frame, text='')
    blank4.grid(row=7, column=0, padx=20, pady=(10,10))

    blank6 = customtkinter.CTkLabel(left_frame, text='')
    blank6.grid(row=8, column=0, padx=20, pady=(10,10))
    
    appearance_mode_optionemenu = customtkinter.CTkOptionMenu(left_frame, values=["Dark", "Light", "System"], command=change_appearance_mode_event)
    appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10,10))
    if original_name == Name:
        downloadLocal = customtkinter.CTkButton(left_frame, text='Fix/Download Korepi', command= lambda: ThreadLocal())
        downloadLocal.grid(row=10, column=0, padx=20, pady=(10,10))
    else:
        downloadLocal = customtkinter.CTkButton(left_frame, text='Update Korepi', command= lambda: ThreadLocal())
        downloadLocal.grid(row=10, column=0, padx=20, pady=(10,10))

    downloadJson = customtkinter.CTkButton(left_frame, text='Download TP Jsons', command= lambda: download_json())
    downloadJson.grid(row=11, column=0, padx=20, pady=(10,10))

    tabview = customtkinter.CTkTabview(root, width=670, height= 450)
    tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    tabview.add("Launch Options")
    tabview.add("Skin Manager")
    tabview.add("Key Manager")
    tabview.tab("Launch Options").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
    tabview.tab("Skin Manager").grid_columnconfigure(0, weight=1)
    tabview.tab("Key Manager").grid_columnconfigure(0, weight=1)

    injectorSel = customtkinter.StringVar(tabview.tab('Launch Options'))
    injectorSel.set(InjPath)
    InjSec = customtkinter.CTkOptionMenu(tabview.tab('Launch Options'), values=InjPath, variable=injectorSel)
    InjSec.grid(row=3, column=0, padx=20, pady=10)

    LaunchButton = customtkinter.CTkButton(tabview.tab('Launch Options'), text='Launch', command= lambda: ThreadLaunch())
    LaunchButton.grid(row=2, column=0, padx=20, pady=10)

    urllib.request.urlretrieve("https://raw.githubusercontent.com/Schvis/account_manager/main/image.png", "./backup/image.png")
    byteImgIO = io.BytesIO()
    byteImg = Image.open("./backup/image.png")
    byteImg.save(byteImgIO, "PNG")
    byteImgIO.seek(0)
    byteImg = byteImgIO.read()
    image_pil = Image.open(byteImgIO)
    my_image = customtkinter.CTkImage(dark_image=image_pil,size=(256, 256))

    image_label = customtkinter.CTkLabel(tabview.tab('Launch Options'), image=my_image, text="")
    image_label.grid(row=1, column=0, padx=20, pady=10)

    bframe = customtkinter.CTkFrame(tabview.tab('Key Manager'), width= 200,corner_radius=0)
    bframe.grid(row=0, column=0, rowspan=4, sticky='nsew')

    lframe = customtkinter.CTkFrame(tabview.tab('Key Manager'), width= 60,corner_radius=0)
    lframe.grid(row=0, column=2, rowspan=4, sticky='nsew')

    key_enter= customtkinter.CTkEntry(tabview.tab('Key Manager'), placeholder_text='Key(41)', width= 300)
    key_enter.grid(row=1, column=1, padx=10, pady=(10,10))

    hwid_enter= customtkinter.CTkEntry(tabview.tab('Key Manager'), placeholder_text='HWID(32)/Key to combine(41)', width= 300)
    hwid_enter.grid(row=2, column=1, padx=10, pady=(10,10))

    activate_key = customtkinter.CTkButton(tabview.tab('Key Manager'), text='Activate Key', command=lambda: threading_key('activation'))
    activate_key.grid(row=4, column=1, padx=10, pady=(10,10))

    info_key = customtkinter.CTkButton(tabview.tab('Key Manager'), text='Key Information', command= lambda: threading_key('info'))
    info_key.grid(row=3, column=1, padx=10, pady=(10,10))

    reset_key = customtkinter.CTkButton(tabview.tab('Key Manager'), text='Reset HWID', command= lambda: threading_key('reset'))
    reset_key.grid(row=1, column=0, padx=10, pady=(10,10))

    pause_key = customtkinter.CTkButton(tabview.tab('Key Manager'), text='Pause Key', command= lambda: threading_key('pause'))
    pause_key.grid(row=2, column=0, padx=10, pady=(10,10))

    unpause_key = customtkinter.CTkButton(tabview.tab('Key Manager'), text='Unpause Key', command= lambda: threading_key('unpause'))
    unpause_key.grid(row=3, column=0, padx=10, pady=(10,10))

    stack_key = customtkinter.CTkButton(tabview.tab('Key Manager'), text='Stack Keys', command= lambda: threading_key('combine'))
    stack_key.grid(row=4, column=0, padx=10, pady=(10,10))

    bframe = customtkinter.CTkFrame(tabview.tab('Skin Manager'), width= 200,corner_radius=0)
    bframe.grid(row=0, column=0, rowspan=4, sticky='nsew')

    rframe = customtkinter.CTkFrame(tabview.tab('Skin Manager'), width= 400,corner_radius=0)
    rframe.grid(row=0, column=3, rowspan=4, sticky='nsew')

    listbox = CTkListbox(rframe, height = 220, width = 200, command=show_value)
    listbox.grid(row=1, column=0, padx=10, pady=(5,10))
    listbox.font = ('Helvetica', 8, 'bold')
    # Add subdirectories to the listbox
    try:
        skin_dirs = [f.name for f in os.scandir(first_folder) if f.is_dir()]
        skin_int = 0
        for skins in skin_dirs:
            listbox.insert(skin_int, skins)
            skin_int = skin_int + 1
    except:
        pass

    listbox2 = CTkListbox(rframe, height = 220, width = 200, command=show_value2)
    listbox2.grid(row=1, column=1, padx=10, pady=(5,10))
    listbox2.font = ('Helvetica', 8, 'bold')
    # Add subdirectories to the listbox
    try:
        disabled_dirs = [f.name for f in os.scandir(second_folder) if f.is_dir()]
        disabled_int = 0
        for disable in disabled_dirs:
            listbox2.insert(disabled_int, disable)
            disabled_int = disabled_int + 1
    except:
        pass
    
    move_left = customtkinter.CTkButton(rframe, text='<--', command=lambda: threading_skins('left'))
    move_left.grid(row=8, column=1, padx=10, pady=(10,10))

    move_right = customtkinter.CTkButton(rframe, text='-->', command=lambda: threading_skins('right'))
    move_right.grid(row=8, column=0, padx=10, pady=(10,10))

    blank5_label = customtkinter.CTkLabel(bframe, text='')
    blank5_label.grid(row=0, column=0, padx=10, pady=0)
    
    extract_skin = customtkinter.CTkButton(bframe, text='Extract', command=lambda: threading_skins('extract'))
    extract_skin.grid(row=2, column=0, padx=10, pady=(15,10))

    active_label = customtkinter.CTkLabel(rframe, text='Active Mods', font=('Helvetica', 18, 'bold'))
    active_label.grid(row=0, column=1, padx=10, pady=0)

    disabled_label = customtkinter.CTkLabel(rframe, text='Disabled Mods', font=('Helvetica', 18, 'bold'))
    disabled_label.grid(row=0, column=0, padx=10, pady=(10, 0))

    select_folders = customtkinter.CTkButton(bframe, text='Select Skin Folders', command= lambda: enable_skin())
    select_folders.grid(row=1, column=0, padx=10, pady=(15,10))

    edit_ini = customtkinter.CTkButton(bframe, text='Edit .ini', command= lambda: edit_inis())
    edit_ini.grid(row=3, column=0, padx=10, pady=(15,10))

    edit_key = customtkinter.CTkButton(bframe, text='Edit Hotkeys', command= lambda: edit_keys())
    edit_key.grid(row=4, column=0, padx=10, pady=(15,10))

    open_folder = customtkinter.CTkButton(bframe, text='Open Folder', command= lambda: open_folders())
    open_folder.grid(row=5, column=0, padx=10, pady=(15,10))

    edit_key = customtkinter.CTkButton(bframe, text='Remove', command= lambda: remove_folder())
    edit_key.grid(row=6, column=0, padx=10, pady=(15,10))

    edit_key = customtkinter.CTkLabel(bframe, text='Search: ', font=('Helvetica', 22, 'bold'))
    edit_key.grid(row=7, column=0, padx=10, pady=(15,10))
    
    sv = StringVar()
    search = customtkinter.CTkEntry(tabview.tab('Skin Manager'), placeholder_text='Search Skin', textvariable=sv, width= 500)
    sv.trace_add('write', search_bar)
    search.grid(row=3, column=3, padx=10, pady=(362,10))
except Exception as e:
    print(f'{bcolors.WARNING}[i] Reloading...{bcolors.ENDC}')
    print('GUI Error: ', e)

try:
    Region.set(LastUsed[1] if LastUsed[1] else 'Select Region')
    Account.set(LastUsed[2] if LastUsed[2] else 'Select Account')
    InjSec.set(LastUsed[3] if LastUsed[3] else 'Select Injector')
except Exception as e:
    print(f'{bcolors.WARNING}[Warning] Failed to retrieve last session: {e}{bcolors.ENDC}')
    try:
        Region.set('Select Region')
        Account.set('Select Account')
        InjSec.set('Select Injector')
    except:
        pass

try:
    root.mainloop()
except:
    print(f'{bcolors.WARNING}[i] Loading...{bcolors.ENDC}')
    exit()