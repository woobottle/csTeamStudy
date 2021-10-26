# 연결 리스트
 - 단일 연결 리스트
 - 이중 연결 리스트
 - 원형 연결 리스트

<br />

 ### 단일 연결 리스트
 ![스크린샷 2021-10-25 오후 9 28 52](https://user-images.githubusercontent.com/72545106/138695139-767dbf71-efc5-4556-9b19-a15a788f265b.png)

 - data, link가 하나의 노드로 구성되며 첫번째 노드를 head, 마지막 노드를 tail이라 한다.
 - tail의 link는 null

 ``` c++
class IntElement {
  public:
    IntElement( int value): next( Null ), data( value ) {}
    ~IntElement() {}

    IntElement *getNext() const { return next; }
    int value() const { return data; }
    void setNext( IntElement *elem ) { next = elem; }

  private:
    IntElement *next;
    Int data;
 }
 ```
  - 자바에는 포인터가 없으므로 레퍼런스를 씀.

<br/>

### 이중 연결 리스트
- 단일 연결 리스트는 단방향으로 밖에 순회하지 못함.
- 이러한 단점을 보완한 이중 연결 리스트는 양방향으로 순회할 수 있음.

<br />

### 원형 연결 리스트
- head와 tail이 없어 무한루프를 돌 수 있음. 시작점을 제대로 추적해야함. 이러한 사이클 회피 문제가 많이 나옴.

<br/>

## 연결 리스트 연산 (단일 연결 리스트)
### head 추적
- 리스트의 첫 번째 원소를 제거하거나 첫 번째 원소 앞에 추가하는 경우 head에 대한 포인터를 갱신해야함.
- 또, 리스트를 변형할 때 head를 제대로 추적해야함.

### 리스트 종주
- 리스트의 첫번째 원소가 아닌 원소에 대한 연산시 종주가 필요할 수 있음.
- 리스트가 tail에 도달했는지 확인이 필요. 예외처리.
```java
public ListElement<Integer> find(ListElement<Integer>head, int data) {
  ListElement<Integer> elem = head;
  while( elem != null && elem.value() != data) {
    elem = elem.next();
  }
  return elem;
}
```
- 메서드를 호출하는 쪽에서 return 값이 null이 아닌지 확인하는 예외처리도 필요.

### 원소 삽입 & 삭제
- 리스트의 노드들은 다음 노드에 대한 link를 통해서만 관리되기 때문에 중간에 노드를 삽입 또는 삭제하려면 그 앞 노드의 link를 수정해야함. 
- 삭제할 노드만 지정된 상황이면 해당 노드의 이전 노드를 알 수 없으므로 리스트 종주가 필요함.
- 삭제할 노드가 리스트의 head이면 더 주의가 필요.
- C나 C++처럼 가비지 컬렉터가 없는 경우에는 포인터를 두개 써야함. 노드를 제거하는 작업과 다음 포인터로 넘어가는 작업이 충돌하기 때문.
  - 다음 포인터로 넘어가는 작업을 먼저 할 경우 제거해야할 노드의 링크를 덮어쓴 상황이기 때문에 메모리 할당을 해제할 수 없음.
  - 노드를 제거하는 작업을 먼저 할 경우 링크가 제거됐기 때문에 다음 노드로 이동이 불가능함.
```c
void deleteList( IntElement **head )
{
  IntElement *deleteMe = *head;

  while( deleteMe ) {
    IntElement *next = deleteMe -> next;
    free( deleteMe );
    deleteMe = next;
  }

  *head = NULL;
}
```

<br/>

## 문제
### 스택구현
> 스택 자료구조에 대해 논하라. 연결 리스트, 또는 동작 배열을 써서 C로 스택을 구현하고 그 자료구조를 사용한 이유를 설명하라. 완전하고 일관성 있으면서 사용하기 편리한 스택 인터페이스를 설계하라.
- 동적 배열은 인덱스만 알면 어떤 노드든 즉시 접근이 가능하다는 장점이 있지만, 후입선출(push, pop)이라는 스택의 특징 때문에 위 장점이 별로 효과가 없고 동적 배열의 크기가 증가하면 length를 조절해야하고 이 과정에서 모든 원소들을 새 배열로 복사해야한다.
- pop시 스택이 비어있다면 오류코드를 리턴하고 비어있지 않다면 해당 데이터 리턴.

```c++
typedef struct Element {
  struct Element *next;
  void *data;
}

bool createStack(Element **stack) {
  // stack pointer
  *stack = NULL;
  return true;
}

// 함수를 호출한 쪽의 포인터를 변경하기 위해 이중 포인터 사용

bool push( Element **stack, void *data) {
  Element *elem = new Element;
  if (!elem) return false;

  elem->data = data;
  elem->next = *stack;
  *stack = elem;
  return true
}

bool pop( Element **stack) {
  Element *elem;
  if (!(elem = *stack)) return false;

  *data = elem->data;
  *stack = elem->next;
  free(elem);
  return true
}

bool deleteStack( Element **stack ) {
  Element *next;
  while( *stack ) {
    next = (*stack)->next;
    free( *stack );
    *stack = next;
  }
  return true;
}

```
- 객체지향의 경우 위 createStack과 deleteStack을 constructor와 destructor로 만들 수 있음.

<br/>

### 연결 리스트의 꼬리 포인터
> 정수를 저장하기 위한 어떤 단일 연결 리스트의 첫번째와 마지막 원소를 가리키는 Head와 tail이라는 전역 포인터가 있다. 다음과 같은 함수 원형에 대한 C 함수를 구현하라.   
*bool delete(Element *elem);**  
*bool insertAfter(Element *elem, int data);**  
delete 함수의 인자는 삭제할 원소. insertAfter의 인자는 새로 추가될 원소의 바로 앞 원소에 대한 포인터와 새로 추가될 데이터. NULL을 넘겨줄 경우 리스트 맨 앞에 추가. 성공적으로 실행시 true, 아니면 false. head와 tail 포인터는 항상 최신 값 유지.
- head와 tail 포인터는 리스트의 맨 앞 혹은 맨 뒤의 노드가 바뀔때 바꿔준다.
- 맨 앞, 중간, 맨 뒤에 따라 다른 방식으로 처리해야 함.
- 중간과 맨 뒤에 있을 경우 리스트 순회가 필요함.
``` c++
bool delete ( Element *elem ) {
  Element *curPos = head;
  // 순회시 elem과 같은지 판단할 현재 노드.

  if ( !elem ) return false;
  // elem 이 NULL일 때 노드를 순회하는 것은 비효율 적이므로 바로 false를 return하는게 효율적일 듯.

  if ( elem == head ) {
    head = elem->next;
    // elem의 포인터가 가리키는 곳. 여기서는 다음 노드.
    free(elem);

    if (!head) tail = NULL;
    //노드가 하나 뿐인 리스트의 경우. 위에서 head가 NULL이 됐고 메모리도 해제됐으나 tail은 여전히 제거한 노드를 가리게 됨. 이를 해제하는 작업.
    return true;
  }

  while (curPos) {
    if (curPos->next == elem) {
      curPos->enxt = elem->next;
      free(elem);
      if (curPos->next == NULL)
        tail = curPos;
        // 다음 노드가 마지막 노드일시 현재 순회 중인 노드를 tail로.
      return true
    }
    curPos = curPos->next;
  }
  return false
}
```

``` c++
bool insertAfter ( Element *elem, int data ) {
  Element *newElem, *curPos = head;
  // elem = 새로 추가될 원소의 바로 앞 원소에 대한 포인터
  newElem = malloc( sizeOf(Element) );
  // 새로운 elem를 메모리에 할당.

  if ( !newElem ) return false;
  newElem->data = data;
  
  // 맨 앞에 삽입
  if ( !elem ) {
    newElem->next = head;
    head = newElem;
    
    //비어있는 리스트의 경우
    if (!tail) tail = newElem;
    return true;
  }

  while (curPos) {
    if (curPos == elem) {
      newElem->enxt = curPos->next;
      curPos->next = newElem;
      
      //리스트 맨 뒤 추가.
      if ( !(newElem->next) ) tail = newElem;
      return true
    }
    curPos = curPos->next;
  }
  //삽입할 위치를 찾지 못한 경우. 할당된 메모리를 비우고 false 반환.
  free( newElem );
  return false
}
```

### remove Head의 버그
> 단일 연결 리스트에서 맨 앞의 있는 원소를 제거하기 위한 용도로 만들어진 다음 C 함수에 있는 버그를 찾아내어 수정하라.
``` c
void removeHead( ListElement *head ) {  
  free( head );  
  head = head->next
  // 이미 메모리에서 지워진 데이터를 참조.
}
```
- 주어진 코드의 분량이 적기 때문에 실제 디버깅과는 다른 전략 필요.
  - 데이터가 함수에 제대로 들어오는지 확인. 없는 변수 혹은 타입 체크.
  - 함수의 각 줄이 제대로 동작하는지 확인.
  - 함수에서 데이터가 올바르게 리턴되는지 확인.
  - 흔히 발생하는 오류 조건 확인
    - NULL ptr가 인자로 들어오는 경우
    - 메모리 할당이나 입출력 오류.
  

위 함수는 다음과 같이 수정 가능하다.
``` c
// *head 매개변수를 사용하면 호출하는 쪽의 head를 바꿀 수 없다.
void removeHead( ListElement **head ) {    
  ListElement *temp;  

  if (head && *head) { // 노드가 하나도 없는 경우.
    temp = (*head)->next; // 메모리에서 제거하기 전에 미리 할당해놓음.
    free( *head );  
    *head = temp;
  }
}
```
- c에서는 변수를 레퍼런스로 전달할 수 없기 때문에 변경하고자 하는 변수에 대한 포인터를 전달하는 방법을 사용해야함.

<br/>

### 연결 리스트의 마지막에서 m번째 원소
> 단일 연결 리스트에서 m번째 원소를 찾아내는 알고리즘 구현. 시간 및 공간 효율 모두 고려할 것. 오류 조건 처리에 유의. m = 0인 경우 tail 반환.
- 단일 연결 리스트에서는 head에서 tail로 단방향 순회만 가능함. 
- 리스트의 길이가 n일 때 어떤 노드로부터 m개만큼 앞으로 이동했을 때 리스트의 마지막 노드가 나온다면 우리가 찾는 노드일 것. 하지만 시간복잡도는 O(mn).
- 1 = n-m으로 계산. O(n). 하지만 기존 자료구조를 바꾸거나 자료구조에 액세스하는 메서드에 특별한 제약 조건을 가하지 않는 풀이를 원할 것임.
- 리스트를 순회하면서 노드를 별도로 저장한다면 시간 복잡도는 O(n)으로 줄어들지만, m이 커지면 임시 데이터를 저장하는 공간도 커져야 하기 때문에 공간 효율이 좋지 못함.
  - 모든 데이터를 저장하는 것이 아닌 m번째 앞에 있는 원소에 대한 포인터를 저장한다.

```c
  // 두 개의 포인터를 이용하여 m만큼 간격을 두고 두 포인터 모두 순회 시작. 먼저 m만큼 이동한 포인터가 tail에 도달할 때까지 포인터를 계속 순회. 도달시 m만큼 뒤에 있는 mBehind를 리턴함.
  ListElement *findMToLastElement( ListElement *head, int m) {
    ListElement *current, *mBehind;
    int i;
    // 예외처리
    if ( !head ) return null

    current = head;
    
    for ( i = 0; i < m; i++ ) {
      if (current->next) {
        current = current->next;
      } else {
        return NULL;
      }
    }

    mBehind = head;
    while ( current->next ) {
      current = current->next;
      mBehind = mBehind->next;
    }

    return mBehind;
  }
``` 

<br/>

### 리스트 단층화
> 다층 이중 연결리스트를 단층화하여 한 층 짜리 이중 연결리스트를 구현 하는 문제. 각 층은 아래의 c struct로 이루어져 있음.

```c
typedef struct Node {
  struct Node *next;
  struct Node *prev;
  struct Node *child;
  int value;
} Node;
```


![스크린샷 2021-10-26 오후 10 31 05](https://user-images.githubusercontent.com/72545106/138889340-72864ca8-d619-4dd7-8394-2a0ed223722e.png)

### 풀이법들
- 트리 순회 알고리즘을 사용하되 sibling들을 순회하는 알고리즘 추가하여 사용.
  - 각 노드를 한 번씩 검사하므로 시간 복잡도는 O(n)
  - 재귀로 인한 오버헤드
  - 새 리스트를 만들기 위한 노드의 복사본.
- 각 층을 저층부터 순서대로 나열.
  -  너비우선 탐색 사용(효율 bad)
- 자식 리스트를 하나씩 첫째층의 맨 뒤에 추가하는 방법.(그나마 최선)
  - 리스트 순회 필요. child가 있는 노드 등장시 그 자식을 첫째 층 tail로 갱신.
  - 첫번째 노드를 제외한 층들은 자식 노드를 추가할때마다 tail을 갱신하기 위해 자식 리스트 전체를 순회해야하고 자식이 있는지 다시 한번 확인해야하기 때문에 두번씩 순회해야함. 
  - 2n번 순회하면 되므로 O(n)

``` c
  void flatternList( Node *head, Node **tail ) {
    Node *curNode = head;
    while ( curNode ) {
      if ( curNode->child ) {
        append( curNode->child, tail );
      }
      curNode = curNode->next;
    }
  }

  //자식 리스트를 tail 뒤에 붙이고 tail 포인터 갱신
  void apeend( Node *child, Node **tail ) {
    Node *curNode;

    (*tail)->next = child;
    child->prev = *tail;

    // tail이 될 자식 리스트의 끝을 탐색.
    for ( curNode = child; curNode->next; curNode = curNode->next) {
     ... 
    }

    // tail pointer 갱신.
    *tail = curNode;
  }
```

<br/>

### 리스트 단층화 해제
> 리스트 단층화를 해제하라. 위 함수에 전달하기 전의 상태로 복구.
- 단층화 리스트 로직 정반대로 구현.
  - tail에서 시작하여 첫째 층 부분 분리.
  - 자식 리스트의 시작부분에 해당하는 곳에 도달할 때마다 리스트를 분리. 
  - but, 어떤 노드가 자식이었는지 판단이 어려움. 자식인지 판단하기 위해서는 자식 포인터를 일일이 확인해야함. 효율이 별로.
- 자식 노드에 대한 포인터를 전부 저장.
  - 별도의 자료구조를 만들어야하는 점이 별로.
- 순회하면서 재귀적으로 자식리스트 순회.
  - O(n). 이 방법 사용.

```c
void unflatten( Node *start, Node **tail ) {
  Node *curNode;

  exploreAndSeperate( start )

  for (curNode = start; curNode->next; curNode = curNode->next) {
    ...
  }
  *tail = curNode;
}

void exploreAndSeperate( Node *childListStart ) {
  Node *curNode = childListStart;

  while( curNode ){
    if ( curNode->child ) {
      curNode->child->prev->next = NULL;
      curNode->child->prev = NULL;
      exploreAndSeperate( curNode->childe )
    }
  }
  curNode = curNode->next;
}
```

재귀보단 반복문이 더 효율적일지도
```c
void unflattenIterative(Node *start, Node** tail){
  if (!(*tail)) return;
  while (tracker) {
    if (tracker->child) {
      *tail = tracker->child->prev;
      tarcker->child->prev = NULL;
      (*tail)->next = NULL;
    }
    tracker = tracker->prev;
  }
}
```

### 순환형 리스트와 비순환형 리스트
> 리스트의 *head를 받아 그 리스트가 순환형인지 비순환형인지 알아내는 함수를 작성. 비순환형이면 false, 순환형이면 true 반환.
>> 비순환형 : NULL로 종료되는 연결리스트  
순환형 : 사이클로 연결되는 연결리스트

- 순환형에서는 tail을 찾기 쉽지 않음.
- 순환형에서는 같은 노드를 가리키는 포인터가 두 개 무조건 존재. 하지만 이를 체크하는 것은 쉽지 않음.
- 이미 지나간 노드인지 체크.
  - 새로운 리스트를 만들기엔 비효율적임.
- 현재 노드의 next 포인터를 그 앞에 있던 모든 노드의 next 포인터와 직접 비교.
  - O(n^2) 
- ***속도가 다른 두 포인터를 사용.*** 
  - 빨리 움직이는 포인터가 느린 포인터를 앞 질러가는 일이 발생. 앞 질러 간다면 그 리스트는 순환형.
  - O(n)

```c
  bool isCyclicList( Node *head ) {
    Node *fast, *slow;
    if ( !head ) return false;
    slow = head;
    fast = head->next;
    while( true ) {
      if ( !fast || !fast->next ) 
        return false
      else if ( fast = slow || fast->next == slow)
        return true;
      else {
        slow = slow->next;
        fast = fast->next->next;
      }
    }
  }
```