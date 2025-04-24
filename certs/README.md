# Local HTTPS Certificates

This directory contains local development certificates for HTTPS.

## Setup Instructions

1. Install mkcert:

   ```bash
   # Windows (using Chocolatey)
   choco install mkcert

   # Windows (using PowerShell)
   # 1. Download mkcert to your current directory
   $mkcertUrl = "https://github.com/FiloSottile/mkcert/releases/latest/download/mkcert-v1.4.4-windows-amd64.exe"
   Invoke-WebRequest -Uri $mkcertUrl -OutFile ".\mkcert.exe"

   # 2. Install the local CA
   .\mkcert -install

   # 3. Generate certificates
   .\mkcert localhost 127.0.0.1 ::1

   # 4. Move the generated certificates to the certs directory
   Move-Item -Path ".\localhost.pem" -Destination ".\certs\localhost.crt" -Force
   Move-Item -Path ".\localhost-key.pem" -Destination ".\certs\localhost.key" -Force

   # macOS (using Homebrew)
   brew install mkcert

   # Linux
   sudo apt install mkcert
   ```

2. Install the local CA:

   ```bash
   mkcert -install
   ```

3. Generate certificates for local development:

   ```bash
   mkcert localhost 127.0.0.1 ::1
   ```

4. Move the generated certificates to this directory:
   - `localhost.pem` -> `certs/localhost.crt`
   - `localhost-key.pem` -> `certs/localhost.key`

## Security Note

These certificates are for local development only. Never commit the actual certificate files to version control.
