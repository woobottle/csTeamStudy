# 5. 연결리스트

* 별거 아닌 것 처럼 보이지만 동적인 데이터를 처리하는 것과 관련된 수많은 문제의 근간을 이루는 자료 구조

## 왜 연결 리스트인가?

* 단순한 편이라 한 시간에 두세 문제를 내야하는 인터뷰 특성에 잘 맞아 떨어진다.

## 연결 리스트의 종류

### 단일 연결 리스트

* '연결 리스트'면 보통 이거임 

```c
typedef struct IntElement{
  struct IntElement *next;
  int data;
} IntElement;
```

```c++
class IntElement{
  public:
  	IntElement( int value ):next(Null), data(value){}
  ~IntElement(){}
  
  IntElement *getNext() const { return next; }
  int value() const { return data; }
  void setNext(IntElement *elem){ next = elem; }
  void setValue( int value ) { data = value; }
  private:
  	IntElement *next;
    int data;
}

// template으로 
template <class T>
class ListElement{
  public:
  	ListElement( const T &value ):next(Null), data(value){}
  ~ListElement(){}
  
  ListElement *getNext() const { return next; }
  const T& value() const { return data; }
  void setNext(ListElement *elem){ next = elem; }
  void setValue( int value ) { data = value; }
  private:
  	ListElement *next;
    T data;
}
```

```java
public class ListElement<T>{
  public ListElement( T value ){ data = value; }
  public ListElement<T> next(){ return next; }
  public T value() { return data; }
  public void setNext( ListElement<T> elem ){ next = elem; }
  public void setValue(T value){ data = value; }
  private ListElement<T> next;
  private T data;
}
```

### 이중 연결 리스트

* 이거 쓰면 쉬워지는 경우도있고, 불필요하게 복잡한 경우도 있어서 면접문제로 그리 많이 안나움

### 원형 연결 리스트

* 단일 - 이중 둘다 있고, 없으면 자기자신 
* 사이클 회피 문제가 많이 나옴, 시작점을 제대로 추적하지 않으면 리스트에서 무한 루프

## 기초적인 연결 리스트 연산

### 머리 원소 추적

* 머리 원소를 추적해야함 그러지 않으면 언어에 따라 가비지 컬렉터에 의해 제거되거나 어딘가에서 길을 잃음
* 새 원소를 첫 번째 원소 앞에 추가하거나, 첫 원소 제거할 때 포인터를 갱신해줘야함
* 머리 원소를 제대로 추적 할 수 있도록 주의

```java
public void insertInFront(ListElement<Integer> list, int data){
  ListElement<Integer> l = new ListElement<Integer>(data);
  l.setNext(list);
}
// ||
//

public ListElement<Integer> insertInFront(ListElement<Integer> list, int data){
  ListElement<Integer> l = new ListElement<Integer>(data);
  l.setNext(list);
  return l;
}

int data = ...;
ListElement<Integer> head = ....;
head = insertInFront(head, data);
```



```c++
bool insertInFront( IntElement *head, int data){
  IntElement *newElem = new IntElement;
  if(!newElem) return false;
  newElem->data = data;
  newElem->next = head;
  head = newElem;// -> 지역 변수만 바꿈 사본만 갱신함
  return true
}

bool insertInFront( IntElement **head, int data){
  IntElement *newElem = new IntElement;
  if(!newElem) return false;
  newElem->data = data;
  newElem->next = *head;
  *head = newElem;// -> 
  return true
}
```

### 리스트 종주

**항상 리스트가 끝나지 않는지 확인을 해야함**

```java
public ListElement<Integer> find(ListElement<Integer> head, int data){
  ListElement<Integer> elem = head;
  while(elem.value() != data){
    elem = elem.next();
  }
  return elem;
}
```

* 찾아낼 객체가 있으면 갠춘한데, NullReferenceException

