// Sample API route — proves Next.js → Prisma → Supabase is wired up.
// GET /api/questions?cat=Pharmacology&limit=10
import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const cat = searchParams.get('cat') ?? undefined;
  const limit = Math.min(Number(searchParams.get('limit') ?? 20), 100);

  try {
    const [total, questions] = await Promise.all([
      prisma.question.count({ where: { cat } }),
      prisma.question.findMany({
        where: { cat },
        take: limit,
        select: { id: true, cat: true, type: true, difficulty: true, stem: true },
      }),
    ]);
    return NextResponse.json({ total, count: questions.length, questions });
  } catch (err) {
    return NextResponse.json(
      { error: 'Database not reachable. Check DATABASE_URL and run the migration + import (see ../SETUP.md).' },
      { status: 500 },
    );
  }
}
