#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
import pytest
import json
from py_result_uploader import py_result_uploader


class TestLoadingInputJunitXMLFile(object):
    """Test cases for the '_load_input_file' function"""

    def test_load_file_happy_path(self, flat_all_passing_xml):
        """Verify that a valid JUnitXML file can be loaded"""

        # Setup
        junit_xml = py_result_uploader._load_input_file(flat_all_passing_xml)

        # Expectations
        root_tag_atribute_exp = {'errors': '0',
                                 'failures': '0',
                                 'name': 'pytest',
                                 'skips': '0',
                                 'tests': '5',
                                 'time': '1.664'}

        # Test
        assert root_tag_atribute_exp == junit_xml.attrib

    def test_invalid_file_path(self):
        """Verify that an invalid file path raises an exception"""

        # Test
        with pytest.raises(RuntimeError):
            py_result_uploader._load_input_file('/path/does/not/exist')

    def test_invalid_xml_content(self, bad_xml):
        """Verify that invalid XML file content raises an exception"""

        # Test
        with pytest.raises(RuntimeError):
            py_result_uploader._load_input_file(bad_xml)

    def test_missing_junit_xml_root(self, bad_junit_root):
        """Verify that XML files missing the expected JUnitXML root element raises an exception"""

        # Test
        with pytest.raises(RuntimeError):
            py_result_uploader._load_input_file(bad_junit_root)


class TestGenerateTestLog(object):
    """Test cases for the '_generate_test_log' function"""

    @pytest.fixture()
    def properties(self):
        props = {'JENKINS_CONSOLE_LOG_URL': 'JENKINS_CONSOLE_LOG_URL',
                 'SCENARIO': 'SCENARIO',
                 'ACTION': 'ACTION',
                 'IMAGE': 'IMAGE',
                 'OS_ARTIFACT_SHA': 'OS_ARTIFACT_SHA',
                 'PYTHON_ARTIFACT_SHA': 'PYTHON_ARTIFACT_SHA',
                 'APT_ARTIFACT_SHA': 'APT_ARTIFACT_SHA',
                 'GIT_REPO': 'GIT_REPO',
                 'GIT_BRANCH': 'GIT_BRANCH'}

        return props

    def test_pass(self, single_passing_xml, properties):
        """Verify that a valid qTest 'AutomationTestLogResource' swagger model is generated from a JUnitXML file
        that contains a single passing test
        """

        # Setup
        junit_xml = py_result_uploader._load_input_file(single_passing_xml)
        # noinspection PyUnresolvedReferences
        test_log_dict = py_result_uploader._generate_test_log(junit_xml.find('testcase'), properties).to_dict()

        # Expectation
        test_name = 'test_pass'
        test_log_exp = {'name': test_name,
                        'status': 'PASSED',
                        'module_names': [properties['GIT_BRANCH']],
                        'automation_content': '{}#{}'.format(properties['GIT_BRANCH'], test_name)}

        # Test
        for exp in test_log_exp:
            assert test_log_exp[exp] == test_log_dict[exp]

    def test_fail(self, single_fail_xml, properties):
        """Verify that a valid qTest 'AutomationTestLogResource' swagger model is generated from a JUnitXML file
        that contains a single failing test
        """

        # Setup
        junit_xml = py_result_uploader._load_input_file(single_fail_xml)
        # noinspection PyUnresolvedReferences
        test_log_dict = py_result_uploader._generate_test_log(junit_xml.find('testcase'), properties).to_dict()

        # Expectation
        test_name = 'test_fail'
        test_log_exp = {'name': test_name,
                        'status': 'FAILED',
                        'module_names': [properties['GIT_BRANCH']],
                        'automation_content': '{}#{}'.format(properties['GIT_BRANCH'], test_name)}

        # Test
        for exp in test_log_exp:
            assert test_log_exp[exp] == test_log_dict[exp]

    def test_error(self, single_error_xml, properties):
        """Verify that a valid qTest 'AutomationTestLogResource' swagger model is generated from a JUnitXML file
        that contains a single erroring test
        """

        # Setup
        junit_xml = py_result_uploader._load_input_file(single_error_xml)
        # noinspection PyUnresolvedReferences
        test_log_dict = py_result_uploader._generate_test_log(junit_xml.find('testcase'), properties).to_dict()

        # Expectation
        test_name = 'test_error'
        test_log_exp = {'name': test_name,
                        'status': 'FAILED',
                        'module_names': [properties['GIT_BRANCH']],
                        'automation_content': '{}#{}'.format(properties['GIT_BRANCH'], test_name)}

        # Test
        for exp in test_log_exp:
            assert test_log_exp[exp] == test_log_dict[exp]

    def test_skip(self, single_skip_xml, properties):
        """Verify that a valid qTest 'AutomationTestLogResource' swagger model is generated from a JUnitXML file
        that contains a single skipping test
        """

        # Setup
        junit_xml = py_result_uploader._load_input_file(single_skip_xml)
        # noinspection PyUnresolvedReferences
        test_log_dict = py_result_uploader._generate_test_log(junit_xml.find('testcase'), properties).to_dict()

        # Expectation
        test_name = 'test_skip'
        test_log_exp = {'name': test_name,
                        'status': 'SKIPPED',
                        'module_names': [properties['GIT_BRANCH']],
                        'automation_content': '{}#{}'.format(properties['GIT_BRANCH'], test_name)}

        # Test
        for exp in test_log_exp:
            assert test_log_exp[exp] == test_log_dict[exp]


