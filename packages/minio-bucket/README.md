# minio-bucket

A init container to create a bucket, a user and a policy for minio.

## Config via Environment Variables

**MINIO_URL** &nbsp;&nbsp; <span style="color:red">required</span>

The URL of the minio server.

**MINIO_ROOT_USER** &nbsp;&nbsp; <span style="color:red">required</span>

The root user of the minio server.

**MINIO_ROOT_PASSWORD** &nbsp;&nbsp; <span style="color:red">required</span>

The root password of the minio server.

**MINIO_BUCKET** &nbsp;&nbsp; <span style="color:red">required</span>

The name of the bucket to create.

**MINIO_ACCESS_KEY** &nbsp;&nbsp; <span style="color:red">required</span>

The access key of the user to create.

**MINIO_SECRET_KEY** &nbsp;&nbsp; <span style="color:red">required</span>

The secret key of the user to create.

**MINIO_POLICY_NAME**

The name of the policy to create.

_Default:_ `$MINIO_BUCKET-rw`

**MINIO_POLICY**

The policy to create.

_Default:_

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["arn:aws:s3:::$MINIO_BUCKET", "arn:aws:s3:::$MINIO_BUCKET/*"]
    }
  ]
}
```
