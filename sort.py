import random
from time import clock


# 冒泡排序，从索引号0开始，和后一位的值比较，如果大于则交换值，
# 再对索引号1和2的值进行比较，大于则交换，迭代进行至数组倒数第二位，
# 就将最大值交换到了数组最后一位，重复进行此步骤直至数组有序。
def bubble_sort(l):
    lenth = len(l)
    for i in range(lenth - 1, 0, -1):
        for j in range(i):
            if l[j] > l[j + 1]:
                l[j], l[j + 1] = l[j + 1], l[j]
    return l


# 选择排序，从索引号0开始，遍历数组取选最小值跟当前序号交换值，
# 迭代至数组最后一位。
def select_sort(l):
    lenth = len(l)
    for i in range(lenth):
        min = i
        for j in range(i + 1, lenth):
            if l[j] < l[min]:
                min = j
        l[i], l[min] = l[min], l[i]
    return l


# 插入排序，将无序数组的每一位X跟之前的有序数组进行比较，直到有序
# 数组的某一位数值小于或等于X，完成X插入到有序数组中。
# 从索引号1开始，依次和前面的有序数组进行比较，如果小于则交换值，
# 继续再和之前的序号比较，直至大于等于或到序号0，
# 迭代完成此类比较至数组最后一位。
def insert_sort(l):
    lenth = len(l)
    for i in range(1, lenth):
        for j in range(i, 0, -1):
            if l[j] < l[j - 1]:
                l[j], l[j - 1] = l[j - 1], l[j]
            else:
                break
    return l


# 快速排序，选取数组的第一位作为比较位，将小于该比较位的数组放到前面，
# 将大于等于该比较位的数组放到后面，再对前面和后面的数组递归执行该算法，
# 直到数组长度小于等于1，从而完成快速排序。
def quick_sort(l):
    if len(l) <= 1:
        return l
    return (quick_sort([lt for lt in l[1:] if lt < l[0]]) +
            [l[0]] + quick_sort([gt for gt in l[1:] if gt >= l[0]]))


# 堆排序，堆是一颗完全二叉树，二叉树的几个概念。
# 若根节点为索引号0，则最后一个父节点的索引号为length(数组长度)
# 整除2 - 1，若父节点的索引号是x，则他的左子节点为2x+1，
# 右子节点为2x+2。
# heap_adjus函数为父节点调整函数，即将父节点和左右子节点进行比较，
# 把最大值和父节点进行交换，并将交换下去的父节点递归进行调整函数，
# 函数要注意索引号不要超过二叉树的长度。
# 先将函数调整为大顶堆，即从最后一个父节点开始至根节点，迭代执行调整
# 函数。把大顶堆的最大值R[0]和数组最后一位交换，就将数组分为了无序区
# R[0,n-1]和有序区R[n-1],然后再次对根节点执行调整函数调整为大顶堆，
# 再交换R[0]和R[n-2],迭代进行此步骤直至无序区只有一个数值，进而
# 完成堆排序。
def heap_sort(l):
    length = len(l)
    for i in range(length >> 2 - 1, -1, -1):
        heap_adjust(l, i, length - 1)
    for i in range(1, length):
        l[0], l[length - i] = l[length - i], l[0]
        heap_adjust(l, 0, length - i - 1)
    return l


def heap_adjust(l, n, m):
    greater = n
    if 2 * n + 1 <= m and l[2 * n + 1] > l[greater]:
        greater = 2 * n + 1
    if 2 * n + 2 <= m and l[2 * n + 2] > l[greater]:
        greater = 2 * n + 2
    if greater != n:
        l[n], l[greater] = l[greater], l[n]
        heap_adjust(l, greater, m)


arr = list(range(100000))
random.shuffle(arr)
st = clock()
arr = quick_sort(arr)
et = clock()
for i in range(len(arr) - 1):
    if arr[i] > arr[i + 1]:
        break
else:
    print('sucess')
print((et - st))
