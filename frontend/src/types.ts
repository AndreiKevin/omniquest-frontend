export type Product = {
  product_name: string
  brand: string
  category: string
  price: number
  quantity: number
  product_id: string
  product_image: string
}

export type ProductsResponse = {
  items: Product[]
  page: number
  page_size: number
  total: number
  has_next: boolean
}

export type ChatRequest = {
  query: string
  top_k?: number
  messages?: { role: 'system' | 'user' | 'assistant'; content: string }[]
}

export type ChatResponse = {
  message: string
  products: Product[]
}

export type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  text: string
  products?: Product[]
  loading?: boolean
}

// No ChatTurn export needed; we pass LLM-standard messages


