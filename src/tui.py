#!/usr/bin/env python3
"""
ZeroBrave TUI - Interactive Terminal User Interface.

Professional look with ASCII symbols and smooth animations.
"""

from dataclasses import dataclass
from typing import Callable
import json
import os
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich import box

# 3D ASCII Banner
BANNER = """[bold cyan]
 ███████╗███████╗██████╗  ██████╗ ██████╗ ██████╗  █████╗ ██╗   ██╗███████╗
 ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝
   ███╔╝ █████╗  ██████╔╝██║   ██║██████╔╝██████╔╝███████║██║   ██║█████╗  
  ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  
 ███████╗███████╗██║  ██║╚██████╔╝██████╔╝██║  ██║██║  ██║ ╚████╔╝ ███████╗
 ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝[/]
                    [bold yellow]Privacy-First Brave Configuration[/]
"""

# Categories with ASCII tags
CATEGORIES = [
    ("ai", "[AI]", "Disable AI Features", "Leo, Gemini, Lens, AI Writing", {
        "BraveAIChatEnabled": False,
        "HelpMeWriteSettings": 2,
        "GeminiSettings": 1,
        "GenAiDefaultSettings": 2,
        "GenAiLensOverlaySettings": 2,
        "GenAILocalFoundationalModelSettings": 1,
        "LensRegionSearchEnabled": False,
        "LensDesktopNTPSearchEnabled": False,
        "LensOverlaySettings": 1,
    }),
    ("privacy", "[PRIV]", "Block Tracking", "Cookies, Fingerprinting, WebRTC", {
        "BlockThirdPartyCookies": True,
        "PrivacySandboxFingerprintingProtectionEnabled": True,
        "PrivacySandboxPromptEnabled": False,
        "PrivacySandboxAdTopicsEnabled": False,
        "PrivacySandboxSiteEnabledAdsEnabled": False,
        "PrivacySandboxAdMeasurementEnabled": False,
        "WebRtcIPHandling": "disable_non_proxied_udp",
        "WebRtcEventLogCollectionAllowed": False,
    }),
    ("telemetry", "[TEL]", "Disable Telemetry", "Metrics, Reports, Feedback", {
        "MetricsReportingEnabled": False,
        "DeviceMetricsReportingEnabled": False,
        "UrlKeyedAnonymizedDataCollectionEnabled": False,
        "UrlKeyedMetricsAllowed": False,
        "CloudProfileReportingEnabled": False,
        "CloudReportingEnabled": False,
        "ReportExtensionsAndPluginsData": False,
        "ReportMachineIDData": False,
        "ReportPolicyData": False,
        "ReportUserIDData": False,
        "ReportVersionData": False,
        "UserFeedbackAllowed": False,
        "FeedbackSurveysEnabled": False,
    }),
    ("security", "[SEC]", "Enhanced Security", "Safe Browsing, Updates", {
        "SafeBrowsingProtectionLevel": 2,
        "SafeBrowsingExtendedReportingEnabled": False,
        "SafeBrowsingSurveysEnabled": False,
        "ComponentUpdatesEnabled": True,
    }),
    ("autofill", "[AUTO]", "Disable Autofill", "Passwords, Payments, Addresses", {
        "PaymentMethodQueryEnabled": False,
        "AutofillAddressEnabled": False,
        "AutofillCreditCardEnabled": False,
        "AutofillPredictionSettings": 2,
        "PasswordManagerEnabled": False,
        "PasswordLeakDetectionEnabled": False,
        "PasswordSharingEnabled": False,
    }),
    ("sync", "[SYNC]", "Disable Sync", "No Cloud, No Sign-in", {
        "SyncDisabled": True,
        "BrowserSignin": 0,
    }),
    ("perms", "[PERM]", "Block Permissions", "Location, Notifications, USB", {
        "DefaultGeolocationSetting": 2,
        "DefaultNotificationsSetting": 2,
        "DefaultWebBluetoothGuardSetting": 2,
        "DefaultWebUsbGuardSetting": 2,
        "DefaultFileSystemReadGuardSetting": 2,
        "DefaultFileSystemWriteGuardSetting": 2,
        "DefaultLocalFontsSetting": 2,
        "DefaultSensorsSetting": 2,
        "DefaultSerialGuardSetting": 2,
        "AutoplayAllowed": False,
    }),
    ("brave", "[BRAVE]", "Brave Specific", "Rewards, Wallet, VPN disabled", {
        "BraveRewardsDisabled": True,
        "BraveWalletDisabled": True,
        "BraveVPNDisabled": 1,
        "TorDisabled": True,
    }),
]


