import os
import subprocess
from menu import Menu
from Logger import Logger
from pathlib import Path

import Config
import Client

# -----Constants--------------#
# String constants
STR_HEADER = "--------------------------------------------------------------------"
STR_FOOTER = "--------------------------------------------------------------------"
STR_PROMPT = ">>"
STR_HELLO = "Hello"
STR_SUFFIX = ": "
STR_PY_APP_DIR = "[DOCKERIZE PY APP DIR:'{}']"
STR_PY_APP_PATH = "[DOCKERIZE PY APP PATH:'{}']"
STR_COMPOSE_APP_PATH = "[DOCKER COMPOSE APP PATH:'{}']"
STR_PY_FILES = "[Available PY Files::{}]"
# BACK
COMMON_MENU_BACK = "Go back"
# Main Menu Items
MAIN_MENU_ITEM1 = "Docker Basic Operations"
MAIN_MENU_ITEM2 = "Containerize a Python Program"
MAIN_MENU_ITEM3 = "Docker-Compose Demo"
MAIN_MENU_ITEM4 = "Setting"
MAIN_MENU_ITEM5 = "Exit"
# Docker Basic Operations Menu Items
DC_BASIC_MENU_ITEM1 = "List all containers"
DC_BASIC_MENU_ITEM2 = "Run a container[detach={}]"
DC_BASIC_MENU_ITEM3 = "Stop containers"
DC_BASIC_MENU_ITEM4 = "Remove stopped/exited containers"
# "Containerize a Python Program" Menu Items
CTR_PY_PGM_MENU_ITEM1 = "Containerize a Python Program"
CTR_PY_PGM_MENU_ITEM2 = "Run Containerized Python Program"
# "Docker Compose Demo" Menu Items
DC_COMPOSE_DEMO_MENU_ITEM1 = "Run Docker-Compose"
# "Setting" Menu Items
SETTING_MENU_ITEM1 = "Disable Color Menu"
SETTING_MENU_ITEM2 = "Enable Color Menu"
SETTING_MENU_ITEM3 = "Display Docker Client Info"
SETTING_MENU_ITEM4 = "Hide Docker Client Info"

# Menu Titles
TITLE_MAIN_MENU = "\n[Main Menu]"
TITLE_DC_BASIC_MENU = "\n[Docker Basic Operations-Menu]"
TITLE_CTR_PY_PGM_MENU = "\n[Containerize a Python Program-Menu]"
TITLE_DC_COMPOSE_DEMO_MENU = "\n[Run Docker Compose Demo-Menu]"
TITLE_SETTING_MENU = "\n[Setting Menu]"
# Messages
MSG_INFO_WELCOME_MESSAGE = "Select from below options"
MSG_PROMPT_INPUT_IMAGE_NAME = "Input Image Name{}(Press Enter for back)"
MSG_PROMPT_INPUT_CMD = "Input CMD(Optional)"
MSG_PROMPT_INPUT_ID = "Input {} id from above list(Press Enter for back)"
MSG_ERR_INVALID_CONTAINER_ID = "Invalid container id: {}"
MSG_PROMPT_STOP_CONTAINERS = "Do you want to stop all running containers(Y/N):"
MSG_PROMPT_REMOVE_CONTAINERS = "Do you want to remove all stopped containers(Y/N):"
MSG_ERR_WRONG_INPUT = "Wrong Input:{}"
MSG_WARN_IMAGE_EXIST = "Image with name-{} already exist.give another name "
MSG_INFO_STOP_ALL_CONTAINERS = "Stopping all running containers '{}'."
MSG_INFO_REMOVE_ALL_CONTAINERS = "Removing all stopped containers '{}'."
MSG_PROMPT_INPUT_PY_PGM_PATH = "Input path to a python program(press enter for default)"
MSG_PROMPT_INPUT_PY_VERSION = "Using old python version(input 'Y' for 2.7(press enter for default 3.8)"
MSG_INFO_DOCKER_FILE_CREATED = "Dockerfile Created in {} Dir."
MSG_INFO_DOCKER_FILE_CREATING = "Creating Dockerfile in {} Dir."
MSG_ERR_WRONG_PATH = "Path does not exist {}"
MSG_INFO_RUNNING_PY_PGM = "Running Containerized Python Program"
STR_IMAGE_TAG = "{}:latest"
REQUIREMENTS_FILE = "requirements.txt"