class TestGenerateAutoRequest(object):
    """Test cases for the '_generate_auto_request' function"""

    def test_mix_status(self, flat_mix_status_xml):
        """Verify that a valid qTest 'AutomationRequest' swagger model is generated from a JUnitXML file
        that contains multiple tests with different status results
        """

        # Setup
        test_cycle = 'CL-1'
        junit_xml = py_result_uploader._load_input_file(flat_mix_status_xml)
        # noinspection PyUnresolvedReferences
        auto_req_dict = py_result_uploader._generate_auto_request(junit_xml, test_cycle).to_dict()

        # Expectation
        prop_value = 'Unknown'
        test_logs_exp = [{'name': 'test_pass',
                          'status': 'PASSED',
                          'module_names': [prop_value],
                          'automation_content': '{}#{}'.format(prop_value, 'test_pass')},
                         {'name': 'test_fail',
                          'status': 'FAILED',
                          'module_names': [prop_value],
                          'automation_content': '{}#{}'.format(prop_value, 'test_fail')},
                         {'name': 'test_error',
                          'status': 'FAILED',
                          'module_names': [prop_value],
                          'automation_content': '{}#{}'.format(prop_value, 'test_error')},
                         {'name': 'test_skip',
                          'status': 'SKIPPED',
                          'module_names': [prop_value],
                          'automation_content': '{}#{}'.format(prop_value, 'test_skip')}]

        # Test
        for x in range(len(auto_req_dict['test_logs'])):
            for key in test_logs_exp[x]:
                assert test_logs_exp[x][key] == auto_req_dict['test_logs'][x][key]


class TestOutputJsonAutoRequest(object):
    """Test cases for the 'output_json_auto_request' function"""

    def test_happy_path(self, single_passing_xml, tmpdir_factory):
        """Verify that a valid JSON representation of a qTest 'AutomationRequest' swagger model is written to disk
        from a JUnitXML file that contains a single passing test
        """

        # Setup
        test_cycle = 'CL-1'
        filename = tmpdir_factory.mktemp('data').join('happy_path.json').strpath
        # noinspection PyUnresolvedReferences
        py_result_uploader.output_json_auto_request(filename, single_passing_xml, test_cycle)
        auto_req_dict = json.load(open(filename))

        # Expectation
        test_name = 'test_pass'
        prop_value = 'Unknown'
        test_log_exp = {'name': test_name,
                        'status': 'PASSED',
                        'module_names': [prop_value],
                        'automation_content': '{}#{}'.format(prop_value, test_name)}

        # Test
        for exp in test_log_exp:
            assert test_log_exp[exp] == auto_req_dict['test_logs'][0][exp]
