import docker
import docker.errors

from Logger import Logger


class Client:
    # A class for instantiate Docker Client and its exposing its services
    CONTAINER_LIST_DISPLAY_FORMAT = "  {:<15}{:<25}{:<25}{:<10}{:<25}{}"
    CONTAINER_LIST_HEADER_DISPLAY_FORMAT = CONTAINER_LIST_DISPLAY_FORMAT.format("CONTAINER ID", "IMAGE", "COMMAND",
                                                                                "STATUS", "NAMES", "CREATED")
    IMAGE_LIST_DISPLAY_FORMAT = "  {:<25}{:<15}{:<15}{:<15}{}"
    IMAGE_LIST_HEADER_DISPLAY_FORMAT = IMAGE_LIST_DISPLAY_FORMAT.format("REPOSITORY", "TAG", "IMAGE ID", "SIZE",
                                                                        "CREATED")
    IMAGE_HEADER_DISPLAY_FORMAT = "<Available Local Images>"
    CONTAINERS_HEADER_DISPLAY_FORMAT = "<{} Containers>"
    CLIENT_INFO_DISPLAY_FORMAT = "\t{:<20}{}"
    CLIENT_SUB_INFO_DISPLAY_FORMAT = "\t\t{:<12}{}"
    CLIENT_VERSION_DISPLAY_FORMAT = "----------<{}[{}]>----------"
    STR_FOOTER = "--------------------------------------------------------"
    STR_HEADER_DOCKER_BUILD = '---------------Building Docker Image[Start]---------------'
    STR_FOOTER_DOCKER_BUILD = '----------------Building Docker Image[End]----------------'
    STR_TOTAL_CONTAINER = "Total Containers:"
    STR_RUNNING_CONTAINER = "Running:"
    STR_PAUSED_CONTAINER = "Paused:"
    STR_STOPPED_CONTAINER = "Stopped:"
    STR_IMAGES = "Total Images:"
    MSG_WARN_NO_CONTAINER = "There is no {}Docker Container at this moment.."
    MSG_INFO_CONTAINER_STOPPING = "Container stopping:'{}'"
    MSG_INFO_CONTAINER_STOPPED = "Container stopped:'{}'"
    MSG_INFO_CONTAINER_REMOVING = "Container removing:'{}'"
    MSG_INFO_CONTAINER_REMOVED = "Container removed:'{}'"
    MSG_WARN_NO_IMAGE = "There is no {}Docker Image at this moment.."
    MSG_ERROR = "Error::<{}>"

    STR_IMAGE = "IMAGE"

    def __init__(self):
        # client instance
        self.client = docker.from_env()
        self.low_api_client = docker.APIClient()

    def get_client_info(self):
        # Print client Info
        try:
            c_info = self.client.info()
            c_ver = self.client.version()
            Logger.header(self.CLIENT_VERSION_DISPLAY_FORMAT.format(c_ver["Platform"]["Name"], c_ver["Version"]))
            Logger.info(self.CLIENT_INFO_DISPLAY_FORMAT.format(self.STR_IMAGES, c_info["Images"]))
            Logger.info(self.CLIENT_INFO_DISPLAY_FORMAT.format(self.STR_TOTAL_CONTAINER, c_info["Containers"]))
            Logger.sub_info(
                self.CLIENT_SUB_INFO_DISPLAY_FORMAT.format(self.STR_RUNNING_CONTAINER, c_info["ContainersRunning"]))
            Logger.sub_info(
                self.CLIENT_SUB_INFO_DISPLAY_FORMAT.format(self.STR_PAUSED_CONTAINER, c_info["ContainersPaused"]))
            Logger.sub_info(
                self.CLIENT_SUB_INFO_DISPLAY_FORMAT.format(self.STR_STOPPED_CONTAINER, c_info["ContainersStopped"]))
            Logger.header(self.STR_FOOTER)
        except docker.errors.DockerException as error:
            Logger.err(error)

    def get_all_containers_list(self):
        # Get all containers list
        all_containers_list = self.client.containers.list(all=True)
        if len(all_containers_list) == 0:
            Logger.warn(self.MSG_WARN_NO_CONTAINER.format(""))
            return all_containers_list
        else:
            Logger.sub_info(self.CONTAINERS_HEADER_DISPLAY_FORMAT.format("Available"))
            return self.get_dc_containers_list(all_containers_list)

    def get_running_containers_list(self):
        # Get running containers list
        running_containers_list = self.client.containers.list(filters={"status": "running"})
        if len(running_containers_list) == 0:
            Logger.warn(self.MSG_WARN_NO_CONTAINER.format("running "))
            return running_containers_list
        else:
            Logger.sub_info(self.CONTAINERS_HEADER_DISPLAY_FORMAT.format("Running"))
            return self.get_dc_containers_list(running_containers_list)

    def get_dc_containers_list(self, containers_list):
        # Print all containers list
        try:
            containers = []
            Logger.header(self.CONTAINER_LIST_HEADER_DISPLAY_FORMAT)
            trunk_len = 20
            for container in containers_list:
                containers.append(container.short_id)
                container_id = container.short_id
                container_image = container.attrs['Config']['Image']
                container_image = container_image[0:trunk_len] + ".." if len(
                    container_image) > trunk_len else container_image
                container_cmd = " ".join(container.attrs['Config']['Cmd'])
                container_cmd = "'" + container_cmd[0:trunk_len] + "..'" if len(
                    container_cmd) > trunk_len else "'{}'".format(container_cmd)
                container_name = container.name[0:trunk_len] + ".." if len(
                    container.name) > trunk_len else container.name
                Logger.avail_info(
                    self.CONTAINER_LIST_DISPLAY_FORMAT.format(container_id, container_image, container_cmd,
                                                              container.status, container_name,
                                                              container.attrs['Created']))
        except docker.errors.DockerException as error:
            Logger.err(error)
        return containers

    def run_dc_container(self, image_name, detach_mode, input_cmd):
        # Run a container
        try:
            if input_cmd is not None and len(input_cmd) != 0:
                cmd = input_cmd
                Logger.info("Input CMD:" + str(cmd))
            else:
                cmd = ["sh", "-c", 'while true; do echo hello world; sleep 1; done']
                Logger.info("Default CMD:" + str(cmd))
            container = self.client.containers.run(image_name, cmd, detach=detach_mode)
            if detach_mode:
                logs = container.logs(tail=10)
                Logger.avail_info(str(logs.strip()))
        except docker.errors.DockerException as error:
            Logger.err(error)

    def stop_dc_containers(self, running_containers):
        # Stop running containers
        try:
            for running_container in running_containers:
                container = self.client.containers.get(running_container)
                Logger.info(self.MSG_INFO_CONTAINER_STOPPING.format(container.short_id))
                container.stop()
                Logger.sub_info(self.MSG_INFO_CONTAINER_STOPPED.format(container.short_id))
        except docker.errors.DockerException as error:
            Logger.err(error)

    def get_stopped_containers_list(self):
        # Get stopped containers list
        stopped_containers_list = self.client.containers.list(filters={"status": "exited"})
        if len(stopped_containers_list) == 0:
            Logger.warn(self.MSG_WARN_NO_CONTAINER.format("stopped/exited "))
            return stopped_containers_list
        else:
            Logger.sub_info(self.CONTAINERS_HEADER_DISPLAY_FORMAT.format("Available"))
            return self.get_dc_containers_list(stopped_containers_list)

    def remove_stopped_dc_containers(self, stopped_containers):
        # Removed Stopped containers
        try:
            for stopped_container in stopped_containers:
                container = self.client.containers.get(stopped_container)
                Logger.info(self.MSG_INFO_CONTAINER_REMOVING.format(container.short_id))
                container.remove()
                Logger.sub_info(self.MSG_INFO_CONTAINER_REMOVED.format(container.short_id))
        except docker.errors.DockerException as error:
            Logger.err(error)

    def get_all_images_list(self):
        return self.get_images_list(True)

    def get_all_images_list_no_print(self):
        return self.get_images_list(False)

    def get_images_list(self, display_flag):
        # Get all images list
        all_images_list = self.client.images.list()
        if len(all_images_list) == 0:
            if display_flag:
                Logger.warn(self.MSG_WARN_NO_IMAGE.format("Local "))
            return all_images_list
        else:
            if display_flag:
                Logger.sub_info(self.IMAGE_HEADER_DISPLAY_FORMAT)
            return self.get_dc_images_list(all_images_list, display_flag)

    def get_dc_images_list(self, images_list, display_flag):
        # Print all images list
        try:
            images = []
            if display_flag:
                Logger.header(self.IMAGE_LIST_HEADER_DISPLAY_FORMAT)
            trunk_len = 20
            for image in images_list:
                rep_tag = image.attrs['RepoTags']
                if len(rep_tag) == 0:
                    rep_tag.append("NA:NA")
                repo_tags = rep_tag[0].split(":")
                image_name = repo_tags[0][0:trunk_len] + ".." if len(
                    repo_tags[0]) > trunk_len else repo_tags[0]
                tag = repo_tags[1]
                image_id = image.attrs['Id'].split(":")[1][0:12]
                size = self.format_size(image.attrs['Size'])
                images.append(rep_tag[0])
                if display_flag:
                    Logger.avail_info(
                        self.IMAGE_LIST_DISPLAY_FORMAT.format(image_name, tag, image_id, size, image.attrs['Created']))
        except docker.errors.DockerException as error:
            Logger.err(error)
        return images

    def image_from_docker_file(self, dockerfile_path, image_name):
        try:
            # Build docker image
            Logger.info(self.STR_HEADER_DOCKER_BUILD)
            streamer = self.low_api_client.build(decode=True, nocache=True, path=dockerfile_path, tag=image_name,
                                                 rm=True)
            build_success = True
            for chunk in streamer:
                if 'stream' in chunk:
                    for line in chunk['stream'].splitlines():
                        Logger.info(line)
                if 'error' in chunk:
                    build_success = False
                    Logger.err(self.MSG_ERROR.format(chunk['error']))
            Logger.info(self.STR_FOOTER_DOCKER_BUILD)
            if build_success:
                image = self.client.images.get(image_name)
                self.get_dc_images_list([image], True)
                Logger.info(self.STR_FOOTER)
        except docker.errors.DockerException as error:
            Logger.err(error)

    @staticmethod
    def format_size(size):
        if size > 1000:
            if size > 1000000:
                size = "{:.1f}MB".format(size / 1000000)
            else:
                size = "{:.1f}KB".format(size / 1000)
        else:
            size = "{:.1f}B".format(size)
        return size
