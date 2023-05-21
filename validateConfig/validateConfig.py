import os
from pathlib import Path

from jsonschema import validate
import yaml
import sys


def loadFile(filename):
    with open(filename, "r") as file:
    # with open("/home/runner/work/_actions/HeBaBoRo/OrganizationAction/main/validateConfig/configSchemas/members.yml", "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as err:
            print(err)


def validateConfig(dataFile, schemaFile):
    data = loadFile(dataFile)
    schema = loadFile(schemaFile)

    validate(data, schema) # passes

    bad_instance = """
    testing: ['this', 'is', 'a', 'bad', 'test']
    """

    validate(yaml.full_load(bad_instance), schema)


def getUnvalidatableFiles(schemaFolderPath, configFolderPath):
    unvalidatable = []
    schemas = os.listdir(schemaFolderPath)
    for configFilePath in os.listdir(configFolderPath):
        configFile = Path(configFilePath)
        if configFile.stem + "Schema" + configFile.suffix not in schemas:
            unvalidatable.append(configFile)
    return unvalidatable


def getValidatableFiles(schemaFolderPath, configFolderPath):
    validatable = []
    schemas = os.listdir(schemaFolderPath)
    for configFilePath in os.listdir(configFolderPath):
        configFile = Path(configFilePath)
        if configFile.stem + "Schema" + configFile.suffix in schemas:
            validatable.append(configFile)
    return validatable


def main():
    actionPath = sys.argv[1]
    configFolderPath = sys.argv[1]
    print(actionPath)

    if len(getUnvalidatableFiles(schemaFolderPath="/".join([actionPath, "configSchemas"]),
                                 configFolderPath=configFolderPath)) > 0:
        raise Exception("Unvalidatable files found!")

    for validatableFile in getValidatableFiles(schemaFolderPath="/".join([actionPath, "configSchemas"]),
                                               configFolderPath=configFolderPath):
        validateConfig(actionPath=actionPath,
                       dataFile="/".join([configFolderPath, validatableFile]),
                       schemaFile="/".join([actionPath, "configSchemas", "membersSchema.yml"]))


if __name__ == "__main__":
    main()
