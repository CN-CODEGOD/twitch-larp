$ErrorActionPreference = 'Stop'

$userChannelId = '555862343'

if (-not (Get-Command twitch.exe -ErrorAction SilentlyContinue)) {
    throw 'twitch.exe was not found in PATH. Install the Twitch CLI and try again.'
}

$followedResponse = & twitch.exe api get channels followed -q "user_id=$userChannelId" 2>$null

if (-not $followedResponse) {
    Write-Host 'No followed channels returned.'
    exit 0
}

$followed = $followedResponse | ConvertFrom-Json
$logins = @($followed.data | Where-Object { $_.broadcaster_login } | Select-Object -ExpandProperty broadcaster_login)

if (-not $logins -or $logins.Count -eq 0) {
    Write-Host 'No followed channels found.'
    exit 0
}

$query = ($logins | ForEach-Object { "user_login=$_" }) -join '&'
& twitch.exe api get streams -q $query
