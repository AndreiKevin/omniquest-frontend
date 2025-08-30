import type { Product } from '../types'
import { Card, CardContent } from '@/components/ui/card'

type Props = { product: Product }

export default function ProductCard({ product }: Props) {
  return (
    <Card className="animate-in fade-in duration-200">
      <CardContent className="p-3">
        <div className="h-[100px] flex items-center justify-center overflow-hidden rounded-md bg-white">
          <img
            src={product.product_image}
            alt={product.product_name}
            className="h-[100px] w-auto object-contain"
          />
        </div>
        <div className="mt-2 space-y-1">
          <div className="text-sm font-medium line-clamp-2" title={product.product_name}>{product.product_name}</div>
          <div className="text-xs text-zinc-500">{product.brand} · {product.category}</div>
          <div className="text-sm font-semibold text-blue-600">${product.price.toFixed(2)}</div>
        </div>
      </CardContent>
    </Card>
  )
}


