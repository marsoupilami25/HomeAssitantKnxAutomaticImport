import logging
import os
import sys
from typing import Annotated
import typer

from ClassFromTypedDict import ClassFromTypedDict

import knx_project_management
from knx_function_analyzer.ha_knx_locations_repository import HAKNXLocationsRepository
from knx_function_analyzer.knx_function_analyzer import KNXFunctionAnalyzer
from knx_project_management.knx_project_manager import KNXProjectManager

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
        raise typer.BadParameter(f"'{value}' is not a valid log level. "
                                 f"Options are : {', '.join(VALID_LOG_LEVELS)}")
    return value.upper()

# pylint: disable=too-many-arguments, too-many-positional-arguments
def main(file: Annotated[str, typer.Argument(help="KNX Project file", show_default=False)],
         input_path: Annotated[str, typer.Option("--input-path",
                                                 "-i",
                                                 show_default="Current directory",
                                                 help="Path containing the 'knx' folder "
                                                      "with existing knx configuration file.\n"
                                                      "Inoperative if no roundtrip."
                                                 )] = os.getcwd(),
         output_path: Annotated[str, typer.Option("--output-path",
                                                  "-o",
                                                  show_default="Current directory",
                                                  help="Path for generation. "
                                                       "knx configuration files will be put "
                                                       "in the 'knx' folder."
                                                  )] = os.getcwd(),
         roundtrip: Annotated[bool, typer.Option("--roundtrip",
                                                 "-r",
                                                 help="Indicates to perform a roundtrip "
                                                      "on the yaml configuration files."
                                                 )] = False,
         overwrite: Annotated[bool, typer.Option("--overwrite",
                                                 "-w",
                                                 help="Authorize to overwrite "
                                                      "if files already exist."
                                                 )] = False,
         hamode: Annotated[bool, typer.Option("--hamode",
                                              "-h",
                                                 help="Indicate if a 'knx' entry should be added"
                                                      " at the beginning of the yaml file.\n"
                                                      "Is complementary with the nhamode option. "
                                                      "If none is indicated, the default mode is "
                                                      "nhamode except in roundtrip mode where "
                                                      "the mode is defined from the read yaml."
                                              )] = False,
         nhamode: Annotated[bool, typer.Option("--nhamode",
                                               "-nh",
                                                 help="Indicate that no 'knx' entry will be added "
                                                      "at the beginning of the yaml file.\n"
                                                      "Is complementary with the hamode option. "
                                                      "If none is indicated, the default mode is "
                                                      "nhamode except in roundtrip mode where "
                                                      "the mode is defined from the read yaml."
                                               )] = False,
         log_level: Annotated[str, typer.Option("--log-level",
                                                "-l",
                                                help="Logs level (DEBUG, INFO, WARNING, "
                                                     "ERROR, CRITICAL)",
                                                metavar="[DEBUG|INFO|WARNING|ERROR|CRITICAL]",
                                                show_default=True,
                                                callback=validate_log_level)] = "WARNING"
                                                ):
    """
    HomeAssistantKNXAutomaticImport is a script tool to create configuration
    file for the Home Assistant KNX integration.
    """
    if hamode and nhamode:
        logging.error("hamode and nhamode can't be activated simultaneously")
        sys.exit(1)
    setup_logging(log_level)
    my_locations_repository = HAKNXLocationsRepository()
    if roundtrip:
        logging.info("RoundTrip activated")
        target_path = os.path.join(input_path, "knx")  #path where files are read
        #if the path exists, existing files are loaded
        if not os.path.exists(target_path):
            logging.warning("Path %s does not exists, roundtrip is skipped.", target_path)
        else:
            my_locations_repository.import_from_path(target_path)
    logging.info("Opening %s", file)
    ClassFromTypedDict.import_package(knx_project_management)
    my_project = KNXProjectManager.init(file)
    my_project.print_knx_project_properties()
    my_analyzer = KNXFunctionAnalyzer(my_project)
    my_analyzer.star_analysis()
    logging.info("Start locations analysis")
    my_locations_repository.import_from_knx_spaces_repository(my_analyzer.locations, my_project)
    target_path = os.path.join(output_path, "knx")  #path where files are stored
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)
    if not os.path.isdir(target_path):
        raise NotADirectoryError(f"Output path '{target_path}' is not a directory.")
    if (not hamode) and (not nhamode):
        final_hamode = None
    else:
        final_hamode = hamode
    my_locations_repository.dump(target_path,
                                 create_output_path=True,
                                 overwrite=overwrite,
                                 ha_mode=final_hamode)


if __name__ == "__main__":
    typer.run(main)
