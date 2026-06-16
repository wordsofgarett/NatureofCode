class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def addNums(l1, l2):

    carry = 0
    current_node_1 = l1
    current_node_2 = l2
    solution = []
    while current_node_1 or current_node_2:
        if current_node_1:
            val1 = current_node_1.val
        else:
            val1 = 0
        if current_node_2:
            val2 = current_node_2.val
        else: val2 = 0
        sum = val1 + val2 + carry
        if sum < 10:
            solution.append(sum)
            carry = 0
        else:
            digits = list(map(int, str(sum)))
            solution.append(int(digits.pop(len(digits)-1)))
            carry = int(''.join(map(str, digits)))

        if current_node_1:
            current_node_1 = current_node_1.next
        if current_node_2:
            current_node_2 = current_node_2.next

    if carry > 0:
        solution.append(carry)

    nodes = []
    for i in range(len(solution)):
        nodes.append(ListNode(solution[i]))
    for i in range(len(solution)-1):
        nodes[i].next = nodes[i+1]

    return solution




l2_3 = ListNode(1)
l2_2 = ListNode(7, l2_3)
l2_1 = ListNode(3, l2_2)

l1_3 = ListNode(4)
l1_2 = ListNode(4, l1_3)
l1_1 = ListNode(6, l1_2)

print(addNums(l1_1, l2_1))
print(173+446)

l3_1 = ListNode(0)
l4_1 = ListNode(0)
print(addNums(l3_1, l4_1))

l5_5 = ListNode(9)
l5_4 = ListNode(9, l5_5)
l5_3 = ListNode(9, l5_4)
l5_2 = ListNode(9, l5_3)
l5_1 = ListNode(9, l5_2)

l6_3 = ListNode(9)
l6_2 = ListNode(9, l6_3)
l6_1 = ListNode(9, l6_2)
print(addNums(l5_1, l6_1))
print(999+99999)


# l = [1,2,3]
# print(''.join(str(l)))