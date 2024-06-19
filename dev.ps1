# Path to your Python scripts
$C2_SCRIPT = "central-server.py"
$BEACON_SCRIPT = "beacon.py"

# Start the central C2 script in a new PowerShell window
Write-Output "Starting the central C2 server..."
Start-Process powershell -ArgumentList "Start-Process python -ArgumentList '$C2_SCRIPT' -NoNewWindow -Wait; Read-Host 'Press Enter to exit'"

# Wait for a few seconds to ensure the C2 server starts before starting beacons
Start-Sleep -Seconds 1

# Start the beacon scripts in new PowerShell windows
for ($i = 1; $i -le 3; $i++) {
    Write-Output "Starting beacon instance $i..."
    Start-Process powershell -ArgumentList "Start-Process python -ArgumentList '$BEACON_SCRIPT' -NoNewWindow -Wait; Read-Host 'Press Enter to exit'"
    Start-Sleep -Seconds 1
}

Write-Output "All beacons have been started."
