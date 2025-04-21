#!/bin/bash

read -p "gitlab.cern.ch username: " GITLAB_USERNAME
read -s -p "gitlab.cern.ch Password: " GITLAB_PASSWORD
echo

GITLAB_REPO_URL="https://gitlab.cern.ch/acc-models/acc-models-sps"
FILES=("archive/SPS_LS2_2025-03-05.seq" "strengths/ft_q26.str" "aperture/STANDARD_SPS_EYETS 2024-2025_05-MAR-2025.seq" "toolkit/macro.madx" "toolkit/match_tune.madx" "toolkit/match_chrom.madx") # following examples/job_ft_q26.madx
#FILES=("SPS_LS2_2020-05-26.seq" "sps/strengths/lhc_q26.str" "aperture/APERTURE_SPS_LS2_30-SEP-2020.dbx" "sps/toolkit/macro.madx")
LOCAL_DESTINATION_DIRECTORY="."

for FILE_PATH in "${FILES[@]}"; do
    ENCODED_FILE_PATH="${FILE_PATH// /%20}"
    FILE_URL="$GITLAB_REPO_URL/-/raw/2025/$ENCODED_FILE_PATH"
    OUTPUT_FILE="$LOCAL_DESTINATION_DIRECTORY/$(basename "$FILE_PATH")"
    curl -sSL --fail --user "$GITLAB_USERNAME:$GITLAB_PASSWORD" "$FILE_URL" -o "$OUTPUT_FILE"

    if [[ $? -eq 0 ]]; then
        echo "File '$FILE_PATH' downloaded to '$OUTPUT_FILE'."
    else
        echo "Failed to download '$FILE_PATH'"
    fi
done