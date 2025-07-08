## GitHub Copilot Chat

- Extension Version: 0.28.5 (prod)
- VS Code: vscode/1.101.2
- OS: Windows

## Network

User Settings:
```json
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 20.233.83.146 (65 ms)
- DNS ipv6 Lookup: Error (66 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (19 ms)
- Electron fetch (configured): HTTP 200 (238 ms)
- Node.js https: HTTP 200 (254 ms)
- Node.js fetch: HTTP 200 (471 ms)
- Helix fetch: HTTP 200 (470 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.113.21 (65 ms)
- DNS ipv6 Lookup: Error (37 ms): getaddrinfo ENOTFOUND api.individual.githubcopilot.com
- Proxy URL: None (14 ms)
- Electron fetch (configured): HTTP 200 (792 ms)
- Node.js https: HTTP 200 (764 ms)
- Node.js fetch: HTTP 200 (667 ms)
- Helix fetch: HTTP 200 (695 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).