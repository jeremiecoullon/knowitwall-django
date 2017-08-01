# AWS and deployment tips

## Git

`Master` and `dev` branches model: see this [blog post](http://nvie.com/posts/a-successful-git-branching-model/):
- only deploy from `master`
- only work on stuff in `dev`

## Billing alarm

- created a $30 billing alarm on CloudWatch

## Elastic Beanstalk

- Don't have backticks ( \` ) in environment variables; bash interprets these, and then it messes with other environment variables
- to set environment variables, add all the variables in `le_local_setup.txt`, and set them using:

```bash
eb setenv `cat le_local_setup.txt| tr '\n' ' '`
```

## Database stuff

- Don't couple the RDS database to elastic beanstalk, create them separately (see [SO question](https://serverfault.com/questions/540828/how-to-associate-an-existing-rds-instance-to-an-elastic-beanstalk-environment)) or [AWS docs](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html?icmpid=docs_elasticbeanstalk_console)
- `RDS_HOSTNAME`:  this is 'endpoint' in the RDS console. Note that it _doesn't_ include the port number at the end. For example: `RDS_HOSTNAME = 'kiw-db-test-july.cj66h95sniau.us-west-2.rds.amazonaws.com'`
- Pointing 2 different versions of the site (in an entirely different application) to the same database works fine.
- Watch out for AWS pricing (see this [Quora question](https://www.quora.com/Is-it-very-costly-to-use-AWS-Elastic-Beanstalk-for-a-startup)). Set up CloudWatch alarms to notify me when billings exceeds a certain amount

#### To restore a database

AWS creates snapshots of the db automatically (every 7 days). You can restore a database from a snapshot (this will create a new db).

To restore a database:
- got to the [RDS console](https://us-west-2.console.aws.amazon.com/rds)
- Go under the 'snaptshots' in the navigation panel on the left
- Choose a snapshot, then click 'restore snapshot' in the "Snapshot actions" dropdown button
- Once the database is built, the only thing to change is the `RDS_HOSTNAME` in the elasticbeanstalk environment variables

## Deployment timings

- spinning up a new web server (on elasticbeanstalk) takes approximately 20 min. A lot of this time is spent manually adding environment variables though.
- Restoring a db from a snapshot takes approximately 5-10 minutes
