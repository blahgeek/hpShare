#!/bin/bash -e
# @Author: BlahGeek
# @Date:   2016-08-14
# @Last Modified by:   BlahGeek
# @Last Modified time: 2016-08-14

USAGE="Usage: hpshorten [OPTIONS] URL
    -u, --user:     username
    -p, --private:  use longer URL
    -c, --cloak:    cloak redirect
    -i, --insecure: use insecure http protocol
    -s, --server:   server hostname, default to z1k.co"

SERVER="share.z1k.dev"
USERNAME="$(whoami | tr [:upper:] [:lower:])"
PROTOCAL="https"

function getJsonVal () {
    python -c "import json,sys;sys.stdout.write(str(json.load(sys.stdin)$1))";
}

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
        -c|--cloak)
            CLOAK=true
            ;;
        -s|--server)
            SERVER="$2"
            shift
            ;;
        -i|--insecure)
            PROTOCAL="http"
            ;;
        -h|--help)
            echo "$USAGE"
            exit 0
            ;;
        *)
            URL="$1"
            ;;
    esac
    shift
done

if [[ "$URL" = "" ]]; then
    echo "$USAGE"
    exit 1
fi

echo -n "Password for $USERNAME@$SERVER:"
read -s PASSWORD
echo

OUTPUT=$(curl -s -X POST -u "$USERNAME:$PASSWORD" \
         "$PROTOCAL://$SERVER/~api/hpshorten/create/" \
         -d "private=$PRIVATE" \
         -d "cloak=$CLOAK" \
         --data-urlencode "url=$URL")
S_URL=$(echo "$OUTPUT" | getJsonVal "['url']")
echo "Done, URL: $S_URL"
