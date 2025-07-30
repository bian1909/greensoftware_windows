; ====================================================
; INSTALADOR DEFINITIVO - GreenSoftwareMonitor
; Versión optimizada para PyInstaller + Wine
; ====================================================

[Setup]
; --- Identificación única ---
AppId={{B3A1F2D4-5C6E-4A8B-9D7C-1E3F5A9B8D0E}
AppName=GreenSoftwareMonitor
AppVersion=1.0.0
AppVerName=GreenSoftwareMonitor 1.0
AppPublisher=UTN FRRE
AppPublisherURL=https://www.frre.utn.edu.ar
AppCopyright=Copyright © 2025 UTN FRRE
VersionInfoVersion=1.0.0
VersionInfoCompany=UTN FRRE

; --- Configuración de instalación ---
DefaultDirName={autopf}\GreenSoftwareMonitor
DefaultGroupName=GreenSoftwareMonitor
UninstallDisplayName=GreenSoftwareMonitor
UninstallDisplayIcon={app}\GreenSoftwareMonitor.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.\Installer
OutputBaseFilename=GreenSoftwareMonitor_Setup
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
ChangesEnvironment=no

; --- Apariencia ---
SetupIconFile=assets\icono.ico
WizardImageFile=assets\installer_banner.bmp
WizardSmallImageFile=assets\installer_logo.bmp
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=auto
DisableProgramGroupPage=auto

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; --- Todos los archivos principales (EXE, DLLs, _internal, etc.) ---
Source: "dist\GreenSoftwareMonitor\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
; --- Recursos ---
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs
Source: "fonts\*"; DestDir: "{app}\fonts"; Flags: ignoreversion

[Icons]
; --- Menú Inicio ---
Name: "{group}\GreenSoftwareMonitor"; Filename: "{app}\GreenSoftwareMonitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icono.ico"

; --- Escritorio ---
Name: "{commondesktop}\GreenSoftwareMonitor"; Filename: "{app}\GreenSoftwareMonitor.exe"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\assets\icono.ico"

; --- Desinstalador ---
Name: "{group}\Desinstalar GreenSoftwareMonitor"; Filename: "{uninstallexe}"

[Run]
; --- Ejecución post-instalación ---
Filename: "{app}\GreenSoftwareMonitor.exe"; Description: "{cm:LaunchProgram,GreenSoftwareMonitor}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; --- Limpieza durante desinstalación ---
Filename: "{cmd}"; Parameters: "/C taskkill /im GreenSoftwareMonitor.exe /f /t"; Flags: runhidden

[Code]
procedure InitializeWizard();
begin
  // Ajuste de tamaño para alta resolución
  WizardForm.Bevel.Width := ScaleX(500);
  WizardForm.Bevel.Height := ScaleY(50);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  // Verificación opcional de requisitos
  if CurStep = ssPostInstall then begin
    if not IsWin64 then
      MsgBox('Esta aplicación funciona mejor en sistemas de 64-bit', mbInformation, MB_OK);
  end;
end;

function InitializeSetup(): Boolean;
begin
  // Verificar si ya está instalado
  if RegKeyExists(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1') then
  begin
    if MsgBox('GreenSoftwareMonitor ya está instalado. ¿Desea reinstalarlo?', mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
      Exit;
    end;
  end;
  Result := True;
end;
