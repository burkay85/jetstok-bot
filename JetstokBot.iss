#define AppName "Jetstok Trendyol Bot"
#define AppVersion "1.0.0"
#define AppPublisher "Cartiva"
#define AppExeName "JetstokBot_Launcher.exe"

[Setup]
AppId={{B7F2A8C0-7E81-4A6A-BB62-7F3E1D2A9A11}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={pf}\{#AppPublisher}\{#AppName}
DefaultGroupName={#AppPublisher}\{#AppName}
OutputDir=dist
OutputBaseFilename=JetstokBot_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "rules_defaults.py"; DestDir: "{app}"; Flags: onlyifdoesntexist

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"

[Run]
; Kurulum sırasında Chromium indir (tek sefer) -- launcher.py '--prepare' destekli olmalı
Filename: "{app}\{#AppExeName}"; Parameters: "--prepare"; StatusMsg: "Chromium indiriliyor..."; Flags: waituntilterminated
; Kurulum bitince uygulamayı aç
Filename: "{app}\{#AppExeName}"; Description: "Uygulamayı şimdi başlat"; Flags: nowait postinstall skipifsilent

[Code]
var
  P: String;
procedure CurStepChanged(CurStep: TSetupStep);
var
  F: Integer; S: String;
begin
  if CurStep = ssInstall then begin
    P := ExpandConstant('{app}\.env');
    S :=
      'PANEL_URL=https://app.jetstok.com'#13#10 +
      'LIST_URL=https://app.jetstok.com/products-2/not-live'#13#10 +
      'EMAIL='#13#10 +
      'PASSWORD='#13#10 +
      'HEADLESS=0'#13#10;
    F := FileCreate(P);
    if F <> -1 then begin
      FileWrite(F, S, Length(S)); FileClose(F);
    end;
  end;
end;
