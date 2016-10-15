import time
import sys
import subprocess
import os
import shutil
import ConfigParser
from argparse import ArgumentParser
from job import job as j

CREATE_HELP = """Create an orthrus workspace"""
ADD_HELP = """Add a fuzzing job"""
REMOVE_HELP = """Remove a fuzzing job"""
START_HELP = """Start a fuzzing jobs"""
STOP_HELP = """Stop a fuzzing jobs"""
SHOW_HELP = """Show what's currently going on"""
TRIAGE_HELP = """Triage crash corpus"""
COVERAGE_HELP = """Run afl-cov on existing AFL corpus"""
DESTROY_HELP = """Destroy an orthrus workspace"""
VALIDATE_HELP = """Check if all Orthrus dependencies are met"""
## A/B Tests
ABTEST_ADD_HELP = """Add an A/B test job based on supplied config"""
ABTEST_REMOVE_HELP = """Remove an A/B test job"""
ABTEST_START_HELP = """Start an A/B test job"""
ABTEST_STOP_HELP = """Stop an A/B test job"""
ABTEST_SHOW_HELP = """Display A/B test info"""
ABTEST_TRIAGE_HELP = """Triage an A/B test job"""
ABTEST_COVERAGE_HELP = """Run afl-cov for an A/B test job"""
ABTEST_DESTROY_HELP = """Destroy an A/B test job"""

TEST_SLEEP = 5

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    INFO = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color_print(color, msg):
    sys.stdout.write(color + msg + bcolors.ENDC + "\n")
    sys.stdout.flush()

def color_print_singleline(color, msg):
    sys.stdout.write(color + msg + bcolors.ENDC)
    sys.stdout.flush()

def run_cmd(command, env=None, logfile=None):
    if not logfile:
        logfile = os.devnull

    if not env:
        env = os.environ.copy()

    logfh = open(logfile, 'w')
    proc = subprocess.Popen(command, shell=True, executable='/bin/bash',
                            env=env, stdout=logfh, stderr=subprocess.STDOUT)
    ret = proc.wait()
    logfh.close()

    if ret != 0:
        return False
    return True


def return_elf_binaries(inpath=None):

    if not inpath:
        # Search everywhere in working dir except in .orthrus
        command = "find -type f -executable -not -path \"./.orthrus/*\"" \
                  " -exec file -i '{}' \; | grep 'x-executable; charset=binary' | cut -d':' -f1"
    else:
        # Search everywhere in specified path
        command = "find {} -type f ".format(inpath) + "-executable -exec file -i '{}' \; | " \
                                                     "grep 'x-executable; charset=binary' | " \
                                                     "cut -d':' -f1"
    output = subprocess.check_output(command, shell=True)
    return filter(None, output.split("\n"))

def copy_binaries(dest):
    # Create bin dir if it doesn't exist
    if not os.path.isdir(dest):
        os.makedirs(dest)

    binaries = return_elf_binaries()
    # Overwriting existing binaries is fine
    for f in binaries:
        if not os.path.isfile(dest + os.path.basename(f)):
            shutil.copy(f, dest)


