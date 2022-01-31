# ci_servers
Batching container inspection (CI) for servers in the entire environment or in a specific group/s 

## Goal:
The main purpose of this script is to batch container inspection (CI) for servers in the entire environment 
or in a specific group/s. if the server has containers running, then the script will batch container inspection 
to be **"ENABLED"**. Otherwise, the script will batch container inspection to be **"DISABLED"**. 
After batching all the servers, the script exports these results into external CSV file format.

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
| HALO_API_KEY_ID | ID of HALO API Key | ef\*\*ds\*\*fa |
| HALO_API_KEY_SECRET | Secret of HALO API Key | fgfg\*\*\*\*\*heyw\*\*\*\*ter352\*\*\* |
| HALO_API_HOSTNAME | Halo API Host Name | https://api.cloudpassage.com |
| HALO_API_PORT | Halo API Port Number | 443 |
| HALO_API_VERSION | HALO EndPoint Version | v1 |
| TARGET_GROUP_ID | Target Group ID | hte\*\*\*hw42\*\*\*y617\*\*\* |
| OUTPUT_DIRECTORY | Location for generated CSV file | /var/log |

#### Note (Setting TARGET_GROUP_ID):
There are two cases for setting **TARGET_GROUP_ID** variable when batching servers:
1. if the customer wants to batch servers for the entire environment, then there is **NO NEED** to set the variable "TARGET_GROUP_ID".
2. if the customer wants to batch servers that belongs to one or more specific group/s, then these group id/s **MUST BE SET** to the variable "TARGET_GROUP_ID" 
as a comma separated list (i.e. TARGET_GROUP_ID={GROUP_ID_1},{GROUP_ID_2},...,{GROUP_ID_N}).

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
- Retrieve list of servers that belongs to more than one group. 
Used API Endpoint:
```
https://api.cloudpassage.com/v1/servers?group_id={GROUP_ID_1},{GROUP_ID_2},...,{GROUP_ID_N}
```
- Retrieve list of servers that belongs to the entire environment. 
Used API Endpoint:
```
https://api.cloudpassage.com/v1/servers
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

- Export all batched servers into external CSV file format and save it in the provided output directory.


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

- Batch Servers that belongs to specific Group/s.
```
    docker run -it \
    -e HALO_API_KEY_ID=$HALO_API_KEY_ID \
    -e HALO_API_KEY_SECRET=$HALO_API_KEY_SECRET \
    -e TARGET_GROUP_ID=$TARGET_GROUP_ID \
    -v $OUTPUT_DIRECTORY:/var/log \
    ci_servers
```
- Batch Servers that belongs to the entire environment.
```
    docker run -it \
    -e HALO_API_KEY_ID=$HALO_API_KEY_ID \
    -e HALO_API_KEY_SECRET=$HALO_API_KEY_SECRET \
    -v $OUTPUT_DIRECTORY:/var/log \
    ci_servers
```