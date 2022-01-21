import sys

from halo import config_helper
from halo import halo_api_caller
from halo import utility
from halo import json_to_csv


def main():
    global ci_status, ci_value
    utility.Utility.log_stdout("CI_Servers Script Started ...")
    config = config_helper.ConfigHelper()
    json_to_csv_obj = json_to_csv.JSONToCSV()
    output_directory = config.output_directory

    utility.Utility.log_stdout("1- Creating HALO API CALLER Object.")
    halo_api_caller_obj = halo_api_caller.HaloAPICaller(config)

    """
    First we make sure that all configs are sound...
    """
    utility.Utility.log_stdout("2- Checking the provided configuration parameters")
    check_configs(config, halo_api_caller_obj)

    """
    Retrieving and Batching all group servers
    """
    utility.Utility.log_stdout("3- Retrieving and Batching all group servers")
    group_servers_lst = halo_api_caller_obj.get_group_servers(config.target_group_id)
    group_servers_lst_data = group_servers_lst[0]
    servers_data = group_servers_lst_data['servers']
    for server in servers_data:
        if server['containerd_running']:
            ci_status = "true"
            ci_value = "Enabled"

        if not server['containerd_running']:
            ci_status = "false"
            ci_value = "Disabled"

        """
        Batching Container Inspection
        """
        utility.Utility.log_stdout("Server_ID: [%s] , Containerd_Running: [%s] , Container Inspection: [%s]" % (
        server['id'], server['containerd_running'], ci_value))
        batch_response = halo_api_caller_obj.batch_container_inspection(server['id'], ci_status)
        utility.Utility.log_stdout(batch_response)

    """
    Exporting Data of all servers into CSV format
    """
    utility.Utility.log_stdout(
        "4- Exporting Data of all servers into CSV format")
    group_servers_lst = halo_api_caller_obj.get_group_servers(config.target_group_id)
    json_to_csv_obj.convert_json_to_csv(output_directory, group_servers_lst)

    """
    Operation Completed
    """
    utility.Utility.log_stdout(
        "Operation Completed, Check Generated CSV File!")


def check_configs(config, halo_api_caller):
    halo_api_caller_obj = halo_api_caller
    if halo_api_caller_obj.credentials_work() is False:
        utility.Utility.log_stdout("Halo credentials are bad!  Exiting!")
        sys.exit(1)

    if config.sane() is False:
        utility.Utility.log_stdout("Configuration is bad!  Exiting!")
        sys.exit(1)


if __name__ == "__main__":
    main()
