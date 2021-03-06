#! /usr/bin/env python
from optparse import OptionParser
from github import Github
import re

#-----------------------------------------------------------------------------------
#---- Parser Options
#-----------------------------------------------------------------------------------
parser = OptionParser(usage="usage: %prog ACTION [options] \n ACTION = TESTS_OK_PR | PARSE_UNIT_TESTS_FAIL | PARSE_BUILD_FAIL | PARSE_MATRIX_FAIL")

parser.add_option("-u", action="store", type="string", dest="username", help="Your github account username", default='None')
parser.add_option("-p", action="store", type="string", dest="password", help="Your github account password", default='None')
parser.add_option("--pr", action="store", type="int", dest="pr_number", help="The number of the pull request to use", default=-1)
parser.add_option("--pr-job-id", action="store", type="int", dest="pr_job_id", help="The jenkins job id for the  pull request to use", default=-1)
parser.add_option("--unit-tests-file", action="store", type="string", dest="unit_tests_file", help="Unit tests file to analyze", default='None')

(options, args) = parser.parse_args()

#------------------------------------------------------------------------------------
#---- Error Class
#------------------------------------------------------------------------------------
#TODO

#-------------------------------------------------------------------------------------
 
def read_matrix_log_file(repo,matrix_log,tests_url):
	pull_request = repo.get_pull(pr_number)
	workflows_with_error = []
	for line in open(matrix_log):
		if 'ERROR executing' in line:
			parts = line.split(" ")
			workflow = parts[4]
			workflow = re.sub('_.*$', '', workflow)
			workflows_with_error.append(workflow)
	message = '-1 \n When I ran the RelVals I found an error in the following worklfows: \n '
	for wf in workflows_with_error:
		message += wf + '\n'
	message += '\n you can see the results of the tests here: \n %s ' % tests_url
        print message
	pull_request.create_issue_comment(message) 


def read_build_log_file(repo,build_log,tests_url):
	pull_request = repo.get_pull(pr_number)
	error_found = False
	line_number = 0
	error_line = 0
	lines_to_keep_before=5
	lines_to_keep_after=5
	lines_since_error=0
	lines_before = ['']
	lines_after = ['']
	error_found = False
	for line in open(build_log):
		line_number += 1
		if (not error_found):
			lines_before.append(line)
			if (line_number > lines_to_keep_before):
				lines_before.pop(0)
		if 'error: ' in line:
			error_found = True
			error_line = line_number
		if error_found:
			if (lines_since_error == 0):
				lines_since_error += 1
				continue
			elif (lines_since_error <= lines_to_keep_after):
				lines_since_error += 1
				lines_after.append(line)
			else:
				break
	message = '-1 \n I found an error when building: \n \n <pre>'
	for line in lines_before:
		message += line + '\f'
	for line in lines_after:
		message += line + '\f'
	message += '</pre> \n you can see the results of the tests here: \n %s ' % tests_url
	print message 
	#pull_request.create_issue_comment(message)

def read_unit_tests_file(repo,unit_tests_file,tests_url):
	pull_request = repo.get_pull(pr_number)
	errors_found=''
	for line in open(unit_tests_file):
		if( 'had ERRORS' in line):
			errors_found = errors_found + line
	message = '-1 \n I ran the usual tests and I found errors in the following unit tests: \n \n %s \n \n' % errors_found
	message = message + 'you can see the results of the tests here: \n %s ' % tests_url
	print message
	pull_request.create_issue_comment(message)

def send_tests_approved_pr_message(repo,pr_number,tests_url):
	pull_request = repo.get_pull(pr_number)
	print 'I will send an approval comment for PR %d:' % pr_number
	message = '+1' +'\n' + tests_url
	print 'Message:'
	print message
	#pull_request.create_issue_comment(message)

def get_cmssw_official_repo(github):
        user = github.get_user()
        orgs = user.get_orgs()
        for org in orgs:
                if (org.login == 'cms-sw'):
			repo = org.get_repo('cmssw')
			return repo

def complain_missing_param(param_name):
	print '\n'
	print 'I need a %s to continue' % param_name
	print '\n'
	parser.print_help()
        exit()

#----------------------------------------------------------------------------------------
#---- Check arguments and options
#---------------------------------------------------------------------------------------

if (len(args)==0):
	print 'you have to choose an action'
	parser.print_help()
	exit()

action = args[0]

if (action == 'prBot.py'):
	print 'you have to choose an action'
        parser.print_help()
        exit()

print 'you chose the action %s' % action

if (options.username == 'None' ):
	complain_missing_param('github username')
	exit()
else:
	username = options.username

if (options.password == 'None' ):
        complain_missing_param('github password')
        exit()
else:
	password = options.password

if (options.pr_number == -1 ):
        complain_missing_param('pull request number')
        exit()
else:
	pr_number = options.pr_number

if (options.pr_job_id == -1 ):
        complain_missing_param('pull request job id')
        exit()
else:
	pr_job_id=options.pr_job_id

github = Github(username, password)
official_cmssw=get_cmssw_official_repo(github)

if (action == 'TESTS_OK_PR'):
	tests_results_url='https://cmssdt.cern.ch/SDT/jenkins-artifacts/pull-request-integration/%d/summary.html' % pr_job_id
	send_tests_approved_pr_message(official_cmssw,pr_number,tests_results_url)
elif (action == 'PARSE_UNIT_TESTS_FAIL'):
	tests_results_url='https://cmssdt.cern.ch/SDT/jenkins-artifacts/pull-request-integration/%d/summary.html' % pr_job_id
	unit_tests_file = options.unit_tests_file
	read_unit_tests_file(official_cmssw,unit_tests_file,tests_results_url)
elif (action == 'PARSE_BUILD_FAIL'):
	tests_results_url='https://cmssdt.cern.ch/SDT/jenkins-artifacts/pull-request-integration/%d/summary.html' % pr_job_id
	build_log_file = options.unit_tests_file
	read_build_log_file(official_cmssw,build_log_file, tests_results_url)
elif (action == 'PARSE_MATRIX_FAIL'):
	tests_results_url='https://cmssdt.cern.ch/SDT/jenkins-artifacts/pull-request-integration/%d/summary.html' % pr_job_id
	matrix_log_file = options.unit_tests_file
	read_matrix_log_file(official_cmssw,matrix_log_file,tests_results_url)
else:
	print "I don't recognize that action!"
