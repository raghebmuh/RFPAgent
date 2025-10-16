export function truncate(str: string, n: number) {
  // slices long strings and ends with ...
  return str.length > n ? str.slice(0, n - 1) + '...' : str;
}

export function formatBytes(bytes: number | null): string {
  if (!bytes || bytes <= 0) return '';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}

/**
 * Detects if text contains RTL (Right-to-Left) characters
 * Checks for Arabic, Hebrew, Persian, Urdu and other RTL scripts
 * @param text - The text to check
 * @returns true if text contains RTL characters
 */
export function isRTL(text: string | undefined): boolean {
  if (!text) return false;

  // RTL Unicode ranges:
  // \u0600-\u06FF: Arabic
  // \u0750-\u077F: Arabic Supplement
  // \u08A0-\u08FF: Arabic Extended-A
  // \uFB50-\uFDFF: Arabic Presentation Forms-A
  // \uFE70-\uFEFF: Arabic Presentation Forms-B
  // \u0590-\u05FF: Hebrew
  const rtlPattern =
    /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u0590-\u05FF]/;

  return rtlPattern.test(text);
}
