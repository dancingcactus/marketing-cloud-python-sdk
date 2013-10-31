#!/usr/bin/python
from apiWrapper import AnalyticsAPI
import sys
import datetime
import json

def format_datetime(datetime_value):
    return datetime_value.strftime('%Y-%m-%d')

def generate_date_range():
    yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
    eight_days_ago = datetime.date.fromordinal(datetime.date.today().toordinal()-8)
    return format_datetime(eight_days_ago), format_datetime(yesterday)

def main(credentials_file):
    api = AnalyticsAPI(credentials_file)
    report_suites_response = json.loads(api.invoke("Company.GetReportSuites", {}))
    report_suites = report_suites_response['report_suites']
    if len(report_suites) == 0:
        print 'No report suites available'
        sys.exit()
    elif len(report_suites) == 1:
        print 'Using report suite name %s' % report_suites[0]['site_title']
        rsid = report_suites[0]['rsid']
    else:
        for rsid_index in range(len(report_suites)):
            print '%d\t%s' % (rsid_index+1, report_suites[rsid_index]['site_title'])
        rsid_index_value = int(raw_input('Ping which report suite?\n')) - 1
        rsid = report_suites[rsid_index_value]['rsid']
    eightDaysAgo, yesterday = generate_date_range()
    print 'Running test report from %s to %s' % (eightDaysAgo, yesterday)
    reportDef = '''
    {
        "reportDescription":{
            "reportSuiteID": "%s",
            "dateFrom": "%s",
            "dateTo":"%s",
            "metrics":[
                {
                    "id":"page_views"
                },
                {
                    "id":"visits"
                },
                {
                    "id":"visitors"
                }

            ],
            "sortBy":"page_views",
            "elements":[
                {
                    "id":"evar1"
                },
                {
                    "id":"trackingcode"
                }
            ]
        }
    }
    ''' % (rsid, eightDaysAgo, yesterday)
    ranked_report_response = api.invoke("Report.GetRankedReport", reportDef)
    print ranked_report_response

if __name__ == '__main__':
    if len(sys.argv) == 2:
        credentials_file = sys.argv[1]
        main(credentials_file)
    else:
        print 'Need a credentials file'
        print 'Read the README for syntax and see an example in credentials.cfg'
        sys.exit(1)