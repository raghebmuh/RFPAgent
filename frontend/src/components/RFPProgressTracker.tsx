import React from 'react';
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';

interface RFPProgressTrackerProps {
  completionPercentage: number;
  missingFields?: string[];
  completedFields?: string[];
  isRTL?: boolean;
}

const RFPProgressTracker: React.FC<RFPProgressTrackerProps> = ({
  completionPercentage,
  missingFields = [],
  completedFields = [],
  isRTL = true,
}) => {
  const getProgressColor = (percentage: number) => {
    if (percentage < 30) return 'bg-red-500';
    if (percentage < 60) return 'bg-yellow-500';
    if (percentage < 90) return 'bg-blue-500';
    return 'bg-green-500';
  };

  const fieldLabels: Record<string, string> = {
    entity_name: 'اسم الجهة الحكومية',
    project_name: 'اسم المشروع',
    tender_number: 'رقم المنافسة',
    project_scope: 'نطاق العمل',
    project_type: 'نوع المشروع',
    duration_months: 'مدة التنفيذ',
    work_program_phases: 'مراحل التنفيذ',
    work_program_payment_method: 'طريقة الدفع',
    work_execution_method: 'طريقة تنفيذ الأعمال',
    technical_specifications: 'المواصفات الفنية',
    evaluation_criteria: 'معايير التقييم',
    budget_range: 'نطاق الميزانية',
    warranty_period: 'فترة الضمان',
    training_required: 'التدريب مطلوب',
    local_content_percentage: 'نسبة المحتوى المحلي',
    location: 'مكان التنفيذ',
    contact_department: 'الإدارة المسؤولة',
    contact_email: 'البريد الإلكتروني',
    submission_deadline: 'آخر موعد للتقديم',
  };

  return (
    <div
      className="border-light-silver dark:border-raisin-black dark:bg-eerie-black rounded-lg border bg-white p-4"
      dir={isRTL ? 'rtl' : 'ltr'}
    >
      <div className="mb-4">
        <div className="mb-2 flex items-center justify-between">
          <h3 className="text-lg font-semibold">
            {isRTL ? 'تقدم إنشاء وثيقة RFP' : 'RFP Document Progress'}
          </h3>
          <span className="text-2xl font-bold">{completionPercentage}%</span>
        </div>

        {/* Progress Bar */}
        <div className="h-4 w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
          <div
            className={`h-full transition-all duration-300 ${getProgressColor(
              completionPercentage,
            )}`}
            style={{ width: `${completionPercentage}%` }}
          />
        </div>
      </div>

      {/* Status Message */}
      <div className="mb-4">
        {completionPercentage === 100 ? (
          <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
            <CheckCircleIcon className="h-5 w-5" />
            <span>
              {isRTL
                ? 'جميع البيانات مكتملة! يمكن إنشاء الوثيقة الآن.'
                : 'All data complete! Document can be generated now.'}
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-2 text-yellow-600 dark:text-yellow-400">
            <ExclamationCircleIcon className="h-5 w-5" />
            <span>
              {isRTL
                ? `المتبقي ${missingFields.length} حقول لإكمالها`
                : `${missingFields.length} fields remaining to complete`}
            </span>
          </div>
        )}
      </div>

      {/* Field Status Lists */}
      {(missingFields.length > 0 || completedFields.length > 0) && (
        <div className="space-y-3">
          {/* Completed Fields */}
          {completedFields.length > 0 && (
            <div>
              <h4 className="mb-2 text-sm font-medium text-gray-600 dark:text-gray-400">
                {isRTL ? 'الحقول المكتملة:' : 'Completed Fields:'}
              </h4>
              <div className="flex flex-wrap gap-2">
                {completedFields.slice(0, 5).map((field) => (
                  <span
                    key={field}
                    className="inline-flex items-center gap-1 rounded-full bg-green-100 px-2 py-1 text-xs text-green-800 dark:bg-green-900 dark:text-green-200"
                  >
                    <CheckCircleIcon className="h-3 w-3" />
                    {fieldLabels[field] || field}
                  </span>
                ))}
                {completedFields.length > 5 && (
                  <span className="inline-flex items-center rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600 dark:bg-gray-700 dark:text-gray-400">
                    +{completedFields.length - 5} {isRTL ? 'أخرى' : 'more'}
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Missing Fields */}
          {missingFields.length > 0 && (
            <div>
              <h4 className="mb-2 text-sm font-medium text-gray-600 dark:text-gray-400">
                {isRTL ? 'الحقول المطلوبة:' : 'Required Fields:'}
              </h4>
              <div className="flex flex-wrap gap-2">
                {missingFields.slice(0, 5).map((field) => (
                  <span
                    key={field}
                    className="inline-flex items-center gap-1 rounded-full bg-yellow-100 px-2 py-1 text-xs text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
                  >
                    <ExclamationCircleIcon className="h-3 w-3" />
                    {fieldLabels[field] || field}
                  </span>
                ))}
                {missingFields.length > 5 && (
                  <span className="inline-flex items-center rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600 dark:bg-gray-700 dark:text-gray-400">
                    +{missingFields.length - 5} {isRTL ? 'أخرى' : 'more'}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Action Button */}
      {completionPercentage === 100 && (
        <button
          className="bg-primary hover:bg-primary-dark mt-4 w-full rounded-lg px-4 py-2 text-white transition-colors"
          onClick={() => {
            // Trigger RFP generation
            console.log('Generate RFP Document');
          }}
        >
          {isRTL ? '🔄 إنشاء وثيقة RFP' : '🔄 Generate RFP Document'}
        </button>
      )}
    </div>
  );
};

export default RFPProgressTracker;
