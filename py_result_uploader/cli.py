# -*- coding: utf-8 -*-

"""Console script for py_result_uploader."""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
import sys
import click
from py_result_uploader import py_result_uploader


# ======================================================================================================================
# Main
# ======================================================================================================================
@click.command()
@click.argument('junit_input_file', type=click.Path(exists=True))
@click.argument('json_output_file', type=click.Path())
@click.argument('test_cycle')
def main(json_output_file, junit_input_file, test_cycle):
    """Upload JUnitXML results to qTest manager.

    \b
    Required Arguments:
        JUNIT_INPUT_FILE        A valid JUnit XML results file.
        JSON_OUTPUT_FILE        The output file to store qTest JSON test log results
        TEST_CYCLE              The qTest cycle to use as a parent for results
    """

    exit_code = 0

    try:
        py_result_uploader.output_json_auto_request(json_output_file, junit_input_file, test_cycle)

        print("\nSuccess!")
    except RuntimeError as e:
        exit_code = 1
        print(e)

        print("\nFailed!")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
