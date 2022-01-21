# CI_Servers
Batching Container Inspection for Servers in a specific group

## Goal:
The main purpose of this tool is to batch container inspection for a specific group servers. if the server has containers running, then the script will batch container inspection to be "ENABLED". Otherwise the script will batch container inspection to be "DISABLED". After completing the batch operation, the script exports these results into CSV file.

## Requirements:
- CloudPassage Halo API key (with Administrator privileges).
- Python 3.6 or later including packages specified in "requirements.txt".

## Installation:

```
   git clone https://github.com/cloudpassage/CI_Servers.git
   cd CI_Servers
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


## How to run the tool (stand-alone):
To run the script follow the below steps.

1.  Navigate to the app folder that contains module "runner.py", and run it

```
    cd CI_Servers/app
    python runner.py
```

## How to run the tool (containerized):
Clone the code and build the container:

```
   git clone https://github.com/cloudpassage/CI_Servers.git
   cd CI_Servers
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