class DockerCli:
    # A class for CLI operations on Docker Service.
    # This Docker CLI class used Menu package for creating the Menu for Docker operations.
    # Please refer the below link for more details about Menu package
    # https://pypi.org/project/Menu/#description

    def __init__(self):
        # init
        self.dc_client = None
        self.display_client_info = True
        self.container_run_detach_mode = True

        # -------------Docker Basic Operations-------------
        # Options of  Docker Basic Operations Menu
        self.docker_basic_op_menu_options = [
            (DC_BASIC_MENU_ITEM1, self.list_containers),
            (DC_BASIC_MENU_ITEM2.format(self.container_run_detach_mode), self.run_container),
            (DC_BASIC_MENU_ITEM3, self.stop_container),
            (DC_BASIC_MENU_ITEM4, self.remove_containers),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # Docker Basic Operations Menu
        self.docker_basic_op_menu = Menu(
            options=self.docker_basic_op_menu_options,
            title=TITLE_DC_BASIC_MENU,
            auto_clear=False
        )
        # -------------Containerize a Python Program-------------
        # Options of "Containerize a Python Program" Menu
        self.containerize_py_pgm_menu_options = [
            (CTR_PY_PGM_MENU_ITEM1, self.containerize_py_pgm),
            (CTR_PY_PGM_MENU_ITEM2, self.run_containerize_py_pgm),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # "Containerize a Python Program" Menu
        self.containerize_py_pgm_menu = Menu(
            options=self.containerize_py_pgm_menu_options,
            title=TITLE_CTR_PY_PGM_MENU,
            auto_clear=False
        )
        # -------------Docker Compose Demo-------------
        # Options of "Docker Compose Demo" Menu
        self.docker_compose_menu_options = [
            (DC_COMPOSE_DEMO_MENU_ITEM1, self.run_docker_compose),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # "Docker Compose Demo" Menu
        self.docker_compose_menu = Menu(
            options=self.docker_compose_menu_options,
            title=TITLE_DC_COMPOSE_DEMO_MENU,
            auto_clear=False
        )
        # -------------Setting Menu-------------
        # Options of Setting Menu
        self.setting_menu_options = [
            (SETTING_MENU_ITEM1, self.setting_disable_color_menu),
            (SETTING_MENU_ITEM2, self.setting_enable_color_menu),
            (SETTING_MENU_ITEM3, self.setting_display_client_info),
            (SETTING_MENU_ITEM4, self.setting_hide_client_info),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]

        # Setting Menu
        self.setting_menu = Menu(
            options=self.setting_menu_options,
            title=TITLE_SETTING_MENU,
            refresh=self.set_main_menu_options,
            auto_clear=False
        )
        # -------------Main Menu-------------
        # Options of Main Menu
        self.main_menu_options = [
            (MAIN_MENU_ITEM1, self.docker_basic_op_menu.open),
            (MAIN_MENU_ITEM2, self.containerize_py_pgm_menu.open),
            (MAIN_MENU_ITEM3, self.docker_compose_menu.open),
            (MAIN_MENU_ITEM4, self.setting_menu.open),
            (MAIN_MENU_ITEM5, Menu.CLOSE)
        ]
        # Main Menu
        self.main_menu = Menu(
            title=TITLE_MAIN_MENU,
            message=MSG_INFO_WELCOME_MESSAGE,
            refresh=self.set_main_menu_options,
            auto_clear=False)
        self.main_menu.set_prompt(STR_PROMPT)

    def set_main_menu_options(self):
        # Method will display main menu with client info(if Enable)
        if self.display_client_info:
            self.dc_client.get_client_info()
        self.main_menu.set_options(self.main_menu_options)

    def list_containers(self):
        # List all containers
        Logger.header(STR_HEADER)
        self.dc_client.get_all_containers_list()
        Logger.header(STR_FOOTER)

    def run_container(self):
        # Run a container by input a image name
        while True:
            Logger.header(STR_HEADER)
            self.dc_client.get_all_images_list()
            self.dc_client.get_running_containers_list()
            image_name = input(MSG_PROMPT_INPUT_IMAGE_NAME.format("[<name:tag>]") + STR_SUFFIX)
            if image_name is not None and len(image_name) != 0:
                input_cmd = input(MSG_PROMPT_INPUT_CMD + STR_SUFFIX)
                self.dc_client.run_dc_container(image_name, self.container_run_detach_mode, input_cmd)
            else:
                break
        Logger.header(STR_FOOTER)

    def stop_container(self):
        # Stop containers
        user_selection = None
        while True:
            Logger.header(STR_HEADER)
            running_containers = self.dc_client.get_running_containers_list()
            if len(running_containers) > 0:
                if user_selection is None:
                    user_opt = input(MSG_PROMPT_STOP_CONTAINERS)
                else:
                    user_opt = user_selection
                if user_opt == 'Y' or user_opt == 'y':
                    user_selection = user_opt
                    Logger.info(MSG_INFO_STOP_ALL_CONTAINERS.format(running_containers))
                    self.dc_client.stop_dc_containers(running_containers)
                elif user_opt == 'N' or user_opt == 'n':
                    user_selection = user_opt
                    container_id = input(MSG_PROMPT_INPUT_ID.format("running container") + STR_SUFFIX)
                    if container_id is not None and len(container_id) != 0:
                        if any(running_container.startswith(container_id) for running_container in running_containers):
                            user_cont_list = [container_id]
                            self.dc_client.stop_dc_containers(user_cont_list)
                        else:
                            Logger.err(MSG_ERR_INVALID_CONTAINER_ID.format(container_id))
                    else:
                        break
                else:
                    Logger.warn(MSG_ERR_WRONG_INPUT.format(user_opt))
            else:
                break
        Logger.header(STR_FOOTER)

    def remove_containers(self):
        # Stop containers
        user_selection = None
        while True:
            Logger.header(STR_HEADER)
            stopped_containers = self.dc_client.get_stopped_containers_list()
            if len(stopped_containers) > 0:
                if user_selection is None:
                    user_opt = input(MSG_PROMPT_REMOVE_CONTAINERS)
                else:
                    user_opt = user_selection
                if user_opt == 'Y' or user_opt == 'y':
                    user_selection = user_opt
                    Logger.info(MSG_INFO_REMOVE_ALL_CONTAINERS.format(stopped_containers))
                    self.dc_client.remove_stopped_dc_containers(stopped_containers)
                elif user_opt == 'N' or user_opt == 'n':
                    user_selection = user_opt
                    container_id = input(MSG_PROMPT_INPUT_ID.format("stopped container") + STR_SUFFIX)
                    if container_id is not None and len(container_id) != 0:
                        if any(stopped_container.startswith(container_id) for stopped_container in stopped_containers):
                            user_cont_list = [container_id]
                            self.dc_client.remove_stopped_dc_containers(user_cont_list)
                        else:
                            Logger.err(MSG_ERR_INVALID_CONTAINER_ID.format(container_id))
                    else:
                        break
                else:
                    Logger.warn(MSG_ERR_WRONG_INPUT.format(user_opt))
            else:
                break
        Logger.header(STR_FOOTER)

    def containerize_py_pgm(self):
        while True:
            Logger.header(STR_HEADER)
            try:
                images_list = self.dc_client.get_all_images_list_no_print()
                image_name = input(MSG_PROMPT_INPUT_IMAGE_NAME.format("[<name:tag>]") + STR_SUFFIX)
                if image_name is not None and len(image_name) != 0:
                    new_image_name = STR_IMAGE_TAG.format(image_name) if len(image_name.split(":")) == 1 else image_name
                    if new_image_name not in images_list:
                        py_app_dir = os.path.join(os.getcwd(), Config.DOCKERIZE_PY_APP_PATH)
                        Logger.info(STR_PY_APP_DIR.format(py_app_dir))
                        file_list = self.get_files_from_dir(py_app_dir, ".py")
                        Logger.sub_info(STR_PY_FILES.format(file_list))
                        input_py_version = input(MSG_PROMPT_INPUT_PY_VERSION + STR_SUFFIX)
                        py_pgm_version = '3.8'
                        if input_py_version is not None and len(input_py_version) > 0 and (
                                input_py_version == 'Y' or input_py_version == 'y'):
                            py_pgm_version = '2.7'
                        py_pgm_path = input(MSG_PROMPT_INPUT_PY_PGM_PATH + STR_SUFFIX)
                        if py_pgm_path is None or len(py_pgm_path) == 0:
                            app_file = Config.DOCKERIZE_PY_APP_FILE if py_pgm_version == '3.8' else Config.DOCKERIZE_PY2_APP_FILE
                            py_pgm_path = os.path.join(py_app_dir, app_file)
                        Logger.avail_info(STR_PY_APP_PATH.format(py_pgm_path))
                        if os.path.exists(py_pgm_path):
                            abspath = os.path.abspath(py_pgm_path)
                            parent_path = Path(abspath).parent
                            req_file_path = os.path.join(parent_path, REQUIREMENTS_FILE)
                            # Check if requirements.txt exists
                            is_req_file_exist = "" if os.path.exists(req_file_path) else "#"
                            # For Commenting the requirements.txt section in Dockerfile template
                            base_dir = os.path.basename(parent_path)
                            # For "EXEC_FILE" in Dockerfile template
                            entry_file = os.path.basename(py_pgm_path)
                            # For "BASE_DIR" in Dockerfile template
                            Logger.info("<BASE_DIR>:" + base_dir)
                            docker_file_data_dict = {
                                "PY_VERSION": py_pgm_version,
                                "BASE_DIR": base_dir,
                                "IS_REQ_FILE_EXIST": is_req_file_exist,
                                "EXEC_FILE": entry_file
                            }
                            docker_file_data = Config.DOCKER_FILE_TEMPLATE.format(**docker_file_data_dict)
                            docker_file_path = os.path.join(parent_path, "Dockerfile")
                            Logger.info(MSG_INFO_DOCKER_FILE_CREATING.format(base_dir))
                            file_object = open(docker_file_path, "w+")
                            file_object.write(docker_file_data)
                            file_object.close()
                            Logger.info(MSG_INFO_DOCKER_FILE_CREATED.format(base_dir))
                            self.dc_client.image_from_docker_file(os.path.abspath(parent_path), image_name)
                            Logger.header(MSG_INFO_RUNNING_PY_PGM)
                            self.docker_run(image_name)
                        else:
                            Logger.warn(MSG_ERR_WRONG_PATH.format(py_pgm_path))
                    else:
                        Logger.warn(MSG_WARN_IMAGE_EXIST.format(image_name))
                else:
                    break
            except Exception as ex_err:
                Logger.err(str(ex_err))
        Logger.header(STR_FOOTER)

    def run_containerize_py_pgm(self):
        # run containerize program
        while True:
            Logger.header(STR_HEADER)
            images_list = self.dc_client.get_all_images_list()
            if len(images_list) > 0:
                image_name = input(MSG_PROMPT_INPUT_IMAGE_NAME.format("[<name:tag>]") + STR_SUFFIX)
                if image_name is not None and len(image_name) != 0:
                    new_image_name = STR_IMAGE_TAG.format(image_name) if len(image_name.split(":")) == 1 else image_name
                    if new_image_name not in images_list:
                        Logger.warn(MSG_ERR_WRONG_INPUT.format(image_name))
                    else:
                        self.docker_run(image_name)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    @staticmethod
    def docker_run(image_name):
        # Run docker using subprocess
        try:
            output = subprocess.check_output("docker run -it " + image_name, shell=True)
            Logger.info(output.decode("utf-8"))
        except subprocess.CalledProcessError as err:
            Logger.err(err.output.decode("utf-8"))

    @staticmethod
    def run_docker_compose():
        Logger.header(STR_HEADER)
        try:
            compose_file_path = os.path.join(os.getcwd(), Config.DOCKER_COMPOSE_APP_PATH,"docker-compose.yml")
            Logger.avail_info(STR_COMPOSE_APP_PATH.format(compose_file_path))
            output = subprocess.check_output("docker-compose -f '" + compose_file_path+"' up -d", shell=True)
            Logger.info(output.decode("utf-8"))
        except subprocess.CalledProcessError as err:
            Logger.err(err.output.decode("utf-8"))
        Logger.header(STR_FOOTER)

    def setting_enable_color_menu(self):
        # Enable color Menu
        if self.setting_menu:
            Logger.enable_color()

    def setting_disable_color_menu(self):
        # Enable color Menu to make simple
        if self.setting_menu:
            Logger.disable_color()

    def setting_display_client_info(self):
        # display Docker Client Info
        if self.setting_menu:
            self.display_client_info = True

    def setting_hide_client_info(self):
        # Hide Docker Client Info
        if self.setting_menu:
            self.display_client_info = False

    @staticmethod
    def get_files_from_dir(parent_path, ext):
        file_list = []
        for file in os.listdir(parent_path):
            if not os.path.isdir(os.path.join(parent_path, file)):
                if file.endswith(ext):
                    # exclude dir inside download dir
                    file_list.append(file)
        return file_list

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        # Main method
        self.clear_console()
        self.dc_client = Client.Client()
        self.main_menu.open()


if __name__ == "__main__":
    try:
        DockerCli().run()
    except KeyboardInterrupt as error:
        Logger.err(str(error))
    except Exception as e:
        Logger.err(str(e))
