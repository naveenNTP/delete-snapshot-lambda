import boto3
from datetime import datetime,timedelta
from botocore.exceptions import ClientError
def delete_snapshot(snapshot_id):
     print "Deleting snapshot %s " % (snapshot_id)
     try:
          ec2resource = boto3.resource('ec2')
          snapshot = ec2resource.Snapshot(snapshot_id)
          snapshot.delete()
     except ClientError as e:
          print "Caught exception: %s" % e
def lambda_handler(event, context):
     now = datetime.now()
     #print str(now)
     account_id = 'youraccountid'
     ec2 = boto3.client('ec2')
     result = ec2.describe_snapshots( OwnerIds=[account_id],Filters=[{'Name': 'tag:created-by', 'Values': ['lambda_snapshot_create']}] )
     #print str(result)
     retention_days = 7
     for snapshot in result['Snapshots']:
          print "Checking snapshot %s which was created on %s" % (snapshot['SnapshotId'],snapshot['StartTime'])
          snapshot_time = snapshot['StartTime'].replace(tzinfo=None)
          if (now - snapshot_time) > timedelta(retention_days):
               print "Snapshot is older than configured retention of %d days - deleting" % (retention_days)
               delete_snapshot(snapshot['SnapshotId'])
          else:
               print "Snapshot is newer than configured retention of %d days so we are keeping it" % (retention_days)
