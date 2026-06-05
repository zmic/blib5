. $PSScriptRoot/util.ps1
$bp = get-blender-python-executable 

& $bp -m pip install scipy

$root_folder = Split-Path $PSScriptRoot -Parent
write-host "pushd package root folder"
pushd $root_folder/package
& $bp -m pip install -e .
popd



