# Checks the mod's XML against the real game classes without launching the game.
param([string]$ModRoot = (Join-Path (Split-Path $PSScriptRoot -Parent) 'HeirsOfEarth'))

$game = 'C:\Program Files (x86)\Steam\steamapps\common\RimWorld'
$managed = Join-Path $game 'RimWorldWin64_Data\Managed'
$script:problems = New-Object System.Collections.ArrayList
function Add-Problem([string]$text) { [void]$script:problems.Add($text) }

[AppDomain]::CurrentDomain.add_ReflectionOnlyAssemblyResolve({
    param($s, $e)
    $n = (New-Object Reflection.AssemblyName $e.Name).Name
    $p = Join-Path $managed "$n.dll"
    if ($n -eq '0Harmony') { $p = 'C:\Program Files (x86)\Steam\steamapps\workshop\content\294100\2009463077\1.6\Assemblies\0Harmony.dll' }
    if (Test-Path $p) { [Reflection.Assembly]::ReflectionOnlyLoadFrom($p) } else { [Reflection.Assembly]::ReflectionOnlyLoad($e.Name) }
})
$harmonyPath = 'C:\Program Files (x86)\Steam\steamapps\workshop\content\294100\2009463077\1.6\Assemblies\0Harmony.dll'
[void][Reflection.Assembly]::ReflectionOnlyLoadFrom($harmonyPath)
$gameAsm = [Reflection.Assembly]::ReflectionOnlyLoadFrom((Join-Path $managed 'Assembly-CSharp.dll'))
$modBytesPath = Join-Path $ModRoot '1.6\Assemblies\HeirsOfEarth.dll'
$modAsm = [Reflection.Assembly]::ReflectionOnlyLoadFrom($modBytesPath)

$types = @{}
foreach ($asm in @($gameAsm, $modAsm)) {
    try { $all = $asm.GetTypes() } catch [Reflection.ReflectionTypeLoadException] { $all = $_.Exception.Types }
    foreach ($t in $all) {
        if ($null -eq $t) { continue }
        $types[$t.FullName] = $t
        if (-not $types.ContainsKey($t.Name)) { $types[$t.Name] = $t }
    }
}

$defNames = New-Object 'System.Collections.Generic.HashSet[string]'
$abstractNames = New-Object 'System.Collections.Generic.HashSet[string]'
$xmlFiles = @(Get-ChildItem (Join-Path $game 'Data\Core\Defs') -Recurse -Filter *.xml) + @(Get-ChildItem (Join-Path $ModRoot 'Defs') -Recurse -Filter *.xml)
foreach ($f in $xmlFiles) {
    $doc = New-Object Xml.XmlDocument
    $doc.Load($f.FullName)
    foreach ($d in $doc.DocumentElement.ChildNodes) {
        if ($d.NodeType -ne 'Element') { continue }
        $name = $d.SelectSingleNode('defName')
        if ($name) { [void]$defNames.Add($name.InnerText.Trim()) }
        if ($d.GetAttribute('Name')) { [void]$abstractNames.Add($d.GetAttribute('Name')) }
    }
}

