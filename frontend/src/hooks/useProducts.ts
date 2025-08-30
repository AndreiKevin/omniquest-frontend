import { useInfiniteQuery } from '@tanstack/react-query'
import { fetchProducts } from '../lib/api'
import type { ProductsResponse } from '../types'

export function useProducts(params: { pageSize: number; category?: string; sort?: 'price_asc' | 'price_desc' }) {
  return useInfiniteQuery<ProductsResponse>({
    queryKey: ['products', params],
    queryFn: ({ pageParam = 1 }) => fetchProducts({ page: pageParam, pageSize: params.pageSize, category: params.category, sort: params.sort }),
    initialPageParam: 1,
    getNextPageParam: (lastPage) => (lastPage.has_next ? lastPage.page + 1 : undefined),
  })
}


