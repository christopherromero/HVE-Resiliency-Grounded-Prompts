<#
.SYNOPSIS
    Creates a resiliency assessment workspace for a microservice repository.

.DESCRIPTION
    Builds an assessment folder that mirrors the governed framework layout:

        <DestinationRoot>\<AssessmentName>
            .copilot\
            .copilot-tracking\
            .github\            (agents, prompts, instructions, skills)
            application-context\
            examples\
            grounding\
            prompts\
            source\             (the microservice code being assessed)
            tools\

    By default the framework content is pulled fresh from the specified branch of the
    HVE-Resiliency-Grounded-Prompts repository on GitHub. Use -UseLocalFramework to copy
    from the local clone that contains this script instead.

    The microservice code is copied from the supplied path into the source folder so
    assessment prompts and generated artifacts stay outside the customer repository.

.PARAMETER MicroservicePath
    Path to the microservice repository to assess. Prompted for when omitted.

.PARAMETER DestinationRoot
    Parent folder that will contain the new assessment folder. Prompted for when omitted.

.PARAMETER AssessmentName
    Name of the assessment folder created under DestinationRoot. Defaults to the
    microservice folder name.

.PARAMETER Branch
    Branch of the framework repository to pull. Defaults to the branch recorded in
    $script:DefaultBranch.

.PARAMETER RepositoryUrl
    Framework repository URL to clone. Defaults to the public HVE-Resiliency-Grounded-Prompts repository.

.PARAMETER UseLocalFramework
    Copy framework content from the local clone containing this script instead of cloning.

.PARAMETER SourceSubfolder
    Optional subfolder under source for the microservice code, for example customer-app.
    When omitted the code is copied directly into source.

.PARAMETER IncludeSourceGitFolder
    Copy the microservice .git folder into the assessment workspace. Excluded by default.

.PARAMETER ExcludeFromSource
    Directory names excluded while copying the microservice code.

.PARAMETER Force
    Allow writing into an existing, non-empty assessment folder.

.EXAMPLE
    .\New-AssessmentWorkspace.ps1

    Prompts for the microservice path and destination, then builds the workspace.

