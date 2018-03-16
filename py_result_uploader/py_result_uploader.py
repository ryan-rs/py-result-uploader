# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
import json
import re
import swagger_client
import xml.etree.ElementTree as Etree
from datetime import datetime

# ======================================================================================================================
# Globals
# ======================================================================================================================
TESTCASE_NAME_RGX = re.compile(r'(\w+)(\[.+\])')


# ======================================================================================================================
# Functions
# ======================================================================================================================
def _load_input_file(file_path):
    """Read and validate the input file contents.

    Args:
        file_path (str): A string representing a valid file path.

    Returns:
        ElementTree: An ET object already pointed at the root "testsuite" element.

    Raises:
        RuntimeError: invalid path.
    """

    root_element = "testsuite"

    try:
        junit_xml = Etree.parse(file_path).getroot()
    except IOError:
        raise RuntimeError('Invalid path "{}" for JUnitXML results file!'.format(file_path))
    except Etree.ParseError:
        raise RuntimeError('The file "{}" does not contain valid XML!'.format(file_path))

    if junit_xml.tag != root_element:
        raise RuntimeError('The file "{}" does not have JUnitXML "{}" root element!'.format(file_path, root_element))

    return junit_xml


def _generate_test_log(junit_testcase_xml, testsuite_props):
    """Construct a qTest swagger model for a single JUnitXML test result.

    Args:
        junit_testcase_xml (ElementTree): A XML element representing a JUnit style testcase result.
        testsuite_props (dict): A dictionary of properties for the testsuite from within which the testcase executed.

    Returns:
        AutomationTestLogResource: A qTest swagger model for an test log.
    """

    testcase_status = 'PASSED'

    if junit_testcase_xml.find('failure') is not None or junit_testcase_xml.find('error') is not None:
        testcase_status = 'FAILED'
    elif junit_testcase_xml.find('skipped') is not None:
        testcase_status = 'SKIPPED'

    test_log = swagger_client.AutomationTestLogResource()

    test_log.name = TESTCASE_NAME_RGX.match(junit_testcase_xml.attrib['name']).group(1)
    test_log.status = testcase_status
    test_log.module_names = [testsuite_props['GIT_BRANCH']]                      # GIT_BRANCH == RPC release
    test_log.exe_start_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')   # UTC timezone 'Zulu'
    test_log.exe_end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')     # UTC timezone 'Zulu'
    test_log.automation_content = "{}#{}".format(testsuite_props['GIT_BRANCH'], test_log.name)

    return test_log


def _generate_auto_request(junit_xml, test_cycle):
    """Construct a qTest swagger model for a JUnitXML test run result. (Called an "automation request" in
    qTest parlance)

    Args:
        junit_xml (ElementTree): A XML element representing a JUnit style testsuite result.
        test_cycle (str): The parent qTest test cycle for test results.

    Returns:
        AutomationRequest: A qTest swagger model for an automation request.
    """

    testsuite_props = {p.attrib['name']: p.attrib['value'] for p in junit_xml.findall('./properties/property')}
    test_logs = [_generate_test_log(tc_xml, testsuite_props) for tc_xml in junit_xml.findall('testcase')]

    auto_req = swagger_client.AutomationRequest()
    auto_req.test_cycle = test_cycle
    auto_req.test_logs = test_logs
    auto_req.execution_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')   # UTC timezone 'Zulu'

    return auto_req


def output_json_auto_request(output_file_path, junit_xml_file_path, test_cycle):
    """Construct a JSON string object representing a 'AutomationRequest' qTest swagger model.

    Args:
        output_file_path (str): The file path to use for writing out the 'AutomationRequest' JSON.
        junit_xml_file_path (str): A file path to a XML element representing a JUnit style testsuite result.
        test_cycle (str): The parent qTest test cycle for test results.

    Returns:
        str: A JSON string representation of the qTest swagger model for an automation request.
    """

    junit_xml = _load_input_file(junit_xml_file_path)

    api_client = swagger_client.ApiClient()
    auto_request_dict = api_client.sanitize_for_serialization(_generate_auto_request(junit_xml, test_cycle))

    try:
        with open(output_file_path, 'w') as f:
            f.write(json.dumps(auto_request_dict, indent=2))
    except IOError:
        raise RuntimeError('Cannot write to "{}" file!'.format(output_file_path))
