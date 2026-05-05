if ($islinux)
{
    $bp = '~/.local/share/blender-5.1.1-linux-x64/5.1/python/bin/python3.13'
}
elseif ($iswindows)
{

}
elseif ($macos)
{

}


$package_root = Split-Path $PSScriptRoot -Parent
write-host "pushd package root folder"
pushd $package_root
& $bp -m pip install -e .
popd


