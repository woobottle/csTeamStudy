# Chapter 5. 연결리스트

### 왜 연결 리스트인가??
연결 리스트는 단순한 편이여서 한 시간에 두세 문제를 내야 하는 인터뷰 특성에도 잘 맞아 떨어진다.  
### 연결 리스트의 종류
단일 연결 리스트, 이중 연결 리스트, 원형 연결 리스트   
면접에서는 대부분 단인 연결 리스트 문제가 나온다

* 단일 연결리스트
<img src="https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F8475c3b6-33ce-4364-a31d-6690e0ff27f8%2FUntitled.png?table=block&id=20e264cb-5ed1-4f25-a46c-2c3138f0a4e3&spaceId=359809db-cb83-47c2-9cce-0c45f96418ab&width=2000&userId=56059f96-1ce0-4d35-87f6-3200db26ea2a&cache=v2" />

python용 연결리스트
```python
class Node :
  def __init__(self, data, next = None) :
    self.data = data
    self.next = next
```

javscript용 연결리스트
```js
class Node {
  constructor(data, next) {
    this.data = data;
    this.next = next;
  }
}

const a = new Node(1, null)
const b = new Node(2, null)
a.next = b
```

* 이중 연결 리스트
<img src="https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F71324d22-9c5f-4f50-9475-6df76165414f%2FUntitled.png?table=block&id=898f0be0-c1bf-4283-b1e5-4f4ecd48f0ca&spaceId=359809db-cb83-47c2-9cce-0c45f96418ab&width=1470&userId=56059f96-1ce0-4d35-87f6-3200db26ea2a&cache=v2">


python용 연결리스트
```python
class Node :
  def __init__(self, before = None, data, next = None) :
    self.before = before
    self.data = data
    self.next = next
```

javscript용 연결리스트
```js
class Node {
  constructor(before, data, next) {
    this.before = before;
    this.data = data;
    this.next = next;
  }
}

const a = new Node(null, 1, null)
const b = new Node(a, 2, null)
a.next = b
```

* 원형 연결 리스트
원형 연결 리스트에는 끝, 즉 머리나 꼬리가 없다. 원형 연결 리스트의 모든 원소에서 다음 원소를 가리키는 포인터나 레퍼런스에는 반드시 널이 아닌 어떤 원소가 들어가며, 이중 연결 리스트라면 포인터/레퍼런스에도 널이 아닌 원소가 들어가야 한다.

### 기초적인 연결 리스트 연산
리스트를 잃어버리지 않기 위한 머리 원소 추적, 리스트 종주, 리스트 원소 추가 및 제거 등이 있다. => 이중 연결 리스트로 하면 너무 쉬워지므로 단일 연결 리스트로만 하겠다.    

##### 머리 원소 추적
새로운 원소를 첫 번째 원소 앞에 추가한다거나 리스트의 첫번째 원소를 제거할 때 리스트의 머리에 대한 포인터 또는 레퍼런스를 갱신해야 한다.   

잘못된 코드
```java
public void insertInFront(ListElement<Integer> list, int data) {
  ListElement<Integer> l = new ListElement<Integer>(data);
  l.setNext(list);
}
```

머리 원소에 대한 레퍼런스를 반환해야 한다.
```java
public ListElement<Integer> insertInFront(ListElement<Integer> list, int data) {
  ListElement<Integer> l = new ListElement<Integer>(data);
  l.setNext(list);
  return l;
}
```

머리 원소에 대한 레퍼런스를 적당히 갱신해줘야 한다.
```java
int data = ....; // 삽입할 데이터
ListElement<Integer> head = ....; // 머리에 대한 레퍼런스 => 원래 머리

head = insertInFront(head, data) => 갱신된 머리
```

##### 리스트 종주
연결 리스트의 첫 번째 원소가 아닌 원소에 대한 연산을 하려면 항상 리스트가 끝나지 않는지 확인을 해야 한다.

```java
public ListElement<Integer> find(ListElement<Integer> head, int data) {
  ListElement<Integer> elem = head;
  while (elem != null && elem.value() != data) { // elem이 null인지 확인한다.
    elem = elem.next();
  }
  return elem;
}
```

> 리스트를 종주할 때는 반드시 연결 리스트가 끝났는지 확인해야 한다.

##### 원소의 삽입 및 삭제
리스트 중간에 요소를 삽입하거나 삭제하려면 그 앞 원소의 연결 고리를 수정해야 한다. 삭제할 원소가 리스트의 head라면 더 주의를 기울여야 한다.

