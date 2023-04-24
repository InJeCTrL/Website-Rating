import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda'
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Duration } from 'aws-cdk-lib';
import path = require('path');

export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const ratingTbl = new dynamodb.Table(this, "website_rating", {
      partitionKey: {
        name: 'host',
        type: dynamodb.AttributeType.STRING
      }
    });

    const getWebsiteRatingLambda = new lambda.Function(this, "getWebsiteRatingLambda", {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "get_website_rating.handler",
      timeout: Duration.seconds(10),
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../../lambdas/get_website_rating.py")),
      environment: {
        RATINGTABLE: ratingTbl.tableName
      }
    });

    const setWebsiteRatingLambda = new lambda.Function(this, "setWebsiteRatingLambda", {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "set_website_rating.handler",
      timeout: Duration.seconds(10),
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../../lambdas/set_website_rating.py")),
      environment: {
        RATINGTABLE: ratingTbl.tableName
      }
    });
  }
}
