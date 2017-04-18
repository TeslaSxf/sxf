import random
from time import clock


def sort_test(func, have_func=set()):
    '''排序测试装饰器，判断排序算法是否成功，并测出排序时间。
    have_func用来判断是否首次调用装饰器，如是首次，则初始化
    一个无序数组，并测试排序时间,如不是首次(针对递归函数),
    直接返回函数。
    '''
    def wrapper(*args, **kwargs):
        if func not in have_func:
            have_func.add(func)
            arr = list(range(10000))
            random.shuffle(arr)
            st = clock()
            ret = func(arr)
            et = clock()
            for r in range(len(ret) - 1):
                if ret[r] > ret[r + 1]:
                    break
            else:
                print('sort success')
            print('{0} cost {1}'.format(func.__name__, et - st))
            have_func.remove(func)
        else:
            ret = func(*args, **kwargs)
        return ret
    return wrapper


@sort_test
def bubble_sort(l):
    '''冒泡排序，从索引号0开始，和后一位的值比较，如果大于
    则交换值，迭代进行至数组最后第二位，就将最大值交换到了数
    组最后一位，重复进行此步骤直至数组有序。
    '''
    lenth = len(l)
    for i in range(lenth - 1, 0, -1):
        for j in range(i):
            if l[j] > l[j + 1]:
                l[j], l[j + 1] = l[j + 1], l[j]
    return l


@sort_test
def select_sort(l):
    '''选择排序，从索引0开始，向后遍历数组选取最小值跟当前
    索引交换值，再从索引1开始，向后遍历数组选取最小值跟当前
    索引交换值，迭代进行此步骤至数组最后一位，完成数组排序。
    '''
    lenth = len(l)
    for i in range(lenth):
        min = i
        for j in range(i + 1, lenth):
            if l[j] < l[min]:
                min = j
        l[i], l[min] = l[min], l[i]
    return l


@sort_test
def insert_sort(l):
    '''插入排序，将无序数组的每一位X跟之前的有序数组进行
    比较，直到有序数组的某一位数值小于或等于X，完成X插入到
    有序数组中。

    从索引号1开始，依次和前面的有序数组进行比较，如果小于
    则交换值，继续再和之前的序号比较，直至大于等于或到序号
    0，迭代完成此步骤至数组最后一位。
    '''
    lenth = len(l)
    for i in range(1, lenth):
        for j in range(i, 0, -1):
            if l[j] < l[j - 1]:
                l[j], l[j - 1] = l[j - 1], l[j]
            else:
                break
    return l


@sort_test
def quick_sort(l):
    '''快速排序，选取数组的第一位作为比较位，将小于该比较位
    的数组放到前面，将大于等于该比较位的数组放到后面，再对前
    面和后面的数组递归执行该算法，直到数组长度小于等于1，从
    而完成快速排序。
    '''
    if len(l) <= 1:
        return l
    return (quick_sort([lt for lt in l[1:] if lt < l[0]]) +
            [l[0]] + quick_sort([gt for gt in l[1:] if gt >= l[0]]))


@sort_test
def heap_sort(l):
    '''堆排序，堆是一颗完全二叉树，二叉树的几个概念。若根节
    点为索引号0，则最后一个父节点的索引号为length(数组长度)
    整除2 - 1，若父节点的索引号是x，则他的左子节点为2x+1，
    右子节点为2x+2。

    先将函数调整为大顶堆，即从最后一个父节点开始至根节点，迭
    代执行调整函数。把大顶堆的最大值R[0]和数组最后一位交换，
    就将数组分为了无序区R[0,n-2]和有序区R[n-1],然后再次对
    根节点执行调整函数调整为大顶堆，再交换R[0]和R[n-2],迭
    代进行此步骤直至无序区只有一个数值，进而完成堆排序。
    '''
    length = len(l)
    for i in range(length >> 2 - 1, -1, -1):
        heap_adjust(l, i, length - 1)
    for i in range(1, length):
        l[0], l[length - i] = l[length - i], l[0]
        heap_adjust(l, 0, length - i - 1)
    return l


def heap_adjust(l, n, m):
    '''节点调整函数，即将父节点和左右子节点进行比较，把最
    大值和父节点进行交换，并将交换下去的父节点递归进行调整
    函数，函数要注意索引号不要超过二叉树的长度。
    '''
    greater = n
    if 2 * n + 1 <= m and l[2 * n + 1] > l[greater]:
        greater = 2 * n + 1
    if 2 * n + 2 <= m and l[2 * n + 2] > l[greater]:
        greater = 2 * n + 2
    if greater != n:
        l[n], l[greater] = l[greater], l[n]
        heap_adjust(l, greater, m)


@sort_test
def merge_sort(l):
    '''归并排序，如果数组长度小于等于1，直接返回，否则将数
    组分为2个部分，各自递归执行归并排序，再对2个排序后的数
    组进行归并操作。
    '''
    length = len(l)
    if length <= 1:
        return l
    else:
        left = merge_sort(l[:length // 2])
        right = merge_sort(l[length // 2:])
        return merge(left, right)


def merge(left, right):
    '''归并操作，对2个有序列表从头开始比较，将二者之中较小
    的数添加到结果列表，然后将较小数的列表指针后移一位，迭
    代进行此操作直至一个有序列表取完，将另一组列表的剩余元
    素添加到结果列表后面，返回此列表。
    '''
    lp, rp = 0, 0
    result = []
    while lp < len(left) and rp < len(right):
        if left[lp] <= right[rp]:
            result.append(left[lp])
            lp += 1
        else:
            result.append(right[rp])
            rp += 1
    result += left[lp:]
    result += right[rp:]
    return result


@sort_test
def shell_sort(l):
    '''希尔排序,把数组按一定增量分组，对每组使用插入排序算
    法排序。随着增量逐渐减少，每组的元素越来越多，当增量减
    至1时，整个数组正好分成一组，再对其使用插入排序，完成数
    组排序。
    '''
    length = len(l)
    d = length // 2
    while d:
        for x in range(d):
            for i in range(x + d, length, d):
                for j in range(i, 0, -d):
                    if l[j] < l[j - d]:
                        l[j], l[j - d] = l[j - d], l[j]
                    else:
                        break
        d = d // 2
    return l


bubble_sort()
select_sort()
insert_sort()
quick_sort()
heap_sort()
merge_sort()
shell_sort()
