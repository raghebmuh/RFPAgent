import React, { useState } from 'react';
import { PlusCircleIcon } from '@heroicons/react/24/outline';

interface RFPQuickInputProps {
  onSubmit: (data: Record<string, any>) => void;
  fields: Array<{
    name: string;
    label: string;
    type: 'text' | 'number' | 'select' | 'date' | 'textarea';
    options?: string[];
    required?: boolean;
    placeholder?: string;
  }>;
  isRTL?: boolean;
}

const RFPQuickInput: React.FC<RFPQuickInputProps> = ({
  onSubmit,
  fields,
  isRTL = true,
}) => {
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [expanded, setExpanded] = useState(false);

  const handleChange = (fieldName: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [fieldName]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({});
    setExpanded(false);
  };

  const renderField = (field: (typeof fields)[0]) => {
    const commonClasses =
      'w-full rounded-lg border border-gray-300 px-3 py-2 dark:border-gray-600 dark:bg-gray-800';

    switch (field.type) {
      case 'select':
        return (
          <select
            value={formData[field.name] || ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
            className={commonClasses}
            required={field.required}
            dir={isRTL ? 'rtl' : 'ltr'}
          >
            <option value="">{field.placeholder || 'اختر...'}</option>
            {field.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );

      case 'textarea':
        return (
          <textarea
            value={formData[field.name] || ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            className={`${commonClasses} min-h-[100px]`}
            required={field.required}
            dir={isRTL ? 'rtl' : 'ltr'}
          />
        );

      case 'number':
        return (
          <input
            type="number"
            value={formData[field.name] || ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            className={commonClasses}
            required={field.required}
            dir={isRTL ? 'rtl' : 'ltr'}
          />
        );

      case 'date':
        return (
          <input
            type="date"
            value={formData[field.name] || ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
            className={commonClasses}
            required={field.required}
          />
        );

      default:
        return (
          <input
            type="text"
            value={formData[field.name] || ''}
            onChange={(e) => handleChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            className={commonClasses}
            required={field.required}
            dir={isRTL ? 'rtl' : 'ltr'}
          />
        );
    }
  };

  return (
    <div
      className="border-light-silver dark:border-raisin-black dark:bg-eerie-black rounded-lg border bg-white p-4"
      dir={isRTL ? 'rtl' : 'ltr'}
    >
      {!expanded ? (
        <button
          onClick={() => setExpanded(true)}
          className="flex w-full items-center justify-between rounded-lg bg-blue-50 p-3 text-blue-600 hover:bg-blue-100 dark:bg-blue-900/20 dark:text-blue-400 dark:hover:bg-blue-900/30"
        >
          <span className="flex items-center gap-2">
            <PlusCircleIcon className="h-5 w-5" />
            {isRTL ? 'إدخال سريع للبيانات' : 'Quick Data Entry'}
          </span>
          <span className="text-sm">
            {isRTL
              ? 'اضغط لملء الحقول المطلوبة'
              : 'Click to fill required fields'}
          </span>
        </button>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-lg font-semibold">
              {isRTL ? 'إدخال البيانات' : 'Data Entry'}
            </h3>
            <button
              type="button"
              onClick={() => setExpanded(false)}
              className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              ✕
            </button>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {fields.map((field) => (
              <div key={field.name}>
                <label className="mb-1 block text-sm font-medium">
                  {field.label}
                  {field.required && (
                    <span className="ml-1 text-red-500">*</span>
                  )}
                </label>
                {renderField(field)}
              </div>
            ))}
          </div>

          <div className="flex gap-3">
            <button
              type="submit"
              className="flex-1 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              {isRTL ? 'إرسال البيانات' : 'Submit Data'}
            </button>
            <button
              type="button"
              onClick={() => {
                setFormData({});
                setExpanded(false);
              }}
              className="rounded-lg border border-gray-300 px-4 py-2 hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-800"
            >
              {isRTL ? 'إلغاء' : 'Cancel'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default RFPQuickInput;