```c++
bool deleteElement(IntElement **head, IntElement *deleteMe) {
  IntElement *elem;

  if (!head || !*head || !deleteMe) 
    return false;

  elem = *head;
  if (deleteMe == *head) {
    *head = elem -> next;
    free(deleteMe);
    return true;
  } 

  while(elem) {
    if (elem -> next == deleteMe) {
      elem -> next = delteMe -> next;
      free(deleteMe);
      return true;
    }
    elem = elem -> next; 
  }
  return false;
}
```

다음 포인터로 넘어가는 작업과 원소를 제거하는 작업중 어느 것을 먼저 해야할까?
다음 포인터로 먼저 넘어가 버리면 제거해야할 원소의 포인터를 뒤집어 쓴 거여서 메모리 해제를 못한다.
원소를 먼저 제거하면 다음 원소에 접근한 next 포인터가 없기 때문에 접근이 불가능하다. 
포인터를 두개 써야 한다. 

```c++
void deleteList(IntElement **head) {
  IntElement *deleteMe = *head;

  while (deleteMe) {
    IntElement *next = delteMe -> next;
    free(deleteMe);
    deleteMe = next;
  }
  *head = NULL;
}
```

### 연결 리스트 문제

##### 스택 구현법
> 스택 자료구조에 대해 논하라. 연결 리스트, 또는 동적 배열을 써서 C로 스택을 구현하고 그 자료구조를 사용한 이유를 설명하라. 완전하고 일관성 있으면서 사용하기 편리한 스택 인터페이스를 설계하라.

1. 기본적인 자료구조에 대한 지식
2. 자료구조를 조작하기 위한 루틴을 만드는 능력
3. 일련의 루틴에 대해 일관성 있는 인터페이스를 설계하는 능력

```python
class Stack :
  def __init__(self):
    self.array = [];

  def push(self, data) :
    return self.array.append(data)

  def pop(self) :
    return self.array.pop()
```

```js
class Stack {
  constructor() {
      this.array = [];
  };

  push(data) {
    return this.array.push(data);
  };

  pop() {
    return this.array.pop();
  };
}
```

연결 리스트에서는 각 원소마다 메모리를 동적으로 할당해야 한다.   
메모리 할당자의 오버헤드에 따라 동적 배열에서 필요한 복사 작업보다 메모리 할당에 더 오랜 시간이 걸릴 수도 있다.   

void 포인터를 저장해서 일반적인 데이터 형을 모두 커버할 수 있도록 만드는 것도 나쁘지 않다.
```c++
typedef struct Element {
  struct Element *next;
  void *data;
} Element;
```

```c++
void push(Element **stack, void *data);
void *pop(Element **stack);
```

c언어로 되어있어서 다르게 짜야하는 부분이 있는 것 같다.   

구현 방법과 무관한 인터페이스, 그리고 일관성 있는 인터페이스를 만들기 위해서는 이 함수에서도 오류 코드를 반환하는 것이 좋다.

```c++
bool createStack(Element **stack);
bool deleteStack(Element **stack);
```

```c++
bool createStack(Element **stack) {
  *stack = NULL;
  return true;
}
```

##### 연결 리스트의 꼬리포인터

```c++
bool delete(Element *elem) {
  Element *curPos = head;

  if(elem == head) { 
    head = elem->next; // head가 elem일때는 head를 변경해주고 true 리턴
    free(elem);
    return true
  }

  while(curPos) {
    if (curPos->next == elem) { // 계속 next를 찾아본다
      curPos->next = elem->next; 
      free(elem);
      if (curPos->next == NULL) {
        tail = curPos;
      }
      return true;
    }
    curPos = curPos->next;
  }

  return false;
}
```

체크리스트
1. 입력이 Null일때 (elem == NULL; return false)
2. 리스트에 원소가 하나도 없는경우
3. 리스트에 원소가 하나뿐인 경우 => tail쪽에서 처리가 필요
4. 리스트에 원소가 두개일 경우

```c++
bool delete(Element *elem) {
  Element *curPos = head;

  if(!elem)
    return false;

  if(elem == head) { 
    head = elem->next; // head가 elem일때는 head를 변경해주고 true 리턴
    free(elem);
    if(!head) {
      tail = NULL;
    }
    return true
  }

  while(curPos) {
    if (curPos->next == elem) { // 계속 next를 찾아본다
      curPos->next = elem->next; 
      free(elem);
      if (curPos->next == NULL) {
        tail = curPos;
      }
      return true;
    }
    curPos = curPos->next;
  }

  return false;
}
```

