using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Steamworks;
using UnityEngine;
using Verse;
using Verse.Steam;

namespace HeProbe
{
    /// <summary>
    /// First Workshop release of Heirs of Earth. Runs only when the launcher armed it (HE_UPLOAD_DIR) and only after a fully clean test.
    /// Creates a new Workshop item, then sets title, description, preview, tags, visibility, files and change note in one update.
    /// Refuses to create a second item if the mod already has a PublishedFileId.txt.
    /// </summary>
    public class Uploader : MonoBehaviour
    {
        private const string PackageId = "kerem.heirs";
        private const string Version = "4.3.1";
        private const float TimeoutSeconds = 600f;
        private const int SteamTextLimit = 8000;

        private static CallResult<CreateItemResult_t> createCall;
        private static CallResult<SubmitItemUpdateResult_t> submitCall;
        private static UGCUpdateHandle_t handle;
        private static string folder, modDir, title, description, note, preview;
        private static float startedAt, nextReport, quitAt = -1f;
        private static bool submitting, finished, media, describe;
        private static PublishedFileId_t item;
        private static CallResult<AddUGCDependencyResult_t> dependencyCall;
        private static CallResult<SteamUGCQueryCompleted_t> queryCall;
        private static string[] shots;

        private static void Say(string text)
        {
            Debug.Log("HETEST UPLOAD " + text);
        }

        /// <summary>Returns true when the upload started; the caller must then leave the shutdown to the uploader.</summary>
        public static bool TryStart(int fails, int errors, int untranslated, int missingTex, int missingKeys)
        {
            folder = Environment.GetEnvironmentVariable("HE_UPLOAD_DIR");
            describe = Environment.GetEnvironmentVariable("HE_UPLOAD_MODE") == "description";
            media = describe || Environment.GetEnvironmentVariable("HE_UPLOAD_MODE") == "media";
            if (string.IsNullOrEmpty(folder))
            {
                Say("not armed");
                return false;
            }
            if (fails != 0 || errors != 0 || untranslated != 0 || missingTex != 0 || missingKeys != 0)
            {
                Say("BLOCKED test not clean fails=" + fails + " errors=" + errors + " untranslated=" + untranslated + " missingTex=" + missingTex + " missingKeys=" + missingKeys);
                return false;
            }
            try
            {
                if (!SteamManager.Initialized || !SteamUser.BLoggedOn())
                {
                    Say("BLOCKED steam not ready");
                    return false;
                }
                ModMetaData mod = ModLister.GetActiveModWithIdentifier(PackageId);
                if (mod == null || mod.OnSteamWorkshop || mod.ModVersion != Version)
                {
                    Say("BLOCKED wrong mod copy version=" + (mod == null ? "none" : mod.ModVersion));
                    return false;
                }
                modDir = mod.RootDir.FullName;
                if (media)
                {
                    return StartMedia();
                }
                if (File.Exists(Path.Combine(modDir, "About", "PublishedFileId.txt")))
                {
                    Say("BLOCKED item already exists: " + File.ReadAllText(Path.Combine(modDir, "About", "PublishedFileId.txt")).Trim());
                    return false;
                }
                title = mod.Name;
                description = File.ReadAllText(Path.Combine(folder, "description_3.0.txt"));
                note = File.ReadAllText(Path.Combine(folder, "change_note_3.0.txt"));
                preview = Path.Combine(folder, "preview.jpg");
                int dBytes = System.Text.Encoding.UTF8.GetByteCount(description), nBytes = System.Text.Encoding.UTF8.GetByteCount(note);
                if (title != "Heirs of Earth" || description.Length < 1500 || dBytes >= SteamTextLimit || note.Length < 1500 || nBytes >= SteamTextLimit
                    || !File.Exists(preview) || new FileInfo(preview).Length >= 1024 * 1024)
                {
                    Say("BLOCKED texts or preview title=" + title + " description=" + dBytes + " note=" + nBytes + " preview=" + (File.Exists(preview) ? new FileInfo(preview).Length.ToString() : "missing"));
                    return false;
                }
                GameObject host = new GameObject("HeUploader");
                DontDestroyOnLoad(host);
                host.AddComponent<Uploader>();
                createCall = CallResult<CreateItemResult_t>.Create(OnCreated);
                createCall.Set(SteamUGC.CreateItem(SteamUtils.GetAppID(), EWorkshopFileType.k_EWorkshopFileTypeCommunity));
                startedAt = Time.realtimeSinceStartup;
                nextReport = startedAt + 5f;
                Say("creating item folder=" + modDir + " description=" + dBytes + " note=" + nBytes);
                return true;
            }
            catch (Exception error)
            {
                Say("BLOCKED exception " + error.GetType().Name + ": " + error.Message);
                return false;
            }
        }

