from minds.client import Client
from minds.datasources import DatabaseConfig
import os
import click
import json

@click.group()
@click.version_option("1.0.0")
@click.pass_context
def cli(ctx):
    """
    A minds command line tool that helps you interact with minds API.
    You need a valid API key from Minds for the tool to work. You can
    sign up for a free account at https://mdb.ai/.
    """
    api_key = os.getenv('MINDS_API_KEY')

    if not api_key:
        click.echo("Error: MINDS_API_KEY environment variable not set.")
        ctx.exit(1)

    base_url = os.getenv('MINDS_BASE_ENDPOINT', default="https://mdb.ai")

    ctx.obj = {
        'client': Client(api_key=api_key, base_url=base_url)
    }


@cli.group("minds")
@click.pass_context
def minds(ctx):
    """
    Command group to deal with minds
    """
    pass

@cli.group("datasources")
@click.pass_context
def datasources(ctx):
    """
    Command group to deal with datasources
    """
    pass

@minds.command("list")
@click.pass_context
def list_mind(ctx):
    """
    List the minds
    """
    client = ctx.obj.get('client')
    try:
        click.echo(client.minds.list())
    except Exception as exc:
        click.echo(str(exc), err=True)

@minds.command("get")
@click.argument("mind_name", required=True, type=str)
@click.pass_context
def get_mind(ctx, mind_name):
    """
    Get a mind
    """
    client = ctx.obj.get('client')
    try:
        click.echo(client.minds.get(mind_name))
    except Exception as exc:
        click.echo(exc, err=True)


@minds.command("drop")
@click.argument("mind_name", required=True, type=str)
@click.pass_context
def drop_mind(ctx, mind_name):
    """
    Drop a mind
    """
    client = ctx.obj.get('client')
    try:
        click.echo(client.minds.drop(mind_name))
        click.echo(f"{mind_name} successfully deleted.")
    except Exception as exc:
        click.echo(exc, err=True)


@minds.command("add_datasource")
@click.argument("mind_name", required=True, type=str)
@click.argument("datasource_name", required=True, type=str)
@click.pass_context
def add_datasource_mind(ctx, mind_name, datasource_name):
    """
    Add a datasource to a mind
    """
    client = ctx.obj.get('client')
    try:
        mind = client.minds.get(mind_name)
        mind.add_datasource(datasource_name)
        click.echo(f"{datasource_name} added to {mind_name}")
    except Exception as exc:
        click.echo(exc, err=True)


@minds.command("drop_datasource")
@click.argument("mind_name", required=True, type=str)
@click.argument("datasource_name", required=True, type=str)
@click.pass_context
def drop_datasource_mind(ctx, mind_name, datasource_name):
    """
    Drop a datasource from a mind
    """
    client = ctx.obj.get('client')
    try:
        mind = client.minds.get(mind_name)
        mind.del_datasource(datasource_name)
        click.echo(f"{datasource_name} dropped from {mind_name}")
    except Exception as exc:
        click.echo(exc, err=True)


@minds.command("create")
@click.option("--name", required=True, type=str, help="name of the mind")
@click.option('--model_name', type=str, default=None, help="llm model name, optional")
@click.option('--provider', type=str, default=None, help="llm provider, optional. Ex. openai")
@click.option('--prompt_template', type=str, default=None, help="instructions to llm, optional")
@click.option('--datasources',  type=str, default=None, help="Comma-separated list of datasources used by mind, optional. Ex. --datasources testds, testds1, testds2")
@click.option('--parameters', type=str, default=None, help="other parameters of the mind, optional. This is a json string.")
@click.option('--replace', is_flag=True, default=False, help="if true - to remove existing mind, default is false")
@click.pass_context
def create_mind(ctx, name, model_name, provider, prompt_template, datasources, parameters, replace):
    """
    Create a mind
    """
    client = ctx.obj.get('client')
    try:
        ds_list = datasources.split(',') if datasources else []
        ds_list = [ds.strip() for ds in ds_list]
        mind = client.minds.create(name,
                    model_name=model_name,
                    provider=provider,
                    # prompt_template=prompt_template,
                    datasources=ds_list,
                    parameters=json.loads(parameters) if parameters else None,
                    replace=replace
                )
        click.echo(f"{name} successfully created.")
    except Exception as exc:
        click.echo(exc, err=True)


