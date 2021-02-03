# DOCKER_CLI_Manual
## Installation on Docker Node
 >**Note:**  All installation instructions are specific to **`[Amazon Linux 2 AMI (HVM), SSD Volume Type - ami-01720b5f421cf0179 (64-bit x86) / ami-04c2a5c7e6c051fb2 (64-bit Arm)]`**
  1. **Prerequisite**
       1. Running  EC2 instance **`[Amazon Linux 2 AMI (HVM), SSD Volume Type - ami-01720b5f421cf0179 (64-bit x86) / ami-04c2a5c7e6c051fb2 (64-bit Arm)]`**
       2. Security groups having `SSH permission`
       3. Security groups having `5000 port open` for docker-compose demo

 2. **Install Docker**
 
		>`sudo yum update -y`
		>`sudo amazon-linux-extras install docker`
    
>**Note:**  Please refer the below link for more details:
[https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
 3.  **Install Docker-Compose**
 
			>`sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
 
 4. **Install python 3**
 
         >`sudo yum install python3`
         
       >**Note:**  python3 is required to run the program.
## Configuration		
 1.  **Change Permission of Docker-Compose:**
 
			>`sudo chmod +x /usr/local/bin/docker-compose`

 2.  **Configure Docker Service:**
		1. **Start the Docker service**
    
			    >`sudo service docker start`
          
		2. **Add the `ec2-user` to the `docker` group so you can execute Docker commands without using `sudo`**.
    
				>`sudo usermod -a -G docker ec2-user`
        
		3.  **Enable Docker Service**
    
			    >`sudo systemctl enable docker.service`
		>**Note:**  
    
		>1. Log out and log back in again to pick up the new `docker` group permissions. You can accomplish this by closing your current SSH terminal window and reconnecting to your instance in a new one. Your new SSH session will have the appropriate `docker` group permissions.
    
		>2. Verify that the `ec2-user` can run Docker commands without `sudo`.
    
		>**`docker info`**
 
 3. **`config.py`** Class

	 Below are the config parameter defined in `config.py` class.
	 1. DOCKERIZE_PY_APP_PATH **(default `'./DOCKERIZE_PY_APP/'`)**
	 2. DOCKERIZE_PY_APP_FILE **(default`'app.py'[3.8 version] `)**
	 3. DOCKERIZE_PY2_APP_FILE **(default `'app2.py'[2.7 version]`)**
	 4. DOCKER_COMPOSE_APP_PATH **(default `'./DOCKER_COMPOSE_DEMO_APP/'`)**
	 5. DOCKER_FILE_TEMPLATE **(template for creating docker file)**
 4.  **Copy  `DOCKER_CLI` and run `requirements.txt`**
	 1. Copy the `DOCKER_CLI` from local to Docker node using winscp or any other tool.
      2. Go to root dir  `DOCKER_CLI` 
      3.  Run below command
			  > `sudo python3 -m pip install -r requirements.txt`
			  
## RUN
 1. **Run Docker-CLI program**
 
    >**Note:**  Do the `SSH`  to Docker Node 
	 1. Go to root dir  `DOCKER_CLI` 
	 2. Run below command 
   
			  >`python3 DockerCli.py`
## Menu Description

#### Main Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/ec2_docker/main/main_menu.png)
 >`Press-1` for navigate to `Docker Basic Operations` Menu. 
 
> `Press-2` for navigate to `Containerize a Python Program` Menu.

> `Press-3` for navigate to `Docker Compose Demo` Menu.

> `Press-4` for navigate to `Setting` Menu.

> `Press-5` for Exit.

#### 1.`Docker Basic Operations` Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/ec2_docker/main/docker_basic_menu.png)

 >`Press-1` List all containers. 
 
> `Press-2` Run a container[detach Mode].

> `Press-3` Stop containers.

> `Press-4` Remove stopped/exited containers.

> `Press-5` Go Back.

#### 2. `Containerize a Python Program` Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/ec2_docker/main/containerize_py_pgm_menu.png)

 >`Press-1` Containerize and Run a Python Program. 
 
> `Press-2` Run a Python Program.

> `Press-3` Go Back.

#### 3. `Docker Compose Demo` Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/ec2_docker/main/docker_compose_menu.png)

 >`Press-1` Run Docker Compose Demo. 
 
> `Press-2` Go Back.

#### 4. `Setting` Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/ec2_docker/main/setting_menu.png)

> `Press-1` for disabling the color menu. **(default `enable`)**

>  `Press-2` for enable color menu after disabling.

> `Press-3` for display "Docker Client Info"  in Main Menu.**(default `display`)**

> `Press-4`for hiding "Docker Client Info"  in Main Menu.

>  `Press-5` Go Back.

## Notes
> 1. For Docker Compose i have taken the reference from below link and modified(Added new containers) for demo.
>[https://github.com/arsenidze/microservice_application](https://github.com/arsenidze/microservice_application)
> 2. Docker-Compose APP Details:


![enter image description here](https://raw.githubusercontent.com/GitPointer/ec2_docker/main/Docker-Compose-App-Details.png)


> 3. After `Docker-Compose Demo`  run successfully.App can be open in browser using `Docker AMI public IP`
> **http://Public_IP_of_Docker_Node:5000**

![enter image description here](https://raw.githubusercontent.com/GitPointer/ec2_docker/main/docker_compose_result.png)
