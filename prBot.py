#! /usr/bin/env python
from optparse import OptionParser
from github import Github

parser = OptionParser(usage="usage: %prog ACTION [options] \n ACTION = TESTS_OK_PR | PARSE_UNIT_TESTS_FAIL")

parser.add_option("-u", action="store", type="string", dest="username", help="Your github account username", default='None')
parser.add_option("-p", action="store", type="string", dest="password", help="Your github account password", default='None')
parser.add_option("--pr", action="store", type="int", dest="pr_number", help="The number of the pull request to use", default=-1)
parser.add_option("--pr-job-id", action="store", type="int", dest="pr_job_id", help="The jenkins job id for the  pull request to use", default=-1)

(options, args) = parser.parse_args()

#-------------------------------------------------------------------------------------
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
	unit_tests_file = options.unit_tests_file
else:
	print "I don't recognize that action!"