@minds.command("update")
@click.option("--existing_name", required=True, type=str, help="existing name of the mind. New name and existing name can be same.")
@click.option("--new_name", required=True, type=str, help="new name of the mind. New name and existing name can be same.")
@click.option('--new_model_name', type=str, default=None, help="new llm model name, optional")
@click.option('--new_provider', type=str, default=None, help="new llm provider, optional. Ex. openai")
@click.option('--new_prompt_template', type=str, default=None, help="new instructions to llm, optional")
@click.option('--new_datasources',  type=str, default=None, help="new Comma-separated list of datasources used by mind, optional. Ex. --datasources testds, testds1, testds2")
@click.option('--new_parameters', type=str, default=None, help="new other parameters of the mind, optional. This is a json string.")
@click.pass_context
def update_mind(ctx, existing_name, new_name, new_model_name, new_provider, new_prompt_template, new_datasources, new_parameters):
    """
    Update a mind
    """
    client = ctx.obj.get('client')
    try:
        ds_list = new_datasources.split(',') if new_datasources else []
        ds_list = [ds.strip() for ds in ds_list]
        mind = client.minds.get(existing_name)
        mind.update(
            name=new_name,
            model_name=new_model_name,
            provider=new_provider,
            # prompt_template=new_prompt_template,
            datasources=ds_list,
            parameters=new_parameters
        )
        click.echo(f"{existing_name} successfully updated.")
        click.echo(mind)
    except Exception as exc:
        click.echo(exc, err=True)


@datasources.command("create")
@click.option("--name", type=str, required=True, help="name of datatasource")
@click.option('--engine', type=str, required=True, help="type of database handler, for example 'postgres', 'mysql', ...")
@click.option('--description', type=str, required=True, help="description of the database. Used by mind to know what data can be got from it.")
@click.option('--connection_data_file', type=click.Path(exists=True, dir_okay=False), required=True, help="Credentials json file to connect to database. Refer https://docs.mdb.ai/docs/data_sources")
@click.option('--tables',  type=str, default=None, help="Comma-separated list of allowed tables, optional. Ex. --tables table1,table2,table3")
@click.option('--replace', is_flag=True, default=False, help="if true - to remove existing datasource, default is false")
@click.pass_context
def create_datasource(ctx, name, engine, description, connection_data_file, tables, replace):
    """
    Create a datasource
    """
    client = ctx.obj.get('client')
    try:
        connection_data = {}
        with open(connection_data_file, 'r') as file:
            connection_data = json.load(file)  # Parse the JSON data
        table_list = tables.split(',') if tables else []
        table_list = [table.strip() for table in table_list]
        
        ds_config = DatabaseConfig(
                        name=name,
                        engine=engine,
                        description=description,
                        connection_data=connection_data,
                        tables=table_list
                    )

        ds = client.datasources.create(
                        ds_config=ds_config,
                        replace=replace
                    )
        click.echo(f"{name} successfully created.")
    except Exception as exc:
        click.echo(exc, err=True)




@datasources.command("list")
@click.pass_context
def list_datasources(ctx):
    """
    List the datasources
    """
    client = ctx.obj.get('client')
    try:
        click.echo(client.datasources.list())
    except Exception as exc:
        click.echo(exc, err=True)

@datasources.command("get")
@click.argument("datasource_name", required=True, type=str)
@click.pass_context
def get_datasource(ctx, datasource_name):
    """
    Get a datasource
    """
    client = ctx.obj.get('client')
    try:
        click.echo(client.datasources.get(datasource_name))
    except Exception as exc:
        click.echo(exc, err=True)


@datasources.command("drop")
@click.argument("datasource_name", required=True, type=str)
@click.pass_context
def drop_datasource(ctx, datasource_name):
    """
    Drop a datasource
    """
    client = ctx.obj.get('client')

    try:
        click.echo(client.datasources.drop(datasource_name))
        click.echo(f"{datasource_name} successfully deleted.")
    except Exception as exc:
        click.echo(exc, err=True)


def main():
    cli(obj={})

if __name__ == "__main__":
    main()