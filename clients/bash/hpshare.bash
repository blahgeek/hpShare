#!/bin/bash -e

USAGE="Usage: hpshare [OPTIONS] file.ext
    -u, --user:    username
    -p, --private: use longer URL
    -s, --server:  server host name, default to blaa.ml"

SERVER="blaa.ml"
USERNAME="$(whoami | tr [:upper:] [:lower:])"

hash jsawk 2>/dev/null || { echo "jsawk(https://github.com/micha/jsawk) not installed."; exit 1; }

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
            FILE="$1"
            ;;
    esac
    shift
done

if [[ ! -f $FILE ]]; then
    echo "$USAGE"
    exit 1
fi

TOKEN=$(curl -s -X POST -u "$USERNAME" \
        "http://$SERVER/permit/" \
        -d "filename=$FILE" \
        -d "private=$PRIVATE")

if [[ -z $TOKEN ]]; then
    echo "Permit error."
    exit 1
fi
echo "Uploading..."

curl --progress-bar "http://up.qiniu.com" \
     -F token="$TOKEN" \
     -F "file=@$FILE"
