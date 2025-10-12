export interface PaneRecord {
  label: string;
  type: string;
}

export type UniformValue = 
  | number
  | [number, number]
  | [number, number, number]
  | [number, number, number, number]

export function isUniformValue(value: any): value is UniformValue {
  if (!value && value !== 0) return false
  console.log("TYPEOF:", value);
  
  if (typeof value === 'number') return true 
  if (Array.isArray(value)) {
    if (value.length <= 4 && value.length >= 2 && value.every(v => typeof v === 'number')) return true
  }
  return false
}

export interface Uniform {
  name: string,
  value: UniformValue
}

export function isUniform(value: any): value is Uniform {
  if (!value) return false 
  if (!value.name) return false 
  if (!isUniformValue(value.value)) return false
  return true
}

export interface Status {
  success: bool,
  message: string
}
