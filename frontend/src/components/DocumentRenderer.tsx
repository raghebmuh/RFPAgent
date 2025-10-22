import React, { useRef, useState } from 'react';
import CopyButton from './CopyButton';
import { useSelector } from 'react-redux';
import { selectStatus } from '../conversation/conversationSlice';
import { selectToken } from '../preferences/preferenceSlice';
import { useDarkTheme } from '../hooks';
import { DocumentRendererProps } from './types';

const DocumentRenderer: React.FC<DocumentRendererProps> = ({
  docId,
  title,
  sections,
  previewText,
  isLoading,
  language,
  rtl,
}) => {
  const [isDarkTheme] = useDarkTheme();
  const status = useSelector(selectStatus);
  const token = useSelector(selectToken);
  const [showDownloadMenu, setShowDownloadMenu] = useState<boolean>(false);
  const [showPreview, setShowPreview] = useState<boolean>(true);
  const downloadMenuRef = useRef<HTMLDivElement>(null);

  const isCurrentlyLoading =
    isLoading !== undefined ? isLoading : status === 'loading';

  // Detect RTL content (Arabic, Hebrew, etc.)
  const isRTL =
    rtl || language === 'ar' || /[\u0600-\u06FF\u0750-\u077F]/.test(title);

  const downloadDocx = async (): Promise<void> => {
    try {
      // console.log('Attempting to download document:', docId);
      // console.log('API Host:', import.meta.env.VITE_API_HOST);
      // console.log('Token present:', !!token);
      // console.log('Token value:', token);
      // console.log('LocalStorage authToken:', localStorage.getItem('authToken'));

      const downloadUrl = `${import.meta.env.VITE_API_HOST}/api/documents/download/${docId}`;

      // Try the fetch approach first
      try {
        const headers: Record<string, string> = {
          'Content-Type': 'application/json',
        };

        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(downloadUrl, {
          method: 'GET',
          headers,
        });

        // console.log('Response status:', response.status);
        // console.log('Response headers:', Object.fromEntries(response.headers.entries()));

        if (!response.ok) {
          const errorText = await response.text();
          console.error(
            'Download failed:',
            response.status,
            response.statusText,
            errorText,
          );
          throw new Error(
            `Download failed: ${response.status} ${response.statusText}`,
          );
        }

        // Handle the blob response more carefully
        const blob = await response.blob();
        console.log('Blob created successfully, size:', blob.size);

        // Create download URL
        const url = window.URL.createObjectURL(blob);
        console.log('Object URL created:', url);

        // Create download link
        const link = document.createElement('a');
        link.href = url;
        link.download = `${title.replace(/[^a-z0-9]/gi, '_')}.docx`;
        link.style.display = 'none';

        // Add to DOM, trigger download, and clean up
        document.body.appendChild(link);

        try {
          link.click();
          console.log('Download link clicked successfully');
        } catch (clickError) {
          console.error('Error clicking download link:', clickError);
          throw clickError;
        }

        // Clean up after a short delay to ensure download starts
        setTimeout(() => {
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
          console.log('Download cleanup completed');
        }, 1000);

        console.log('Download completed successfully');
        return;
      } catch (fetchError) {
        console.error('Fetch approach failed:', fetchError);
        console.log('Trying direct link approach as fallback...');

        // Fallback: Direct link approach
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `${title.replace(/[^a-z0-9]/gi, '_')}.docx`;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.style.display = 'none';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        console.log('Direct link download attempted');
      }
    } catch (error) {
      console.error('Error downloading document:', error);
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error occurred';
      alert(`Failed to download document: ${errorMessage}`);
    }
  };

  const downloadOptions = [{ label: 'Download as DOCX', action: downloadDocx }];

  return (
    <div className="w-inherit group border-light-silver dark:border-raisin-black dark:bg-eerie-black relative rounded-lg border bg-white">
      <div className="bg-platinum dark:bg-eerie-black-2 flex items-center justify-between px-2 py-1">
        <span className="text-just-black dark:text-chinese-white flex items-center gap-2 text-xs font-medium">
          <svg
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          document
        </span>
        <div className="flex items-center gap-2">
          <CopyButton textToCopy={previewText || title} />

          {!isCurrentlyLoading && (
            <div className="relative" ref={downloadMenuRef}>
              <button
                onClick={() => setShowDownloadMenu(!showDownloadMenu)}
                className="flex h-full items-center rounded-sm bg-gray-100 px-2 py-1 text-xs dark:bg-gray-700"
                title="Download options"
              >
                Download <span className="ml-1">▼</span>
              </button>
              {showDownloadMenu && (
                <div className="absolute right-0 z-10 mt-1 w-40 rounded-sm border border-gray-200 bg-white shadow-lg dark:border-gray-700 dark:bg-gray-800">
                  <ul>
                    {downloadOptions.map((option, index) => (
                      <li key={index}>
                        <button
                          onClick={() => {
                            option.action();
                            setShowDownloadMenu(false);
                          }}
                          className="w-full px-4 py-2 text-left text-xs hover:bg-gray-100 dark:hover:bg-gray-700"
                        >
                          {option.label}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {!isCurrentlyLoading && (
            <button
              onClick={() => setShowPreview(!showPreview)}
              className={`flex h-full items-center rounded px-2 py-1 text-xs ${
                showPreview
                  ? 'bg-blue-200 dark:bg-blue-800'
                  : 'bg-gray-100 dark:bg-gray-700'
              }`}
              title="Toggle Preview"
            >
              Preview
            </button>
          )}
        </div>
      </div>

      {isCurrentlyLoading ? (
        <div className="dark:bg-eerie-black flex items-center justify-center bg-white p-4">
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Generating document...
          </div>
        </div>
      ) : (
        <div
          className={`dark:bg-eerie-black bg-white p-4 ${isRTL ? 'rtl' : ''}`}
          dir={isRTL ? 'rtl' : 'ltr'}
        >
          {showPreview && (
            <div className="prose dark:prose-invert max-w-none">
              <h3
                className={`mb-4 text-lg font-bold ${isRTL ? 'text-right' : ''}`}
              >
                {title}
              </h3>

              {sections && sections.length > 0 && (
                <div className="space-y-2">
                  <p
                    className={`text-sm font-semibold text-gray-600 dark:text-gray-400 ${isRTL ? 'text-right' : ''}`}
                  >
                    {isRTL
                      ? `هيكل الوثيقة (${sections.length} أقسام):`
                      : `Document Structure (${sections.length} sections):`}
                  </p>
                  <ul
                    className={`list-disc space-y-1 ${isRTL ? 'list-inside pr-6' : 'pl-6'}`}
                  >
                    {sections.map((section: any, index: number) => (
                      <li
                        key={index}
                        className={`text-sm ${
                          section.level === 1
                            ? 'font-semibold'
                            : section.level === 2
                              ? isRTL
                                ? 'pr-4'
                                : 'pl-4'
                              : isRTL
                                ? 'pr-8'
                                : 'pl-8'
                        } text-gray-600 dark:text-gray-400`}
                      >
                        {section.heading}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {previewText && (
                <div
                  className={`mt-4 border-t border-gray-200 pt-4 dark:border-gray-700 ${isRTL ? 'text-right' : ''}`}
                >
                  <pre
                    className={`font-sans text-sm whitespace-pre-wrap ${isRTL ? 'text-right' : ''}`}
                  >
                    {previewText}
                  </pre>
                </div>
              )}

              <div
                className={`mt-6 rounded-lg bg-blue-50 p-4 dark:bg-blue-900/20 ${isRTL ? 'text-right' : ''}`}
              >
                <p className="text-sm text-blue-800 dark:text-blue-200">
                  {isRTL
                    ? '📄 وثيقة Word القابلة للتحرير جاهزة! انقر على "تحميل" لحفظها.'
                    : '📄 Your editable Word document is ready! Click "Download" to save it.'}
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DocumentRenderer;
