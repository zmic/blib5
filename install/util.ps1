function get-blender-python-executable
{
    if ($islinux)
    {
        '~/.local/share/blender-5.1.1-linux-x64/5.1/python/bin/python3.13'
    }
    elseif ($iswindows)
    {

    }
    elseif ($macos)
    {

    }
}

function get-blender-executable
{
    if ($islinux)
    {
        '~/.local/share/blender-5.1.1-linux-x64/blender-launcher'
    }
    elseif ($iswindows)
    {

    }
    elseif ($macos)
    {

    }
}