def parse_cmdline(description, args, createfunc=None, addfunc=None, removefunc=None,
                  startfunc=None, stopfunc=None, showfunc=None, triagefunc=None,
                  coveragefunc=None, destroyfunc=None, validatefunc=None):
    argParser = ArgumentParser(description)

    argParser.add_argument('-v', '--verbose',
                           action='store_true',
                           help="""Verbose mode, print information about the progress""",
                           default=False)

    subparsers = argParser.add_subparsers(description="Orthrus subcommands")

    # Command 'create'
    create_parser = subparsers.add_parser('create', help=CREATE_HELP)
    create_parser.add_argument('-asan', '--afl-asan',
                               action='store_true',
                               help="""Setup binaries for afl with AddressSanitizer""",
                               default=False)
    create_parser.add_argument('-fuzz', '--afl-harden',
                               action='store_true',
                               help="""Setup binaries for afl in 'harden' mode (stack-protector, fortify)""",
                               default=False)
    create_parser.add_argument('-cov', '--coverage',
                               action='store_true',
                               help="""Setup binaries to collect coverage information""",
                               default=False)
    create_parser.add_argument('-d', '--configure-flags', nargs='?',
                               type=str, default="",
                               help='Additional flags for configuring the source')
    # create_parser.add_argument('-f', '--cflags', nargs='?',
    #                         type = str, default="",
    #                         help = 'Additional flags to go into CFLAGS for compilation')
    # create_parser.add_argument('-l', '--ldflags', nargs='?',
    #                         type = str, default="",
    #                         help = 'Additional flags to go into LDFLAGS for compilation')
    create_parser.set_defaults(func=createfunc)

    # Command 'add'
    add_parser = subparsers.add_parser('add', help=ADD_HELP)
    add_parser.add_argument('-n', '--job', required=True, type=str,
                            help='Add a job with executable command line invocation string')
    # add_parser.add_argument('-j', '--job-id', nargs='?',
    #                         type=str, default="",
    #                         help='Job Id for the job which should be selected')
    add_parser.add_argument('-i', '--import', dest='_import', nargs='?',
                            type=str, default="",
                            help='Import an AFL fuzzing output directory provided as tar.gz')
    add_parser.add_argument('-s', '--sample', nargs='?',
                            type=str, default="",
                            help='A single file or directory of afl testcases for fuzzing')
    add_parser.add_argument('-abtest-conf', '--abconf', nargs='?', type=str,
                            default="", help=ABTEST_ADD_HELP)
    add_parser.set_defaults(func=addfunc)

    # Command 'remove'
    remove_parser = subparsers.add_parser('remove', help=REMOVE_HELP)
    remove_parser.add_argument('-j', '--job-id', required=True,
                               type=str, help='Job Id for the job which should be removed')
    remove_parser.add_argument('-abtest', '--abtest', action='store_true',
                            help=ABTEST_REMOVE_HELP, default=False)
    remove_parser.set_defaults(func=removefunc)

    # Command 'start'
    start_parser = subparsers.add_parser('start', help=START_HELP)
    start_parser.add_argument('-j', '--job-id', required=True,
                              type=str, help='Job Id for the job which should be started')
    start_parser.add_argument('-c', '--coverage',
                              action='store_true',
                              help="""Collect coverage information while fuzzing""",
                              default=False)
    start_parser.add_argument('-m', '--minimize',
                              action='store_true',
                              help="""Minimize corpus before start""",
                              default=False)
    start_parser.add_argument('-abtest', '--abtest', action='store_true',
                            help=ABTEST_START_HELP, default=False)
    start_parser.set_defaults(func=startfunc)

    # Command 'stop'
    stop_parser = subparsers.add_parser('stop', help=STOP_HELP)
    stop_parser.add_argument('-c', '--coverage',
                             action='store_true',
                             help="""Stop afl-cov instances on stop""",
                             default=False)
    stop_parser.add_argument('-abtest', '--abtest', action='store_true',
                            help=ABTEST_STOP_HELP, default=False)
    stop_parser.set_defaults(func=stopfunc)

    # Command 'show'
    show_parser = subparsers.add_parser('show', help=SHOW_HELP)
    show_parser.add_argument('-j', '--jobs',
                             action='store_true',
                             help="""Show configured jobs""",
                             default=False)
    show_parser.add_argument('-cov', '--cov',
                             action='store_true',
                             help="""Show coverage of job""",
                             default=False)
    show_parser.add_argument('-abtest', '--abtest', action='store_true',
                            help=ABTEST_SHOW_HELP, default=False)
    show_parser.set_defaults(func=showfunc)

    # Command 'triage'
    triage_parser = subparsers.add_parser('triage', help=TRIAGE_HELP)
    triage_parser.add_argument('-j', '--job-id', nargs='?',
                               type=str, default="",
                               help="""Job Id for the job which should be triaged""")
    triage_parser.add_argument('-abtest', '--abtest', action='store_true',
                            help=ABTEST_TRIAGE_HELP, default=False)
    triage_parser.set_defaults(func=triagefunc)

    # Command 'coverage'
    coverage_parser = subparsers.add_parser('coverage', help=COVERAGE_HELP)
    coverage_parser.add_argument('-j', '--job-id', nargs='?',
                               type=str, default="", required=True,
                               help="""Job Id for checking coverage""")
    coverage_parser.add_argument('-abtest', '--abtest', action='store_true',
                            help=ABTEST_COVERAGE_HELP, default=False)
    coverage_parser.set_defaults(func=coveragefunc)

    # Command 'destroy'
    destroy_parser = subparsers.add_parser('destroy', help=DESTROY_HELP)
    # create_parser.add_argument('-x', type=int, default=1)
    destroy_parser.add_argument('-abtest', '--abtest', action='store_true',
                            help=ABTEST_DESTROY_HELP, default=False)
    destroy_parser.set_defaults(func=destroyfunc)

    # Command 'validate'
    validate_parser = subparsers.add_parser('validate', help=VALIDATE_HELP)
    validate_parser.set_defaults(func=validatefunc)

    return argParser.parse_args(args)

