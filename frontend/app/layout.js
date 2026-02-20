import './globals.css'

export const metadata = {
  title: 'CampaignBrain',
  description: 'Multi-Agent AI Assistant',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
