import type { Metadata } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })
const playfair = Playfair_Display({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'АРУАХ - Эзотерическая платформа для Казахстана',
  description: 'Первая в Казахстане комплексная эзотерическая платформа: Таро, нумерология, астрология, чакры, матрица судьбы и Human Design',
  keywords: 'таро, нумерология, астрология, чакры, матрица судьбы, human design, казахстан, эзотерика',
  authors: [{ name: 'АРУАХ' }],
  openGraph: {
    title: 'АРУАХ - Эзотерическая платформа для Казахстана',
    description: 'Первая в Казахстане комплексная эзотерическая платформа',
    type: 'website',
    locale: 'ru_KZ',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={`${inter.className} antialiased`}>
        {children}
      </body>
    </html>
  )
}

