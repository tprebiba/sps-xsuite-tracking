#!/bin/bash

read -p "gitlab.cern.ch username: " GITLAB_USERNAME
read -s -p "gitlab.cern.ch Password: " GITLAB_PASSWORD
echo

GITLAB_REPO_URL="https://gitlab.cern.ch/acc-models/acc-models-sps"
FILES=("SPS_LS2_2020-05-26.seq" "aperture/APERTURE_SPS_LS2_30-SEP-2020.dbx" "sps/strengths/lhc_q26.str" "sps/toolkit/macro.madx")
LOCAL_DESTINATION_DIRECTORY="."

for FILE_PATH in "${FILES[@]}"; do
    FILE_URL="$GITLAB_REPO_URL/raw/2021/$FILE_PATH"
    OUTPUT_FILE="$LOCAL_DESTINATION_DIRECTORY/$(basename $FILE_PATH)"
    curl --user "$GITLAB_USERNAME:$GITLAB_PASSWORD" "$FILE_URL" -o "$OUTPUT_FILE"

    echo "File '$FILE_PATH' downloaded to '$OUTPUT_FILE'."
done