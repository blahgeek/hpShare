#!/bin/bash -e

USAGE="Usage: hpshare [OPTIONS] file1 file2 ...
    -u, --user:        username
    -p, --private:     use longer URL
    -n, --no-checksum: do not check sha1sum during upload
    -s, --server:      server host name, default to z1k.co"

SERVER="z1k.co"
USERNAME="$(whoami | tr [:upper:] [:lower:])"
DO_CHECKSUM="yes"
UNAMESTR=`uname`

function getJsonVal () {
    python -c "import json,sys;sys.stdout.write(json.load(sys.stdin)$1)";
}

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
        -n|--no-checksum)
            DO_CHECKSUM="no"
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

if [[ $DO_CHECKSUM = "yes" ]]; then
    SHA1SUM="sha1sum"
    hash $SHA1SUM 2>/dev/null || SHA1SUM="shasum"
    hash $SHA1SUM 2>/dev/null || { echo "sha1sum/shasum not installed."; exit 1; }
fi

echo -n "Password for $USERNAME@$SERVER:"
read -s PASSWORD
echo

IDS=""

if [[ ${#FILES[*]} -eq 0 ]]; then
    echo "$USAGE"
    exit 1
fi

for FILE in "${FILES[@]}"
do
    CHECKSUM=""
    if [[ $DO_CHECKSUM = "yes" ]]; then
        echo "Calculating checksum of $FILE..."
        CHECKSUM=$($SHA1SUM "$FILE" | cut -c 1-40)
        echo "sha1sum: $CHECKSUM"
    fi
    if [[ "$UNAMESTR" == "Darwin" ]]; then
        FILESIZE=$(stat -f "%z" "$FILE")
    else
        FILESIZE=$(stat --format "%s" "$FILE")
    fi
    echo "Uploading $FILE ($FILESIZE bytes)..."
    PERMIT_OUTPUT=$(curl -s -X POST -u "$USERNAME:$PASSWORD" \
                    "http://$SERVER/~api/hpshare/permit/" \
                    -d "filename=$FILE" \
                    -d "sha1sum=$CHECKSUM" \
                    -d "private=$PRIVATE" \
                    -d "fsize=$FILESIZE")
    TOKEN=$(echo $PERMIT_OUTPUT | getJsonVal "['token']")
    UPLOAD_DOMAIN=$(echo $PERMIT_OUTPUT | getJsonVal "['upload_domain']")

    if [[ -z $TOKEN ]]; then
        echo "Permit error."
        continue
    fi

    UPLOAD_OUTPUT=$(curl "http://$UPLOAD_DOMAIN" \
                    -F token="$TOKEN" \
                    -F "file=@$FILE")
    URL=$(echo $UPLOAD_OUTPUT | getJsonVal "['url']")
    ID=$(echo $UPLOAD_OUTPUT | getJsonVal "['id']")
    if [[ -n $URL ]]; then
        echo "Upload done, URL: $URL"
        echo
        IDS="$IDS,$ID"
    else
        ERR_MSG=$(echo $UPLOAD_OUTPUT | getJsonVal "['error']")
        if [[ -n $ERR_MSG ]]; then
            echo "Upload error: $ERR_MSG"
        else
            echo "Unknow error: $UPLOAD_OUTPUT"
        fi
    fi
done

IDS=${IDS:1:${#IDS}}

if [[ ${#FILES[*]} -gt 1 ]]; then
    echo "Grouping..."
    GROUP_OUTPUT=$(curl -s -X POST -u "$USERNAME:$PASSWORD" \
                   "http://$SERVER/~api/hpshare/newgroup/" \
                   -d "ids=$IDS" -d "private=$PRIVATE")
    URL=$(echo $GROUP_OUTPUT | getJsonVal "['url']")
    COUNT=$(echo $GROUP_OUTPUT | getJsonVal "['count']")
    echo "$COUNT files in group, URL: $URL"
fi