```java
public ListElement<Integer> find(ListElement<Integer> head, int data){
  ListElement<Integer> elem = head;
  while(elem != null && elem.value() != data){
    elem = elem.next();
  }
  return elem;
}
```

### 원소의 삽입 삭제

* 리스트 중간에서 원소를 삽입/삭제 하려면 그 앞 원소의 연결고리 수정해야함
* 리스트 종주 해야만 할 수도 있음

```c
bool deleteElement( IntElement **head, IntElement *deleteMe){
  IntElement *elem;
  if (!head || !*head || !deleteMe )
    return false;
  if(deleteMe == *head){
    *head = elem->next;
    free(deleteMe);
    return true;
  }
  while(elem){
    if(elem->next == delete){
      elem->next = deleteMe->next;
      free(deleteMe);
      return true;
    }
    elem = elem->next;
  }
  return false
}
```

* 가비지 컬렉션이 없는 언어에서 연결 리스트에 있는 모든 원소를 지울 떄
  * 삭제할 때는 포인터 두개 써야함
  * 다음 포인터로 넘어가는 일, 제거하는 작업 / 먼저 넘어가면 덮어 씌니까 할당 해제 안되고, 삭제 먼저도 뭐 ..
  * 종주하면서..

```c++
void deleteList( IntElement **head ){
  IntElement *deleteMe = *head;
  while( deleteMe ){
    IntElement *next = deleteMe->next;
    free(deleteMe)
    deleteMe = next;
  }
  *head = NULL;
}
```



## 연결 리스트 문제

### 스택 구현법

> 스택 자료구조에 대해 논하라, 연결 리스트 또는 동적 배열을 써서 C로 스택을 구현하고 그 자료구조를 사용한 이유를 설명하라, 완전하고 일관성 있으면서 사용하기 편리한 인터페이스를 설계하라

1. 기본적인 자료구조에 대한 지식
2. 자료구조를 조작하기 위한 루틴을 만드는 능력
3. 일련의 루틴에 대한 일관성 있는 인터페이스를 성계하는 능력

* 동적 배열은 임의 접근이 가능하지만 스택은 한쪽 끝에 대해서만 연산이 이뤄지므로 장점을 발휘할게 없음
* 동적 배열은 커지면 그에 맞춰 크기를 조절해야 하므로, 그 과정에서 기존 배열의 모든 원소들을 새 배열로 복사해야하므로 오래걸림

* 연결 리스트에선 각 원소마다 메모리를 동적으로 할당, 오버헤드에 따라 동적배열보다 더 오래 걸릴 수 있음
* 동적배열에서 인접한 원소는 메모리상에서도 인접하지만 / 연결리스트에서 인접한 원소는 메모리상에서 떨어져 있을 수도 있다.
* https://bluejake.tistory.com/44
* -> 인덱스 곱 이라서 그런듯? 주소 확인 하고 들어가는거랑, 자료형 크기 곱 인덱스 곱으로 주소 확인하는거랑?

```c
typedef struct Element{
  struct Element *next;
  void *data;
}Element;
```

* 자료형은 범용성 있게

```c
void push(Element *stack, void *data);
void *pop(Element *stack)
```

* 이제 기능과 오류처리
* 두 연산 모두 리스트의 첫 원소를 변경함, 함수를 호출하는 루틴의 스택 포인터를 변경해야함. 
* 스택에 대한 포인터에 대한 포인터를 받도록 한다. - 그니까 포인터를 변경 해야하는거니까. 포인터의 포인터

```c++
void push(Element **stack, void *data);
void *pop(Element **stack)
```

* 푸시에서 새 원소 만들면서 메모리 할당,
  * 할당 실패 확인 코드 에러처리
* 푸시 성공하면 알아낼 수 있도록 반환값
* pop에서 비어있는 스택에서 팝 연산을 한다면?
  * 이거도 알려줘야하는데...
* 일관성 있게 둘다 반환을 성공/실패 여부로 하고 매개변수로 아웃풋