$flags = [Reflection.BindingFlags]'Public,NonPublic,Instance,DeclaredOnly'
function Find-Field($type, [string]$name) {
    $c = $type
    while ($null -ne $c) {
        $f = $c.GetField($name, $flags)
        if ($f) { return $f }
        # The game also loads a field from XML under any name given by a [LoadAlias] attribute (StorageSettings.priority).
        foreach ($cand in $c.GetFields($flags)) {
            foreach ($attr in $cand.GetCustomAttributesData()) {
                if ($attr.AttributeType.Name -eq 'LoadAliasAttribute' -and $attr.ConstructorArguments.Count -gt 0 -and $attr.ConstructorArguments[0].Value -eq $name) { return $cand }
            }
        }
        $c = $c.BaseType
    }
    return $null
}
function Test-IsDef($type) {
    $c = $type
    while ($null -ne $c) { if ($c.FullName -eq 'Verse.Def') { return $true }; $c = $c.BaseType }
    return $false
}
function Test-Value($type, $node, [string]$path) {
    if ($node.GetAttribute('IsNull') -eq 'True') { return }
    $cls = $node.GetAttribute('Class')
    if ($cls) {
        if (-not $types.ContainsKey($cls)) { Add-Problem "$path : unknown Class $cls"; return }
        $type = $types[$cls]
    }
    if ($type.FullName -eq 'System.Type') {
        if (-not $types.ContainsKey($node.InnerText.Trim())) { Add-Problem "$path : unknown type $($node.InnerText.Trim())" }
        return
    }
    if (Test-IsDef $type) {
        if ($node.GetAttribute('MayRequire')) { return }
        if (-not $defNames.Contains($node.InnerText.Trim())) { Add-Problem "$path : unknown def $($node.InnerText.Trim())" }
        return
    }
    if ($type.IsGenericType -and $type.GetGenericTypeDefinition().Name -eq 'List`1') {
        $item = $type.GetGenericArguments()[0]
        foreach ($c in $node.ChildNodes) {
            if ($c.NodeType -ne 'Element') { continue }
            if ($item.Name -in 'StatModifier', 'ThingDefCountClass', 'SkillRequirement', 'PawnGenOption', 'SkillGain' -and -not ($c.Name -eq 'li' -and @($c.ChildNodes | Where-Object { $_.NodeType -eq 'Element' }).Count -gt 0)) {
                if (-not $defNames.Contains($c.Name)) { Add-Problem "$path : unknown def $($c.Name)" }
            } elseif ($c.Name -ne 'li') {
                Add-Problem "$path : expected li, found $($c.Name)"
            } else {
                Test-Value $item $c "$path.li"
            }
        }
        return
    }
    if ($type.IsEnum) { return }
    $elements = @($node.ChildNodes | Where-Object { $_.NodeType -eq 'Element' })
    if ($elements.Count -eq 0) { return }
    foreach ($c in $elements) {
        $f = Find-Field $type $c.Name
        if (-not $f) { Add-Problem "$path : $($type.Name) has no field '$($c.Name)'"; continue }
        Test-Value $f.FieldType $c "$path.$($c.Name)"
    }
}

$texRoot = Join-Path $ModRoot 'Textures'
$injectable = @{}
foreach ($f in Get-ChildItem (Join-Path $ModRoot 'Defs') -Recurse -Filter *.xml) {
    $doc = New-Object Xml.XmlDocument
    $doc.Load($f.FullName)
    foreach ($d in $doc.DocumentElement.ChildNodes) {
        if ($d.NodeType -ne 'Element') { continue }
        # LocalName: PowerShell's .Name returns a Name="" attribute when one exists.
        $defClass = $d.LocalName
        if (-not $types.ContainsKey($defClass)) { Add-Problem "$($f.Name): unknown def class $defClass"; continue }
        $nameNode = $d.SelectSingleNode('defName')
        $defName = if ($nameNode) { $nameNode.InnerText } else { $d.GetAttribute('Name') }
        $parent = $d.GetAttribute('ParentName')
        if ($parent -and -not $abstractNames.Contains($parent)) { Add-Problem "$defName : unknown parent $parent" }
        foreach ($c in $d.ChildNodes) {
            if ($c.NodeType -ne 'Element') { continue }
            $field = Find-Field $types[$defClass] $c.LocalName
            if (-not $field) { Add-Problem "$defName : $defClass has no field '$($c.LocalName)'"; continue }
            Test-Value $field.FieldType $c "$defName.$($c.LocalName)"
        }
        foreach ($key in 'label', 'description', 'letterLabel', 'letterText') {
            if ($d.SelectSingleNode($key)) { $injectable["$defClass/$defName.$key"] = $true }
        }
        foreach ($p in $d.SelectNodes('.//texPath | .//texturePath | .//iconPath | .//expandingIconTexture | .//texture | .//uiIconPath | .//settlementTexturePath')) {
            $v = $p.InnerText.Trim()
            if ($v -like 'HeirsOfEarth/*' -and -not (Test-Path (Join-Path $texRoot "$v.png"))) { Add-Problem "$defName : missing texture $v" }
        }
        foreach ($p in $d.SelectNodes('factionIconPath')) {
            if (-not (Test-Path (Join-Path $texRoot "$($p.InnerText.Trim()).png"))) { Add-Problem "$defName : missing icon $($p.InnerText)" }
        }
    }
}