두 개의 포인터를 엮어서 리스트를 종주하는 방법, curPos는 현재 원소, ppNext는 다음 원소

```c++
bool delete(Element *elem) {
  Element *curPos = NULL, **ppNext = &head;

  if (!elem)
    return false;

  while (true) {
    if (*ppNext == elem) {
      *ppNext = elem->next;
      if(!(elem->next))
        tail = curPos;
      free(elem);
      return true;;
    }
    if(!(curPos = *ppNext))
      break;
    ppNext = &(curPos->next);
  }
  return false;
}
```

##### removeHead의 버그
> 단일 연결 리스트에서 맨 앞에 있는 원소를 제거하기 위한 용도로 만들어진 다음 C 함수에 있는 버그를 찾아내어 수정하라
> ```c++
> void removeHead(ListElment *head) {
>   free(head);
>   head = head->next
> }
> ```

중점적으로 봐야 되는 부분 
1. 데이터가 함수에 제대로 들어오는지 확인한다.
2. 함수의 각 줄이 제대로 작동하는지 확인한다.
3. 함수에서 데이터가 올바르게 나오는지 확인한다
4. 흔히 발생하는 오류 조건을 확인한다

미리 head에 대한 메모리를 해제했기 때문에 따로 변수에 등록해주어야 한다.
```c++
void removeHead(ListElement *head) {
  ListElement *temp = head->next;
  free(head);
  head = temp;
}
```

포인터의 포인터를 입력받고 기존 포인터에 대한 접근은 어떻게 하는거지
```c++
void removeHead(ListElement **head) { // 포인터의 포인터를 입력 받음
  ListElement *temp = (*head)->next;
  free(*head);
  *head = temp;
}
```

head가 Null인 경우 체크
```c++
void removeHead(ListElement **head) {
  ListElement *temp 
  if(head && *head) {
    temp = (*head)->next;
    free(*head);
    *head = temp;
  }
}
```

##### 연결 리스트의 마지막에서 m번째 원소
> 단일 연결 리스트가 주어졌을 때 리스트의 맨 뒤에서 m 번째 원소를 찾아내는 알고리즘을 만들어 보라. 이때 시간 및 공간 효율을 모두 고려해야 한다. 오류 조건의 처리에 주의하여 알고리즘을 구현하라. 여기에서 '맨 뒤에서 m번째 원소'는 m = 0일 때 리스트의 마지막 원소를 반환하는 식으로 생각한다.

어떤 원소로부터 m개 만큼 이동했을 경우 마지막 원소가 나오는 방법도 접근 가능하지만 이건 O(mn) => 더 효율적인 방법을 찾아보자

리스트를 한번 쫙 돌리고 각각의 원소에 대한 포인터를 따로 저장해두는 방법이면 O(n)으로 돌릴수 있다. 그러나 메모리가 엄청 커질수 있다는 변수는 있다.
**별도로 저장해두어야 하는 리스트의 크기를 m으로 일정하게 유지하면 메모리 제약도 피해갈 수 있다!!**

따져야 하는 오류 조건 
1. 리스트에 있는 원소 개수가 m개 미만일 경우

```c++
ListElement *findMToLastElement(ListElement *head, int m) {
  ListElement *current, *mBehind;
  int i;
  if (!head)
    return NULL;
  /* 리스트가 끝나지 않는지 확인하면서
  * 앞에서부터 m 개의 원소를 센다.
  */
  current = head;
  for (i = 0; i< m; i++) {
    if (current->head) {
      current = current->next;
    } else {
      return NULL;
    }
  }

  /* mBehind를 head 포인터로 설정한 다음 current 포인터가 마지막
  * 원소를 가리키게 될 때까지 mBehind와 current를 함께 전진시킨다.
  */
  mBehind = head;
  while(current->next){
    current = current->next;
    mBehind = mBehind->next;
  }

  return mBehind;
}
```

##### 리스트 단층화

<img src="https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Ffe36c659-23c6-4da2-8ec4-ae41ccf69c46%2FUntitled.png?table=block&id=d06ee70c-0908-4343-abad-ee654888936d&spaceId=359809db-cb83-47c2-9cce-0c45f96418ab&width=1470&userId=56059f96-1ce0-4d35-87f6-3200db26ea2a&cache=v2"/>

```c++
typedef struct Node {
  struct Node *next;
  struct Node *prev;
  struct Node *child;
  int value;
} Node;
```

