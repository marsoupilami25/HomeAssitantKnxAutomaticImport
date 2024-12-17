import logging
import typer

from KNXFunctionAnalyzer.HAKNXLocationsRepository import ha_knx_locations_repository
from KNXFunctionAnalyzer.KNXFunctionAnalyzer import knx_function_analyzer
from KNXProjectManagement.KNXProjectManager import knx_project_manager
from Utils.FromDict import FromDict

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
         log_level: str = typer.Option(
             "WARNING",
             help="Logs level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
             metavar="[DEBUG|INFO|WARNING|ERROR|CRITICAL]",
             show_default=True,
             callback=validate_log_level
         )):
    setup_logging(log_level)
    logging.info(f"Opening {file}")
    knx_project_manager.init(file)
    knx_project_manager.print_knx_project_properties()
    FromDict.set_typeddict_class_association({
        'DPTType' : 'KNXProjectManagement.KNXDPTType.KNXDPTType'
    })
    knx_function_analyzer.star_analysis()
    logging.info("Start locations analysis")
    ha_knx_locations_repository.init()
    ha_knx_locations_repository.dump()


if __name__ == "__main__":
    typer.run(main)