        private static void Done(string text)
        {
            if (finished) return;
            finished = true;
            Say(text);
            quitAt = Time.realtimeSinceStartup + 3f;
        }

        private static void OnCreated(CreateItemResult_t result, bool ioFailure)
        {
            Say("CREATED result=" + result.m_eResult + " id=" + result.m_nPublishedFileId.m_PublishedFileId + " ioFailure=" + ioFailure + " legalNeeded=" + result.m_bUserNeedsToAcceptWorkshopLegalAgreement);
            if (ioFailure || result.m_eResult != EResult.k_EResultOK)
            {
                Done("RESULT create failed");
                return;
            }
            try
            {
                ulong id = result.m_nPublishedFileId.m_PublishedFileId;
                File.WriteAllText(Path.Combine(modDir, "About", "PublishedFileId.txt"), id.ToString());
                Say("ITEM " + id);
                handle = SteamUGC.StartItemUpdate(SteamUtils.GetAppID(), result.m_nPublishedFileId);
                bool ok = SteamUGC.SetItemTitle(handle, title)
                          & SteamUGC.SetItemDescription(handle, description)
                          & SteamUGC.SetItemUpdateLanguage(handle, "english")
                          & SteamUGC.SetItemContent(handle, modDir)
                          & SteamUGC.SetItemPreview(handle, preview)
                          & SteamUGC.SetItemTags(handle, new List<string> { "Mod", "1.6" })
                          & SteamUGC.SetItemVisibility(handle, ERemoteStoragePublishedFileVisibility.k_ERemoteStoragePublishedFileVisibilityPublic);
                if (!ok)
                {
                    Done("RESULT steam refused item data");
                    return;
                }
                submitCall = CallResult<SubmitItemUpdateResult_t>.Create(OnSubmitted);
                submitCall.Set(SteamUGC.SubmitItemUpdate(handle, note));
                submitting = true;
                Say("submitting");
            }
            catch (Exception error)
            {
                Done("RESULT exception " + error.GetType().Name + ": " + error.Message);
            }
        }

        private static void OnSubmitted(SubmitItemUpdateResult_t result, bool ioFailure)
        {
            if (media && !ioFailure && result.m_eResult == EResult.k_EResultOK)
            {
                Say("SUBMITTED " + result.m_eResult);
                submitting = false;
                dependencyCall = CallResult<AddUGCDependencyResult_t>.Create(OnDependency);
                dependencyCall.Set(SteamUGC.AddDependency(item, new PublishedFileId_t(HarmonyItem)));
                return;
            }
            Done("RESULT " + result.m_eResult + " ioFailure=" + ioFailure + " legalNeeded=" + result.m_bUserNeedsToAcceptWorkshopLegalAgreement);
        }

        private const ulong ItemId = 3845334110UL;
        private const ulong HarmonyItem = 2009463077UL;

