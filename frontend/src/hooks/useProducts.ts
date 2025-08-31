import { useInfiniteQuery } from '@tanstack/react-query'
import { fetchProducts } from '../lib/api'
import type { ProductsResponse } from '../types'

export function useProducts(params: {
  pageSize: number
  categories?: string
  sort?: 'price_asc' | 'price_desc'
}) {
  const { pageSize, categories, sort } = params
  return useInfiniteQuery<ProductsResponse>({
    // Cache is segmented by sort and categories so toggling reuses prior results when revisited
    queryKey: ['products', { pageSize, categories, sort }],
    queryFn: ({ pageParam = 1 }) =>
      fetchProducts({ page: pageParam as number, pageSize, categories, sort }),
    initialPageParam: 1,
    getNextPageParam: (lastPage) => (lastPage.has_next ? lastPage.page + 1 : undefined),
    staleTime: 60_000, // 1 min: recent toggles re-use cache
    gcTime: 5 * 60_000, // retain for quick back-and-forth
    refetchOnWindowFocus: false,
  })
}


