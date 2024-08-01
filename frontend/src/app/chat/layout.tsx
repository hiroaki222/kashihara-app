import Header from '@/components/Header'
import ThreadList from '@/components/ThreadList'

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  const uid = '56b7c890-d12e-5678-f901-4567g8901h23'
  return (
    <div className="flex h-screen w-full flex-col bg-background">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <ThreadList uid={uid} />
        <div className="flex flex-1 flex-col">
          {children}
        </div>
      </div>
    </div>
  )
}