#!/usr/bin/env python3

import os
import yaml

class ConfigurationManager:
    """A tool to allow a program to init from a GIT pull and build its configuration during the first test run"""
    
    def __init__(self, defualt_directory = "",config_filename = "config.yaml"):
        """Initalisation of the Configuration Manager"""
        self.config_filename = config_filename
        self.default_directory = defualt_directory
        self.manage_startup_configuration()

    def manage_startup_configuration(self):
        """
        Overall management of the 2 configurations
        Confirm defualt exists, compare versions to operating config
        enforce comparible versioning through a useable interface
        """
        default_config_data = {}
        if(self.check_default_config_file()):
            default_config_data = self.read_default_config_file()
            #print(default_config_data)
            update_needed_to_configuration = True
            while(update_needed_to_configuration):
                data = {}
                if(self.check_config_file()):
                    data = self.read_config_file()
                    if(data['version'] == default_config_data['version']):
                        update_needed_to_configuration = False
                    else:
                        print("Default configuration version greater than current configuration")
                else:
                    print("No configuration file found")
                    
                
                if(update_needed_to_configuration):
                    if(self.prompt_for_new_configuration_file()):
                        print("Starting generation for config")
                        new_config = {}
                        new_config = self.collect_configuration_data(default_config_data,data)
                        print(new_config)
                        self.make_configuration_file(new_config ,self.default_directory, self.config_filename)
                    elif(self.prompt_for_copy_configuration_file()):
                        new_config = default_config_data
                        self.make_configuration_file(new_config ,self.default_directory, self.config_filename)
        else:
            print("No default file found")

    def prompt_for_copy_configuration_file(self):
        """Queries the user whether they wish to copy a new configuration"""
        return self.collect_input_data("Would you like to copy the configuration file from the default?")

    def prompt_for_new_configuration_file(self):
        """Queries the user whether they wish to edit/create a new configuration"""
        return self.collect_input_data("Would you like to generate the configuration file from the default (while editting)?")

    def collect_input_data(self, question, response_type = "y/n", default_val = ""):
        """Collects a single unit data"""
        input_str = ""
        while(input_str ==  ""):
            input_str = input(f"{question} ({response_type}): ")
            if(input_str == ""):
                input_str = str(default_val)

            if(response_type == "y/n"):
                if(input_str.lower() == "y"):
                    return True
                elif(input_str.lower() == "n"):
                    return False
                else:
                    input_str = ""

            elif(response_type == "int"):
                value = None
                try:
                    value = int(input_str)
                except ValueError:
                    pass
                if(value):
                    return value
                else:
                    input_str = ""

            elif(response_type == "float"):
                value = None
                try:
                    value = float(input_str)
                except ValueError:
                    pass
                if(value):
                    return value
                else:
                    input_str = ""

            elif(response_type == "bool"):
                if(input_str.lower() == "true"):
                    return True
                elif(input_str.lower() == "false"):
                    return False
                else:
                    input_str = ""
            elif(response_type == "str"):
                return input_str
            else:
                print(f"{response_type} currently unimplemented - None will be recorded for this.")
                return None

    def collect_configuration_data(self, default_config_data, config_data):
        """Collects the user data alongside the default configuration data"""
        new_config = {}
        for keys, values in default_config_data.items():
            new_val = 0
            if(keys == "version"):
                new_val = values
            else:
                question = f"var: {keys}\tdefault:\t{values}\tcurrent:\t{config_data.get(keys)}\t\tWhat do you want to set it to? (enter to retain value)"
                new_val = self.collect_input_data(question, str(type(values).__name__), config_data.get(keys))
            new_config[keys] = new_val
        return new_config

    def make_configuration_file(self, new_config, default_directory, config_filename):
        """Takes the congifuration data along with directory and filename to produce the config.yaml file"""
        with open(f"{default_directory}\{config_filename}", 'w') as f:
            yaml.dump(new_config, f, sort_keys=False)

    def check_config_file(self):
        """checks whether the configuration file exists"""
        return os.path.exists(f"{self.default_directory}{self.config_filename}")

    def check_default_config_file(self):
        """checks whether the default_configuration file exists"""
        return os.path.exists(f"{self.default_directory}default_{self.config_filename}")

    def read_config_file(self):
        """Reads the config.yaml file"""
        data = self.read_file(self.default_directory, self.config_filename)
        return data
        
    def read_default_config_file(self):
        """Reads the default_config.yaml file"""
        data = self.read_file(self.default_directory,f"default_{self.config_filename}")
        return data

    def read_file(self,directory,filename):
        try:
            with open(f"{directory}{filename}") as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
                return data
        except FileNotFoundError:
            print(f"No {filename} file found in directory.")

if __name__ == "__main__":
    folder_name = "configuration/"
    print(f"\nConfiguration Manager Test\n\nYou should have a folder named: {folder_name}\nwhich contains a default_config.yaml as the very least.")
    config_man = ConfigurationManager(folder_name)
#.gitignore config.yaml
