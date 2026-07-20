export const metadata = {
  title: 'Must Love Scrubs',
  description: 'The Everything Platform for Nurses.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'system-ui, sans-serif', margin: 0, background: '#f6f3ff', color: '#1e1233' }}>
        {children}
      </body>
    </html>
  );
}