여기에서는 연결 리스트를 따라서 종주하면서 모든 자식 포인터를 확인하는 정도로만 수정하면 된다.    
매번 노드를 확인할 때마다 그 노드를 다른 리스트에 복사해 두면 결과적으로 단층화된 리스트가 만들어 지게 된다 ?????

<img src="https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F8ac740d6-e1cf-47fa-be5b-3140c51a442c%2FUntitled.png?table=block&id=ca7773ff-0ff9-486d-89f2-76352071eb0b&spaceId=359809db-cb83-47c2-9cce-0c45f96418ab&width=1470&userId=56059f96-1ce0-4d35-87f6-3200db26ea2a&cache=v2">

dfs 방식으로 접근 하는것 같다
```
첫째 층 맨 앞에서 시작
첫째 층이 끝나지 않은 동안 
  현재 노드에 자식이 있으면
      자식을 첫째 층 맨 뒤에 추가
      꼬리 포인터 갱신
  다음 노드로 이동
```

```c++
void flattenList(Node *head, Node **tail) {
  Node *curNode = head;
  while (curNode) {
    if (curNode->child) {
      append(curNode->child, tail);
    }
    curNode = curNode->next;
  }
}

void append(Node *child, Node *tail){
  Node *curNode;

  (*tali)->next = child;
  child->prev = *tail;

  for (curNode=child;curNode->next;curNode = curNode->next)
    생략
  *tail = curNode;
}
```

##### 리스트 단층화 해제
> 리스트 단층화를 해제하라. 자료구조를 flattenList로 전달하기 전의 원래 상태로 복구 시켜야 한다.

어떤 노드가 자식인지 어떻게 판단하지??? -> 그 앞 노드의 포인터를 일일히 확인해야 함.
자식이 있는 노드를 발견할 때마다 그 자식을 바로 앞 노드로부터 분리해낸 다음 새로운 자식 리스트를 종주하고, 종주가 끝나면 원래의 자식 리스트를 계속해서 종주하면 된다.
(Node 구조체에 child가 있으므로 자식 유무 판단 가능)
```
경로 탐색:
  끝에 도달하기 전까지
    현재 노드에 자식이 있으면
      자식을 이전 노드로부터 분리
      자식에서 시작하는 경로 탐색
    다음 노드로 넘어감
```

```c++
void unflatten(Node *start, Node **tail) {
  Node *curNode;
  exploreAndSeparate(start);

  for (curNode=start; curNode->next; curNode=curNode->next) 

  *tail = curNode;
}

void exploreAndSeparate(Node *childListStart) {
  Node *curNode = childListStart;

  while (curNode) {
    if (curNode->child) {
      curNode->child->prev->next = NULL;
      curNode->child->prev = NULL;
      exploreAndSepartate(curNode->child);
    }
    curNode = curNode->next;
  }
}
```

##### 순환형 리스트와 비순환형 리스트
<img src="https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Facffadd1-5211-413e-a6cc-3204c790a960%2FUntitled.png?table=block&id=087748f3-7eeb-4504-911f-18e164215e69&spaceId=359809db-cb83-47c2-9cce-0c45f96418ab&width=1470&userId=56059f96-1ce0-4d35-87f6-3200db26ea2a&cache=v2">

비순환형 리스트에서는 NULL 포인터가 들어있는 노드가 나올 때까지 리스트를 종주하면 된다.
순환형 리스트에서는 같은 노드를 참조하는 포인터가 두개다.
메모이제이션 사용해서 조지는게 좋을듯 => 검사하는 리스트와 같은 메모리의 리스트가 생긴다.

포인터를 두개 사용해서 한 개는 빠르게 한 개는 느리게 가게 하고 빠르게 가는 포인터가 느리게 가는 포인터를 앞지르면 순환형 리스트다

```
느린 포인터는 리스트 머리에서 시작
빠른 포인터는 리스트 두 번째 노드에서 시작
무한루프
  빠른 포인터가 널 포인트에 도달하면
    리스트가 널로 끝났음을 알리는 값을 반환
  빠른 포인터가 느린 포인터를 따라잡거나 지나쳐 버리면
    순환형 리스트임을 알리는 값을 반환
  느린 포인터를 한 노드 앞으로 전진
  빠른 포인터를 두 노드 앞으로 전진
```

```c++
bool isCycliList(Node *head) {
  Node *fast, *slow;
  if(!head) 
    return false;
  slow = head;
  fast = head->next;
  while (true) {
    if (!fast || !fast->next)
      return false;
    else if (fast == slow || fast->next == slow)
      return true;
    else {
      slow = slow->next;
      fast = fast->next->next;
    }
  }
}
```