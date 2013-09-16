from apiWrapper import AnalyticsAPI
import json 

creds = {}
execfile("credentials.conf",creds)

print creds

api = AnalyticsAPI(creds['username'],creds['password'])

output = api.invoke("Company.GetReportSuites",{})

obj = json.loads(output)

#	print obj["report_suites"][0]

#Step 1 Get the Data 
reportDef = """
{
	"reportDescription":{
		"reportSuiteID":"jjesquire2",
		"dateFrom":"2013-05-01",
		"dateTo":"2013-05-23",
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
"""
print api.invoke("Report.GetRankedReport",reportDef)