```c++
bool push(Element **stack, void *data);
bool pop(Element **stack, void **data);
```



```c++
bool createStack( Element **stack);
bool deleteStack( Element **stack);
```

* 스택의 인터페이스를 만들고, 자료구조를 변경해도 뜯어고치는게 가능하도록 함수 만들어야함

```c++
bool createStack( Element **stack){
  *stack = NULL;
  return true;
}
// 스택 포인터를 NULL로 하고 실행 성공적으로 끝났음을 알린다.

bool push(Element **stack, void *data){
  Element *elem = new Element;
  // 새 원소를 할당하고
  if(!elem) return false;
  // 메모리 할당 과정에서 문제 없는지 확인
  elem->data = data;
  //데이터를 설정하고
  elem->next = *stack;
  //스텍 맨 위에 두고
  *stack = elem;
  //포인터를 조정
  return tru;
}

bool pop(Element **stack, void **data){
 	Element *elem;
  if(!(elem = *stack)) return false;
  //비어있나 확인
  
  *data = elem->data;
  //맨 위의 데이터를 가져오고
  *stack = elem->next;
  // 포인터 변경
  free(elem);
  // 메모리 할당을 해제
  return true;
}
bool deleteStack( Element **stack){
  Element *next;
  while(*stack){
    next = (*stack)->next;
    free(*stack);
    *stack = next;
  }
  return true;
}
```

* 객체지향쪽에선 생성자와 파괴자쪽에 만들면 될듯
* c에서 void *으로 유형 캐스팅 오류 걱정 안해도 됨

* C++에서 하려면 복사 생성자랑 대입 연산자도 만들어야함



## 연결 리스트의 꼬리 포인터

> 정수를 저장하기 위한 어떤 단일 연결 리스트의 첫 번째와 마지막 원소를 가리키는 head와 tail이라는 전역 포인터가 있다. 다음과 같은 함수 원형에 대한 C 함수를 구현하라.
>
> ````c
> bool delete(Element *elem);
> bool insertAfter(Element *elem, int data);
> ````
>
> delete 함수의 인자는 삭제할 원소, insertAfter 함수의 두 인자는 각각 새로 추가되는 원소의 바로 앞 원소에 대한 포인터와 새 원소의 데이터다. insertAfter 함수를 호출할 때 NULL을 넘겨주는 방식으로 리스트 맨 앞에도 새 원소를 추가할 수 있어야한다. 함수가 성곡적으로 실행되면 true 아니면 false
>
> head / tail은 항상 최신값으로 유지

* 나머진 비슷하고 머리랑 꼬리 포인터만 제대로 고쳐주면 될듯
* 맨앞이나 맨 뒤에 새 원소를 추가하면 새로 추가된 원소가 맨 앞에 있는 원소 혹은 맨 뒤가 됨
* 삭제하면 두번쨰가 되는거고
* 양 끝에서, 특이한 케이스가 발생할 수 있음
* 길이가 0 , 1, 2 일떄를 확인한다.

```c
bool delete(Element *elem){
  if(elem == head){
    head = elem -> next;
    free(elem);
    return true;
  }
}
```

* current position이 필요함

```c
bool delete ( Element *elem ) {
  Element *curPos = head;

  if ( !elem ) 
    return false;

  if ( elem == head ) {
    head = elem->next;
    free(elem);

    if (!head) 
      tail = NULL;
    //tail도 Null로 해주기
    
    return true;
  }

  while (curPos) {
    if (curPos->next == elem) {
      // 순회하면서 찾고,
      curPos->next = elem->next;
      // 변경~
      free(elem);
      if (curPos->next == NULL)
        tail = curPos;
     // 만약 next 없으면 tail~
      return true
    }
    curPos = curPos->next;
  }
  return false
}

```

* NULL이 들어올 때랑 길이에따라 문제 확인

* NULL이면 그냥 리턴

* 원소가 하나뿐이라면 head / tail 둘다 하나 가리켜야함 지우면 둘다 널

