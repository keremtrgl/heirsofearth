param([switch]$CompileOnly, [switch]$Upload, [switch]$Media, [switch]$Description, [switch]$Portraits, [string]$Only)
$project = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$game = 'C:\Program Files (x86)\Steam\steamapps\common\RimWorld'
$managed = "$game\RimWorldWin64_Data\Managed"
$harmony = 'C:\Program Files (x86)\Steam\steamapps\workshop\content\294100\2009463077\1.6\Assemblies\0Harmony.dll'
$here = $PSScriptRoot
$out = "$here\build"
New-Item -ItemType Directory -Force $out | Out-Null
$sdk = (& dotnet --list-sdks | Select-Object -Last 1) -replace '^(\S+) \[(.+)\]$', '$2\$1'
$refs = 'mscorlib', 'System', 'System.Core', 'netstandard', 'Assembly-CSharp', 'UnityEngine', 'UnityEngine.CoreModule', 'UnityEngine.IMGUIModule', 'UnityEngine.TextRenderingModule', 'UnityEngine.AudioModule', 'UnityEngine.ImageConversionModule', 'com.rlabrecque.steamworks.net' | ForEach-Object { "-r:$managed\$_.dll" }
& dotnet "$sdk\Roslyn\bincore\csc.dll" -nologo -noconfig -nostdlib -target:library -langversion:9 -warn:1 "-out:$out\HeProbe.dll" @refs "-r:$harmony" "-r:$project\HeirsOfEarth\1.6\Assemblies\HeirsOfEarth.dll" "$here\Source\Probe.cs" "$here\Source\ProbeRun.cs" "$here\Source\Probe10.cs" "$here\Source\Probe21.cs" "$here\Source\Probe30.cs" "$here\Source\Probe31.cs" "$here\Source\Probe32.cs" "$here\Source\Probe33.cs" "$here\Source\Probe34.cs" "$here\Source\Probe35.cs" "$here\Source\Probe36.cs" "$here\Source\Probe37.cs" "$here\Source\Probe40.cs" "$here\Source\Probe41.cs" "$here\Source\Probe42.cs" "$here\Source\Probe43.cs" "$here\Source\Probe43b.cs" "$here\Source\Probe43c.cs" "$here\Source\ProbeArt.cs" "$here\Source\Upload.cs"
"probe compile exit: $LASTEXITCODE"
if ($LASTEXITCODE -ne 0 -or $CompileOnly) { exit $LASTEXITCODE }

