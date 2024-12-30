import logging
import os
from typing import Annotated

import typer
import KNXProjectManagement

from KNXFunctionAnalyzer.HAKNXLocationsRepository import HAKNXLocationsRepository
from KNXFunctionAnalyzer.KNXFunctionAnalyzer import KNXFunctionAnalyzer
from KNXProjectManagement.KNXProjectManager import KNXProjectManager
from ClassFromTypedDict import ClassFromTypedDict

# Create Typer application instance
app = typer.Typer()

# Authorized logs levels
VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Logs configuration
def setup_logging(level: str):
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level,
                        format="%(levelname)s - %(message)s")

# Function to validate log level
def validate_log_level(value: str):
    if value.upper() not in VALID_LOG_LEVELS:
        raise typer.BadParameter(f"'{value}' is not a valid log level. Options are : {', '.join(VALID_LOG_LEVELS)}")
    return value.upper()

def main(file: str,
         output_path: Annotated[str, typer.Option("--output-path","-o")] = os.getcwd(),
         log_level: Annotated[str, typer.Option("--log-level","-l",
             help="Logs level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
             metavar="[DEBUG|INFO|WARNING|ERROR|CRITICAL]",
             show_default=True,
             callback=validate_log_level )] = "WARNING"
         ):
    setup_logging(log_level)
    my_locations_repository = HAKNXLocationsRepository()
    target_path = os.path.join(output_path, "knx") #path where files are stored
    #if the path exists, existing files are loaded
    if os.path.exists(target_path):
        logging.info(f"Path {target_path} already exists, try to open existing yaml files")
        for file_name in os.listdir(target_path):
            if file_name.endswith(".yaml"):
                file_path = os.path.join(target_path, file_name)
                with open(file_path, 'r') as yaml_file:
                    logging.info(f"Read file {file_path}")
                    pass
    logging.info(f"Opening {file}")
    # ClassFromTypedDict.set_typeddict_class_association({
    #     'DPTType' : 'KNXProjectManagement.KNXDPTType.KNXDPTType',
    #     'ProjectInfo' : "KNXProjectManagement.KNXProjectInfo.KNXProjectInfo"
    # })
    ClassFromTypedDict.import_package(KNXProjectManagement)
    my_project = KNXProjectManager.init(file)
    my_project.print_knx_project_properties()
    my_analyzer = KNXFunctionAnalyzer(my_project)
    my_analyzer.star_analysis()
    logging.info("Start locations analysis")
    my_locations_repository.import_from_knx_spaces_repository(my_analyzer.locations, my_project)
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)
    if not os.path.isdir(target_path):
        raise NotADirectoryError(f"Output path '{target_path}' is not a directory.")
    my_locations_repository.dump(target_path, create_output_path=True, overwrite=True)


if __name__ == "__main__":
    typer.run(main)
