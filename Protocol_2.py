# This script was used to automate creation and running of 126 Breast Invasive Carcinoma samples (each sample was a paired end RNA-Seq sample in TAR.GZ format) from the TCGA data
# command line that was used to run the following script is: python Automating_tasks_creation&Run_STAR-Fusion.py --project-name "STAR-Fusion on Breast Invasive Carcinoma samples" --app-name "star-fusion-workflow" --input-port-name "input_archive_file"
# The same script can be customized to run any app on the platform.

import sevenbridges as sbg
import argparse
# Sleeps on rate limit
from sevenbridges.http.error_handlers import rate_limit_sleeper
# Sleeps if api is in maintanance
from sevenbridges.http.error_handlers import maintenance_sleeper
# Sleeps if any error happens response.status_code >=500
from sevenbridges.http.error_handlers import general_error_sleeper
import time

# auth token hard coded


def arg_parse():
    global project_name, app_name, port_name
    parser = argparse.ArgumentParser(description='Begin fusion tasks.')
    parser.add_argument('--project-name',
                        help='CGC project name. ',
                        required=True)
    parser.add_argument('--app-name',
                        help='app name within project. ',
                        required=True)
    parser.add_argument('--input-port-name',
                        help='input port name for input reads.',
                        required=True)
    args = parser.parse_args()
    project_name = args.project_name
    app_name = args.app_name
    port_name = args.input_port_name
    return


def get_project(api, project_name):
    my_project = [p for p in api.projects.query(limit=100).all()
                  if p.name == project_name]
    # Confirm that target project that you want to run your analysis in exists
    if not my_project:
        print('Target project (%s) not found, check spelling' % project_name)
        raise KeyboardInterrupt
    else:
        my_project = my_project[0]
    return my_project


def get_app(api, my_project, app_name):
    my_app = [a for a in api.apps.query(project=my_project, limit=100).all()
              if a.name == app_name]
    # Confirm that the app that you want to run exists
    if not my_app:
        print('Target app (%s) not found, check spelling' % app_name)
        raise KeyboardInterrupt
    else:
        my_app = my_app[0]
    return my_app


def get_file(api, my_project, file_name):
    my_file = [f for f in api.files.query(project=my_project, limit=100).all()
               if f.name == file_name]
    # Confirm that the files you need for your analysis exists
    if not my_file:
        print('Target file (%s) not found, check spelling' % file_name)
        raise KeyboardInterrupt
    else:
        my_file = my_file[0]
    return my_file

# The function below should be customized according to the app you want to run and the input files that the app requires.
def begin_tasks(api, my_project, my_app, my_files):
    inputs = {}
    if (my_app.name == "star-fusion-workflow"):
        my_file = get_file(api, my_project, "GRCh38_gencode_v24_CTAT_lib_Mar292017_prebuilt.tar.gz")
        inputs["CTAT_resource_lib_tar_gz"] = my_file
    i = 0
    all_tasks = []
    for curr_file in my_files:
        # All the 126 samples names start with U
        if not(curr_file.name.startswith("U")):
            continue
        inputs["input_archive_file"] = [curr_file]
        task_name = my_app.name + " run number " + str(i)
    # In the command below remember to turn run to False in following function call during code development (
    # run = False will ensure that tasks are created in a draft state.
        my_task = api.tasks.create(name=task_name, project=my_project.id,
                                   app=my_app.id, inputs=inputs, run=True)
        all_tasks.append(my_task)
        i += 1
        time.sleep(10)
    return all_tasks


def main(project_name, app_name, port_name):
    config_file = sbg.Config(profile='cgc')
    api = sbg.Api(config=config_file, error_handlers=[rate_limit_sleeper,
                                                      maintenance_sleeper,
                                                      general_error_sleeper])
    my_project = get_project(api, project_name)
    my_app = get_app(api, my_project, app_name)
    my_files = list(api.files.query(project=my_project, limit=100).all())
    all_tasks = begin_tasks(api, my_project, my_app, my_files)
    return
if __name__ == "__main__":
    arg_parse()
    main(project_name, app_name, port_name)
