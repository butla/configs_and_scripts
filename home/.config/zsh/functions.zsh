# Attach to a local Postgres container.
function pgclidocker()
{
    CONTAINER_PORT=$(docker ps | grep '\->5432' | python3 -c "import re; port = re.findall(r':(\d+)->5432', input())[0]; print(port)")
    pgcli -h localhost -p ${CONTAINER_PORT} -d postgres -U postgres
}

function toxac()
{
    for version in py36 py35 py34 py27; do
        if [ -d .tox/$version ]; then
            source .tox/$version/bin/activate
            break
        fi
    done
}

function virtualenv_for_folder_name()
{
    virtualenv_name=$(lsvirtualenv -b | grep $(basename $(pwd)))
    echo $virtualenv_name
}
#
# runs Vim with good Python completions
function v()
{
    if [[ $(virtualenv_for_folder_name) != "" ]]; then
        workon $(virtualenv_for_folder_name)
    else
        toxac
    fi

    PYTHON_PATH=$(pwd)
    # Some projects put the production code in an src directory.
    if [ -d src ]; then
        PYTHON_PATH=${PYTHON_PATH}:src
    fi
    PYTHONPATH=${PYTHON_PATH} vim $@
    # leaving the virtualenv
    deactivate
}

function windows-1250-to-utf-8()
{
    TEMP_FILE=temp_convertion_file
    iconv \
        -f windows-1250 \
        -t utf-8 \
        "$1" > $TEMP_FILE
    mv $TEMP_FILE "$1"
}

function upgrade()
{
    if [[ $(lsb_release -s -i) == 'Ubuntu' ]]; then
        echo "${bg[green]}---${reset_color}Looking for updates with apt${bg[green]}---${reset_color}"
        sudo apt update
        sudo apt upgrade
    else
        echo "${bg[green]}---${reset_color}Looking for updates with yay${bg[green]}---${reset_color}"
        yay -Syu;
    fi
    echo "${bg[green]}---${reset_color}Looking for updates with flatpak${bg[green]}---${reset_color}"
    flatpak update;
}

function record_voice()
{
    NAME=recording
    arecord -vv -fdat $NAME.wav
    ffmpeg -i $NAME.wav -acodec mp3 $NAME.mp3
    rm $NAME.wav
}

function say()
{
    clear
    # I know, it's a tortoise, ugh :) Upstream problems
    cowsay -f turtle "$@" | lolcat --freq 0.2 --seed 900 --speed 300 --animate
}