# Translation coverage
$langRoot = Join-Path $ModRoot 'Languages'
$turkish = Get-ChildItem $langRoot -Directory | Where-Object { $_.Name -like 'Turkish*' } | Select-Object -First 1
function Get-KeyedInfo($folder) {
    $info = @{}
    foreach ($file in Get-ChildItem $folder -Filter *.xml) {
        $doc = New-Object Xml.XmlDocument; $doc.Load($file.FullName)
        foreach ($n in $doc.DocumentElement.ChildNodes) {
            if ($n.NodeType -ne 'Element') { continue }
            if ($info.ContainsKey($n.Name)) { Add-Problem "Duplicate key: $($n.Name)" }
            $info[$n.Name] = (@([regex]::Matches($n.InnerText, '\{(\d+)\}') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique) -join ',')
        }
    }
    return $info
}
$enInfo = Get-KeyedInfo (Join-Path $langRoot 'English\Keyed')
$trInfo = Get-KeyedInfo (Join-Path $turkish.FullName 'Keyed')
$enKeys = @($enInfo.Keys)
$trKeys = @($trInfo.Keys)
foreach ($k in $enKeys) {
    if (-not $trInfo.ContainsKey($k)) { Add-Problem "Turkish key missing: $k" }
    elseif ($enInfo[$k] -ne $trInfo[$k]) { Add-Problem "Placeholder mismatch: $k" }
}
foreach ($k in $trKeys) { if (-not $enInfo.ContainsKey($k)) { Add-Problem "English key missing: $k" } }

$source = (Get-ChildItem (Join-Path $ModRoot 'Source') -Filter *.cs -Recurse | ForEach-Object { [IO.File]::ReadAllText($_.FullName) }) -join "`n"
$used = New-Object 'System.Collections.Generic.HashSet[string]'
foreach ($m in [regex]::Matches($source, '"(HE_[A-Za-z0-9]+)"\.Translate')) { [void]$used.Add($m.Groups[1].Value) }
foreach ($s in 'Heritage', 'Knowledge', 'Diplomacy', 'Traditions', 'Stories', 'Chronicle') { [void]$used.Add("HE_Tab$s") }
foreach ($k in 'Envoy', 'Tribute', 'WarCall', 'Marriage', 'Mediation') { foreach ($suffix in 'Label', 'Text', 'Accept', 'Refuse') { [void]$used.Add("HE_$k$suffix") } }
foreach ($k in $used) { if (-not $enInfo.ContainsKey($k)) { Add-Problem "Key used in code but undefined: $k" } }

# DefOf fields must exist, in the right def class
$defClassByName = @{}
foreach ($f in Get-ChildItem (Join-Path $ModRoot 'Defs') -Recurse -Filter *.xml) {
    $doc = New-Object Xml.XmlDocument; $doc.Load($f.FullName)
    foreach ($d in $doc.DocumentElement.ChildNodes) {
        if ($d.NodeType -eq 'Element' -and $d.SelectSingleNode('defName')) { $defClassByName["$($d.LocalName -replace '^.*\.', '')/$($d.SelectSingleNode('defName').InnerText)"] = $true }
    }
}
foreach ($field in $types['HeirsOfEarth.HeirsDefOf'].GetFields()) {
    if (-not $defClassByName.ContainsKey("$($field.FieldType.Name)/$($field.Name)")) { Add-Problem "DefOf has no matching def: $($field.FieldType.Name) $($field.Name)" }
}

# Runtime-loaded assets
foreach ($m in [regex]::Matches($source, '"(HeirsOfEarth/[A-Za-z0-9_/]+)"')) {
    if (-not (Test-Path (Join-Path $texRoot "$($m.Groups[1].Value).png"))) { Add-Problem "Missing texture used by code: $($m.Groups[1].Value)" }
}

$injected = @{}
foreach ($f in Get-ChildItem (Join-Path $turkish.FullName 'DefInjected') -Recurse -Filter *.xml) {
    $doc = New-Object Xml.XmlDocument; $doc.Load($f.FullName)
    foreach ($n in $doc.DocumentElement.ChildNodes) {
        if ($n.NodeType -eq 'Element') { $injected["$($f.Directory.Name)/$($n.Name)"] = $true }
    }
}
foreach ($k in $injectable.Keys) { if (-not $injected.ContainsKey($k)) { Add-Problem "Turkish injection missing: $k" } }
foreach ($k in $injected.Keys) {
    if ($k -match '^[^/]+/[^.]+\.(label|description)$' -and -not $injectable.ContainsKey($k)) {
        Add-Problem "Turkish injection has no target: $k"
    }
}

foreach ($png in 'About\Preview.png', 'About\ModIcon.png') {
    if (-not (Test-Path (Join-Path $ModRoot $png))) { Add-Problem "Missing $png" }
}
"Checked defs: $($injectable.Count) text fields, keys: $($enKeys.Count), known game defs: $($defNames.Count)"
if ($script:problems.Count -eq 0) { 'RESULT: 0 problems' } else { "RESULT: $($script:problems.Count) problems"; $script:problems | Sort-Object -Unique }
