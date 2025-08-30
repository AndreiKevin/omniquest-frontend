import type { ProductsResponse } from '../types'

const API_URL = 'http://127.0.0.1:8000'

export async function fetchProducts(params: {
  page: number
  pageSize: number
  category?: string
  sort?: 'price_asc' | 'price_desc'
}): Promise<ProductsResponse> {
  const q = new URLSearchParams()
  q.set('page', String(params.page))
  q.set('page_size', String(params.pageSize))
  if (params.category) q.set('category', params.category)
  if (params.sort) q.set('sort', params.sort)
  const res = await fetch(`${API_URL}/products?${q.toString()}`)
  if (!res.ok) throw new Error('Failed to fetch products')
  return res.json()
}

export async function fetchCategories(): Promise<string[]> {
  const res = await fetch(`${API_URL}/categories`)
  if (!res.ok) throw new Error('Failed to fetch categories')
  return res.json()
}


