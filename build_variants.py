from apkmirror import Version
from utils import patch_apk


def build_apks(latest_version: Version):
    # patch
    apk = "big_file_merged.apk"
    integrations = "bins/integrations.apk"
    patches = "bins/patches.jar"
    cli = "bins/cli.jar"

    common_includes = [
        "Disable chirp font",
        "Hook feature flag",
        "Enable PiP mode automatically",
        "Download patch",
        "Enable Reader Mode",
        "Add ability to copy media link",
        "Remove \"Revisit Bookmark\" Banner",
        "Remove message prompts Banner",
        "Remove Ads",
        "Remove \"Creators to subscribe\" Banner",
        "Remove \"Pinned posts by followers\" Banner",
        "Remove Google Ads",
        "Hide Promoted Trends",
        "Show poll results",
        "Hide promote button",
        "Force enable translate",
        "Delete from database",
        "Remove premium upsell",
        "Disable auto timeline scroll on launch",
        "Hide FAB",
        "Custom downloader",
        "Selectable Text",
        "Control video auto scroll",
        "Customize Navigation Bar items",
        "Customize profile tabs",
        "Customize side bar items",
        "Customize timeline top bar",
        "Customize reply sort filter",
        "Custom download folder",
        "Clear tracking params",
        "Open browser chooser on opening links",
        "Custom translator",
        "Enable PiP mode automatically",
        "Enable Undo Posts",
        "Hide Banner",
        "Custom downloader",
        "Hide Promoted Trends",
        "Remove main event",
        "Remove superhero event",
        "Customize explore tabs",
    ]

    patch_apk(
        cli,
        integrations,
        patches,
        apk,
        includes=common_includes,
        out=f"x-piko-material-you-piko-v{latest_version.version}.apk",
    )
