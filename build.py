
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import uuid
from zipfile import ZipFile

#Глобальные параметры
guid = str(uuid.uuid4())

# Настройки путей
root_dir = "./"  # Путь к проекту
resources_dir = os.path.join(root_dir, "resources")     # Папка ресурсов (зависимости, иконки, файлы конфигурации)
source_dir = os.path.join(root_dir, "resources")        # Папка проектов (проекты .NET)
projects_dir = {
    "addin": os.path.join(root_dir, "addin"),           # Папка проекта расширения. Шенерируется подключаемая к Inventor библиотека
    "common": os.path.join(root_dir, "common")          # Папка проекта общего и вспомогательного кода для расширения
    }
output_dir = os.path.join(root_dir, "package"),         # Папка для итоговых файлов


#Настройка манифеста
manifest_path = os.path.join(output_dir, "manifest.addin")
class_id = f"{guid}"
client_id = f"{guid}"
display_name = "Inventor support addin"
description = "Addin for support with some unsafe operations"
assembly = "addin.dll"
os_type = "Win64"
load_automatically = 1
user_unloadable = 1
hidden = 0
supported_software_version = "16.."
data_version = 1
load_behavior = 1
user_interface_version=1


# Функция подготовки данных перед сборкой
def pre_build_operations():
    print("Выполнение предсборочных операций...")
    # Здесь можно добавить код для подготовки данных
    # Например, удаление старых сборок, создание необходимых папок и т.д.
    for dir in projects_dir:
        bin = os.path.join(dir, "bin")
        obj = os.path.join(dir, "obj")
        if os.path.exists(bin): shutil.rmtree(bin)
        if os.path.exists(obj): shutil.rmtree(obj)
    if os.path.exists(output_dir): shutil.rmtree(output_dir)
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    print("Предсборочные операции выполнены.")

# Функция для сборки проекта
def build_project():
    print("Сборка проекта...")
    # Пример сборки через dotnet CLI, можно изменить команду под ваш проект
    result = subprocess.run(["dotnet", "build", "--configuration", "Release", root_dir], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Ошибка сборки проекта!")
        exit(1)
    print("Сборка проекта завершена успешно.")

# Функция генерации XML-файлов
def generate_manifest():
    print("Генерация XML-файлов...")
    
    # Создаем корневой элемент
    addin = ET.Element("Addin", Type="Standard")
    
    # Комментарий с версией Inventor
    comment = ET.Comment("Created for Autodesk Inventor Version 17.0")
    addin.append(comment)
    
    # Добавляем дочерние элементы
    ET.SubElement(addin, "ClassId").text = class_id
    ET.SubElement(addin, "ClientId").text = client_id
    ET.SubElement(addin, "DisplayName").text = display_name
    ET.SubElement(addin, "Description").text = description
    ET.SubElement(addin, "Assembly").text = assembly
    ET.SubElement(addin, "OSType").text = os_type
    ET.SubElement(addin, "LoadAutomatically").text = str(load_automatically)
    ET.SubElement(addin, "UserUnloadable").text = str(user_unloadable)
    ET.SubElement(addin, "Hidden").text = str(hidden)
    ET.SubElement(addin, "SupportedSoftwareVersionGreaterThan").text = supported_software_version
    ET.SubElement(addin, "DataVersion").text = str(data_version)
    ET.SubElement(addin, "LoadBehavior").text = str(load_behavior)
    ET.SubElement(addin, "UserInterfaceVersion").text = str(user_interface_version)
    
    # Создаем дерево и записываем в файл
    tree = ET.ElementTree(addin)
    tree.write(manifest_path, encoding="utf-8", xml_declaration=True)
    
    print(f"XML файл создан: {manifest_path}")

# Функция копирования файлов в нужную структуру каталогов
def copy_files():
    print("Копирование файлов...")
    target_dir = os.path.join(output_dir, "final_structure")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Пример копирования файлов, можно адаптировать под ваши нужды
    shutil.copy(os.path.join(build_dirs, "your_compiled_file.dll"), target_dir)
    print(f"Файлы скопированы в папку: {target_dir}")

# Функция архивирования каталога
def archive_directory():
    print("Архивирование каталога...")
    archive_path = os.path.join(output_dir, "final_structure.zip")
    with ZipFile(archive_path, 'w') as zipf:
        for root, dirs, files in os.walk(os.path.join(output_dir, "final_structure")):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(output_dir, "final_structure")))
    print(f"Каталог заархивирован: {archive_path}")

if __name__ == "__main__":
    # Выполнение всех операций
    pre_build_operations()
    build_project()
    generate_manifest()
    copy_files()
    archive_directory()
    print("Все операции выполнены успешно.")
