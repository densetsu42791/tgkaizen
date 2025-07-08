a1, b1 = "11", "1"
a2, b2 = "1010", "1011"





def addBinary(a: str, b: str) -> str:
    i = len(a) - 1  # указатель на последний символ строки a
    j = len(b) - 1  # указатель на последний символ строки b
    carry = 0  # перенос
    result = []  # список для хранения результата (в обратном порядке)

    # пока есть цифры для сложения или есть перенос
    while i >= 0 or j >= 0 or carry:
        digit_a = int(a[i]) if i >= 0 else 0  # берем цифру из строки a или 0
        digit_b = int(b[j]) if j >= 0 else 0  # берем цифру из строки b или 0

        total = digit_a + digit_b + carry  # сумма двух цифр и переноса
        carry = total // 2  # новый перенос
        result.append(str(total % 2))  # текущая цифра в результат
 

        i -= 1  # сдвигаем указатели
        j -= 1
    
    # результат записан в обратном порядке, переворачиваем
    return ''.join(reversed(result))



print(addBinary(a2, b2))

# a = int(a1, 2)
# b = int(b1, 2)
carry = 1 % 2
print(carry)

