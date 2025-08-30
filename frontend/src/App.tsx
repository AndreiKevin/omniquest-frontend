import { useEffect, useMemo, useRef, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useProducts } from './hooks/useProducts'
import ProductCard from './components/ProductCard'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { SlidersHorizontal, Filter, X, ArrowUpAZ, ArrowDownAZ, ShoppingBasketIcon, CircleDollarSignIcon } from 'lucide-react'
import { fetchCategories, sendChat } from './lib/api'
import type { ChatMessage, Product } from './types'

export default function App() {
  const pageSize = 15
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [sort, setSort] = useState<'price_asc' | 'price_desc' | undefined>(undefined)

  const categoriesParam = selectedCategories.length ? selectedCategories.join(',') : undefined
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useProducts({ pageSize, categories: categoriesParam, sort })
  const items = useMemo(() => data?.pages.flatMap((p) => p.items) ?? [], [data])
  const sentinelRef = useRef<HTMLDivElement | null>(null)
  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: fetchCategories })
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: 'm1', role: 'assistant', text: 'Hi! Looking for anything specific?'
  }])
  const [chatInput, setChatInput] = useState('')

  useEffect(() => {
    if (!sentinelRef.current) return
    const el = sentinelRef.current
    const io = new IntersectionObserver((entries) => {
      const entry = entries[0]
      if (entry.isIntersecting && hasNextPage && !isFetchingNextPage) {
        fetchNextPage()
      }
    })
    io.observe(el)
    return () => io.disconnect()
  }, [fetchNextPage, hasNextPage, isFetchingNextPage])

  async function onSend() {
    const text = chatInput.trim()
    if (!text) return
    const userMsg: ChatMessage = { id: crypto.randomUUID(), role: 'user', text }
    setMessages((m) => [...m, userMsg])
    setChatInput('')
    try {
      const res = await sendChat({ query: text, top_k: 6 })
      const assistant: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        text: res.message,
        products: res.products,
      }
      setMessages((m) => [...m, assistant])
    } catch (e) {
      const err: ChatMessage = { id: crypto.randomUUID(), role: 'assistant', text: 'Sorry, something went wrong.' }
      setMessages((m) => [...m, err])
    }
  }

  return (
    <div className="min-h-screen bg-white text-zinc-900">
      <header className="sticky top-0 z-10 border-b bg-white/80 backdrop-blur">
        <div className="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-semibold text-blue-600">OmniQuest Grocery</h1>
          <nav className="text-sm text-zinc-600">v0.1</nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6 grid grid-cols-1 lg:grid-cols-[1fr_380px] gap-6">
        <section className="space-y-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base flex items-center gap-2"><SlidersHorizontal className="h-4 w-4" /> Browse Products</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex flex-wrap gap-3 items-end">
                <div className="space-y-1">
                  <label className="block text-xs text-zinc-600">Category</label>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="outline" className="w-56 justify-between">
                        {selectedCategories.length ? `${selectedCategories.length} selected` : 'Select categories'}
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent className="w-56">
                      <DropdownMenuLabel>Categories</DropdownMenuLabel>
                      <DropdownMenuSeparator />
                      <DropdownMenuCheckboxItem
                        checked={selectedCategories.length === 0}
                        onCheckedChange={(ck) => { if (ck) setSelectedCategories([]) }}
                      >All</DropdownMenuCheckboxItem>
                      {categories?.map((c) => (
                        <DropdownMenuCheckboxItem
                          key={c}
                          checked={selectedCategories.includes(c)}
                          onCheckedChange={(ck) => setSelectedCategories((prev) => ck ? [...prev, c] : prev.filter((x) => x !== c))}
                        >{c}</DropdownMenuCheckboxItem>
                      ))}
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
                <div className="space-y-1">
                  <label className="block text-xs text-zinc-600">Sort</label>
                  <div className="flex gap-2">
                    <Button
                      variant={sort ? 'default' : 'outline'}
                      size="sm"
                      className="h-10"
                      onClick={() => setSort(sort === undefined ? 'price_asc' : sort === 'price_asc' ? 'price_desc' : undefined)}
                    >
                      {sort === 'price_desc' ? <ArrowDownAZ className="h-4 w-4 mr-2" /> : <ArrowUpAZ className="h-4 w-4 mr-2" />}
                      {sort === undefined ? 'Price: Off' : sort === 'price_asc' ? 'Price: Low → High' : 'Price: High → Low'}
                    </Button>
                  </div>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-zinc-500 mr-1">Active:</span>
                <div className="flex gap-2">
                  {selectedCategories.length === 0 ? (
                    <button onClick={() => setSelectedCategories([])} className="group cursor-pointer">
                      <Badge variant="secondary" className="gap-1">
                        <Filter className="h-3.5 w-3.5 group-hover:hidden" />
                        <X className="h-3.5 w-3.5 hidden group-hover:inline" />
                        Category: All
                      </Badge>
                    </button>
                  ) : (
                    selectedCategories.map((c) => (
                      <button key={c} onClick={() => setSelectedCategories((prev) => prev.filter((x) => x !== c))} className="group cursor-pointer">
                        <Badge variant="secondary" className="gap-1 hover:opacity-90">
                          <ShoppingBasketIcon className="h-3.5 w-3.5 group-hover:hidden" />
                          <X className="h-3.5 w-3.5 hidden group-hover:inline" />
                          {c}
                        </Badge>
                      </button>
                    ))
                  )}
                  {sort && (
                    <button onClick={() => setSort(undefined)} className="group cursor-pointer">
                      <Badge variant="secondary" className="gap-1 hover:opacity-90">
                        <CircleDollarSignIcon className="h-3.5 w-3.5 group-hover:hidden" />
                        <X className="h-3.5 w-3.5 hidden group-hover:inline" />
                        Sort: {sort === 'price_asc' ? 'Price ↑' : 'Price ↓'}
                      </Badge>
                    </button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {items.map((p) => (
              <ProductCard key={p.product_id} product={p} />
            ))}
          </div>
          <div ref={sentinelRef} className="h-10" />
        </section>

        <aside className="lg:sticky lg:top-16 h-[calc(100vh-6rem)]">
          <Card className="h-full flex flex-col">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Overengineered Search™</CardTitle>
            </CardHeader>
            <Separator />
            <CardContent className="flex-1 p-0">
              <ScrollArea className="h-[calc(100vh-16rem)] p-4">
                <div className="space-y-3">
                  {messages.map((m) => (
                    <div key={m.id} className={m.role === 'user' ? 'ml-auto max-w-[80%]' : 'mr-auto max-w-[80%]'}>
                      <div className={
                        m.role === 'user'
                          ? 'rounded-2xl bg-blue-600 text-white px-3 py-2'
                          : 'rounded-2xl bg-zinc-100 text-zinc-900 px-3 py-2'
                      }>
                        {m.text}
                      </div>
                      {m.products && (
                        <div className="mt-2 grid grid-cols-2 gap-2">
                          {m.products.map((p: Product) => (
                            <ProductCard key={p.product_id} product={p} />
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
            <Separator />
            <div className="p-3">
              <div className="flex gap-2">
                <Input className="h-10" placeholder="Ask for recommendations..." value={chatInput} onChange={(e) => setChatInput(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') onSend() }} />
                <Button className="h-10" onClick={onSend}>Send</Button>
              </div>
            </div>
          </Card>
        </aside>
      </main>
    </div>
  )
}
