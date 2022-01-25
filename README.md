# ci_servers
Batching container inspection (CI) for servers in a specific group

## Goal:
The main purpose of this script is to batch container inspection (CI) for a specific group servers. 
if the server has containers running, then the script will batch container inspection to be **"ENABLED"**. 
Otherwise, the script will batch container inspection to be **"DISABLED"**. 
After batching all the group servers, the script exports these results into external CSV file.

## Requirements:
- CloudPassage Halo API key (with Administrator privileges).
- Python 3.6 or later including packages specified in "requirements.txt".

## Installation:

```
   git clone https://github.com/cloudpassage/ci_servers.git
   cd ci_servers
   pip install -r requirements.txt
```

## Configuration:
| Variable | Description | Default Value |
| -------- | ----- | ----- |
| HALO_API_KEY_ID | ID of HALO API Key | <HALO_API_KEY_ID> |
| HALO_API_KEY_SECRET | Secret of HALO API Key | <HALO_API_KEY_SECRET> |
| HALO_API_HOSTNAME | Halo API Host Name | https://api.cloudpassage.com |
| HALO_API_PORT | Halo API Port Number | 443 |
| HALO_API_VERSION | HALO EndPoint Version | v1 |
| TARGET_GROUP_ID | Target Group ID | <TARGET_GROUP_ID> |
| OUTPUT_DIRECTORY | Location for generated CSV file | /var/log |

## How the scripts works:
- Use HALO API key id/secret to generate access token to be used to access Protected HALO resources. 
Used API Endpoint:
```
https://api.cloudpassage.com/oauth/access_token?grant_type=client_credentials
```

- Retrieve list of servers that belongs to a specific group. 
Used API Endpoint:
```
https://api.cloudpassage.com/v1/servers?group_id={GROUP_ID}
```

- Loop on the retrieved list of servers and check the container status. Whether running or no.
Property used in checking: **"containerd_running"**

- If the container status is running, then set **Container Inspection (CI)** to **ENABLED**
Used API Endpoint:
```
https://api.cloudpassage.com/v1/servers/batch
```
Request:
```
{
    "ids": [
        "<SERVER_ID>"
    ],
    "data": {
        "container_inspection": true
    }
}
```

- If the container status is not running, then set **Container Inspection (CI)** to **DISABLED**
```
https://api.cloudpassage.com/v1/servers/batch
```
Request:
```
{
    "ids": [
        "<SERVER_ID>"
    ],
    "data": {
        "container_inspection": false
    }
}
```

- Export all batched servers into external CSV file format in the provided output directory.


## How to run the tool (stand-alone):
To run the script follow the below steps.

1.  Navigate to the app folder that contains module "runner.py", and run it

```
    cd ci_servers/app
    python runner.py
```

## How to run the tool (containerized):
Clone the code and build the container:

```
   git clone https://github.com/cloudpassage/ci_servers.git
   cd ci_servers
   docker build -t ci_servers .
```

To run the container interactively:

```
    docker run -it \
    -e HALO_API_KEY_ID=$HALO_API_KEY_ID \
    -e HALO_API_KEY_SECRET=$HALO_API_KEY_SECRET \
    -e TARGET_GROUP_ID=$TARGET_GROUP_ID \
    -v $OUTPUT_DIRECTORY:/var/log \
    ci_servers
```