if (Get-Process RimWorldWin64 -ErrorAction SilentlyContinue) { 'GAME RUNNING - aborted'; exit 1 }
robocopy "$project\HeirsOfEarth" "$game\Mods\HeirsOfEarth" /MIR /XD Source /NFL /NDL /NJH /NJS /NP | Out-Null
# 4.2.1: robocopy once kept an older HeirsOfEarth.dll of the same size in the game folder, so the assembly is copied outright and checked.
$dll = "$project\HeirsOfEarth\1.6\Assemblies\HeirsOfEarth.dll"
Copy-Item $dll "$game\Mods\HeirsOfEarth\1.6\Assemblies\HeirsOfEarth.dll" -Force
if ((Get-FileHash $dll).Hash -ne (Get-FileHash "$game\Mods\HeirsOfEarth\1.6\Assemblies\HeirsOfEarth.dll").Hash) { 'DLL COPY MISMATCH - aborted'; exit 1 }
"deployed dll: " + (Get-FileHash $dll).Hash.Substring(0, 12)
"installed version: " + ([xml](Get-Content -LiteralPath "$game\Mods\HeirsOfEarth\About\About.xml" -Encoding UTF8)).ModMetaData.modVersion
$test = "$game\Mods\HeProbeTest"
try {
    New-Item -ItemType Directory -Force "$test\About", "$test\1.6\Assemblies" | Out-Null
    [IO.File]::WriteAllText("$test\About\About.xml", '<?xml version="1.0" encoding="utf-8"?><ModMetaData><name>HE probe</name><author>test</author><packageId>he.probe</packageId><supportedVersions><li>1.6</li></supportedVersions><description>Temporary.</description><loadAfter><li>kerem.heirs</li></loadAfter></ModMetaData>')
    Copy-Item "$out\HeProbe.dll" "$test\1.6\Assemblies\HeProbe.dll"
    $work = Join-Path $env:LOCALAPPDATA "HeirsProbe"
    New-Item -ItemType Directory -Force $work | Out-Null
    $data = "$work\savedata"
    if (Test-Path $data) { Remove-Item -Recurse -Force $data }
    New-Item -ItemType Directory -Force "$data\Config" | Out-Null
    $version = (Get-Content "$game\Version.txt" -TotalCount 1).Trim()
    $utf8 = [Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText("$data\Config\ModsConfig.xml", "<?xml version=`"1.0`" encoding=`"utf-8`"?><ModsConfigData><version>$version</version><activeMods><li>brrainz.harmony</li><li>ludeon.rimworld</li><li>kerem.heirs</li><li>he.probe</li></activeMods><knownExpansions /></ModsConfigData>", $utf8)
    $lang = (Get-ChildItem "$game\Data\Core\Languages" | Where-Object { $_.Name -like 'Turkish*' } | Select-Object -First 1).BaseName
    [IO.File]::WriteAllText("$data\Config\Prefs.xml", "<?xml version=`"1.0`" encoding=`"utf-8`"?><PrefsData><langFolderName>$lang</langFolderName><devMode>false</devMode><runInBackground>true</runInBackground></PrefsData>", $utf8)
    "lang: $lang"
    $log = "$work\probe.log"
    if (Test-Path $log) { Remove-Item $log }
    if ($Upload -or $Media -or $Description) { $env:HE_UPLOAD_DIR = "$project\workshop\Heirs_Steam" } else { Remove-Item Env:HE_UPLOAD_DIR -ErrorAction SilentlyContinue }
    if ($Description) { $env:HE_UPLOAD_MODE = "description" } elseif ($Media) { $env:HE_UPLOAD_MODE = "media" } else { Remove-Item Env:HE_UPLOAD_MODE -ErrorAction SilentlyContinue }
    if ($Portraits) { $env:HE_PORTRAIT_DIR = "$work\portraits"; if (Test-Path "$work\portraits") { Remove-Item -Recurse -Force "$work\portraits" } } else { Remove-Item Env:HE_PORTRAIT_DIR -ErrorAction SilentlyContinue }
    if ($Only) { $env:HE_PORTRAIT_ONLY = $Only } else { Remove-Item Env:HE_PORTRAIT_ONLY -ErrorAction SilentlyContinue }
    $p = Start-Process "$game\RimWorldWin64.exe" -ArgumentList "-savedatafolder=`"$data`"", '-quicktest', '-logfile', "`"$log`"", '-popupwindow', '-screen-width', '1280', '-screen-height', '720' -WorkingDirectory $game -PassThru
    if (-not $p.WaitForExit(2400000)) { 'TIMEOUT - stopping test instance'; Stop-Process -Id $p.Id -Force }
    Start-Sleep -Seconds 2
    "exit: $($p.ExitCode)"
}
finally {
    if (Test-Path $test) { Remove-Item -Recurse -Force $test }
    Remove-Item Env:HE_UPLOAD_DIR -ErrorAction SilentlyContinue
    Remove-Item Env:HE_UPLOAD_MODE -ErrorAction SilentlyContinue
    Remove-Item Env:HE_PORTRAIT_DIR -ErrorAction SilentlyContinue
    Remove-Item Env:HE_PORTRAIT_ONLY -ErrorAction SilentlyContinue
}
$published = "$game\Mods\HeirsOfEarth\About\PublishedFileId.txt"
if (Test-Path $published) { Copy-Item $published "$project\HeirsOfEarth\About\PublishedFileId.txt" -Force; "published id: " + (Get-Content $published) }
if (Test-Path $log) {
    $lines = [IO.File]::ReadAllLines($log)
    "log lines: $($lines.Count)"
    $lines | Where-Object { $_ -match '^HETEST' } | Select-Object -First 200
}
Copy-Item $log "$here\probe.log" -Force -ErrorAction SilentlyContinue

