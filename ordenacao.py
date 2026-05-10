def bubble_sort(lista, chave):
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][chave] > arr[j + 1][chave]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def merge_sort(lista, chave):
    if len(lista) <= 1:
        return lista[:]
    
    mid = len(lista) // 2
    left = merge_sort(lista[:mid], chave)
    right = merge_sort(lista[mid:], chave)

    return _merge(left, right, chave)


def _merge(left, right, chave):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][chave] <= right[j][chave]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(lista, chave):
    if len(lista) <= 1:
        return lista[:]
    
    pivot = lista[len(lista) // 2]
    
    left = [x for x in lista if x[chave] < pivot[chave]]
    middle = [x for x in lista if x[chave] == pivot[chave]]
    right = [x for x in lista if x[chave] > pivot[chave]]
    
    return quick_sort(left, chave) + middle + quick_sort(right, chave)
