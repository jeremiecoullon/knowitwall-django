# AWS tips

- Don't have backticks ( \` ) in environment variables; bash interprets these, and then it messes with other environment variables
- Don't couple the RDS database to elastic beanstalk, create them separately (see [SO question](https://serverfault.com/questions/540828/how-to-associate-an-existing-rds-instance-to-an-elastic-beanstalk-environment)) or [AWS docs](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html?icmpid=docs_elasticbeanstalk_console)
  - `RDS_HOSTNAME`:  this is 'endpoint' in the RDS console. Note that it _doesn't_ include the port number at the end. For example: `RDS_HOSTNAME = 'kiw-db-test-july.cj66h95sniau.us-west-2.rds.amazonaws.com'`
  - Pointing 2 different versions of the site (in an entirely different application) to the same database works fine.
  - AWS creates snapshots of the db automatically (every 7 days). You can restore a database from a snapshot (this will create a new db)
- Watch out for AWS pricing (see this [Quora question](https://www.quora.com/Is-it-very-costly-to-use-AWS-Elastic-Beanstalk-for-a-startup)). Set up CloudWatch alarms to notify me when billings exceeds a certain amount
