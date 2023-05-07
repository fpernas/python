import docker

def get_container_by_id(docker_client, container_id):
    try:
        return docker_client.containers.get(container_id)
    except docker.errors.NotFound:
        print(f"Container with id {container_id} not found")
        return None
    except docker.errors.APIError:
        print("An error has ocurred")
        return None
    
def get_container_status(docker_client, container_id):
    container = get_container_by_id(docker_client, container_id)
    if (container != None):
        return container.status
    else:
        return "empty"