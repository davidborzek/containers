#!/bin/bash

set -e

function minio_ready() {
	curl -sf $MINIO_URL/minio/health/ready
}

echo "[info] starting minio bucket setup $VERSION"

if [[ 
	-z "$MINIO_URL" ||
	-z "$MINIO_ROOT_USER" ||
	-z "$MINIO_ROOT_PASS" ||
	-z "$MINIO_BUCKET" ||
	-z "$MINIO_ACCESS_KEY" ||
	-z "$MINIO_SECRET_KEY" ]]; then
	echo "[error] Required environment variables are not set."
	[[ -z "$MINIO_URL" ]] && echo "[error] 'MINIO_URL' is not set."
	[[ -z "$MINIO_ROOT_USER" ]] && echo "[error] 'MINIO_ROOT_USER' is not set."
	[[ -z "$MINIO_ROOT_PASS" ]] && echo "[error] 'MINIO_ROOT_PASS' is not set."
	[[ -z "$MINIO_BUCKET" ]] && echo "[error] 'MINIO_BUCKET' is not set."
	[[ -z "$MINIO_ACCESS_KEY" ]] && echo "[error] 'MINIO_ACCESS_KEY' is not set."
	[[ -z "$MINIO_SECRET_KEY" ]] && echo "[error] 'MINIO_SECRET_KEY' is not set."
	exit 1
fi

MINIO_POLICY_NAME=${MINIO_POLICY_NAME:-"$MINIO_BUCKET-rw"}
MINIO_ALIAS=minio

until minio_ready; do
	echo "[warn] Minio not ready yet, waiting for '$MINIO_URL' to be ready..."
	sleep 1
done

mc alias set $MINIO_ALIAS $MINIO_URL $MINIO_ROOT_USER $MINIO_ROOT_PASS

echo "[info] Creating bucket '$MINIO_BUCKET'"
mc mb \
	--ignore-existing \
	"$MINIO_ALIAS/$MINIO_BUCKET"

echo "[info] Adding user '$MINIO_ACCESS_KEY'"
mc admin user add $MINIO_ALIAS $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

echo "[info] Adding policy '$MINIO_POLICY_NAME'"

if [ ! -z "$MINIO_CUSTOM_POLICY" ]; then
	echo $MINIO_CUSTOM_POLICY >/tmp/$MINIO_POLICY_NAME.json
else
	cat <<EOF >/tmp/$MINIO_POLICY_NAME.json
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
EOF
fi

mc admin policy create $MINIO_ALIAS $MINIO_POLICY_NAME /tmp/$MINIO_POLICY_NAME.json

policy_attached=$(
	mc admin policy entities $MINIO_ALIAS --user $MINIO_ACCESS_KEY --json |
		jq '.result.userMappings[] | select( any(.policies[]; . == "'$MINIO_POLICY_NAME'"))'
)

if [ -z "$policy_attached" ]; then
	echo "[info] Policy '$MINIO_POLICY_NAME' not attached yet. Attaching..."
	mc admin policy attach $MINIO_ALIAS $MINIO_POLICY_NAME --user $MINIO_ACCESS_KEY
fi
