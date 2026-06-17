'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Star, 
  Moon, 
  Sun, 
  Heart, 
  Sparkles, 
  ArrowRight,
  CheckCircle,
  Users,
  Zap,
  Shield
} from 'lucide-react'

export default function Home() {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  const features = [
    {
      icon: <Star className="w-8 h-8" />,
      title: "Таро",
      description: "Расклады на любые вопросы с AI-интерпретацией",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: <Moon className="w-8 h-8" />,
      title: "Нумерология",
      description: "Числа судьбы, квадрат Пифагора, персональные годы",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Sun className="w-8 h-8" />,
      title: "Астрология",
      description: "Натальные карты, прогнозы, совместимость",
      color: "from-yellow-500 to-orange-500"
    },
    {
      icon: <Heart className="w-8 h-8" />,
      title: "Чакры",
      description: "Диагностика энергетических центров",
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: <Sparkles className="w-8 h-8" />,
      title: "Матрица Судьбы",
      description: "22 аркана, кармические задачи, предназначение",
      color: "from-indigo-500 to-purple-500"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Human Design",
      description: "Типы, центры, профили, стратегии",
      color: "from-pink-500 to-rose-500"
    }
  ]

  const pricing = [
    {
      name: "FREE",
      price: "0₸",
      period: "навсегда",
      features: [
        "3 запроса в день",
        "Базовые функции",
        "Карта дня",
        "Да/Нет расклады"
      ],
      color: "from-gray-600 to-gray-700"
    },
    {
      name: "PREMIUM",
      price: "2,500₸",
      period: "в месяц",
      features: [
        "Безлимит запросов",
        "Все функции",
        "PDF-отчёты",
        "Приоритетная поддержка"
      ],
      color: "from-purple-600 to-pink-600",
      popular: true
    },
    {
      name: "VIP",
      price: "15,000₸",
      period: "за консультацию",
      features: [
        "Живая консультация",
        "Персональный прогноз",
        "Закрытое комьюнити",
        "Эксклюзивные материалы"
      ],
      color: "from-yellow-500 to-orange-500"
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-pink-900/20 to-blue-900/20"></div>
        <div className="absolute inset-0 bg-[url('/stars.svg')] bg-cover opacity-20"></div>
        
        <motion.div 
          className="relative z-10 text-center max-w-6xl mx-auto px-4"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: isLoaded ? 1 : 0, y: isLoaded ? 0 : 50 }}
          transition={{ duration: 0.8 }}
        >
          <motion.h1 
            className="text-6xl md:text-8xl font-bold mb-6 gradient-text text-shadow-lg"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: isLoaded ? 1 : 0, scale: isLoaded ? 1 : 0.8 }}
            transition={{ duration: 1, delay: 0.2 }}
          >
            АРУАХ
          </motion.h1>
          
          <motion.p 
            className="text-xl md:text-2xl mb-8 text-gray-300 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isLoaded ? 1 : 0, y: isLoaded ? 0 : 20 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            Первая в Казахстане комплексная эзотерическая платформа
          </motion.p>
          
          <motion.p 
            className="text-lg mb-12 text-gray-400 max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isLoaded ? 1 : 0, y: isLoaded ? 0 : 20 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            Таро • Нумерология • Астрология • Чакры • Матрица Судьбы • Human Design
          </motion.p>
          
          <motion.div 
            className="flex flex-col sm:flex-row gap-4 justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isLoaded ? 1 : 0, y: isLoaded ? 0 : 20 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <a 
              href="https://t.me/aruah_bot" 
              target="_blank" 
              rel="noopener noreferrer"
              className="btn-primary text-lg px-8 py-4 inline-flex items-center gap-2"
            >
              Начать в Telegram
              <ArrowRight className="w-5 h-5" />
            </a>
            <a 
              href="#features" 
              className="btn-secondary text-lg px-8 py-4 inline-flex items-center gap-2"
            >
              Узнать больше
              <ArrowRight className="w-5 h-5" />
            </a>
          </motion.div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
              Возможности платформы
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Все эзотерические практики в одном месте с современными AI-технологиями
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                className="card group hover:scale-105"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <div className={`w-16 h-16 rounded-full bg-gradient-to-r ${feature.color} flex items-center justify-center text-white mb-4 group-hover:animate-pulse`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-slate-800/50 to-purple-900/50">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
              Тарифы
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Выберите подходящий тариф для вашего духовного путешествия
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {pricing.map((plan, index) => (
              <motion.div
                key={index}
                className={`card relative ${plan.popular ? 'ring-2 ring-purple-500 scale-105' : ''}`}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                      Популярный
                    </span>
                  </div>
                )}
                
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                  <div className="text-4xl font-bold gradient-text mb-2">{plan.price}</div>
                  <div className="text-gray-400">{plan.period}</div>
                </div>

                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
                      <span className="text-gray-300">{feature}</span>
                    </li>
                  ))}
                </ul>

                <button className={`w-full py-3 px-6 rounded-lg font-semibold transition-all duration-300 ${
                  plan.popular 
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white' 
                    : 'bg-white/10 hover:bg-white/20 text-white border border-white/20'
                }`}>
                  {plan.name === 'FREE' ? 'Начать бесплатно' : 'Выбрать план'}
                </button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
              Готовы начать?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Присоединяйтесь к тысячам людей, которые уже открыли для себя мир эзотерики
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="https://t.me/aruah_bot" 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn-primary text-lg px-8 py-4 inline-flex items-center gap-2"
              >
                Начать в Telegram
                <ArrowRight className="w-5 h-5" />
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-white/10">
        <div className="max-w-6xl mx-auto text-center">
          <div className="mb-8">
            <h3 className="text-2xl font-bold gradient-text mb-4">АРУАХ</h3>
            <p className="text-gray-400">
              Эзотерическая платформа для Казахстана
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row justify-center items-center gap-6 text-sm text-gray-400">
            <span>© 2024 АРУАХ. Все права защищены.</span>
            <span>•</span>
            <a href="#" className="hover:text-white transition-colors">Политика конфиденциальности</a>
            <span>•</span>
            <a href="#" className="hover:text-white transition-colors">Условия использования</a>
          </div>
        </div>
      </footer>
    </div>
  )
}