def parse_config(configfile=None):
    config = {}
    if not configfile:
        configfile = os.path.expanduser('~/.orthrus/orthrus.conf')

    configparser = ConfigParser.ConfigParser()
    configparser.read(configfile)

    config['orthrus'] = {}
    config['orthrus']['directory'] = configparser.get("orthrus", "directory")

    config['dependencies'] = configparser.items("dependencies")

    # config['joern'] = {}
    # config['joern']['joern_path'] = os.path.abspath(os.path.expanduser((configparser.get("joern", "joern_path"))))
    #
    # config['neo4j'] = {}
    # config['neo4j']['neo4j_path'] = os.path.abspath(os.path.expanduser((configparser.get("neo4j", "neo4j_path"))))

    # config['afl'] = {}
    # config['afl']['afl_path'] = os.path.abspath(os.path.expanduser((configparser.get("afl", "afl_path"))))
    #
    # config['afl-utils'] = {}
    # config['afl-utils']['afl_utils_path'] = os.path.abspath(
    #     os.path.expanduser((configparser.get("afl-utils", "afl_utils_path"))))
    #
    # config['afl-cov'] = {}
    # config['afl-cov']['afl_cov_path'] = os.path.abspath(
    #     os.path.expanduser((configparser.get("afl-cov", "afl_cov_path"))))

    return config

def minimize_sync_dir(job_object):
    color_print(bcolors.OKGREEN, "\t\t[+] Minimizing corpus for job [" + job_object.id + "]...")

    export = {}
    export['PYTHONUNBUFFERED'] = "1"
    env = os.environ.copy()
    env.update(export)
    isasan = False

    if os.path.exists(job_object.orthrusdir + "/binaries/afl-harden"):
        launch = job_object.orthrusdir + "/binaries/afl-harden/bin/" + job_object.target + " " + \
                 job_object.params.replace("&", "\&")
    else:
        isasan = True
        launch = job_object.orthrusdir + "/binaries/afl-asan/bin/" + job_object.target + " " + \
                 job_object.params

    if isasan and is64bit():
        mem_limit = 30000000
    else:
        mem_limit = 800
    cmin = " ".join(
        ["afl-minimize", "-c", job_object.rootdir + "/collect", "--cmin",
         "--cmin-mem-limit={}".format(mem_limit), "--cmin-timeout=5000", "--dry-run",
         job_object.rootdir + "/afl-out", "--", "'" + launch + "'"])
    p = subprocess.Popen(cmin, bufsize=0, shell=True, executable='/bin/bash', env=env, stdout=subprocess.PIPE)
    for line in p.stdout:
        if "[*]" in line or "[!]" in line:
            color_print(bcolors.OKGREEN, "\t\t\t" + line)

    # Sleep for a short bit so that archived queue time stamps differ
    time.sleep(2)

    reseed_cmd = " ".join(
        ["afl-minimize", "-c", job_object.rootdir + "/collect.cmin",
         "--reseed", job_object.rootdir + "/afl-out", "--",
         "'" + launch + "'"])
    p = subprocess.Popen(reseed_cmd, bufsize=0, shell=True, executable='/bin/bash', env=env, stdout=subprocess.PIPE)
    for line in p.stdout:
        if "[*]" in line or "[!]" in line:
            color_print(bcolors.OKGREEN, "\t\t\t" + line)

    if os.path.exists(job_object.rootdir + "/collect"):
        shutil.rmtree(job_object.rootdir + "/collect")
    if os.path.exists(job_object.rootdir + "/collect.cmin"):
        shutil.rmtree(job_object.rootdir + "/collect.cmin")
    if os.path.exists(job_object.rootdir + "/collect.cmin.crashes"):
        shutil.rmtree(job_object.rootdir + "/collect.cmin.crashes")
    if os.path.exists(job_object.rootdir + "/collect.cmin.hangs"):
        shutil.rmtree(job_object.rootdir + "/collect.cmin.hangs")

    return True


