# Minds command line tool

[![PyPI](https://img.shields.io/pypi/v/minds-cli-sdk.svg)](https://pypi.org/project/minds-cli-sdk/)
[![Changelog](https://img.shields.io/github/v/release/Better-Boy/minds-cli-sdk?include_prereleases&label=changelog)](https://github.com/Better-Boy/minds-cli-sdk/releases)
[![Tests](https://github.com/Better-Boy/minds-cli-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/Better-Boy/minds-cli-sdk/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Better-Boy/minds-cli-sdk/blob/master/LICENSE)

A command line tool for interacting with minds - https://mdb.ai/
Documentation for minds - https://docs.mdb.ai/docs/data_sources

## Installation

Install this tool using `pip`:
```bash
pip install minds-cli-sdk
```
## Usage

For help, run:
```bash
minds --help
```
You can also use:
```bash
python -m minds_cli --help
```

## Getting started

### Setting the Minds API Key

Set the environment variable `MINDS_API_KEY` to the api key from minds.
To create an API key - Login to minds (https://mdb.ai) and create an API key.

```bash
export MINDS_API_KEY=<api-key>
```

### Setting the Minds API endpoint

This is optional. If the API endpoint is not provided, the cloud endpoint (https://mdb.ai) is taken by default.

If you have a self-hosted instance of minds, set the environment variable `MINDS_API_KEY` to the new endpoint.

```bash
export MINDS_BASE_ENDPOINT=https://staging.mdb.ai
```

## Datasources

All commands and options related to datasources are as follows:

```bash
minds datasources --help
```

Output:

```bash
Usage: minds datasources [OPTIONS] COMMAND [ARGS]...

Command group to deal with datasources

Options:
  --help  Show this message and exit.

Commands:
  create  Create a datasource
  drop    Drop a datasource
  get     Get a datasource
  list    List the datasources
```

### Creating a Data Source

The command and the different options to be passed is as follows:

```bash
minds datasources create --help
```

Output:
```bash
Usage: minds datasources create [OPTIONS]

Create a datasource

Options:
--name TEXT                  name of datatasource.  [required]
--engine TEXT                type of database handler, for example
                            'postgres', 'mysql', ...  [required]
--description TEXT           description of the database. Used by mind to
                            know what data can be got from it.  [required]
--connection_data_file FILE  Credentials json file to connect to database.
                            Refer https://docs.mdb.ai/docs/data_sources
                            [required]
--tables TEXT                Comma-separated list of allowed tables,
                            optional. Ex. --tables table1,table2,table3
--replace                    if true - to remove existing datasource,
                            default is false
--help                       Show this message and exit.
```

Example to create a postgres datasource:

```bash
minds datasources create --name pssql --engine postgres --description "new pssql db" --connection_data_file /Users/abhi/Downloads/ps_conn.json
```

Output:
```bash
pssql successfully created.
```

The connection_data_file contains the connection json string which is as follows:

```json
{
    "user": "demo_user",
    "password": "demo_password",
    "host": "samples.mindsdb.com",
    "port": "5432",
    "database": "demo",
    "schema": "demo_data"
}
```

### Get a Data Source

The command and the different options to be passed is as follows:

```bash
minds datasources create --help
```

Output:
```bash
Usage: minds datasources get [OPTIONS] DATASOURCE_NAME

Get a datasource

Options:
--help  Show this message and exit.
```

Example:

```
minds datasources get pssql
```

Output:
```bash
name='pssql' engine='postgres' description='new pssql db' connection_data={'database': 'demo', 'host': 'samples.mindsdb.com', 'password': 'demo_password', 'port': '5432', 'schema': 'demo_data', 'user': 'demo_user'} tables=[]
```

### List all Data Sources

The command and the different options to be passed is as follows:

```bash
minds datasources list --help
```

Output:
```bash
Usage: minds datasources list [OPTIONS]

List the datasources

Options:
--help  Show this message and exit.
```

Example:

```
minds datasources list
```

Output:
```bash
[Datasource(name='pssql1', engine='postgres', description='new pssql db', connection_data={'database': 'demo', 'host': 'samples.mindsdb.com', 'password': 'demo_password', 'port': '5432', 'schema': 'demo_data', 'user': 'demo_user'}, tables=[])]
```

### Drop a Data Source

The command and the different options to be passed is as follows:

```bash
minds datasources drop --help
```

Output:
```bash
Usage: minds datasources drop [OPTIONS] DATASOURCE_NAME

  Drop a datasource

Options:
  --help  Show this message and exit.
```

Example:

```bash
minds datasources drop pssql
```

Output:
```bash
pssql successfully deleted.
```


## Minds

All commands and options related to minds are as follows:

```bash
minds minds --help
```

Output:

```bash
Usage: minds minds [OPTIONS] COMMAND [ARGS]...

  Command group to deal with minds

Options:
  --help  Show this message and exit.

Commands:
  add_datasource   Add a datasource to a mind
  create           Create a mind
  drop             Drop a mind
  drop_datasource  Drop a datasource to a mind
  get              Get a mind
  list             List the minds
  update           Update a mind
```

### Creating a Mind

The command and the different options to be passed is as follows:

```bash
minds minds create --help
```

Output:
```bash
Usage: minds minds create [OPTIONS]

  Create a mind

Options:
  --name TEXT             name of the mind  [required]
  --model_name TEXT       llm model name, optional
  --provider TEXT         llm provider, optional. Ex. openai
  --prompt_template TEXT  instructions to llm, optional
  --datasources TEXT      Comma-separated list of datasources used by mind,
                          optional. Ex. --datasources testds, testds1, testds2
  --parameters TEXT       other parameters of the mind, optional. This is a
                          json string.
  --replace               if true - to remove existing mind, default is false
  --help                  Show this message and exit.
```

Example to create a postgres datasource:

```bash
minds minds create --name newMind --model_name gpt-3.5 --datasources pssql1,testds --parameters "{\"owner\":\"abhi\"}" --replace
```

Output:
```bash
newMind successfully created.
```

The connection_data_file contains the connection json string which is as follows:

```json
{
    "user": "demo_user",
    "password": "demo_password",
    "host": "samples.mindsdb.com",
    "port": "5432",
    "database": "demo",
    "schema": "demo_data"
}
```

### Get a Mind

The command and the different options to be passed is as follows:

```bash
minds minds get --help
```

Output:
```bash
Usage: minds minds get [OPTIONS] MIND_NAME

  Get a mind

Options:
  --help  Show this message and exit.
```

Example:

```bash
minds minds get newMind
```

Output:
```bash
<Mind Object details>
```

### List all Minds

The command and the different options to be passed is as follows:

```bash
minds minds list --help
```

Output:
```bash
Usage: minds minds list [OPTIONS]

  List the minds

Options:
  --help  Show this message and exit.
```

Example:

```bash
minds minds list
```

Output:
```bash
[Mind Object1, Mind Object2, ....]
```

### Drop a Mind

The command and the different options to be passed is as follows:

```bash
minds minds drop --help
```

Output:
```bash
Usage: minds minds drop [OPTIONS] MIND_NAME

  Drop a mind

Options:
  --help  Show this message and exit.
```

Example:

```bash
minds minds drop newMind
```

Output:
```bash
newMind successfully deleted.
```

### Add a datasource to Mind

The command and the different options to be passed is as follows:

```bash
minds minds add_datasource --help
```

Output:
```bash
Usage: minds minds add_datasource [OPTIONS] MIND_NAME DATASOURCE_NAME

  Add a datasource to a mind

Options:
  --help  Show this message and exit.
```

Example:

```bash
minds minds add_datasource newMind newds
```

Output:
```bash
newds added to newMind
```

### Remove a datasource from Mind

The command and the different options to be passed is as follows:

```bash
minds minds drop_datasource --help
```

Output:
```bash
Usage: minds minds drop_datasource [OPTIONS] MIND_NAME DATASOURCE_NAME

  Drop a datasource from a mind

Options:
  --help  Show this message and exit.
```

Example:

```bash
minds minds drop_datasource newMind newds
```

Output:
```bash
newds dropped from newMind
```


## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd minds-cli-sdk
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
