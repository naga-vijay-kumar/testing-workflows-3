
import argparse
import json
import os.path
import requests
import subprocess
import sys
import re
import yaml



directory = "trigmetry2.0-alert-configs/"
confluence_link = "https://confluence.freshworks.com/pages/viewpage.action?spaceKey=HAYS&title=Testing+Trigmetry+alerts+in+Local"
# promtool_path = "prometheus-2.31.1.darwin-amd64/promtool"
# amtool_path = "old_alertmanager-0.23.0.darwin-amd64/amtool"


promtool_path = "prometheus-2.31.1.linux-amd64/promtool"
amtool_path = "alertmanager-0.23.0.linux-amd64/amtool"

def modify_alertmanager():
    with open('trigmetry2.0-alert-configs/alertmanager.yml', 'r') as file:
        configuration = yaml.safe_load(file)

    configuration["global"]["smtp_smarthost"] = "smtp.sendgrid.net:587"


    with open('trigmetry2.0-alert-configs/alertmanager.yml', 'w') as outfile:
        yaml.dump(configuration, outfile, default_flow_style=False)
        
        
def validate_alert_rules():
    err_files = "\n\nError Files :: \n"

    i = 1;
    for filename in os.listdir(directory):
        # if(filename == "notification.yml" or ( not (filename.endswith(".yml"))) or filename == "alertmanager_copy.yml" or filename=="alertmanager.yml" or filename=="rules.yml"):
        if(filename == "notification.yml" or ( not (filename.endswith(".yml")))):
               continue;

        if (filename == "alertmanager.yml"):
            run = subprocess.Popen([amtool_path, 'check-config', directory+filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        else:        
            #promtool old version
            run = subprocess.Popen([promtool_path, 'check', 'rules', directory+filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        

        stddata = run.communicate()[0]
        if("FAILED" in stddata):
            err_files = err_files + (f"{i}. {filename}\n")
            i +=1


    if(len(err_files)>19):
        err_files = err_files + f"\n Dont't know how to test Trigmetry alerts in local.\n use the blow link.\n {confluence_link}"
        raise Exception(err_files)


    print("All Good to go")

if __name__ == "__main__":
    modify_alertmanager()
    validate_alert_rules()


