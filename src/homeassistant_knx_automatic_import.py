import logging
import os
import sys
from typing import Annotated
import typer

from classfromtypeddict import ClassFromTypedDict

from hakai_packages import knx_project_objects
from hakai_packages import HAKNXLocationsRepository
from hakai_packages import KNXSpaceAnalyzer
from hakai_packages import KNXProjectManager
from hakai_packages import __version__
from hakai_packages import HAKAIConfiguration

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

def version_callback(value: bool):
    if value:
        typer.echo(f"HomeAssistantKNXAutomaticImport {__version__}")
        raise typer.Exit()

# pylint: disable=too-many-arguments, too-many-positional-arguments
def main(file: Annotated[str, typer.Argument(help="KNX Project file", show_default=False)],
         _version: Annotated[bool | None, typer.Option("--version",
                                                       callback=version_callback,
                                                       is_eager=True)] = None,
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
         location_separator: Annotated[str, typer.Option("--location-separator",
                                                 "-ls",
                                                 show_default = True,
                                                 help="Separator (character) used to separate"
                                                      "location level names in a location name.\n"
                                                      "Use only letters, numbers, and underscores. "
                                                      "'/' indicates no separator."
                                                 )] = '_',
         suppress_project_name: Annotated[bool, typer.Option("--suppress-project-name",
                                               "-spn",
                                               help="Remove the project name in the full"
                                                    "location name."
                                               )] = False,
         replace_spaces: Annotated[str, typer.Option("--replace-spaces",
                                                             "-rs",
                                                     show_default = ' ',
                                                     help="Replace spaces in location and "
                                                          "function names.\n"
                                                          "Use only letters, numbers, "
                                                          "and underscores. "
                                                          "'/' indicates no separator."
                                                     )] = ' ',
         not_remove_location: Annotated[bool, typer.Option("--not-remove-location",
                                               "-nrl",
                                               help="During a roundtrip, do not remove "
                                                    "existing locations no more present "
                                                    "in the project."
                                               )] = False,
         not_remove_device: Annotated[bool, typer.Option("--not-remove-device",
                                               "-nrd",
                                               help="During a roundtrip, do not remove "
                                                    "existing devices no more present "
                                                    "in the project."
                                               )] = False,
         remove_keyword: Annotated[bool, typer.Option("--remove-keyword",
                                               "-rk",
                                               help="Remove the keyword from the device name."
                                               )] = False,
         name_pattern: Annotated[str, typer.Option("--name-pattern",
                                                "-np",
                                                help="Pattern for the device name.\n"
                                                     "In the pattern {location} will be replaced "
                                                     "by the location name, {type} by the device "
                                                     "type and {name} by the device name.",
                                                show_default=True)] = "{name}",
         log_level: Annotated[str, typer.Option("--log-level",
                                                "-l",
                                                help="Logs level (DEBUG, INFO, WARNING, "
                                                     "ERROR, CRITICAL)",
                                                metavar="[DEBUG|INFO|WARNING|ERROR|CRITICAL]",
                                                show_default=True,
                                                callback=validate_log_level)] = "WARNING"
         ): # pylint: disable=too-many-locals
    """
    HomeAssistantKNXAutomaticImport is a script tool to create configuration
    file for the Home Assistant KNX integration.
    """

    # manage logging
    setup_logging(log_level)

    # manage the configuration
    logging.info("")
    logging.info("=====Setup Configuration=====")
    if hamode and nhamode:
        logging.error("hamode and nhamode can't be activated simultaneously")
        sys.exit(1)
    if (not hamode) and (not nhamode):
        final_hamode = None
    else:
        final_hamode = hamode
    logging.info("Opening %s", file)
    ClassFromTypedDict.import_package(knx_project_objects)
    if location_separator == '/':
        location_separator = ""
    configuration = HAKAIConfiguration(KNXProjectManager.init(file),
                                       final_hamode,
                                       overwrite,
                                       location_separator,
                                       suppress_project_name,
                                       replace_spaces,
                                       not_remove_location,
                                       not_remove_device,
                                       remove_keyword,
                                       name_pattern)
    configuration.project.print_knx_project_properties()

    # initialize locations repository
    logging.info("")
    logging.info("=====Initialize locations repository=====")
    my_locations_repository = HAKNXLocationsRepository()
    if roundtrip:
        logging.info("RoundTrip activated")
        target_path = os.path.join(input_path, "knx")  #path where files are read
        #if the path exists, existing files are loaded
        if not os.path.exists(target_path):
            logging.warning("Path %s does not exists, roundtrip is skipped.", target_path)
        else:
            logging.info("Read Files for roundtrip")
            my_locations_repository.import_from_path(target_path)

    # Search locations
    logging.info("")
    logging.info("=====Search locations=====")
    locations = KNXSpaceAnalyzer()

    # Create entities in locations
    logging.info("")
    logging.info("=====Start locations analysis=====")
    my_locations_repository.import_from_knx_spaces_repository(locations.repository)

    # Check roundtrip coherency
    if roundtrip:
        logging.info("")
        logging.info("=====Check roundtrip coherency=====")
        my_locations_repository.check()

    # write the output files
    logging.info("")
    logging.info("=====Generate output files=====")
    target_path = os.path.join(output_path, "knx")  #path where files are stored
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)
    if not os.path.isdir(target_path):
        raise NotADirectoryError(f"Output path '{target_path}' is not a directory.")
    my_locations_repository.dump(target_path,
                                 create_output_path=True)

def main_typer():
    typer.run(main)

if __name__ == "__main__":
    typer.run(main)
