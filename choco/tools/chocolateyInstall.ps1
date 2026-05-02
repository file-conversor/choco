# tools/chocolateyUninstall.ps1

$ErrorActionPreference = 'Stop'

$packageName = "file_conversor"
$version     = "v0.7.4" 
$toolsDir    = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$dir         = Join-Path ${env:ProgramFiles(x86)} "$packageName"
$url         = "https://github.com/file-conversor/file_conversor/releases/download/v0.7.4/file_conversor-v0.7.4-Win_x64-Installer.exe"
$checksum    = "3a6a7d672f6fc606bdc1d7b36da55724003f4cf94f55910aa6aa4e29ff733a26"  # SHA256

Write-Output "Installing app ..."
Install-ChocolateyPackage -PackageName $packageName `
    -FileType "exe" `
    -SilentArgs "/DIR=`"$dir`" /ALLUSERS /SUPPRESSMSGBOXES /VERYSILENT /NORESTART /SP-" `
    -Url $url `
    -Checksum $checksum `
    -ChecksumType "sha256"

Write-Output "Installing shim ..."
$exePath = Join-Path $dir "file_conversor.bat"
Install-BinFile -Name "file_conversor" -Path $exePath