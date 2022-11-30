policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:RestoreTableToPointInTime",
                "dynamodb:CreateTableReplica",
                "dynamodb:UpdateContributorInsights",
                "dynamodb:UpdateGlobalTable",
                "dynamodb:CreateBackup",
                "dynamodb:DeleteTable",
                "dynamodb:UpdateTableReplicaAutoScaling",
                "dynamodb:UpdateContinuousBackups",
                "dynamodb:PartiQLInsert",
                "dynamodb:CreateGlobalTable",
                "dynamodb:EnableKinesisStreamingDestination",
                "dynamodb:ImportTable",
                "dynamodb:DisableKinesisStreamingDestination",
                "dynamodb:UpdateTimeToLive",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:PartiQLUpdate",
                "dynamodb:StartAwsBackupJob",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteTableReplica",
                "dynamodb:CreateTable",
                "dynamodb:UpdateGlobalTableSettings",
                "dynamodb:RestoreTableFromAwsBackup",
                "dynamodb:RestoreTableFromBackup",
                "dynamodb:ExportTableToPointInTime",
                "dynamodb:DeleteBackup",
                "dynamodb:UpdateTable",
                "dynamodb:PartiQLDelete"
            ],
            "Resource": "arn:aws:dynamodb:*:191647208615:table/*linux-challenge"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "dynamodb:PurchaseReservedCapacityOfferings",
            "Resource": "*"
        }
    ]
}
    
trust_policy = { 
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
