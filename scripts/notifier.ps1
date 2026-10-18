param(
    [string]$Titulo = "AI Nexus Core",
    [string]$Mensaje = "Notificación del sistema",
    [string]$Tipo = "info"
)

try {
    # 1. Cargar librerías WinRT de Windows
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

    # 2. Plantilla XML de la notificación
    $template = @"
<toast>
    <visual>
        <binding template="ToastGeneric">
            <text>$Titulo</text>
            <text>$Mensaje</text>
        </binding>
    </visual>
</toast>
"@

    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml($template)
    $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)

    # 3. Usar el AppId oficial y registrado de PowerShell en Windows
    $appId = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId)
    $notifier.Show($toast)
    Write-Host "[OK] Notificación Toast enviada a Windows." -ForegroundColor Green
}
catch {
    # Fallback confiable si el centro de notificaciones de Windows está silenciado
    Add-Type -AssemblyName System.Windows.Forms
    $global:balloon = New-Object System.Windows.Forms.NotifyIcon
    $global:balloon.Icon = [System.Drawing.SystemIcons]::Information
    $global:balloon.BalloonTipTitle = $Titulo
    $global:balloon.BalloonTipText = $Mensaje
    $global:balloon.Visible = $true
    $global:balloon.ShowBalloonTip(4000)
    Write-Host "[OK] Notificación enviada por NotifyIcon (Fallback)." -ForegroundColor Yellow
}
