import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const { keywords } = await request.json()
  console.log("is this association post working?")
  const mockWords = ['funny', 'hilarious', 'comedy', 'joke', 'laugh']
  return NextResponse.json({words: mockWords})
}