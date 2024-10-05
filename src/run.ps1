. ".\shared\loader.ps1"

$host.ui.RawUI.WindowTitle = 'Atari Monk Cli'

$enteredCommand = Read-Host "Enter command"

if ($enteredCommand -eq "help") {
    ShowHelp
}
elseif ($enteredCommand -eq "runtools") {
    $commandsToRun = $scriptAssociations["runtools"].Commands
    RunCommands -commands $commandsToRun
}
else {
    $enteredParameters = Read-Host "Enter parameters (if any)"
    RunCommand -command $enteredCommand -parameters $enteredParameters
}