class TUI:
    """Professional TUI with animations for ZeroBrave."""
    
    def __init__(self, dry_run: bool = False, backup_callback: Callable = None, 
                 apply_callback: Callable = None):
        self.console = Console()
        self.dry_run = dry_run
        self.backup_callback = backup_callback
        self.apply_callback = apply_callback
        self.enabled = {cat[0]: True for cat in CATEGORIES}
    
    def clear(self):
        """Clear screen."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def animate_banner(self):
        """Animate the banner appearing."""
        # Print banner lines as plain text for animation
        banner_plain = """
 ███████╗███████╗██████╗  ██████╗ ██████╗ ██████╗  █████╗ ██╗   ██╗███████╗
 ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝
   ███╔╝ █████╗  ██████╔╝██║   ██║██████╔╝██████╔╝███████║██║   ██║█████╗  
  ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  
 ███████╗███████╗██║  ██║╚██████╔╝██████╔╝██║  ██║██║  ██║ ╚████╔╝ ███████╗
 ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝
                    Privacy-First Brave Configuration
"""
        for line in banner_plain.strip().split('\n'):
            self.console.print(f"[bold cyan]{line}[/]")
            time.sleep(0.04)
    
    def animate_intro(self):
        """Animate program startup."""
        self.clear()
        
        # Loading animation
        with Progress(
            SpinnerColumn("dots12"),
            TextColumn("[bold cyan]Initializing ZeroBrave...[/]"),
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            time.sleep(0.8)
        
        self.animate_banner()
        time.sleep(0.3)
    
    def animate_exit(self):
        """Animate program exit."""
        self.console.print()
        
        messages = [
            "[dim]Saving configuration...[/]",
            "[dim]Cleaning up...[/]",
            "[bold cyan]Goodbye![/]",
        ]
        
        for msg in messages:
            self.console.print(f"  {msg}")
            time.sleep(0.15)
        
        self.console.print()
        self.console.print(Panel(
            "[bold]Remember to restart Brave for changes to take effect![/]",
            border_style="cyan",
            box=box.ROUNDED,
        ))
        time.sleep(0.3)
    
    def build_policies(self) -> dict:
        """Build policies dict from enabled categories."""
        result = {}
        for key, tag, name, desc, policies in CATEGORIES:
            if self.enabled[key]:
                result.update(policies)
        return result
    
    def count_enabled(self) -> tuple[int, int]:
        """Count (enabled_categories, total_policies)."""
        enabled = sum(1 for k, v in self.enabled.items() if v)
        policies = sum(len(cat[4]) for cat in CATEGORIES if self.enabled[cat[0]])
        return enabled, policies
    
    def render_table(self):
        """Render the categories table."""
        table = Table(box=box.DOUBLE_EDGE, show_header=True, header_style="bold white")
        table.add_column("#", style="bold cyan", width=3, justify="center")
        table.add_column("Tag", style="bold", width=8)
        table.add_column("Status", width=8, justify="center")
        table.add_column("Category", width=20)
        table.add_column("Details", style="dim")
        
        for i, (key, tag, name, desc, policies) in enumerate(CATEGORIES, 1):
            if self.enabled[key]:
                status = "[bold green]++ ON[/]"
                tag_style = f"[cyan]{tag}[/]"
            else:
                status = "[dim red]-- OFF[/]"
                tag_style = f"[dim]{tag}[/]"
            
            table.add_row(str(i), tag_style, status, name, desc)
        
        return table
    
    def render(self, animate: bool = False):
        """Render the main screen."""
        self.clear()
        
        if animate:
            self.animate_banner()
        else:
            self.console.print(BANNER)
        
        enabled_cats, total_policies = self.count_enabled()
        
        # Status bar
        status_text = f"[bold]Categories: {enabled_cats}/8[/]  |  [bold]Policies: {total_policies}[/]"
        if self.dry_run:
            status_text = "[bold yellow]>> DRY-RUN MODE <<[/]  |  " + status_text
        
        self.console.print(Panel(status_text, box=box.MINIMAL))
        self.console.print()
        
        # Categories table
        self.console.print(self.render_table())
        self.console.print()
        
        # Commands
        cmd_panel = Panel(
            "[cyan]1-8[/] Toggle  |  "
            "[cyan]A[/] All ON/OFF  |  "
            "[cyan]P[/] Preview  |  "
            "[green]ENTER[/] Apply  |  "
            "[red]Q[/] Quit",
            title="[bold]Commands[/]",
            border_style="dim cyan",
            box=box.ROUNDED,
        )
        self.console.print(cmd_panel)
        self.console.print()
    
    def show_preview(self):
        """Show JSON preview with animation."""
        self.clear()
        self.console.print(BANNER)
        
        policies = self.build_policies()
        
        # Loading animation
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Generating preview..."),
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            time.sleep(0.5)
        
        json_str = json.dumps(policies, indent=2)
        
        self.console.print(Panel(
            f"[cyan]{json_str}[/]",
            title=f"[bold yellow]<< {len(policies)} Policies >>[/]",
            border_style="yellow",
            box=box.DOUBLE,
        ))
        self.console.print()
        input("Press ENTER to go back...")
    
    def apply(self):
        """Apply policies with progress animation."""
        policies = self.build_policies()
        _, total = self.count_enabled()
        
        self.console.print()
        
        if self.dry_run:
            self.console.print("[bold yellow]>> DRY-RUN: Simulating apply...[/]\n")
        
        # Progress animation
        with Progress(
            SpinnerColumn("dots"),
            TextColumn("[bold]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[bold cyan]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("Applying policies...", total=100)
            
            for i in range(100):
                time.sleep(0.015)
                progress.update(task, advance=1)
                
                if i == 30:
                    progress.update(task, description="Writing configuration...")
                elif i == 60:
                    progress.update(task, description="Validating policies...")
                elif i == 90:
                    progress.update(task, description="Finalizing...")
        
        if self.apply_callback:
            try:
                self.apply_callback(policies, self.dry_run)
                self.console.print()
                self.console.print(Panel(
                    "[bold green]>>> SUCCESS <<<[/]\n\n"
                    f"Applied [cyan]{total}[/] policies.\n"
                    "[dim]Restart Brave for changes to take effect.[/]",
                    border_style="green",
                    box=box.DOUBLE,
                ))
            except Exception as e:
                self.console.print(f"\n[bold red]ERROR:[/] {e}")
        else:
            self.console.print("\n[yellow]Note: No apply callback configured[/]")
        
        self.console.print()
        input("Press ENTER to continue...")
    
    def toggle_with_feedback(self, idx: int):
        """Toggle a category with visual feedback."""
        if 1 <= idx <= 8:
            key = CATEGORIES[idx - 1][0]
            tag = CATEGORIES[idx - 1][1]
            self.enabled[key] = not self.enabled[key]
            
            # Quick flash feedback
            status = "[green]ON[/]" if self.enabled[key] else "[red]OFF[/]"
            self.console.print(f"  {tag} -> {status}", highlight=False)
            time.sleep(0.1)
    
    def run(self):
        """Main loop."""
        # Intro animation
        self.animate_intro()
        time.sleep(0.2)
        
        first_render = False  # Already showed banner in intro
        
        while True:
            self.render(animate=first_render)
            first_render = False
            
            try:
                choice = input(">>> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                self.animate_exit()
                return
            
            if choice == 'q':
                self.animate_exit()
                return
            elif choice == 'p':
                self.show_preview()
            elif choice == '' or choice == 'enter':
                self.apply()
            elif choice == 'a':
                if any(self.enabled.values()):
                    self.enabled = {k: False for k in self.enabled}
                else:
                    self.enabled = {k: True for k in self.enabled}
            elif choice.isdigit():
                self.toggle_with_feedback(int(choice))


def run_tui(dry_run: bool = False, backup_callback: Callable = None, 
            apply_callback: Callable = None):
    """Entry point."""
    tui = TUI(dry_run=dry_run, backup_callback=backup_callback, 
              apply_callback=apply_callback)
    tui.run()


if __name__ == "__main__":
    run_tui(dry_run=True)
