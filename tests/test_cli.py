#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
import os.path
from click.testing import CliRunner
from py_result_uploader import cli


def test_cli_happy_path(single_passing_xml, tmpdir_factory):
    """Verify that the CLI will process required arguments and produce a valid JSON representation of a
    qTest 'AutomationRequest' swagger model is written to disk from a JUnitXML file that contains a single
    passing test"""

    # Setup
    test_cycle = 'CL-1'
    json_output_filename = tmpdir_factory.mktemp('data').join('cli_output.json').strpath

    runner = CliRunner()
    cli_arguments = [single_passing_xml, json_output_filename, test_cycle]

    # Test
    result = runner.invoke(cli.main, cli_arguments)
    assert result.exit_code == 0
    assert 'Success!' in result.output

    assert os.path.isfile(json_output_filename)
