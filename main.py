from apkmirror import Version, Variant
from build_variants import build_apks
from download_bins import download_apkeditor, download_revanced_bins
import github
from utils import panic, merge_apk, publish_release
from download_bins import download_release_asset
import apkmirror
import os
import shutil
import zipfile


def get_latest_release(versions: list[Version]) -> Version | None:
    for i in versions:
        if i.version.find("release") >= 0:
            return i


def main():
    # get latest version
    url: str = "https://www.apkmirror.com/apk/x-corp/twitter/"
    repo_url: str = "MondayNitro/twitter-apk"

    versions = apkmirror.get_versions(url)

    latest_version = get_latest_release(versions)
    if latest_version is None:
        raise Exception("Could not find the latest version")

    # only continue if it's a release
    if latest_version.version.find("release") < 0:
        panic("Latest version is not a release version")

    last_build_version: github.GithubRelease | None = github.get_last_build_version(
        repo_url
    )

    if last_build_version is None:
        panic("Failed to fetch the latest build version")
        return

    # Begin stuff
    if last_build_version.tag_name != latest_version.version:
        print(f"New version found: {latest_version.version}")
    else:
        print("No new version found")
        return

    # get bundle and universal variant
    variants: list[Variant] = apkmirror.get_variants(latest_version)

    download_link: Variant | None = None
    for variant in variants:
        if variant.is_bundle and variant.arcithecture == "universal":
            download_link = variant
            break

    if download_link is None:
        raise Exception("Bundle not Found")

    apkmirror.download_apk(download_link)
    if not os.path.exists("big_file.apkm"):
        panic("Failed to download apk")

    with zipfile.ZipFile("big_file.apkm", "r") as zip_ref:
        zip_ref.extractall("big_file")

    files_to_keep = ["base.apk", "split_config.armeabi_v7a.apk", "split_config.en.apk", "split_config.mdpi.apk", "split_config.xhdpi.apk", "split_config.xxhdpi.apk"]

    def keep_files_recursively(directory, files_to_keep):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file not in files_to_keep:
                    os.remove(os.path.join(root, file))
            for dir in dirs:
                if dir not in files_to_keep:
                    shutil.rmtree(os.path.join(root, dir))

    keep_files_recursively("big_file", files_to_keep)

    # Create a new ZIP archive with the remaining files
    with zipfile.ZipFile("big_file.apks", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as zip_ref:
        for root, dirs, files in os.walk("big_file"):
            for file in files:
                zip_ref.write(os.path.join(root, file), os.path.join(os.path.relpath(root, "big_file"), file))
    download_apkeditor()

    if not os.path.exists("big_file_merged.apk"):
        merge_apk("big_file")
        # Delete the big_file directory
        shutil.rmtree("big_file")
    else:
        print("apkm is already merged")
        shutil.rmtree("big_file")

    download_revanced_bins()

    print("Downloading patches")
    pikoRelease = download_release_asset(
        "crimera/piko", "^piko.*jar$", "bins", "patches.jar"
    )

    print("Downloading integrations")
    integrationsRelease = download_release_asset(
        "crimera/revanced-integrations",
        "^rev.*apk$",
        "bins",
        "integrations.apk",
    )

    print(integrationsRelease["body"])

    message: str = f"""
Changelogs:
[piko-{pikoRelease["tag_name"]}]({pikoRelease["html_url"]})
[integrations-{integrationsRelease["tag_name"]}]({integrationsRelease["html_url"]})
"""

    build_apks(latest_version)

    publish_release(
        latest_version.version,
        [
            f"twitter-piko-v{latest_version.version}.apk",
        ],
        message,
    )


if __name__ == "__main__":
    main()
