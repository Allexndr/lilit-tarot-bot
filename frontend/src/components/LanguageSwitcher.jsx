import React from 'react';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher = () => {
    const { i18n } = useTranslation();

    const changeLanguage = (lng) => {
        i18n.changeLanguage(lng);
    };

    const languages = [
        { code: 'ru', label: 'RU' },
        { code: 'en', label: 'EN' },
        { code: 'kk', label: 'KK' }
    ];

    return (
        <div className="flex theme-glass rounded-full p-1">
            {languages.map((lang) => (
                <button
                    key={lang.code}
                    onClick={() => changeLanguage(lang.code)}
                    className={`px-3 py-1 text-xs font-bold rounded-full transition-all duration-300 ${i18n.language === lang.code
                            ? 'bg-purple-600 text-white shadow-lg'
                            : 'text-gray-500 hover:text-purple-400'
                        }`}
                >
                    {lang.label}
                </button>
            ))}
        </div>
    );
};

export default LanguageSwitcher;
