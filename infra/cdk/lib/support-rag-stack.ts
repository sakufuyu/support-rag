import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import * as origins from "aws-cdk-lib/aws-cloudfront-origins";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as rds from "aws-cdk-lib/aws-rds";
import * as ecr from "aws-cdk-lib/aws-ecr";
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
import * as logs from "aws-cdk-lib/aws-logs";
import * as iam from "aws-cdk-lib/aws-iam";

export class SupportRagStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    cdk.Tags.of(this).add('auto-delete', 'no');

    const frontendBucket = new s3.Bucket(this, "FrontendBucket", {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    const distribution = new cloudfront.Distribution(this, "Distribution", {
      defaultBehavior: {
        origin: origins.S3BucketOrigin.withOriginAccessControl(frontendBucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
    });

    const vpc = new ec2.Vpc(this, "Vpc", {
      maxAzs: 2,
      natGateways: 1
    });

    const dbSecret = new secretsmanager.Secret(this, "DbSecret", {
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: "postgres" }),
        generateStringKey: "password",
        excludePunctuation: true,
      },
    });

    const database = new rds.DatabaseInstance(this, "PostgresDatabase", {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_16,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T4G,
        ec2.InstanceSize.MICRO
      ),
      vpc,
      credentials: rds.Credentials.fromSecret(dbSecret),
      databaseName: "support_rag",
      allocatedStorage: 20,
      publiclyAccessible: false,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      deletionProtection: false,
    });

    const backendRepo = new ecr.Repository(this, "BackendRepository", {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteImages: true,
    });

    const openAiSecret = new secretsmanager.Secret(this, "OpenAISecret", {
      secretName: "support-rag/open-api-key",
      description: "OpneAI API key for SupportRAG",
    });

    const cluster = new ecs.Cluster(this, "SupportRagCluster", {
      vpc,
      containerInsights: true
    });

    const albSg = new ec2.SecurityGroup(this, "AlbSecurityGroup", {
      vpc,
      allowAllOutbound: true,
      description: "Security group for public ALB",
    });

    albSg.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(80),
      "Allow HTTP from internet"
    );

    albSg.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      "Allow HTTPS from internet"
    );

    const ecsSg = new ec2.SecurityGroup(this, "EcsServiceSecurityGroup", {
      vpc,
      allowAllOutbound: true,
      description: "Security group for ECS Fargate tasks",
    });

    ecsSg.addIngressRule(
      albSg,
      ec2.Port.tcp(8000),
      "Allow backend traffic from ALB"
    );

    database.connections.allowFrom(
      ecsSg,
      ec2.Port.tcp(5432),
      "Allow ECS tasks to connect to PostgreSQL"
    );

    const backendLogGroup = new logs.LogGroup(this, "BackendLogGroup", {
      logGroupName: "/ecs/support-rag-backend",
      retention: logs.RetentionDays.ONE_YEAR,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const taskDefinition = new ecs.FargateTaskDefinition(
      this,
      "BackendTaskDefinition",
      {
        cpu: 512,
        memoryLimitMiB: 1024,
      }
    );

    new cdk.CfnOutput(this, "FrontendBucketName", {
      value: frontendBucket.bucketName,
    });

    new cdk.CfnOutput(this, "CloudFrontUrl", {
      value: `https://${distribution.distributionDomainName}`,
    });

    new cdk.CfnOutput(this, "BackendRepositoryUri", {
      value: backendRepo.repositoryUri,
    });

    new cdk.CfnOutput(this, "DatabaseEndpoint", {
      value: database.dbInstanceEndpointAddress,
    });

    new cdk.CfnOutput(this, "OpenAISecretName", {
      value: openAiSecret.secretName,
    });
  }
}