def minimize_sync_dir_(config, jobId):
    color_print(bcolors.OKGREEN, "\t\t[+] Minimizing corpus for job [" + jobId + "]...")

    job_config = ConfigParser.ConfigParser()
    job_config.read(config['orthrus']['directory'] + "/jobs/jobs.conf")
    export = {}
    export['PYTHONUNBUFFERED'] = "1"
    env = os.environ.copy()
    env.update(export)
    isasan = False

    if os.path.exists(config['orthrus']['directory'] + "/binaries/afl-harden"):
        launch = config['orthrus']['directory'] + "/binaries/afl-harden/bin/" + job_config.get(jobId,
                                                                                                     "target") + " " + job_config.get(
            jobId, "params").replace("&", "\&")
    else:
        isasan = True
        launch = config['orthrus']['directory'] + "/binaries/afl-asan/bin/" + job_config.get(jobId,
                                                                                                   "target") + " " + job_config.get(
            jobId, "params")

    if isasan and is64bit():
        mem_limit = 30000000
    else:
        mem_limit = 800
    cmin = " ".join(
        ["afl-minimize", "-c", config['orthrus']['directory'] + "/jobs/" + jobId + "/collect", "--cmin",
         "--cmin-mem-limit={}".format(mem_limit), "--cmin-timeout=5000", "--dry-run",
         config['orthrus']['directory'] + "/jobs/" + jobId + "/afl-out", "--", "'" + launch + "'"])
    p = subprocess.Popen(cmin, bufsize=0, shell=True, executable='/bin/bash', env=env, stdout=subprocess.PIPE)
    for line in p.stdout:
        if "[*]" in line or "[!]" in line:
            color_print(bcolors.OKGREEN, "\t\t\t" + line)

    # Sleep for a short bit so that archived queue time stamps differ
    time.sleep(2)

    reseed_cmd = " ".join(
        ["afl-minimize", "-c", config['orthrus']['directory'] + "/jobs/" + jobId + "/collect.cmin",
         "--reseed", config['orthrus']['directory'] + "/jobs/" + jobId + "/afl-out", "--",
         "'" + launch + "'"])
    p = subprocess.Popen(reseed_cmd, bufsize=0, shell=True, executable='/bin/bash', env=env, stdout=subprocess.PIPE)
    for line in p.stdout:
        if "[*]" in line or "[!]" in line:
            color_print(bcolors.OKGREEN, "\t\t\t" + line)

    if os.path.exists(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect"):
        shutil.rmtree(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect")
    if os.path.exists(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect.cmin"):
        shutil.rmtree(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect.cmin")
    if os.path.exists(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect.cmin.crashes"):
        shutil.rmtree(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect.cmin.crashes")
    if os.path.exists(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect.cmin.hangs"):
        shutil.rmtree(config['orthrus']['directory'] + "/jobs/" + jobId + "/collect.cmin.hangs")

    return True

def is64bit():
    cmd = 'uname -m'
    try:
        if 'x86_64' in subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT):
            return True
    except subprocess.CalledProcessError as e:
        print e.output
    return False

def getnproc():
    cmd = 'nproc'
    try:
        nproc = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return 1
    return nproc.rstrip()

# def printfile(filename):
#     cmd = 'cat ' + filename
#     print subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

def which(progname):
    cmd = 'which ' + progname
    try:
        path = os.path.expanduser(subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).rstrip())
    except subprocess.CalledProcessError as e:
        print e.output
        return ''
    return os.path.abspath(path)

def run_afl_cov(orthrus_root, jobId, target, params, livemode=False, test=False):
    target = orthrus_root + "/binaries/coverage/bin/" + \
             target + " " + params.replace("@@", "AFL_FILE")

    if livemode:
        cmd = ["nohup", "afl-cov", "-d", ".orthrus/jobs/" + jobId + \
           "/afl-out", "--live", "--lcov-path", which('lcov'), "--genhtml-path", which('genhtml'), "--coverage-cmd", \
               "'" + target + "'", "--code-dir", "."]
        if test:
            cmd.extend(['--sleep', str(TEST_SLEEP)])
    else:
        cmd = ["nohup", "afl-cov", "-d", ".orthrus/jobs/" + jobId + \
               "/afl-out", "--lcov-path", which('lcov'), "--genhtml-path", which('genhtml'), "--coverage-cmd", \
               "'" + target + "'", "--code-dir", "."]
    logfile = orthrus_root + "/logs/afl-coverage.log"
    p = subprocess.Popen(" ".join(cmd), shell=True, executable="/bin/bash", stdout=open(logfile, 'w'),
                         stderr=subprocess.STDOUT)

def validate_inst(config):

    if not config['dependencies']:
        return False

    for program, mode in config['dependencies']:
        if mode == 'on' and not which(program):
            color_print(bcolors.FAIL, "\t\t\t[-] Could not locate {}. Perhaps modifying the PATH variable helps?".
                        format(program))
            return False
    return True

def validate_job(orthrus_root, jobID):

    try:
        job_token = j.jobtoken(orthrus_root, jobID)
    except ValueError:
        return False

    return True

def func_wrapper(function, *args):
    try:
        rv = function(*args)
        if rv is None or rv:
            return True
        else:
            return False
    except:
        return False

def pprint_decorator_fargs(predicate, prologue, indent=0, fail_msg='failed', success_msg='done'):

    color_print_singleline(bcolors.OKGREEN, '\t'*indent + '[+] {}... '.format(prologue))

    if not predicate:
        color_print(bcolors.FAIL, fail_msg)
        return False
    else:
        color_print(bcolors.OKGREEN, success_msg)
        return True

def pprint_decorator(function, prologue, indent=0, fail_msg='failed', success_msg='done'):

    color_print_singleline(bcolors.OKGREEN, '\t'*indent + '[+] {}... '.format(prologue))

    try:
        rv = function()
        if rv is None or rv:
            color_print(bcolors.OKGREEN, success_msg)
            return True
        else:
            color_print(bcolors.FAIL, fail_msg)
            return False
    except:
        color_print(bcolors.FAIL, fail_msg)
        return False