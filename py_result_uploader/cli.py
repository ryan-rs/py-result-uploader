# -*- coding: utf-8 -*-

"""Console script for py_result_uploader."""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
import os
import sys
import click
import py_result_uploader.py_result_uploader as ptu


# ======================================================================================================================
# Main
# ======================================================================================================================
@click.command()
@click.argument('junit_input_file', type=click.Path(exists=True))
@click.argument('qtest_project_id', type=click.INT)
@click.argument('qtest_test_cycle', type=click.STRING)
def main(junit_input_file, qtest_project_id, qtest_test_cycle):
    """Upload JUnitXML results to qTest manager.

    \b
    Required Arguments:
        JUNIT_INPUT_FILE        A valid JUnit XML results file.
        QTEST_PROJECT_ID        The the target qTest Project ID for results
        QTEST_TEST_CYCLE        The qTest cycle to use as a parent for results

    \b
    Required Environment Variables:
        QTEST_API_TOKEN         The qTest API token to use for authorization
    """

    exit_code = 0
    api_token_env_var = 'QTEST_API_TOKEN'

    try:
        if not os.environ.get(api_token_env_var):
            raise RuntimeError('The "{}" environment variable is not defined! '
                               'See help for more details.'.format(api_token_env_var))

        job_id = ptu.upload_test_results(junit_input_file,
                                         os.environ[api_token_env_var],
                                         qtest_project_id,
                                         qtest_test_cycle)

        click.echo(click.style("\nQueue Job ID: {}".format(str(job_id))))
        click.echo(click.style("\nSuccess!", fg='green'))
    except RuntimeError as e:
        exit_code = 1
        click.echo(click.style(str(e), fg='red'))

        click.echo(click.style("\nFailed!", fg='red'))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
