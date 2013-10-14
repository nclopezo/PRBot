#! /usr/bin/env python
from optparse import OptionParser
from github import Github

parser = OptionParser(usage="usage: %prog [options]")

parser.add_option("-u", action="store", type="string", dest="username", help="Your github account username")
parser.add_option("-p", action="store", type="string", dest="password", help="Your github account password")
parser.add_option("--pr", action="store", type="int", dest="pr_number", help="The number of the pull request to use")
parser.add_option("--pr-job-id", action="store", type="int", dest="pr_job_id", help="The jenkins job id for the  pull request to use")

(options, args) = parser.parse_args()

#-------------------------------------------------------------------------------------
def send_tests_approved_pr_message(repo,pr_number,tests_url):
	pull_request = repo.get_pull(pr_number)
	print 'I will send an approval comment for PR %d:' % pr_number
	message = '+1' +'\n' + tests_url
	print 'Message:'
	print message
	pull_request.create_issue_comment(message)

def get_cmssw_official_repo(github):
        user = github.get_user()
        orgs = user.get_orgs()
        for org in orgs:
                if (org.login == 'cms-sw'):
			repo = org.get_repo('cmssw')
			return repo

#----------------------------------------------------------------------------------------
username = options.username
password = options.password
pr_number = options.pr_number
pr_job_id=options.pr_job_id

github = Github(username, password)
official_cmssw=get_cmssw_official_repo(github)
tests_results_url='https://cmssdt.cern.ch/SDT/jenkins-artifacts/pull-request-integration/%d/summary.html' % pr_job_id
send_tests_approved_pr_message(official_cmssw,pr_number,tests_results_url)
