import os


def copier(copy_from, copy_to):
    return os.system('xcopy /e /i "{}" "{}"'.format(copy_from, copy_to))


def get_setting(file):
    setting = file.readline()
    setting = setting[setting.find('"')+1: -2]
    return setting


def main():
    # Константы
    settings_file = open('WoW UI Copier Settings.txt', 'r', encoding="utf-8")
    WOW_DIRECTORY = get_setting(settings_file)
    ACC_NAME = get_setting(settings_file)
    SERVER_NAME = get_setting(settings_file)
    CHR_NAME = get_setting(settings_file)
    INSTRUCTION_FILE_NAME = 'WoW UI Copier Instruction.txt'
    NEW_FOLDER_NAME = get_setting(settings_file)
    NEW_CHR_FOLDER_NAME = get_setting(settings_file)
    NEW_ACC_FOLDER_NAME = get_setting(settings_file)
    NEW_INSTRUCTION_FILE_NAME = 'Установка.txt'
    settings_file.close()

    # Директории
    new_folder_directory = '{0}\\{1}'.format(WOW_DIRECTORY, NEW_FOLDER_NAME)
    new_chr_folder_directory = '{0}\\{1}'.format(new_folder_directory, NEW_CHR_FOLDER_NAME)
    new_acc_folder_directory = '{0}\\{1}'.format(new_folder_directory, NEW_ACC_FOLDER_NAME)
    new_interface_folder_directory = '{0}\\Interface'.format(new_folder_directory)
    new_fonts_folder_directory = '{0}\\Fonts'.format(new_folder_directory)
    chr_folder_directory = '{0}\\WTF\\Account\\{1}\\{2}\\{3}\\SavedVariables'.format(WOW_DIRECTORY, ACC_NAME,
                                                                                     SERVER_NAME, CHR_NAME)
    acc_folder_directory = '{0}\\WTF\\Account\\{1}\\SavedVariables'.format(WOW_DIRECTORY, ACC_NAME)
    interface_folder_directory = '{0}\\Interface'.format(WOW_DIRECTORY)
    fonts_folder_directory = '{0}\\Fonts'.format(WOW_DIRECTORY)
    instruction_directory = '{0}/{1}'.format(new_folder_directory, NEW_INSTRUCTION_FILE_NAME)
    instruction_directory = instruction_directory.replace('\\', '/')

    # Смена кодировки в cmd на UTF-8
    os.system('chcp 65001')

    print('md "{0}"'.format(new_chr_folder_directory))

    # Создание временной директории
    if os.system('md "{0}"'.format(new_chr_folder_directory)) or os.system('md "{0}"'.format(new_acc_folder_directory)):
        return 'temporary folder creating error'

    # Копирование настроек аккаунта
    if copier(acc_folder_directory, new_acc_folder_directory):
        return 'copying account settings error'

    # Копирование настроек персонажа
    if copier(chr_folder_directory, new_chr_folder_directory):
        return 'copying character settings error'

    # Копирование папки Interface
    if copier(interface_folder_directory, new_interface_folder_directory):
        return 'copying Interface folder error'

    # Копирование шрифтов
    font_err = copier(fonts_folder_directory, new_fonts_folder_directory)

    # Инструкция
    instruction_file = open(INSTRUCTION_FILE_NAME, 'r', encoding='utf-8')
    INSTRUCTION_TEXT = instruction_file.read()
    instruction_file.close()
    instruction_file = open(instruction_directory, 'w')
    instruction_file.write(INSTRUCTION_TEXT)
    instruction_file.close()

    # Архивирование
    print('data archiving, please wait...')
    command = 'tar.exe -c -a -f "{0}.zip" -C "{1}" "{2}"'.format(new_folder_directory, WOW_DIRECTORY, NEW_FOLDER_NAME)
    if os.system(command):
        return 'data archiving error'

    # Удаление временных файлов
    command = 'rd /s /q "{0}"'.format(new_folder_directory)
    if os.system(command):
        return 'temporary folder deleting error'

    # Завершение работы
    print('\n-----------------------------------------------------------------------------------------------------')
    print('The interface was copied successfully!')
    if font_err:
        print("\033[33m {}".format("WARNING: Fonts folder wasn't copy"))
    return 0


if __name__ == '__main__':
    Error = main()
    if Error:
        print("\033[31m ERROR: {}" .format(Error))