```c++
bool insertAfter ( Element *elem, int data ) {
	Element *newElem, *curPos = head;
	newElem = malloc( sizeOf(Element) );
	if(!newElem) 
    return false;
	newElem->data = data;

  if(!elem){
	  newElem->next = head;
  	head = newElem;
	  if (!tail) 
      tail = newElem;
	  return true;
  }
  while (curPos) {
    if (curPos == elem) {
      newElem->enxt = curPos->next;
      curPos->next = newElem;

      if (!(newElem->next)) 
        tail = newElem;
      return true
  	}
  	curPos = curPos->next;
  }
  free(newElem);
  return false
}

```

* 비슷함
* 코드가 이쁘진 않음

```c++
bool delete ( Element *elem ) {
  Element *curPos = NULL, **ppNext = &head
  if ( !elem ) 
    return false;

  while (true) {
    if (*ppNext == elem) {
      *ppNext->next = elem->next;
      if (!(elem->next))// 마지막 원소 지울때 tail 갱신
        tail = curPos;
      free(elem);
      return true
    }
    if(!(curPos = *ppNext))
       break;
    ppNext = &(curPos->next);
  }
  return false
}
```

```

```





## removeHead의 버그

>단일 연결 리스트에서 맨 앞에 있는 원소를 제거하기 위한 용도로 만들어진 다음 C함수에 있는 버그를 찾아어 수정하라
>
>```c
>void removeHead(ListElement *head){
>  free(head);
>  head = head->next;
>}
>```

* 실제 프로그래밍 할 때 버그를 잡아내는 방법하고 조금 다른 전략을 써야함
* 다른 모듈과 상호 작용 걱정 X 대신 디버거 안쓰고 체계적으로 분석

1. 데이터가 함수에 제대로 들어오는지 확인 - 없는 변수 , 타입 캐스팅 등
2. 함수의 각 줄이 제대로 동작하는지 확인 - 올바르게 실행되는지, 의도된 결과가 만들어지는지
3. 함수에서 데이터가 올바르게 나오는지 확인 - 예상되는 결과가 반환값으로 돌아가야한다. 호출한 쪽 변수 갱신도 확인
4. 흔히 발생하는 오류 조건을 확인 - 경계값, 널값, 등

head 지워버리고 참조하니까 문제

```c++
void removeHead(ListElement *head){
  ListElement *temp = head->next;
  free(head);
  head = temp
}
```

* 명시적인 반환값은 없지만 암묵적으로 반환을 하지?
* head바뀌어야하는데...

```c++
void removeHead(ListElement **head){
  ListElement *temp = (*head)->next;
  free(*head);
  *head = temp
}
```

* NULL이면 free x 

```c++
void removeHead(ListElement **head){
  ListElement *temp
  if(head && *head){
    temp = (*head)->next;
    free(*head);
    *head = temp
  }
}
```



## 연결 리스트의 마지막에서 m번째 원소

> 단일 연결 리스트가 주어졌을 때 리스트의 맨 뒤에서 m번째 원소를 찾아내는 알고리즘을 만들어 보라.
> 이때 시간 및 공간 효율을 모두 고려해야한다. 
> 오류 조건의 처리에 주의하여 알고리즘을 구현하라. 여기에서 맨 뒤에서 m번째 원소는 m=0일 때 리스트의 마지막 원소를 반환하는 식으로 생각한다.

* 단일 연결 리스트는 맨 앞에서부터 m번째 원소를 찾아내는 것은 정말 쉽다.
* 뒤에서 m번째 원소를 찾는다면, 단일 연결 리스트 말고 다른 자료구조를 쓰는 것이 더 낫지.. 이중 연결 리스트나 동적 배열

1. 어떤 원소로부터 m만큼 갔을 때 마지막이 나오면 그 원소임 / 근데 리스트 길이가 n이라면 O(mn) 임?