.EXAMPLE
    .\New-AssessmentWorkspace.ps1 -MicroservicePath C:\src\ocsp-subscriptionservice `
        -DestinationRoot "C:\Phase 2\phase2-repos\OCSP\Assessments" -Branch main

    Builds C:\Phase 2\phase2-repos\OCSP\Assessments\ocsp-subscriptionservice from the main branch.
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$MicroservicePath,

    [string]$DestinationRoot,

    [string]$AssessmentName,

    [string]$Branch,

    [string]$RepositoryUrl = 'https://github.com/christopherromero/HVE-Resiliency-Grounded-Prompts.git',

    [switch]$UseLocalFramework,

    [string]$SourceSubfolder,

    [switch]$IncludeSourceGitFolder,

    [string[]]$ExcludeFromSource = @('.git', 'target', 'node_modules', '.gradle', '.idea', 'bin', 'obj'),

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:DefaultBranch = 'feature/refined-context-and-schema'

# Framework content that must never be carried into a new assessment workspace.
$script:FrameworkExcludedDirectories = @('.git', 'source', '.copilot-tracking')

$script:ScaffoldDirectories = @(
    'source',
    '.copilot-tracking\research\handoffs',
    '.copilot-tracking\research\subagents',
    '.copilot-tracking\plans\handoffs',
    '.copilot-tracking\plans\logs',
    '.copilot-tracking\plans\reports',
    '.copilot-tracking\reviews\handoffs',
    '.copilot-tracking\changes\handoffs',
    '.copilot-tracking\details'
)

function Read-RequiredPath {
    param(
        [Parameter(Mandatory)][string]$Prompt,
        [switch]$MustExist
    )

    while ($true) {
        $value = (Read-Host -Prompt $Prompt).Trim().Trim('"')

        if ([string]::IsNullOrWhiteSpace($value)) {
            Write-Warning 'A value is required.'
            continue
        }

        if ($MustExist -and -not (Test-Path -LiteralPath $value -PathType Container)) {
            Write-Warning "Folder not found: $value"
            continue
        }

        return $value
    }
}

function Copy-Tree {
    param(
        [Parameter(Mandatory)][string]$Source,
        [Parameter(Mandatory)][string]$Destination,
        [string[]]$ExcludeDirectory = @(),
        [Parameter(Mandatory)][string]$Activity
    )

    $arguments = @($Source, $Destination, '/E', '/NFL', '/NDL', '/NJH', '/NJS', '/NP', '/R:1', '/W:1')

    if ($ExcludeDirectory.Count -gt 0) {
        $arguments += '/XD'
        foreach ($name in $ExcludeDirectory) {
            $arguments += (Join-Path -Path $Source -ChildPath $name)
        }
    }

    Write-Host "  $Activity" -ForegroundColor DarkGray
    & robocopy @arguments | Out-Null
    $code = $LASTEXITCODE

    # Robocopy exit codes below 8 report copy activity, not failure.
    if ($code -ge 8) {
        throw "robocopy failed with exit code $code while copying '$Source' to '$Destination'."
    }
}

function Get-FrameworkFromGit {
    param(
        [Parameter(Mandatory)][string]$Url,
        [Parameter(Mandatory)][string]$BranchName
    )

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'git was not found on PATH. Install Git or rerun with -UseLocalFramework.'
    }

    $temporaryRoot = Join-Path -Path ([System.IO.Path]::GetTempPath()) -ChildPath ("hve-assessment-" + [System.Guid]::NewGuid().ToString('N'))

    Write-Host "Cloning $Url (branch $BranchName)..." -ForegroundColor Cyan
    & git clone --depth 1 --single-branch --branch $BranchName $Url $temporaryRoot 2>&1 | Write-Verbose

    if ($LASTEXITCODE -ne 0) {
        if (Test-Path -LiteralPath $temporaryRoot) {
            Remove-Item -LiteralPath $temporaryRoot -Recurse -Force -ErrorAction SilentlyContinue
        }
        throw "git clone failed for branch '$BranchName'. Verify the branch name and your access to $Url, or rerun with -UseLocalFramework."
    }

    $revision = (& git -C $temporaryRoot rev-parse --short HEAD).Trim()

    return [pscustomobject]@{
        Path       = $temporaryRoot
        Branch     = $BranchName
        Revision   = $revision
        IsTemporary = $true
    }
}

function Get-FrameworkFromLocalClone {
    $frameworkRoot = Split-Path -Parent $PSScriptRoot

    if (-not (Test-Path -LiteralPath (Join-Path $frameworkRoot 'grounding') -PathType Container)) {
        throw "Local framework root '$frameworkRoot' does not contain a grounding folder. Run the script from the tools folder of a framework clone."
    }

    $branchName = 'local-working-tree'
    $revision = 'n/a'

    if (Get-Command git -ErrorAction SilentlyContinue) {
        $detectedBranch = (& git -C $frameworkRoot rev-parse --abbrev-ref HEAD 2>$null)
        if ($LASTEXITCODE -eq 0 -and $detectedBranch) {
            $branchName = $detectedBranch.Trim()
            $revision = (& git -C $frameworkRoot rev-parse --short HEAD 2>$null).Trim()
        }
    }

    return [pscustomobject]@{
        Path        = $frameworkRoot
        Branch      = $branchName
        Revision    = $revision
        IsTemporary = $false
    }
}

Write-Host ''
Write-Host 'HVE resiliency assessment workspace builder' -ForegroundColor Cyan
Write-Host '-------------------------------------------' -ForegroundColor Cyan

if ([string]::IsNullOrWhiteSpace($MicroservicePath)) {
    $MicroservicePath = Read-RequiredPath -Prompt 'Path to the microservice repository to assess' -MustExist
}

if (-not (Test-Path -LiteralPath $MicroservicePath -PathType Container)) {
    throw "Microservice path not found: $MicroservicePath"
}

$microserviceRoot = (Resolve-Path -LiteralPath $MicroservicePath).ProviderPath

if ([string]::IsNullOrWhiteSpace($AssessmentName)) {
    $AssessmentName = Split-Path -Leaf $microserviceRoot
}

if ([string]::IsNullOrWhiteSpace($DestinationRoot)) {
    $DestinationRoot = Read-RequiredPath -Prompt "Parent folder for the new assessment folder '$AssessmentName'"
}

$DestinationRoot = $DestinationRoot.Trim().Trim('"')
$assessmentRoot = [System.IO.Path]::GetFullPath((Join-Path -Path $DestinationRoot -ChildPath $AssessmentName))

if ($assessmentRoot.TrimEnd('\') -eq $microserviceRoot.TrimEnd('\')) {
    throw 'The assessment folder cannot be the microservice folder. Choose a destination outside the customer repository.'
}

if ($microserviceRoot.TrimEnd('\').StartsWith($assessmentRoot.TrimEnd('\') + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'The microservice folder cannot live inside the assessment folder being created.'
}

if ((Test-Path -LiteralPath $assessmentRoot -PathType Container) -and -not $Force) {
    $existing = Get-ChildItem -LiteralPath $assessmentRoot -Force | Select-Object -First 1
    if ($existing) {
        throw "Assessment folder '$assessmentRoot' already exists and is not empty. Rerun with -Force to write into it."
    }
}

if ([string]::IsNullOrWhiteSpace($Branch)) {
    $Branch = $script:DefaultBranch
}

$sourceTarget = Join-Path -Path $assessmentRoot -ChildPath 'source'
if (-not [string]::IsNullOrWhiteSpace($SourceSubfolder)) {
    $sourceTarget = Join-Path -Path $sourceTarget -ChildPath $SourceSubfolder.Trim().Trim('\', '/')
}

$sourceExclusions = @($ExcludeFromSource | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
if ($IncludeSourceGitFolder) {
    $sourceExclusions = @($sourceExclusions | Where-Object { $_ -ne '.git' })
}

Write-Host ''
Write-Host "Microservice : $microserviceRoot"
Write-Host "Assessment   : $assessmentRoot"
Write-Host "Source target: $sourceTarget"
Write-Host ("Framework    : " + $(if ($UseLocalFramework) { 'local clone' } else { "$RepositoryUrl ($Branch)" }))
Write-Host ''

if (-not $PSCmdlet.ShouldProcess($assessmentRoot, 'Create resiliency assessment workspace')) {
    return
}

$framework = $null

try {
    $framework = if ($UseLocalFramework) { Get-FrameworkFromLocalClone } else { Get-FrameworkFromGit -Url $RepositoryUrl -BranchName $Branch }

    New-Item -ItemType Directory -Path $assessmentRoot -Force | Out-Null

    Write-Host 'Copying framework content...' -ForegroundColor Cyan
    Copy-Tree -Source $framework.Path -Destination $assessmentRoot `
        -ExcludeDirectory $script:FrameworkExcludedDirectories `
        -Activity "framework -> $assessmentRoot"

    Write-Host 'Creating tracking scaffolding...' -ForegroundColor Cyan
    foreach ($relative in $script:ScaffoldDirectories) {
        New-Item -ItemType Directory -Path (Join-Path -Path $assessmentRoot -ChildPath $relative) -Force | Out-Null
    }

    Write-Host 'Copying microservice code...' -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $sourceTarget -Force | Out-Null
    Copy-Tree -Source $microserviceRoot -Destination $sourceTarget `
        -ExcludeDirectory $sourceExclusions `
        -Activity "microservice -> $sourceTarget"
}
finally {
    if ($null -ne $framework -and $framework.IsTemporary -and (Test-Path -LiteralPath $framework.Path)) {
        Remove-Item -LiteralPath $framework.Path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$copiedFileCount = (Get-ChildItem -LiteralPath $sourceTarget -Recurse -File -Force | Measure-Object).Count

Write-Host ''
Write-Host 'Assessment workspace created.' -ForegroundColor Green
Write-Host "  Workspace        : $assessmentRoot"
Write-Host "  Framework branch : $($framework.Branch) ($($framework.Revision))"
Write-Host "  Source files     : $copiedFileCount"
if ($sourceExclusions.Count -gt 0) {
    Write-Host "  Source excludes  : $($sourceExclusions -join ', ')"
}
Write-Host ''
Write-Host 'Next steps:' -ForegroundColor Cyan
Write-Host "  1. Open '$assessmentRoot' as the VS Code workspace root."
Write-Host '  2. Set the application name in application-context\assessment-context.md.'
Write-Host '  3. Prepare application-context\application-architecture-context.yml from the templates.'
Write-Host '  4. Configure application-context\assessment-scope-context.yml, then run the Step 1 inventory prompt.'
Write-Host ''
