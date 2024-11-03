import { NextResponse } from "next/server"

export async function POST(request: Request) { 
  const { word } = await request.json()
  const mockJoke = `Why did the ${word} cross the road? To get to the other side!`
  return NextResponse.json({joke: mockJoke})
}