2. 임시로 레퍼런스를 저장해두면? O(n) 이지만 공간 복잡도도..

3. `l+m=n, l=n-m`,  그 원소가 `l`번째라면 앞에서 `l` 번째 찾으면 된다. `O(n)` 임

4. 리스트 길이를 저장시키도록 해도 되지않을까? 물론 말하는 정도는 괜찮지만 기존 자료구조를 바꾸거나 제약이 있는거 아니면 .. 좋겠디... 

5. 원소 개수를 알고리즘에서 따로 구해야하면 거의 두 번 완전 종주해야함, .. 

   * 메모리에 제약이 있는 시스템이라면 큰 리스크임, 
   * 페이지 아웃된 가상 메모리에 들어가 있을 가능성이 높다.
   * 그러면 리스트를 한 번 완전히 종주하려면 리스트를 조금씩 순서대로 스와핑해서 메모리에 올리는 작업 하면서 디스크에 여러번 올림...
   * 이런 경우는 같은 O(n)이여도 속도차가 꽤 큼
   * 따라서 결국 길이를 따로 저장하지 않았다면 이방법은

6. 한 번만 종주해도 되지만 메모리를 많이 잡아 먹으니, 그 방법은 쓰면서 메모리 용량을 줄여주는 방법은?

   * 어차피 m번째 위치니까 m의 길이로 큐를 유지하면? m만큼만 차지하지
   * 그냥 m번째 앞의 포인터와 현재 위치를 손쉽게 전진하려고인데 그냥 next 포인터로 따라 이동시키면 되니..
   * 포인터는 두 개 있어야함, m개 만큼 보조를 맞춰서 전진함,
   * 오류조건? - 원소가 m개 미만이면 , 문제 - 끝을 잘 지나치는자 봐야함

   ```c++
   ListElement *findMToLastElement( ListElement *head, int m){
     ListElement *current, *mBehind;
     int i;
     if( !head)
       return NULL;
     current = head;
   //  리스트가 끝났는지 확인하면서 앞에서부터 m개를 센다
     for(i = 0 ; i < m ; i ++){
       if(current->next){
         current = current->next;
       }else{
         return NULL;
       }
     }
     
     mBehind = head;
     while(currnet->next){
       current = current->next;
       mBehind = mBehind->next;
     }
     return mBehind;
   }
   
   ```



## 리스트 단층화

> 일반적인 이중 연결 리스트에서 시작, 이제 각 원소에 다음 원소(Nex) 와 이전(prev)를 가리키는 포인터 외에 또 다른 이중 연결 리스트를 가리키는 자식(child) 포인터가 들어올 수 있다고 하자,이 자식에도 또다른 자식이 있을 수있음,,, 
>
> 이 리스트를 단층화(flatten) 시켜서 모든 노드가 한 층짜리 이중 연결 리스트 안에 들어가도록 만들자, 처음에 첫 번째 층의 머리와 꼬리 포인터가 주어진다..
>
> ```c++
> typedef struct Node{
>   struct Node *next;
>   struct Node *prev;
>   struct Node *child;
>   int value;
> }Node;
> ```

#### 흔히 쓰이는 트리 종주 알고리즘을 써 보고 방문한 각 노드를 새로운 이스트에 복사해 넣는 방법으로 단층화 

* 어떤 종주 알고리즘이든 변형 시켜야함
* 연결 리스트를 따라서 종주하면서 모든 자식 포인터를 확인하는 정도로만 ? 
* O(n) 임 , 재귀 호출 및 종주를 하기위한 자료구조로 인한 오버헤드,,, 그외 복사본... 커질수록 문제 심각

#### 층을 정렬 기준으로 잡고, 자식리스트를 한 층에.

* 같은 층을 하나의 리스트로 연결하고, 연결된 각 층을 다시 하나의 커다란 ㅇ리스트로 연결
* 너비 우선 검색을 해야함다. 하지만 효율이 좋지 않으므로 더 나은 풀이 찾자

