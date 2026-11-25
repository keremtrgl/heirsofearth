# Compiles Heirs of Earth against the installed game and Harmony.
$root = Join-Path (Split-Path $PSScriptRoot -Parent) 'HeirsOfEarth'
$managed = 'C:\Program Files (x86)\Steam\steamapps\common\RimWorld\RimWorldWin64_Data\Managed'
$harmony = 'C:\Program Files (x86)\Steam\steamapps\workshop\content\294100\2009463077\1.6\Assemblies\0Harmony.dll'
$sdk = (& dotnet --list-sdks | Select-Object -Last 1) -replace '^(\S+) \[(.+)\]$', '$2\$1'
$csc = Join-Path $sdk 'Roslyn\bincore\csc.dll'
$refs = 'mscorlib', 'System', 'System.Core', 'netstandard', 'Assembly-CSharp', 'UnityEngine', 'UnityEngine.CoreModule',
    'UnityEngine.IMGUIModule', 'UnityEngine.TextRenderingModule', 'UnityEngine.AudioModule' | ForEach-Object { "-r:$managed\$_.dll" }
New-Item -ItemType Directory -Force (Join-Path $root '1.6\Assemblies') | Out-Null
$sources = @(Get-ChildItem (Join-Path $root 'Source') -Filter *.cs -Recurse | ForEach-Object { $_.FullName })
& dotnet $csc -nologo -noconfig -nostdlib -target:library -langversion:9 -optimize+ -warn:3 "-out:$root\1.6\Assemblies\HeirsOfEarth.dll" @refs "-r:$harmony" @sources
"compile exit: $LASTEXITCODE"
exit $LASTEXITCODE
