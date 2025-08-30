import type { Product } from '../types'

type Props = { product: Product }

export default function ProductCard({ product }: Props) {
  return (
    <div className="animate-in fade-in duration-200 rounded-lg border bg-white p-3 shadow-sm">
      <div className="h-[100px] flex items-center justify-center overflow-hidden">
        <img
          src={product.product_image}
          alt={product.product_name}
          className="h-[100px] w-auto object-contain"
        />
      </div>
      <div className="mt-2 space-y-1">
        <div className="text-sm font-medium" title={product.product_name}>{product.product_name}</div>
        <div className="text-xs text-zinc-500">{product.brand} · {product.category}</div>
        <div className="text-sm font-semibold text-blue-600">${product.price.toFixed(2)}</div>
      </div>
    </div>
  )
}


