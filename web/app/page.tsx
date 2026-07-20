// Placeholder landing for the production app. The finished UI migrates the
// prototype's pages (see ../index.html and ../tools/build_pages.py) into React,
// keeping the violet & mint design. Codex builds these out from SETUP.md.
export default function Home() {
  return (
    <main style={{ maxWidth: 640, margin: '0 auto', padding: '4rem 1.5rem' }}>
      <h1 style={{ fontSize: '2.4rem', margin: 0 }}>
        Must Love Scrubs <span style={{ color: '#8b5cff' }}>— web app</span>
      </h1>
      <p style={{ color: '#5b4b73', fontSize: '1.05rem' }}>
        Production skeleton. The database, content import, and a sample API route are wired up.
      </p>
      <ol style={{ lineHeight: 1.9 }}>
        <li>Fill in <code>.env</code> (see <code>.env.example</code>)</li>
        <li><code>npx prisma migrate deploy</code></li>
        <li><code>node scripts/import-content.mjs</code></li>
        <li>
          Open <a href="/api/questions?limit=5" style={{ color: '#14b8a8' }}>/api/questions</a> — your
          content, served from the database.
        </li>
      </ol>
      <p style={{ color: '#5b4b73' }}>
        Next: auth, student dashboard, and the server-side exam engine. See <code>../SETUP.md</code>.
      </p>
    </main>
  );
}
