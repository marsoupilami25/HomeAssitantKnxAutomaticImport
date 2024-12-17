import logging
import typer
import yaml

from HAKNXObjectCreator.HAKNXLocation import HAKNXLocation
from KNXFunctionAnalyzer.HAKNXLocationsRepository import ha_knx_locations_repository
from KNXFunctionAnalyzer.KNXFunctionAnalyzer import KNXFunctionAnalyzer, knx_function_analyzer
from KNXProjectManagement.KNXProjectManager import knx_project_manager
from Utils.Serializable import quoted

# Crée une instance de l'application Typer
app = typer.Typer()

# Liste des niveaux de log autorisés
VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Configuration des logs
def setup_logging(level: str):
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level,
                        format="%(levelname)s - %(message)s")

# Fonction pour valider le niveau de log
def validate_log_level(value: str):
    if value.upper() not in VALID_LOG_LEVELS:
        raise typer.BadParameter(f"'{value}' n'est pas un niveau de log valide. Choisissez parmi : {', '.join(VALID_LOG_LEVELS)}")
    return value.upper()

def main(file: str,
         log_level: str = typer.Option(
             "WARNING",
             help="Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
             metavar="[DEBUG|INFO|WARNING|ERROR|CRITICAL]",
             show_default=True,
             callback=validate_log_level
         )):
    setup_logging(log_level)
    logging.info(f"Opening {file}")
    knx_project_manager.init(file)
    knx_project_manager.print_knx_project_properties()
    knx_function_analyzer.star_analysis()
    logging.info("Start locations analysis")
    ha_knx_locations_repository.init()
    ha_knx_locations_repository.dump()


if __name__ == "__main__":
    typer.run(main)
