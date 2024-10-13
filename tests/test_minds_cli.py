from click.testing import CliRunner
from minds_cli.cli import cli
import json, os
from unittest.mock import patch
import pytest


@pytest.fixture(autouse=True)
def set_env_vars():
    """Set environment variables for the tests."""
    os.environ['MINDS_API_KEY'] = 'api_key'


@pytest.fixture
def runner():
    """Fixture for the Click test runner."""
    return CliRunner()


def test_version(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")

@patch('minds.minds.Minds.list')
def test_list_minds(mock_list, runner):
    mock_list.return_value = json.dumps([{"name":"mind1"},{"name":"mind2"}])
    result = runner.invoke(cli, ['minds', 'list'])
    assert result.exit_code == 0
    assert not result.exception
    assert "mind1" in result.output
    assert "mind2" in result.output


@patch('minds.minds.Minds.list')
def test_list_minds_error(mock_list, runner):
    mock_list.side_effect = Exception("An error occurred")

    result = runner.invoke(cli, ['minds', 'list'])

    assert result.exit_code == 0
    assert "An error occurred" in result.output


@patch('minds.minds.Minds.get')
def test_get_mind(mock_get, runner):
    mind_name = "mind1"
    mock_get.return_value = json.dumps({"name": "mind1", "description": "A test mind"})
    result = runner.invoke(cli, ['minds', 'get', mind_name])

    assert result.exit_code == 0
    assert "mind1" in result.output
    assert "A test mind" in result.output


@patch('minds.minds.Minds.get')
def test_get_mind_error(mock_get, runner):
    mind_name = "mind1"
    msg = f"{mind_name} not found"
    mock_get.side_effect = Exception(msg)
    result = runner.invoke(cli, ['minds', 'get', mind_name])

    assert result.exit_code == 0
    assert msg == result.output.strip()


@patch('minds.minds.Minds.drop')
def test_drop_mind(mock_drop, runner):
    mind_name = "mind1"
    msg = f"{mind_name} successfully deleted."
    mock_drop.return_value = msg
    result = runner.invoke(cli, ['minds', 'drop', mind_name])

    assert result.exit_code == 0
    assert mind_name in result.output
    assert "successfully" in result.output
    assert "deleted" in result.output


@patch('minds.minds.Minds.drop')
def test_drop_mind_error(mock_drop, runner):
    mind_name = "mind1"
    msg = f"{mind_name} could not be deleted."
    mock_drop.side_effect = Exception(msg)
    result = runner.invoke(cli, ['minds', 'drop', mind_name])

    assert result.exit_code == 0
    assert msg == result.output.strip()


@patch('minds.minds.Mind')
@patch('minds.minds.Minds.get')
@patch('minds.minds.Mind.add_datasource')
def test_add_datasource_mind(mock_add_datasource, mock_get, mock_mind, runner):
    mind_name = "mind1"
    ds_name = "ds1"
    mock_get.return_value = mock_mind
    mock_add_datasource.return_value = None
    result = runner.invoke(cli, ['minds', 'add_datasource', mind_name, ds_name])
    assert result.exit_code == 0
    assert not result.exception
    assert f"{ds_name} added to {mind_name}" == result.output.strip()


@patch('minds.minds.Mind')
@patch('minds.minds.Minds.get')
@patch('minds.minds.Mind.del_datasource')
def test_del_datasource_mind(mock_del_datasource, mock_get, mock_mind, runner):
    mind_name = "mind1"
    ds_name = "ds1"
    mock_get.return_value = mock_mind
    mock_del_datasource.return_value = None
    result = runner.invoke(cli, ['minds', 'drop_datasource', mind_name, ds_name])
    assert result.exit_code == 0
    assert not result.exception
    assert f"{ds_name} dropped from {mind_name}" == result.output.strip()


@patch('minds.minds.Minds.create')
def test_create_mind(mock_create, runner):
    mind_name = "mind1"
    ret_val = f"{mind_name} successfully created."
    mock_create.return_value = ret_val
    result = runner.invoke(cli, ['minds', 'create', '--name', mind_name])
    
    assert result.exit_code == 0
    assert not result.exception
    assert ret_val == result.output.strip()


@patch('minds.datasources.Datasources.list')
def test_list_datasources(mock_list, runner):
    mock_list.return_value = json.dumps([{"ds_name":"ds1"},{"ds_name":"ds2"}])
    result = runner.invoke(cli, ['datasources', 'list'])
    assert result.exit_code == 0
    assert not result.exception
    assert "ds1" in result.output
    assert "ds2" in result.output
    
@patch('minds.datasources.Datasources.get')
def test_get_datasources(mock_get, runner):
    ds_name = "ds1"
    ret_val = json.dumps({"ds_name": "ds1", "description": "A pssql datasource"})
    mock_get.return_value = ret_val
    result = runner.invoke(cli, ['datasources', 'get', ds_name])

    assert result.exit_code == 0
    assert ret_val == result.output.strip()
    

@patch('minds.datasources.Datasources.drop')
def test_drop_datasources(mock_drop, runner):
    ds_name = "ds1"
    ret_val = f"{ds_name} successfully deleted."
    mock_drop.return_value = ret_val
    result = runner.invoke(cli, ['datasources', 'drop', ds_name])

    assert result.exit_code == 0
    assert ds_name in result.output
    assert "successfully" in result.output
    assert "deleted" in result.output


@patch('minds.datasources.Datasources.create')
def test_create_datasources(mock_create, runner):
    ds_name = "pssql"
    ret_val = f"{ds_name} successfully created."
    
    mock_create.return_value = ret_val
    with runner.isolated_filesystem():
        with open('test_conn.json', 'w') as f:
            f.write(json.dumps({"user": "demo_user", "password": "demo_password", "host": "samples.mindsdb.com"}))
        
        result = runner.invoke(cli, ['datasources', 'create', '--name', ds_name, '--engine', 'postgres', '--description', "new pssql db", '--connection_data_file', "test_conn.json"])
        
        assert result.exit_code == 0
        assert ret_val == result.output.strip()
        assert ds_name in result.output
        assert "successfully" in result.output
        assert "created" in result.output