#### 자식이 등장하면 맨 뒤에 추가

* child가 있는 노드가 등장하면 그 자식을 첫째 층의 맨 뒤에 붙이고 꼬리 포인터를 갱신한다.
* O(n)
* 자식이 아닌 부모 리스트에 바로 집어넣어도 동일.

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
    //
  *tail = curNode;
}
```



## 리스트 단층화 해제

> 리스트 단층화를 해제하라, 자료구조를 flattenList로 전달하기 전의 원래 상태로 복구시켜야 한다.

* 리스트를 처음부터 끝까지 살펴보면서 자식 노드에 대한 포인터를 전부 별도의 자료구조에 저장하는 방법
* 매번 어떤 노드가 자식인지 아닌지를 보기위해 앞을 확인 안해도 된다.
* 무작정 자식있는 노드 찾으면 분리할 순 없음, 층이 갈라지는 곳에서 리스트 끝에 도달해서 종주 못함
* 모든 자식을 종주할 수도 있음, 자식 또 발견하면 종주
  * 한꺼번에 종주하는 것은 불가능 하지만 따로 저장해두고 종주가능
  * 재귀 호출로 사용해도됨..
* 많아봐야 두 번씩만 확인하므로 O(n) , 어차피 자식 다 확인해야하니까 이보다 빠를 수 없음
* 함수 호출 횟수는 노드 개수에비해 적으므로 그리 많지않ㅇ므

```c++
void unflatten(Node *start, Node **tail) {
  Node *curNode;
  
  exploreAndSeparate(start);

  for (curNode=start; curNode->next; curNode=curNode->next);
		//내용 없음
  *tail = curNode;
}

void exploreAndSeparate(Node *childListStart) {
  Node *curNode = childListStart;

  while (curNode) {
    if (curNode->child){
      curNode->child->prev->next = NULL;
      curNode->child->prev = NULL;
      exploreAndSepartate(curNode->child);
    }
    curNode = curNode->next;
  }
}
```

* 재귀는 반복으로 바꿀 수 없나? 생각

* 반복문 돌리면서 child 포인터 찾기, 근데 전부다 아래로 넘어갈 수도 있으므로... 계단처럼 만들어질수도.

* 윗단계로 올려진 자식이 나중에 검색된 자식보다 더 앞에 배치됨, 거꾸로 올라가면 부모 만날 때마다 각 자식 리스트를 끊어내는식으로... 하면 앞으로 훑을때의 문제를 해결 가능

* tail을 제대로 추적한다면 ..

* ```c++
  void unflattenIteratative(Node *start, Node** tail){
    if (!(*tail)) 
      return;
    while (tracker){
      if (tracker->child){
        *tail = tracker->child->prev;
        tarcker->child->prev = NULL;
        (*tail)->next = NULL;
      }
      tracker = tracker->prev;
    }
  }
  ```



## 순환형 리스트와 비 순환형 리스트

> 리스트의 머리 포인터를 받아서 그 리스트가 순환형인지 비 순환형인지 알아내는 함수 작성

* 순환형에서 같은 노드를 가리키는 포인터가 존재할 것
* 이미 지나간 노드인지 체크하는거 - 새로 만들지 말고 그냥 원본 리스트 사용
* 현재 노드의 Next를 앞의 모든 next포인터하고 비교, 같은게 있으면 순환형? - n^2
* 두 포인터가 속도가 다르게 움직인다면? 따라잡는일이 발생하면 순환형?

```c++
  bool isCyclicList( Node *head ){
    Node *fast, *slow;
    if ( !head ) 
      return false;
    slow = head;
    fast = head->next;
    while(true){
      if (!fast || !fast->next) 
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

* 비 순환이라면 첫 포인터는 n개 두번째 포인터는 n/2개 검사하면 되니까 O(n)임
* 순환이라면 느린게 n개 빠른게 2n개 검사이므로 O(n)









