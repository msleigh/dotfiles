#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE}")" || exit

while IFS= read -r FILE ; do

    DIFF="$(diff --minimal "./${FILE}" "${HOME}/${FILE}")"
    if [[ -n "${DIFF}" ]] ; then
        echo "${FILE}"
        echo
        echo "${DIFF}"
        echo " ---------------------------------------------------- "
    fi

done < \
<(find . -type f \
    -not -path "./.git/*"    \
    -not -path "./.DS_Store" \
    -not -path "./.osx" \
    -not -path "./bootstrap.sh" \
    -not -path "./check.sh" \
    -not -path "./README.md" \
    -not -path "./LICENSE-MIT.txt" \
    -not -path "./init/*" \
    -not -path "./bin/subl"
)

exit 0
