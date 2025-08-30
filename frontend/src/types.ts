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


