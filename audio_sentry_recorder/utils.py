import os
import sys
import argparse
import logging

from datetime import datetime
from pathlib import Path, PurePath


def get_args(arguments=None):
    log = logging.getLogger()
    
    parser = argparse.ArgumentParser(
        description="Records audio to a file only when the signal strength is above a given threshold.")

    parser.add_argument('--save-to-folder',
                        action='store',
                        default=os.getcwd(),
                        type=str,
                        metavar='<Saved data to Path>',
                        dest='save_to_folder',
                        help='Path for saving recordings Default <./>')
    
    parser.add_argument('--threshold',
                        action='store',
                        default=100,
                        type=int,
                        metavar='<Threshold>',
                        dest='threshold',
                        help='Sound level rms threshold.')

    args = parser.parse_args(args=arguments)

    return args


def get_filename(start: datetime, end: datetime, save_to_folder: Path, format: str = 'wav') -> str:
    folder_name = PurePath(save_to_folder).joinpath(start.strftime("%Y%m%d"))
    name_start = start.strftime("%Y%m%d_%H%M%S")
    name_end = "CE2LS"

    filename = folder_name.joinpath(f"{name_start}_{name_end}.{format}")
    return filename, folder_name


def setup_logging(debug=False):
    if '--debug' in sys.argv or debug:
        log_format = '[%(asctime)s][%(levelname)8s]: %(message)s ' \
                     '[%(module)s.%(funcName)s:%(lineno)d]'
        logging_level = logging.DEBUG
    else:
        log_format = '[%(asctime)s][%(levelname).1s]: %(message)s'
        logging_level = logging.INFO

    date_format = '%H:%M:%S'

    formatter = logging.Formatter(fmt=log_format,
                                  datefmt=date_format)

    logging.basicConfig(level=logging_level,
                        format=log_format,
                        datefmt=date_format)

    log = logging.getLogger(__name__)