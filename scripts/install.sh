#!/usr/bin/bash

# begin inlined cloudflare/semver_bash
function semverParseInto() {
    local RE='[^0-9]*\([0-9]*\)[.]\([0-9]*\)[.]\([0-9]*\)\([0-9A-Za-z-]*\)'
    #MAJOR
    eval $2=`echo $1 | sed -e "s#$RE#\1#"`
    #MINOR
    eval $3=`echo $1 | sed -e "s#$RE#\2#"`
    #MINOR
    eval $4=`echo $1 | sed -e "s#$RE#\3#"`
    #SPECIAL
    eval $5=`echo $1 | sed -e "s#$RE#\4#"`
}

function semverEQ() {
    local MAJOR_A=0
    local MINOR_A=0
    local PATCH_A=0
    local SPECIAL_A=0

    local MAJOR_B=0
    local MINOR_B=0
    local PATCH_B=0
    local SPECIAL_B=0

    semverParseInto $1 MAJOR_A MINOR_A PATCH_A SPECIAL_A
    semverParseInto $2 MAJOR_B MINOR_B PATCH_B SPECIAL_B

    if [ $MAJOR_A -ne $MAJOR_B ]; then
        return 1
    fi

    if [ $MINOR_A -ne $MINOR_B ]; then
        return 1
    fi

    if [ $PATCH_A -ne $PATCH_B ]; then
        return 1
    fi

    if [[ "_$SPECIAL_A" != "_$SPECIAL_B" ]]; then
        return 1
    fi


    return 0

}

function semverLT() {
    local MAJOR_A=0
    local MINOR_A=0
    local PATCH_A=0
    local SPECIAL_A=0

    local MAJOR_B=0
    local MINOR_B=0
    local PATCH_B=0
    local SPECIAL_B=0

    semverParseInto $1 MAJOR_A MINOR_A PATCH_A SPECIAL_A
    semverParseInto $2 MAJOR_B MINOR_B PATCH_B SPECIAL_B

    if [ $MAJOR_A -lt $MAJOR_B ]; then
        return 0
    fi

    if [[ $MAJOR_A -le $MAJOR_B  && $MINOR_A -lt $MINOR_B ]]; then
        return 0
    fi
    
    if [[ $MAJOR_A -le $MAJOR_B  && $MINOR_A -le $MINOR_B && $PATCH_A -lt $PATCH_B ]]; then
        return 0
    fi

    if [[ "_$SPECIAL_A"  == "_" ]] && [[ "_$SPECIAL_B"  == "_" ]] ; then
        return 1
    fi
    if [[ "_$SPECIAL_A"  == "_" ]] && [[ "_$SPECIAL_B"  != "_" ]] ; then
        return 1
    fi
    if [[ "_$SPECIAL_A"  != "_" ]] && [[ "_$SPECIAL_B"  == "_" ]] ; then
        return 0
    fi

    if [[ "_$SPECIAL_A" < "_$SPECIAL_B" ]]; then
        return 0
    fi

    return 1

}

function semverGT() {
    semverEQ $1 $2
    local EQ=$?

    semverLT $1 $2
    local LT=$?

    if [ $EQ -ne 0 ] && [ $LT -ne 0 ]; then
        return 0
    else
        return 1
    fi
}

# end inlined cloudflare/semver_bash

# https://stackoverflow.com/a/2990533/
function echoerr { echo "$@" 1>&2; }

function doStuffWithPython {
    $1 -m pip install pipx
    echo $1 -m pipx install vanilla-installer[gui]
    # $1 -m pipx install vanilla-installer[gui]
    echo "Installation complete. You can run the GUI by running \`vanilla-installer-gui\` or the CLI with \`vanilla-installer\`."
    exit 0
}

pythons=( $(which -a python python3) )

if (( ${#pythons[@]} == 0 )); then
    echo "Fatal error: Python is not installed. Get it from https://www.python.org/downloads or with your system package manager."
    exit 1
fi

for i in "${pythons[@]}"
do
	rawVersion=$($i -V 2>&1 | grep -Po '(?<=Python )(.+)')
    if [[ -z "$rawVersion" ]]
    then
        echoerr "Attention: Could not parse version data ($rawVersion) for Python installation @ '$i'. Skipping."
        continue
    fi
    
    MAJOR=0
    MINOR=0
    PATCH=0
    SPECIAL=""

    semverParseInto $rawVersion MAJOR MINOR PATCH SPECIAL

    if [ "$MAJOR" -lt "3" ]
    then
        echoerr "Skipping Python ($MAJOR.$MINOR.$PATCH) @ '$i' as it is not Python 3."
        continue
     elif [ "$MINOR" -lt "8" ]
    then
        echoerr "Skipping Python ($MAJOR.$MINOR.$PATCH) @ '$i' as only Python 3.8.1 onwards is supported."
        continue
     elif [ "$MINOR" -eq "8" ] && [ "$PATCH" -lt "1" ]
    then
        echoerr "Skipping Python ($MAJOR.$MINOR.$PATCH) @ '$i' as only Python 3.8.1 onwards is supported. This is Python 3.8 and that is not supported."
        continue
     elif [ "$MINOR" -ge "12" ]
    then
        echoerr "Skipping Python ($MAJOR.$MINOR.$PATCH) @ '$i' as Python 3.12 onwards is not supported."
        continue
    fi

    echo "Supported Python installation ($MAJOR.$MINOR.$PATCH) found at $i, beginning VI installation."
    doStuffWithPython $i
    exit $?

done