        /// <summary>
        /// Updates the published item: new files, change note, and the screenshots in the upload folder REPLACING the ones on the page
        /// (the item is queried first and its old extra previews are removed in the same update), then lists Harmony as a required item.
        /// With an empty screenshots folder the page keeps its screenshots. Title, description and main preview stay as they are.
        /// </summary>
        private static bool StartMedia()
        {
            string idFile = Path.Combine(modDir, "About", "PublishedFileId.txt");
            if (!File.Exists(idFile) || File.ReadAllText(idFile).Trim() != ItemId.ToString())
            {
                Say("BLOCKED media mode needs item " + ItemId);
                return false;
            }
            if (describe)
            {
                // Description only: no files, no screenshots, no change note entry.
                description = File.ReadAllText(Path.Combine(folder, "description_" + Version + ".txt"));
                if (description.Length < 1500 || System.Text.Encoding.UTF8.GetByteCount(description) >= SteamTextLimit)
                {
                    Say("BLOCKED description");
                    return false;
                }
                shots = new string[0];
            }
            string shotDir = Path.Combine(folder, "screenshots");
            if (!describe) shots = Directory.Exists(shotDir) ? Directory.GetFiles(shotDir, "*.jpg").OrderBy(f => f).ToArray() : new string[0];
            if (!describe && ((shots.Length > 0 && shots.Length < 6) || shots.Any(f => new FileInfo(f).Length >= 1024 * 1024)))
            {
                Say("BLOCKED screenshots count=" + shots.Length);
                return false;
            }
            note = describe ? null : File.ReadAllText(Path.Combine(folder, "change_note_" + Version + ".txt"));
            if (!describe && (note.Length < 300 || System.Text.Encoding.UTF8.GetByteCount(note) >= SteamTextLimit))
            {
                Say("BLOCKED change note");
                return false;
            }
            item = new PublishedFileId_t(ItemId);
            GameObject host = new GameObject("HeUploader");
            DontDestroyOnLoad(host);
            host.AddComponent<Uploader>();
            startedAt = Time.realtimeSinceStartup;
            nextReport = startedAt + 5f;
            UGCQueryHandle_t query = SteamUGC.CreateQueryUGCDetailsRequest(new[] { item }, 1);
            SteamUGC.SetReturnAdditionalPreviews(query, true);
            queryCall = CallResult<SteamUGCQueryCompleted_t>.Create(OnQueried);
            queryCall.Set(SteamUGC.SendQueryUGCRequest(query));
            Say("media querying item " + ItemId);
            return true;
        }

        private static void OnQueried(SteamUGCQueryCompleted_t result, bool ioFailure)
        {
            if (ioFailure || result.m_eResult != EResult.k_EResultOK || result.m_unNumResultsReturned < 1)
            {
                SteamUGC.ReleaseQueryUGCRequest(result.m_handle);
                Done("RESULT query failed " + result.m_eResult + " ioFailure=" + ioFailure);
                return;
            }
            uint old = SteamUGC.GetQueryUGCNumAdditionalPreviews(result.m_handle, 0);
            SteamUGC.ReleaseQueryUGCRequest(result.m_handle);
            handle = SteamUGC.StartItemUpdate(SteamUtils.GetAppID(), item);
            bool ok = (describe ? SteamUGC.SetItemDescription(handle, description) : SteamUGC.SetItemContent(handle, modDir)) & SteamUGC.SetItemUpdateLanguage(handle, "english");
            if (shots.Length > 0)
            {
                // Remove from the highest index down so the remaining indices stay valid.
                for (int i = (int)old - 1; i >= 0; i--)
                {
                    ok &= SteamUGC.RemoveItemPreview(handle, (uint)i);
                }
                foreach (string shot in shots)
                {
                    ok &= SteamUGC.AddItemPreviewFile(handle, shot, EItemPreviewType.k_EItemPreviewType_Image);
                }
            }
            if (!ok)
            {
                Done("RESULT steam refused the media update");
                return;
            }
            submitCall = CallResult<SubmitItemUpdateResult_t>.Create(OnSubmitted);
            submitCall.Set(SteamUGC.SubmitItemUpdate(handle, note));
            submitting = true;
            Say((describe ? "description submitting bytes=" + System.Text.Encoding.UTF8.GetByteCount(description) + " " : "") + "media submitting files=" + modDir + " oldShots=" + old + " newShots=" + shots.Length + (shots.Length > 0 ? " (replacing)" : " (keeping)"));
        }

        private static void OnDependency(AddUGCDependencyResult_t result, bool ioFailure)
        {
            Done("RESULT media ok, dependency " + result.m_eResult + " child=" + result.m_nChildPublishedFileId.m_PublishedFileId + " ioFailure=" + ioFailure);
        }

        private void Update()
        {
            float now = Time.realtimeSinceStartup;
            if (finished)
            {
                if (quitAt > 0f && now >= quitAt)
                {
                    quitAt = -1f;
                    Say("COMPLETE");
                    Root.Shutdown();
                }
                return;
            }
            if (submitting && now >= nextReport)
            {
                nextReport = now + 10f;
                EItemUpdateStatus status = SteamUGC.GetItemUpdateProgress(handle, out ulong processed, out ulong total);
                Say("progress " + status + " " + processed + "/" + total);
            }
            if (now - startedAt > TimeoutSeconds)
            {
                Done("RESULT timeout");
            }
        }
    }
}
