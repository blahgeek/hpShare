#!/bin/bash -e

USAGE="Usage: hpshare [OPTIONS] file1 file2 ...
    -u, --user:    username
    -p, --private: use longer URL
    -s, --server:  server host name, default to blaa.ml"

SERVER="blaa.ml"
USERNAME="$(whoami | tr [:upper:] [:lower:])"

hash jsawk 2>/dev/null || { echo "jsawk(https://github.com/micha/jsawk) not installed."; exit 1; }

FILES=()

while [[ $# > 0 ]]
do
    key="$1"
    case $key in
        -u|--user)
            USERNAME="$2"
            shift
            ;;
        -p|--private)
            PRIVATE=true
            ;;
        -s|--server)
            SERVER="$2"
            shift
            ;;
        -h|--help)
            echo "$USAGE"
            exit 0
            ;;
        *)
            FILES+=("$1")
            ;;
    esac
    shift
done

echo -n "Password for $USERNAME@$SERVER:"
read -s PASSWORD
echo

IDS=""

if [[ ${#FILES[*]} -eq 0 ]]; then
    echo "$USAGE"
    exit 1
fi

for FILE in ${FILES[*]}
do
    echo "Uploading $FILE..."
    PERMIT_OUTPUT=$(curl -s -X POST -u "$USERNAME:$PASSWORD" \
                    "http://$SERVER/permit/" \
                    -d "filename=$FILE" \
                    -d "private=$PRIVATE")
    TOKEN=$(echo $PERMIT_OUTPUT | jsawk "return this.token")
    UPLOAD_DOMAIN=$(echo $PERMIT_OUTPUT | jsawk "return this.upload_domain")

    if [[ -z $TOKEN ]]; then
        echo "Permit error."
        continue
    fi

    UPLOAD_OUTPUT=$(curl "http://$UPLOAD_DOMAIN" \
                    -F token="$TOKEN" \
                    -F "file=@$FILE")
    URL=$(echo $UPLOAD_OUTPUT | jsawk "return this.url")
    ID=$(echo $UPLOAD_OUTPUT | jsawk "return this.id")
    if [[ -n $URL ]]; then
        echo "Upload done, URL: $URL"
        echo
        IDS="$IDS,$ID"
    else
        echo "Upload error: $UPLOAD_OUTPUT"
    fi
done

IDS=${IDS:1:${#IDS}}

if [[ ${#FILES[*]} -gt 1 ]]; then
    echo "Grouping..."
    GROUP_OUTPUT=$(curl -s -X POST -u "$USERNAME:$PASSWORD" \
                   "http://$SERVER/newgroup/" \
                   -d "ids=$IDS" -d "private=$PRIVATE")
    URL=$(echo $GROUP_OUTPUT | jsawk "return this.url")
    COUNT=$(echo $GROUP_OUTPUT | jsawk "return this.count")
    echo "$COUNT files in group, URL: $URL"
fi
