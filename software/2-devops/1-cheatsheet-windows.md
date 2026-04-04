# Quick Reference — Windows (PowerShell)

Native PowerShell equivalents for the Linux cheatsheet. Docker and Kubernetes commands are the same on all platforms — only the shell/OS commands differ.

---

## Files and navigation

```powershell
Get-ChildItem -Force                          # list with hidden files (alias: ls, dir)
Get-ChildItem -Recurse -Depth 2               # visual directory tree
Get-ChildItem -Recurse -Filter "*.yaml"       # find files by name
Select-String -Path *.* -Pattern "error" -Recurse   # search content recursively (alias: sls)
(Get-Content file.txt).Count                  # count lines
Get-ChildItem -Directory | ForEach-Object { "{0}`t{1:N2} MB" -f $_.Name, ((Get-ChildItem $_ -Recurse | Measure-Object Length -Sum).Sum / 1MB) }  # size of each subdirectory
Get-PSDrive -PSProvider FileSystem            # disk usage per drive
```

## Text processing

```powershell
(Select-String -Path app.log -Pattern "error").Count                          # count error lines
Get-Content file.txt | Sort-Object | Group-Object | Sort-Object Count -Descending | Select-Object -First 10  # top 10 most frequent lines
Get-Content file.txt | ForEach-Object { ($_ -split '\s+')[0,2] -join ' ' }   # print columns 1 and 3
(Get-Content file.txt) -replace 'old', 'new'                                  # replace text
Get-Content C:\Windows\System32\drivers\etc\hosts | ForEach-Object { ($_ -split '\s+')[0] }  # split by delimiter, take field 1
```

## Processes

```powershell
Get-Process | Where-Object ProcessName -like "*nginx*"   # find a process
Stop-Process -Id <pid>                                    # graceful stop
Stop-Process -Id <pid> -Force                             # force kill
Get-NetTCPConnection -LocalPort 8080                      # what's using port 8080
Get-NetTCPConnection -State Listen                        # all listening TCP ports
```

## Networking

```powershell
Invoke-RestMethod http://localhost:8080                                    # HTTP request (parses JSON automatically)
(Invoke-WebRequest http://localhost:8080).StatusCode                       # just the status code
Resolve-DnsName google.com                                                # DNS lookup
Test-NetConnection -ComputerName host -Port 5432                          # test if TCP port is open
Test-Connection -Count 3 host                                             # basic connectivity (ping)
Get-NetIPAddress | Where-Object AddressFamily -eq "IPv4"                  # network interfaces
```

## Environment and scripting

```powershell
Get-ChildItem Env: | Sort-Object Name                    # all environment variables
$env:MY_VAR = "value"                                    # set variable (current session)
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("secret"))       # base64 encode
[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("c2VjcmV0")) # base64 decode
-join ((1..32) | ForEach-Object { [char](Get-Random -Min 33 -Max 126) }) # generate random password
```

## JSON processing

PowerShell has native JSON support — no need for `jq`:

```powershell
$data = Get-Content data.json | ConvertFrom-Json
$data.name                                               # extract a field
$data.items | Select-Object name, status                 # reshape objects
$data.items.id                                           # raw list of IDs
$data.items.Count                                        # count items in array

# With APIs — Invoke-RestMethod parses JSON automatically
$pods = kubectl get pods -o json | ConvertFrom-Json
$pods.items | ForEach-Object { "$($_.metadata.name) $($_.status.phase)" }
```

## Key paths

| Path | Purpose |
|---|---|
| `C:\Windows\System32\drivers\etc\hosts` | Local DNS overrides |
| `C:\Windows\System32\config` | System registry hives |
| `$env:USERPROFILE\.ssh\` | SSH keys and config |
| `$env:APPDATA` | Per-user app config |
| `$env:LOCALAPPDATA` | Per-user app cache/data |
| `$PROFILE` | PowerShell profile (like `.bashrc`) |

## Useful PowerShell tips

```powershell
# Aliases you already know
# ls    → Get-ChildItem
# cd    → Set-Location
# cat   → Get-Content
# curl  → Invoke-WebRequest (note: not the same as Linux curl)
# wget  → Invoke-WebRequest

# Pipe to clip for clipboard
kubectl get pods -o wide | clip

# Run as admin from a regular shell
Start-Process powershell -Verb RunAs

# Tail a file (like tail -f)
Get-Content app.log -Wait -Tail 20
```
